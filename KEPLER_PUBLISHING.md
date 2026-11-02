# Publishing to the Kepler mission log

Site: https://zwitched.github.io/kepler-log/
Repo: https://github.com/zwitched/kepler-log (public, GitHub Pages serves `main:/docs`)
Script: `/workspace/kepler-log/publish.py` (run it with the planet-hunter venv python)

Every search gets one post. The post shows your write-up, the stats, every signal with a plain-language explanation of why it passed or failed, the diagnostic plots, the candidates table, and the full report.md. The home page, Discoveries log, RSS feed and stats update automatically.

## After every batch (the one command)

When a batch finishes (hunt.log ends with `Finished in ...`):

1. Write a short post in markdown, e.g. `/workspace/kepler-log/writeups/S88_seed3.md` (see "Writing the post" below).
2. Run:

```
cd /workspace/kepler-log
/workspace/planet-hunter/.venv/bin/python publish.py /workspace/planet-hunter/results/S88_seed3 \
  --writeup writeups/S88_seed3.md \
  --title "Sector 88, third draw: <one honest line>"
```

That imports the run, rebuilds the site, commits and pushes. The post is live at `https://zwitched.github.io/kepler-log/posts/S88_seed3.html` about a minute later.

- The script refuses a batch that is still running. `--allow-partial` overrides that; avoid it unless Nick asks for a live update.
- `--no-push` commits without pushing; `--no-git` only builds (handy for previewing `docs/index.html`).
- Re-running the same command for the same folder updates the post in place.

## Deep (TLS) follow-ups

`results/deep` gets overwritten by every `--out results/deep` run, so publish each follow-up **right after it finishes**, before starting the next one:

```
/workspace/planet-hunter/.venv/bin/python publish.py /workspace/planet-hunter/results/deep \
  --writeup writeups/deep-TIC373846934.md --title "Deep dive on TIC 373846934: ..."
```

It is named `deep-TIC<tic>` automatically. Better still, give each follow-up its own folder (`--out results/deep_TIC373846934`) so nothing gets overwritten; then publish that folder the normal way.

## Eyeball verdicts

The site reads `eyeball_verdict` and the `eyeball: ...` notes from `/workspace/planet-hunter/hunt_log.csv` on every build. After you log or change a verdict, refresh the site:

```
/workspace/planet-hunter/.venv/bin/python publish.py --rebuild
```

What the site shows:
- passed vetting, no eyeball verdict yet: **"Candidate, awaiting eyeball check"** (orange, counted as an open candidate)
- passed vetting, verdict `promising` or `unsure`: still an open candidate, with your notes shown
- passed vetting, verdict `probably_false_positive`: **"Failed eyeball check"**
- failed vetting: **"Vetted out"** with the reasons
- catalog match: **"Known planet recovered"** / known TOI

## Changing a post later

```
/workspace/planet-hunter/.venv/bin/python publish.py --run-id S88_seed2 --writeup writeups/S88_seed2.md
/workspace/planet-hunter/.venv/bin/python publish.py --run-id S88_seed2 --title "New title"
```

Post ids are the results folder name (`known_test`, `S80_seed1`, `deep-TIC232022864`, ...). Sources live in `content/runs/<id>/`.

## Art (use sparingly)

Only for something genuinely interesting: a strong candidate, a weird star, a good story. Generate an image, then attach it:

```
# attach to a star (shows on that signal and in the home-page gallery)
publish.py --run-id S88_seed3 --art /path/img.jpg@219144734 --caption "Artist's impression of ..."
# use as the post's cover (no @TIC)
publish.py --run-id S88_seed3 --art /path/img.jpg --caption "Artist's impression of ..."
```

Several stars: `img.jpg@111,222`. Every caption must start with "Artist's impression". The site also adds an "artist's impression" badge. Name image files sensibly; the file name is the key (re-using a name replaces that image).

## Writing the post

3 to 6 short paragraphs. Lively, specific, honest:
- Lead with what was searched (sector, how many stars) and the headline result.
- Pick the two or three most interesting signals and say in plain words what they are: "dims 5% every 16 hours, but the star is 14 times the Sun's size, so the orbit would be inside the star".
- Give numbers people can picture: hours, days, percent, Earth radii.
- Say what happens next for anything still open.

Honesty rules (non-negotiable):
- Never call anything a confirmed planet, a discovery of a planet, or "a new world". The best word available is **candidate**. There is no pixel-level vetting, so even a perfect light curve can be a blended eclipsing binary.
- Known planets are "recovered" or "found again".
- Don't overclaim a size or period you haven't checked, and say when a signal rests on few transits or low SNR.
- Write like a person. Skip the "not because X, because Y" construction, stacked rhetorical questions, "delve", "testament to", "in the vast cosmos" and similar filler.

## Troubleshooting

- `PUSH FAILED`: run `gh auth status`. If gh is logged out, stop and tell Nick; don't try to work around the auth.
- Site didn't change: Pages takes 1 to 2 minutes. Check https://github.com/zwitched/kepler-log/actions.
- Bad import: delete `content/runs/<id>/` and `docs/plots/<id>/`, then `publish.py --rebuild`.
