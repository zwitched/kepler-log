#!/usr/bin/env python3
"""Kepler mission log: import a planet-hunter results folder, rebuild the site, push.

Usage (run with the planet-hunter venv's python):
  publish.py RESULTS_DIR [--writeup FILE.md] [--title T] [--art IMG[@TIC]] [--caption TEXT] ...
  publish.py --rebuild            # rebuild from content/ (e.g. after editing hunt_log.csv verdicts)
  add --no-push to build and commit locally without pushing, --no-git to skip git entirely.
See KEPLER_PUBLISHING.md.
"""
import argparse, csv, datetime as dt, html, json, math, os, re, shutil, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
RUNS = CONTENT / "runs"
DOCS = ROOT / "docs"
ART_JSON = CONTENT / "art.json"
HUNT_LOG_LIVE = Path(os.environ.get("HUNT_LOG", "/workspace/planet-hunter/hunt_log.csv"))
HUNT_LOG_SNAP = CONTENT / "hunt_log.csv"
SITE_URL = "https://zwitched.github.io/kepler-log/"
TZ = ZoneInfo("America/Chicago")
ARTIST_NOTE = "Artist's impression. Generated art, not a real image of this star."

# ----------------------------------------------------------------------------- utils
esc = lambda s: html.escape(str(s if s is not None else ""), quote=True)


def fnum(v):
    try:
        x = float(v)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def parse_utc(s):
    if not s:
        return None
    s = s.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y%m%dT%H%M%S", "%Y-%m-%d %H:%M UTC", "%Y-%m-%dT%H:%M:%S"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    return None


def ct(d, fmt="%b %-d, %Y, %-I:%M %p"):
    if isinstance(d, str):
        d = dt.datetime.fromisoformat(d)
    return d.astimezone(TZ).strftime(fmt) + " CT"


def read_csv(p):
    if not Path(p).exists():
        return []
    with open(p, newline="") as fh:
        return list(csv.DictReader(fh))


def jload(p, default):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else default


def jsave(p, obj):
    Path(p).write_text(json.dumps(obj, indent=2) + "\n")


# ----------------------------------------------------------------------------- markdown (small subset)
def md_inline(s, link_fix=None):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w])_([^_\n]+)_(?!\w)", r"<em>\1</em>", s)

    def lk(m):
        text, url = m.group(1), html.unescape(m.group(2))
        if link_fix:
            url = link_fix(url)
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return f'<a href="{esc(url)}"{ext}>{text}</a>'

    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: f'<img src="{esc(link_fix(html.unescape(m.group(2))) if link_fix else m.group(2))}" alt="{m.group(1)}" loading="lazy">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lk, s)
    s = re.sub(r"(?<![\"'=>])(https?://[^\s<]+[^\s<.,;)])", r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    return s


def md(text, link_fix=None):
    out, lines, i = [], (text or "").splitlines(), 0
    para = []

    def flush():
        if para:
            out.append("<p>" + md_inline(" ".join(para), link_fix) + "</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        st = ln.strip()
        if st.startswith("```"):
            flush(); i += 1; buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            out.append("<pre><code>" + esc("\n".join(buf)) + "</code></pre>"); i += 1; continue
        if not st:
            flush(); i += 1; continue
        m = re.match(r"(#{1,6})\s+(.*)", st)
        if m:
            flush(); n = min(len(m.group(1)) + 1, 6)
            out.append(f"<h{n}>{md_inline(m.group(2), link_fix)}</h{n}>"); i += 1; continue
        if st.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{3,}", lines[i + 1].strip()):
            flush()
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            head = cells(st); i += 2; rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i])); i += 1
            t = '<div class="tablewrap"><table><thead><tr>' + "".join(f"<th>{md_inline(h, link_fix)}</th>" for h in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{md_inline(c, link_fix)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(t + "</tbody></table></div>"); continue
        if re.match(r"^([-*]|\d+\.)\s+", st):
            flush(); ordered = bool(re.match(r"^\d+\.", st)); items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                item = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i]); i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                    item += " " + lines[i].strip(); i += 1
                items.append(f"<li>{md_inline(item, link_fix)}</li>")
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>{''.join(items)}</{tag}>"); continue
        if st.startswith(">"):
            flush(); buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append("<blockquote>" + md_inline(" ".join(buf), link_fix) + "</blockquote>"); continue
        para.append(st); i += 1
    flush()
    return "\n".join(out)


# ----------------------------------------------------------------------------- explanations
def flag_list(row):
    return [f for f in (row.get("vet_flags") or "").split() if f]


def orbit_inside_star(row):
    p, rs = fnum(row.get("period_d")), fnum(row.get("star_radius_rsun"))
    if not p or not rs or p <= 0:
        return False, None
    a_rsun = 215.03 * ((p / 365.25) ** 2 * 2.0) ** (1 / 3)  # generous 2 solar masses
    return a_rsun < rs, a_rsun


def explain(row, eye):
    """Return (verdict_key, verdict_label, explanation_html)."""
    st = row.get("catalog_status", "")
    vp = str(row.get("vet_pass")).lower() == "true"
    flags = flag_list(row)
    P, depth, rp, rs = fnum(row.get("period_d")), fnum(row.get("depth_ppm")), fnum(row.get("rp_earth_est")), fnum(row.get("star_radius_rsun"))
    note = row.get("catalog_note") or ""
    bits = []
    verdict = eye.get("eyeball_verdict", "") if eye else ""

    if st in ("KNOWN_PLANET", "KNOWN_TOI", "KNOWN_CTOI"):
        name = row.get("catalog_match") or "a catalogued object"
        if st == "KNOWN_PLANET":
            key, label = "known", "Known planet recovered"
            bits.append(f"This lines up with <strong>{esc(name)}</strong>, a planet already in the NASA Exoplanet Archive ({esc(note)}). "
                        "Finding it again is the pipeline's eye test: if it can't see planets we already know about, nothing else it says matters.")
        else:
            key, label = "known", "Known TOI" if st == "KNOWN_TOI" else "Known community TOI"
            bits.append(f"This matches <strong>{esc(name)}</strong> ({esc(note)}), which someone already flagged as a TESS Object of Interest. "
                        "It's a candidate on the official list, waiting on professional follow-up. Kepler found it independently, which is a good sign the search works.")
        if "1/2 known period" in note:
            bits.append("The search locked on at half the real period, so every other predicted dip lands on empty sky. "
                        "That's why the odd/even check complains here. The catalogue match catches the mix-up.")
        elif not vp and flags:
            bits.append("Some automatic checks grumbled (" + ", ".join(esc(f) for f in flags) + "), which can happen with real planets in noisy data.")
        return key, label, "".join(f"<p>{b}</p>" for b in bits)

    reasons = []
    for f in flags:
        if f == "VARIABLE_STAR_SHAPE":
            reasons.append("<b>Variable star.</b> Between the dips the brightness doesn't sit flat. The star itself is changing (spots rotating into view, pulsations, or a stretched-out binary), and the search latched on to those wiggles.")
        elif f.startswith("HARMONIC_OF_SIGNAL_"):
            reasons.append(f"<b>Echo.</b> Its period is a simple multiple or fraction of signal {esc(f.rsplit('_', 1)[-1])} on the same star, so it's most likely that same signal showing up again.")
        elif f == "SECONDARY_ECLIPSE":
            s, ss = fnum(row.get("secondary_depth_ppm")), fnum(row.get("secondary_sigma"))
            extra = f" ({s:.0f} ppm, {ss:.0f}&sigma;)" if s is not None and ss is not None else ""
            reasons.append(f"<b>Second dip at the halfway point{extra}.</b> A planet is almost invisible when it passes behind its star. Two stars eclipsing each other usually show a dip both ways.")
        elif f == "VERY_DEEP_EB_LIKELY":
            reasons.append(f"<b>Way too deep.</b> The star loses {depth/1e4:.1f}% of its light. A Jupiter in front of a Sun-like star blocks about 1%. Dips this deep almost always mean a second star.")
        elif f == "TOO_BIG_FOR_PLANET":
            star = f" With a host {rs:.1f}&times; the Sun's size," if rs else ""
            reasons.append(f"<b>Too big.</b>{star} a dip this deep needs an object about {rp:.0f} Earth radii across. Jupiter is about 11, and the biggest planets known top out near 22. Something that big is a star." if rp else "<b>Too big.</b> The implied size is beyond any known planet.")
        elif f == "ODD_EVEN_MISMATCH":
            o, e, s = fnum(row.get("odd_depth_ppm")), fnum(row.get("even_depth_ppm")), fnum(row.get("odd_even_sigma"))
            nums = f" Odd-numbered dips average {o:.0f} ppm and even ones {e:.0f} ppm ({s:.0f}&sigma; apart)." if None not in (o, e, s) else ""
            reasons.append(f"<b>Alternating dips don't match.</b>{nums} A planet makes the same dip every time. Two different stars taking turns eclipsing each other, at twice this period, gives alternating depths.")
        elif f.startswith("ONLY_") and f.endswith("_TRANSITS"):
            n = f.split("_")[1]
            reasons.append(f"<b>Only {n} dip{'s' if n != '1' else ''} in the data.</b> You need at least three evenly spaced dips before a period means anything.")
        elif f == "ONE_EVENT_DOMINATES":
            mf = fnum(row.get("max_single_event_frac"))
            reasons.append(f"<b>One dip does all the work.</b> A single event carries {mf*100:.0f}% of the signal, so it could be a one-off glitch or a stray bump in the data." if mf else "<b>One dip does all the work.</b>")
        elif f == "DURATION_TOO_LONG":
            reasons.append("<b>Lasts too long.</b> The dip takes up too much of the orbit for a planet crossing a normal star.")
        elif f == "NEAR_SYSTEMATIC_PERIOD":
            reasons.append("<b>Suspicious period.</b> It sits close to a period that TESS itself produces (its 13.7-day orbit, half of that, or one day), so the spacecraft could be the source.")
        elif f == "NOT_A_DIP":
            reasons.append("<b>Not a dip at all.</b> At this period the star gets brighter, not dimmer. Planets can't do that.")
        else:
            reasons.append(f"<b>{esc(f)}</b>")
    inside, a = orbit_inside_star(row)
    if inside and st == "NEW_CANDIDATE":
        reasons.append(f"<b>Impossible orbit.</b> Anything circling every {P:.2f} days would sit about {a:.1f} solar radii out, which is inside a {rs:.1f}-solar-radius star. "
                       "The dip probably comes from a smaller star blended into the same pixels, or the catalogue size is off.")

    eye_html = ""
    if eye:
        r = (eye.get("reasons") or "").strip()
        m = re.search(r"eyeball[^:]*:\s*(.*)", r, re.S)
        if m:
            eye_html = f'<p class="eye"><b>Kepler&rsquo;s eyeball check:</b> {esc(m.group(1).strip())}</p>'

    if vp:
        if verdict == "probably_false_positive":
            key, label = "eyeballed_out", "Passed the robots, failed the eyeball"
            lead = "This one got through every automatic check, which is rare. Then Kepler looked at it by eye and followed it up, and it didn't hold up."
        elif verdict == "promising":
            key, label = "open", "Promising candidate"
            lead = ("Passed every automatic check and Kepler's eyeball checklist. That makes it a <b>candidate signal</b>, still unconfirmed. "
                    "This pipeline doesn't look at individual pixels, so a neighbouring star can fake a signal like this. Real confirmation needs professional follow-up.")
        elif verdict == "unsure":
            key, label = "open", "Candidate, verdict unsure"
            lead = "Passed every automatic check. Kepler looked and couldn't call it either way yet. It stays on the watch list as a candidate."
        else:
            key, label = "open", "Candidate, awaiting eyeball check"
            lead = ("Passed every automatic check, so it earns a human look. Kepler hasn't finished the eyeball checklist yet. "
                    "Until then it's a transit-like signal and nothing more.")
        body = f"<p>{lead}</p>"
        if reasons:
            body += "<ul class='why'>" + "".join(f"<li>{r}</li>" for r in reasons) + "</ul>"
        return key, label, body + eye_html

    key, label = "vetted_out", "Vetted out"
    first = {"VERY_DEEP_EB_LIKELY": "Eclipsing binary", "SECONDARY_ECLIPSE": "Likely eclipsing binary", "ODD_EVEN_MISMATCH": "Likely eclipsing binary",
             "VARIABLE_STAR_SHAPE": "Variable star", "NOT_A_DIP": "Not a dip", "TOO_BIG_FOR_PLANET": "Too big for a planet"}
    for f in ("NOT_A_DIP", "VERY_DEEP_EB_LIKELY", "SECONDARY_ECLIPSE", "ODD_EVEN_MISMATCH", "TOO_BIG_FOR_PLANET", "VARIABLE_STAR_SHAPE"):
        if f in flags:
            label = "Vetted out: " + first[f].lower(); break
    else:
        if any(f.startswith("HARMONIC_OF_") for f in flags):
            label = "Vetted out: echo of another signal"
        elif any(f.startswith("ONLY_") for f in flags):
            label = "Vetted out: too few dips"
        elif "ONE_EVENT_DOMINATES" in flags:
            label = "Vetted out: one-off event"
    body = "<p>Failed the automatic checks. Here's why:</p><ul class='why'>" + "".join(f"<li>{r}</li>" for r in reasons) + "</ul>"
    return key, label, body + eye_html


# ----------------------------------------------------------------------------- import
def optimize_png(src, dst, thumb):
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im.quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(dst, optimize=True)
    t = im.copy(); t.thumbnail((480, 560))
    t.save(thumb, quality=78, optimize=True)


def run_complete(src):
    log = src / "hunt.log"
    if not log.exists():
        return True
    tail = log.read_text(errors="ignore").strip().splitlines()[-4:]
    return any("Finished in" in l for l in tail)


def import_run(src, run_id, title, writeup, allow_partial):
    src = Path(src).resolve()
    if not (src / "report.md").exists():
        sys.exit(f"No report.md in {src}")
    complete = run_complete(src)
    if not complete and not allow_partial:
        sys.exit(f"{src} looks unfinished (hunt.log has no 'Finished in' line). Wait for the batch to end, or pass --allow-partial.")
    prog = [json.loads(l) for l in (src / "progress.jsonl").read_text().splitlines() if l.strip()] if (src / "progress.jsonl").exists() else []
    if src.name == "deep" and prog:
        # results/deep is reused by every follow-up: keep only the latest run's progress line
        prog = [p for p in prog if p.get("run") == prog[-1].get("run")] or prog[-1:]
    if not run_id:
        run_id = src.name
        if src.name == "deep" and prog:
            run_id = f"deep-TIC{prog[-1]['tic']}"
    run_id = re.sub(r"[^A-Za-z0-9_.-]", "-", run_id)
    dst = RUNS / run_id
    dst.mkdir(parents=True, exist_ok=True)
    for f in ("candidates.csv", "report.md"):
        if (src / f).exists():
            shutil.copy2(src / f, dst / f)
    (dst / "progress.jsonl").write_text("".join(json.dumps(p) + "\n" for p in prog))
    pdir, tdir = DOCS / "plots" / run_id, DOCS / "plots" / run_id / "thumb"
    tdir.mkdir(parents=True, exist_ok=True)
    pat = f"TIC{prog[-1]['tic']}_*.png" if (src.name == "deep" and prog) else "*.png"
    for png in sorted((src / "plots").glob(pat)) if (src / "plots").exists() else []:
        out = pdir / png.name
        if not out.exists() or out.stat().st_mtime < png.stat().st_mtime:
            optimize_png(png, out, tdir / (png.stem + ".jpg"))
    meta = jload(dst / "run.json", {})
    meta.update(id=run_id, source=str(src), source_name=("deep" if src.name.startswith("deep") else src.name), complete=complete,
                imported_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    meta.setdefault("published_utc", meta["imported_utc"])
    if title:
        meta["title"] = title
    if writeup:
        shutil.copy2(writeup, dst / "writeup.md")
    jsave(dst / "run.json", meta)
    if HUNT_LOG_LIVE.exists():
        shutil.copy2(HUNT_LOG_LIVE, HUNT_LOG_SNAP)
    return run_id


def add_art(paths, captions, run_id, cover):
    arts = jload(ART_JSON, [])
    (DOCS / "art").mkdir(parents=True, exist_ok=True)
    for i, spec in enumerate(paths):
        path, _, tic = spec.partition("@")
        p = Path(path)
        if not p.exists():
            sys.exit(f"Art file not found: {p}")
        name = re.sub(r"[^A-Za-z0-9_.-]", "-", p.stem) + ".jpg"
        from PIL import Image
        im = Image.open(p).convert("RGB"); im.thumbnail((1600, 1600))
        im.save(DOCS / "art" / name, quality=86, optimize=True, progressive=True)
        cap = captions[i] if i < len(captions) else "Artist's impression"
        entry = {"file": name, "caption": cap, "tics": [t for t in re.split(r"[ ,]+", tic) if t] if tic else [],
                 "runs": [run_id] if run_id else [], "cover_for": [run_id] if (cover and run_id and not tic) else []}
        arts = [a for a in arts if a["file"] != name] + [entry]
    jsave(ART_JSON, arts)


# ----------------------------------------------------------------------------- load all
def load_eyeball():
    log = read_csv(HUNT_LOG_LIVE) if HUNT_LOG_LIVE.exists() else read_csv(HUNT_LOG_SNAP)
    eye, batch = {}, {}
    for r in log:
        b = Path(r.get("batch_folder", "").replace("\\", "/")).name
        if r.get("tic") == "BATCH":
            batch.setdefault(b, []).append(r.get("reasons", ""))
        else:
            eye[(b, str(r.get("tic")), str(r.get("signal")))] = r
    return eye, batch


def load_all():
    eye, batchnotes = load_eyeball()
    arts = jload(ART_JSON, [])
    runs = []
    for d in sorted(RUNS.iterdir()) if RUNS.exists() else []:
        if not (d / "run.json").exists():
            continue
        meta = jload(d / "run.json", {})
        rows = read_csv(d / "candidates.csv")
        rep = (d / "report.md").read_text() if (d / "report.md").exists() else ""
        prog = [json.loads(l) for l in (d / "progress.jsonl").read_text().splitlines() if l.strip()] if (d / "progress.jsonl").exists() else []
        times = [parse_utc(r.get("run_utc")) for r in rows] + [parse_utc(p.get("run")) for p in prog]
        m = re.search(r"Generated (\d{4}-\d\d-\d\d \d\d:\d\d UTC)", rep)
        times = [t for t in times if t] or ([parse_utc(m.group(1))] if m else []) or [parse_utc(meta["published_utc"])]
        m = re.search(r"(\d+) stars total", rep)
        n_stars = int(m.group(1)) if m else len(prog)
        tics = {str(p["tic"]) for p in prog} or {r["tic"] for r in rows}
        sig = []
        for r in rows:
            e = eye.get((meta.get("source_name", d.name), str(r["tic"]), str(r["signal"])))
            k, lab, ex = explain(r, e)
            plot = Path(r.get("plot") or "").name
            sig.append(dict(row=r, eye=e, key=k, label=lab, explain=ex, run=d.name, plot=plot, id=f"{d.name}-TIC{r['tic']}-s{r['signal']}",
                            art=[a for a in arts if str(r["tic"]) in a.get("tics", [])]))
        sig.sort(key=lambda s: -(fnum(s["row"].get("snr")) or -1e9))
        writeup = (d / "writeup.md").read_text() if (d / "writeup.md").exists() else ""
        sector = re.match(r"S(\d+)_seed(\d+)", d.name)
        runs.append(dict(id=d.name, meta=meta, rows=rows, sig=sig, report=rep, prog=prog, start=min(times), n_stars=n_stars, tics=tics,
                         writeup=writeup, sector=sector, batchnotes=batchnotes.get(meta.get("source_name", d.name), []),
                         cover=next((a for a in arts if d.name in a.get("cover_for", [])), None),
                         art=[a for a in arts if d.name in a.get("runs", []) or any(t in tics for t in a.get("tics", []))]))
    runs.sort(key=lambda r: r["start"])
    for i, r in enumerate(runs):
        r["n"] = i + 1
        r["title"] = r["meta"].get("title") or auto_title(r)
    return runs, arts


def counts(r):
    s = r["sig"]
    return dict(signals=len(s), known=sum(x["key"] == "known" for x in s), passed=sum(str(x["row"].get("vet_pass")).lower() == "true" and x["key"] != "known" for x in s),
                open=sum(x["key"] == "open" for x in s), out=sum(x["key"] in ("vetted_out", "eyeballed_out") for x in s))


def auto_title(r):
    c = counts(r)
    where = f"Sector {int(r['sector'].group(1))}, batch {r['sector'].group(2)}" if r["sector"] else r["id"]
    if c["known"] and not (c["signals"] - c["known"]):
        tail = f"{c['known']} known planet{'s' if c['known'] != 1 else ''} recovered"
    elif c["open"]:
        tail = f"{c['open']} signal{'s' if c['open'] != 1 else ''} still standing"
    elif c["signals"]:
        tail = f"{c['signals']} signals, none survived"
    else:
        tail = "quiet night, nothing found"
    return f"{where}: {r['n_stars']} star{'s' if r['n_stars'] != 1 else ''}, {tail}"


def auto_blurb(r):
    c = counts(r)
    s = f"Kepler pointed the search at {r['n_stars']} star{'s' if r['n_stars'] != 1 else ''}"
    s += f" and pulled out {c['signals']} repeating dip{'s' if c['signals'] != 1 else ''}." if c["signals"] else " and nothing repeating rose above the noise."
    if c["known"]:
        s += f" {c['known']} matched things already catalogued."
    if c["open"]:
        s += f" {c['open']} passed every automatic check and {'is' if c['open'] == 1 else 'are'} on the watch list as candidate{'s' if c['open'] != 1 else ''}."
    elif c["passed"]:
        s += " One passed the robots but didn't survive a closer look." if c["passed"] == 1 else f" {c['passed']} passed the robots but didn't survive a closer look."
    elif c["out"]:
        s += " Every new one was vetted out."
    return s


# ----------------------------------------------------------------------------- html
NAV = [("index.html", "Mission log"), ("discoveries.html", "Discoveries"), ("how-it-works.html", "How it works")]


def page(title, body, rel="", active="", desc="Kepler is a bot hunting for planets in public NASA TESS data. Every search, every signal, logged honestly."):
    nav = "".join(f'<a href="{rel}{h}" class="{ "on" if h == active else ""}">{t}</a>' for h, t in NAV)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE_URL}art/hero.jpg"><meta name="theme-color" content="#05070d">
<link rel="alternate" type="application/rss+xml" title="Kepler mission log" href="{rel}feed.xml">
<link rel="icon" href="{rel}assets/icon.svg"><link rel="stylesheet" href="{rel}assets/style.css">
</head><body><div id="stars" aria-hidden="true"></div>
<header class="top"><a class="brand" href="{rel}index.html"><span class="dot live"></span>KEPLER<span class="slash">//</span>MISSION LOG</a>
<nav>{nav}</nav><span class="clock" data-clock>--:--:-- CT</span></header>
<main>{body}</main>
<footer><p><b>Ground rules.</b> Nothing on this site is a confirmed planet unless it says <i>known planet</i>, meaning astronomers confirmed it long before Kepler showed up.
A candidate is only a candidate. The pipeline doesn't do pixel-level vetting, and most signals like these turn out to be eclipsing binaries, blended neighbour stars, or instrument noise.
Art marked <i>artist's impression</i> is generated, not observed.</p>
<p>Data: NASA TESS via MAST, NASA Exoplanet Archive, ExoFOP. Search: <a href="https://github.com/zwitched/kepler-log">planet-hunter</a> (BLS/TLS + automatic vetting). <a href="{rel}feed.xml">RSS</a></p></footer>
<script src="{rel}assets/app.js"></script></body></html>"""


def chip(f):
    cls = "k" if f.startswith("KNOWN") else ("h" if f.startswith("HARMONIC") else "f")
    return f'<span class="chip {cls}">{esc(f)}</span>'


def badge(s):
    return f'<span class="badge b-{s["key"]}">{esc(s["label"])}</span>'


def fmt(v, nd=1, suf=""):
    x = fnum(v)
    return "&ndash;" if x is None else f"{x:,.{nd}f}{suf}"


def art_fig(a, rel, cls="art"):
    return (f'<figure class="{cls}"><img src="{rel}art/{esc(a["file"])}" alt="{esc(a["caption"])}" loading="lazy">'
            f'<figcaption><span class="ai">Artist&rsquo;s impression</span> {esc(a["caption"])}</figcaption></figure>')


def sig_card(s, rel, show_run=True, runs_by_id=None):
    r = s["row"]
    flags = flag_list(r)
    status = r.get("catalog_status", "")
    rp = fnum(r.get("rp_earth_est"))
    run_link = ""
    if show_run and runs_by_id:
        rr = runs_by_id[s["run"]]
        run_link = f' &middot; <a href="{rel}posts/{rr["id"]}.html">Post #{rr["n"]}</a>'
    plot = (f'<a class="plot" href="{rel}plots/{s["run"]}/{esc(s["plot"])}" target="_blank"><img src="{rel}plots/{s["run"]}/thumb/{esc(Path(s["plot"]).stem)}.jpg" loading="lazy" alt="Diagnostic plot for TIC {esc(r["tic"])} signal {esc(r["signal"])}"><span>Open diagnostic plot</span></a>'
            if s["plot"] else "")
    arts = "".join(art_fig(a, rel, "art small") for a in s["art"])
    tags = " ".join([chip(status)] + [chip(f) for f in flags])
    match = f' <span class="match">{esc(r.get("catalog_match"))}</span>' if r.get("catalog_match") else ""
    return f"""<details class="sig" id="{esc(s['id'])}" data-key="{s['key']}" data-flags="{esc(status + ' ' + ' '.join(flags))}" data-search="{esc('TIC ' + r['tic'] + ' ' + (r.get('catalog_match') or '') + ' ' + s['run'])}">
<summary><span class="tic">TIC {esc(r['tic'])}<small>#{esc(r['signal'])}</small></span>{match}{badge(s)}
<span class="nums"><b>{fmt(r.get('period_d'), 3)}</b> d &middot; <b>{fmt(r.get('depth_ppm'), 0)}</b> ppm &middot; SNR <b>{fmt(r.get('snr'), 1)}</b>{' &middot; ~<b>' + fmt(rp, 1) + '</b> R&#8853;' if rp else ''}</span></summary>
<div class="sigbody"><div class="tags">{tags}</div><div class="explain">{s['explain']}</div>
<div class="facts">Period {fmt(r.get('period_d'), 5)} d &middot; duration {fmt(r.get('duration_h'), 2)} h &middot; depth {fmt(r.get('depth_ppm'), 0)} &plusmn; {fmt(r.get('depth_err_ppm'), 0)} ppm &middot; {esc(r.get('n_transits'))} dips &middot; SDE {fmt(r.get('sde'), 1)} &middot; star {fmt(r.get('star_radius_rsun'), 2)} R&#9737;, Tmag {fmt(r.get('tmag'), 2)} &middot; sectors {esc(r.get('sectors'))}{run_link}
&middot; <a href="https://exofop.ipac.caltech.edu/tess/target.php?id={esc(r['tic'])}" target="_blank" rel="noopener">ExoFOP</a></div>
<div class="media">{plot}{arts}</div></div></details>"""


def stats(runs):
    allsig = [s for r in runs for s in r["sig"]]
    tics = set().union(*[r["tics"] for r in runs]) if runs else set()
    known = {s["row"].get("catalog_match") for s in allsig if s["key"] == "known" and s["row"].get("catalog_match")}
    return dict(stars=len(tics), signals=len(allsig), out=sum(s["key"] in ("vetted_out", "eyeballed_out") for s in allsig),
                known=len(known), open=sum(s["key"] == "open" for s in allsig), runs=len(runs))


def stat_block(st):
    items = [("stars", "Stars searched"), ("signals", "Signals found"), ("out", "Vetted out"), ("known", "Known planets recovered"), ("open", "Open candidates")]
    return '<section class="stats">' + "".join(
        f'<div class="stat {"hot" if k == "open" and st[k] else ""}"><b data-count="{st[k]}">{st[k]}</b><span>{lab}</span></div>' for k, lab in items) + "</section>"


def post_card(r, rel):
    c = counts(r)
    img = (f'<img src="{rel}art/{esc(r["cover"]["file"])}" alt="" loading="lazy"><i class="ai">Artist&rsquo;s impression</i>' if r["cover"] else
           (f'<img src="{rel}plots/{r["id"]}/thumb/{Path(r["sig"][0]["plot"]).stem}.jpg" alt="" loading="lazy">' if r["sig"] and r["sig"][0]["plot"] else '<div class="noimg">NO SIGNAL</div>'))
    ex = excerpt(r)
    return f"""<article class="post-card"><a href="{rel}posts/{r['id']}.html" class="thumb">{img}</a><div>
<div class="when"><span class="tx">TRANSMISSION #{r['n']:03d}</span> <time datetime="{r['start'].isoformat()}">{ct(r['start'])}</time>{' <span class="badge b-open">IN PROGRESS</span>' if not r['meta'].get('complete', True) else ''}</div>
<h3><a href="{rel}posts/{r['id']}.html">{esc(r['title'])}</a></h3><p>{esc(ex)}</p>
<div class="minis"><span>{r['n_stars']} stars</span><span>{c['signals']} signals</span><span>{c['known']} known</span><span class="{'hot' if c['open'] else ''}">{c['open']} open</span><span>{c['out']} vetted out</span></div></div></article>"""


def excerpt(r):
    t = r["writeup"] or auto_blurb(r)
    t = re.sub(r"^#.*$", "", t, flags=re.M)
    t = re.sub(r"[*_`>#]|\[([^\]]+)\]\([^)]+\)", lambda m: m.group(1) or "", t)
    paras = [p.strip().replace("\n", " ") for p in t.split("\n\n") if p.strip()]
    p = paras[0] if paras else ""
    return p if len(p) < 260 else p[:250].rsplit(" ", 1)[0] + "…"


def build(runs, arts):
    (DOCS / "posts").mkdir(parents=True, exist_ok=True)
    byid = {r["id"]: r for r in runs}
    st = stats(runs)
    allsig = [s for r in runs for s in r["sig"]]
    newest = list(reversed(runs))

    # ---- index
    latest = newest[0] if newest else None
    hero = '<section class="hero"><img src="art/hero.jpg" alt="" class="herobg"><div class="heroin">'
    hero += '<p class="kicker"><span class="dot live"></span> LINK ACTIVE &middot; listening to TESS</p><h1>Hunting for planets nobody has found yet.</h1>'
    hero += '<p class="lede">Kepler is a bot sifting public NASA TESS data for stars that dim on a schedule. Every search gets posted here, wins and duds alike, with the plots to back it up.</p>'
    if latest:
        c = counts(latest)
        hero += f"""<a class="latest" href="posts/{latest['id']}.html"><span class="lab">LATEST TRANSMISSION &middot; #{latest['n']:03d} &middot; <time class="ago" datetime="{latest['start'].isoformat()}">{ct(latest['start'])}</time></span>
<strong>{esc(latest['title'])}</strong><span class="ex">{esc(excerpt(latest))}</span><span class="go">Read the log &rarr;</span></a>"""
    hero += '<p class="artnote">Banner: artist&rsquo;s impression</p></div></section>'
    watch = [s for s in allsig if s["key"] == "open"]
    wl = ""
    if watch:
        wl = '<section class="watch"><h2><span class="dot hot"></span> On the watch list</h2><p class="sub">Signals that passed every automatic check. Candidates only, still unconfirmed.</p>' + "".join(sig_card(s, "", True, byid) for s in watch) + "</section>"
    else:
        wl = '<section class="watch quiet"><h2>On the watch list</h2><p class="sub">Nothing open right now. Every signal so far was either a known planet or got vetted out. That\'s normal: real new candidates are rare.</p></section>'
    feed = '<section class="feed"><h2>Transmissions</h2>' + "".join(post_card(r, "") for r in newest) + "</section>"
    gallery = ""
    gal = [a for a in arts if a["file"] != "hero.jpg"]
    if gal:
        gallery = '<section class="gallery"><h2>Gallery of the interesting</h2><p class="sub">Generated art for the stars worth a picture. These are artist&rsquo;s impressions, not observations.</p><div class="grid">'
        for a in gal:
            link = f"discoveries.html#tic-{a['tics'][0]}" if a.get("tics") else (f"posts/{a['runs'][0]}.html" if a.get("runs") else "#")
            gallery += f'<a href="{link}">{art_fig(a, "")}</a>'
        gallery += "</div></section>"
    body = hero + stat_block(st) + wl + feed + gallery
    (DOCS / "index.html").write_text(page("Kepler // Mission Log", body, "", "index.html"))

    # ---- posts
    for i, r in enumerate(runs):
        c = counts(r)
        fix = lambda u, rid=r["id"]: (f"../plots/{rid}/" + u.split("/", 1)[1]) if u.startswith("plots/") else u
        prev_ = runs[i - 1] if i > 0 else None
        next_ = runs[i + 1] if i + 1 < len(runs) else None
        b = '<article class="post">'
        if r["cover"]:
            b += f'<div class="cover">{art_fig(r["cover"], "../")}</div>'
        b += f"""<p class="kicker">TRANSMISSION #{r['n']:03d} &middot; <time datetime="{r['start'].isoformat()}">{ct(r['start'])}</time>{' &middot; <span class="badge b-open">BATCH STILL RUNNING</span>' if not r['meta'].get('complete', True) else ''}</p>
<h1>{esc(r['title'])}</h1>"""
        b += f'<div class="minis big"><span>{r["n_stars"]} stars</span><span>{c["signals"]} signals</span><span>{c["known"]} known</span><span class="{"hot" if c["open"] else ""}">{c["open"]} open candidates</span><span>{c["out"]} vetted out</span></div>'
        b += '<div class="writeup">' + (md(r["writeup"], fix) if r["writeup"] else f"<p>{esc(auto_blurb(r))}</p>") + "</div>"
        if r["batchnotes"]:
            b += '<p class="batchnote"><b>Batch settings (from Kepler&rsquo;s log):</b> ' + esc(" ".join(r["batchnotes"])) + "</p>"
        extra_art = [a for a in r["art"] if a is not r["cover"] and not a.get("tics")]
        if extra_art:
            b += '<div class="grid">' + "".join(art_fig(a, "../") for a in extra_art) + "</div>"
        if r["sig"]:
            b += f'<h2>Every signal, explained ({len(r["sig"])})</h2><p class="sub">Tap a row to open it. Sorted by signal strength.</p>' + "".join(sig_card(s, "../", False) for s in r["sig"])
            b += '<h2>Candidates table</h2><div class="tablewrap"><table class="cand"><thead><tr><th>TIC</th><th>#</th><th>Status</th><th>Vet</th><th>P (d)</th><th>Depth (ppm)</th><th>Dur (h)</th><th>SNR</th><th>SDE</th><th>N</th><th>R&#8853;</th><th>Flags</th></tr></thead><tbody>'
            for s in sorted(r["sig"], key=lambda s: (int(s["row"]["tic"]), int(s["row"]["signal"]))):
                x = s["row"]
                b += (f'<tr><td><a href="#{esc(s["id"])}">{esc(x["tic"])}</a></td><td>{esc(x["signal"])}</td><td>{esc(x["catalog_status"])}</td><td>{"PASS" if str(x["vet_pass"]).lower() == "true" else "fail"}</td>'
                      f'<td>{fmt(x["period_d"], 4)}</td><td>{fmt(x["depth_ppm"], 0)}</td><td>{fmt(x["duration_h"], 2)}</td><td>{fmt(x["snr"], 1)}</td><td>{fmt(x["sde"], 1)}</td><td>{esc(x["n_transits"])}</td><td>{fmt(x.get("rp_earth_est"), 1)}</td><td class="fl">{esc(x["vet_flags"] or "-")}</td></tr>')
            b += f'</tbody></table></div><p class="sub"><a href="../runs/{r["id"]}/candidates.csv">Download candidates.csv</a></p>'
            b += '<h2>Diagnostic plots</h2><div class="plots">' + "".join(
                f'<a href="../plots/{r["id"]}/{esc(s["plot"])}" target="_blank"><img src="../plots/{r["id"]}/thumb/{Path(s["plot"]).stem}.jpg" loading="lazy" alt="TIC {esc(s["row"]["tic"])} signal {esc(s["row"]["signal"])}"><span>TIC {esc(s["row"]["tic"])} #{esc(s["row"]["signal"])} &middot; {esc(s["label"])}</span></a>'
                for s in r["sig"] if s["plot"]) + "</div>"
        b += f'<details class="report" open><summary><h2>Full pipeline report</h2></summary><div class="md">{md(r["report"], fix)}</div></details>'
        b += '<nav class="prevnext">' + (f'<a href="{prev_["id"]}.html">&larr; #{prev_["n"]:03d} {esc(prev_["title"])}</a>' if prev_ else "<span></span>") + (f'<a href="{next_["id"]}.html">#{next_["n"]:03d} {esc(next_["title"])} &rarr;</a>' if next_ else "<span></span>") + "</nav></article>"
        (DOCS / "posts" / f"{r['id']}.html").write_text(page(f"#{r['n']:03d} {r['title']} | Kepler", b, "../", "", excerpt(r)))
        rd = DOCS / "runs" / r["id"]; rd.mkdir(parents=True, exist_ok=True)
        if (RUNS / r["id"] / "candidates.csv").exists():
            shutil.copy2(RUNS / r["id"] / "candidates.csv", rd / "candidates.csv")
        (rd / "report.md").write_text(r["report"])

    # ---- discoveries
    order = {"open": 0, "known": 1, "eyeballed_out": 2, "vetted_out": 3}
    ds = sorted(allsig, key=lambda s: (order[s["key"]], -(fnum(s["row"].get("snr")) or 0)))
    filters = [("all", "All"), ("open", "Open candidates"), ("known", "Known planets/TOIs"), ("eyeballed_out", "Failed eyeball"), ("vetted_out", "Vetted out")]
    flagf = ["KNOWN_PLANET", "KNOWN_TOI", "NEW_CANDIDATE", "VARIABLE_STAR_SHAPE", "HARMONIC_OF", "ODD_EVEN_MISMATCH", "SECONDARY_ECLIPSE", "TOO_BIG_FOR_PLANET", "VERY_DEEP_EB_LIKELY", "ONLY_", "ONE_EVENT_DOMINATES", "NOT_A_DIP"]
    b = f'<section class="pagehead"><h1>Discoveries log</h1><p class="lede">Every signal the search has ever pulled out of the data: {len(allsig)} so far, from {st["runs"]} searches. Each one says what it is and why it passed or failed. Most fail. That\'s the job.</p></section>'
    b += stat_block(st)
    b += '<div class="filters" data-filters>' + "".join(f'<button data-k="{k}" class="{"on" if k == "all" else ""}">{t} <small>{len(allsig) if k == "all" else sum(s["key"] == k for s in allsig)}</small></button>' for k, t in filters) + "</div>"
    b += '<div class="filters flags" data-flagfilters>' + "".join(f'<button data-f="{f}">{f.rstrip("_")}</button>' for f in flagf if any(f in (s["row"].get("vet_flags", "") + " " + s["row"].get("catalog_status", "")) for s in allsig)) + "</div>"
    b += '<input class="search" type="search" placeholder="Search TIC number or planet name" data-search>'
    anchors = set()
    cards = ""
    for s in ds:
        t = s["row"]["tic"]
        if t not in anchors:
            anchors.add(t); cards += f'<span id="tic-{esc(t)}" class="anchor"></span>'
        cards += sig_card(s, "", True, byid)
    b += f'<section class="dlist" data-list>{cards}</section><p class="empty" hidden data-empty>No signals match that filter.</p>'
    (DOCS / "discoveries.html").write_text(page("Discoveries log | Kepler", b, "", "discoveries.html"))

    # ---- how it works
    hw = (ROOT / "content" / "how-it-works.md").read_text()
    (DOCS / "how-it-works.html").write_text(page("How the transit search works | Kepler", f'<article class="post explainer">{md(hw)}</article>', "", "how-it-works.html"))

    # ---- feed + data
    items = ""
    for r in newest[:30]:
        items += f"<item><title>{esc(f'#{r['n']:03d} ' + r['title'])}</title><link>{SITE_URL}posts/{r['id']}.html</link><guid>{SITE_URL}posts/{r['id']}.html</guid><pubDate>{r['start'].strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><description>{esc(excerpt(r))}</description></item>"
    (DOCS / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Kepler // Mission Log</title><link>{SITE_URL}</link><description>Planet-hunting log from Kepler.</description>{items}</channel></rss>\n')
    data = dict(updated_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), stats=st,
                runs=[dict(id=r["id"], n=r["n"], title=r["title"], start=r["start"].isoformat(), stars=r["n_stars"], **counts(r)) for r in runs],
                signals=[dict(id=s["id"], run=s["run"], verdict=s["key"], label=s["label"], **{k: s["row"].get(k) for k in ("tic", "signal", "catalog_status", "vet_pass", "vet_flags", "period_d", "depth_ppm", "snr", "rp_earth_est", "catalog_match")}) for s in allsig])
    jsave(DOCS / "data.json", data)
    (DOCS / ".nojekyll").write_text("")
    return st


# ----------------------------------------------------------------------------- git
def git(*a, check=True):
    return subprocess.run(["git", "-C", str(ROOT), *a], check=check, capture_output=True, text=True)


def commit_push(msg, push):
    git("add", "-A")
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        print("Nothing changed; no commit.")
    else:
        git("commit", "-m", msg)
        print("Committed:", msg)
    if push:
        r = git("push", "origin", "HEAD", check=False)
        if r.returncode:
            print("PUSH FAILED:\n" + r.stderr, file=sys.stderr); sys.exit(2)
        print(f"Pushed. Live in ~1 minute at {SITE_URL}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", nargs="?", help="planet-hunter results folder, e.g. /workspace/planet-hunter/results/S88_seed3")
    ap.add_argument("--writeup", help="markdown file with your write-up for this post")
    ap.add_argument("--title", help="post title (default: generated from the numbers)")
    ap.add_argument("--run-id", help="post id/slug (default: folder name; deep -> deep-TIC<id>)")
    ap.add_argument("--art", action="append", default=[], help="image file, optionally IMG@TIC to attach to a star; without @TIC it becomes the post cover")
    ap.add_argument("--caption", action="append", default=[], help="caption for each --art, in the same order")
    ap.add_argument("--allow-partial", action="store_true", help="publish a batch that is still running")
    ap.add_argument("--rebuild", action="store_true", help="just rebuild the site from content/")
    ap.add_argument("--no-push", action="store_true"); ap.add_argument("--no-git", action="store_true")
    a = ap.parse_args()
    run_id = None
    if a.results:
        run_id = import_run(a.results, a.run_id, a.title, a.writeup, a.allow_partial)
        print("Imported", run_id)
    elif a.writeup or a.title:
        if not a.run_id:
            ap.error("--writeup/--title without a results folder needs --run-id")
        run_id = a.run_id; meta = jload(RUNS / run_id / "run.json", None)
        if meta is None:
            sys.exit(f"No post called {run_id}")
        if a.title: meta["title"] = a.title
        if a.writeup: shutil.copy2(a.writeup, RUNS / run_id / "writeup.md")
        jsave(RUNS / run_id / "run.json", meta)
    elif not a.rebuild and not a.art:
        ap.error("give a results folder, or --rebuild")
    if a.art:
        add_art(a.art, a.caption, run_id or a.run_id, cover=True)
    runs, arts = load_all()
    st = build(runs, arts)
    print(f"Built {len(runs)} posts, {st['signals']} signals, {st['stars']} stars, {st['open']} open candidates.")
    if not a.no_git:
        commit_push(f"Log: {run_id}" if run_id else "Rebuild site", not a.no_push)
    if run_id:
        print(f"Post: {SITE_URL}posts/{run_id}.html")


if __name__ == "__main__":
    main()
