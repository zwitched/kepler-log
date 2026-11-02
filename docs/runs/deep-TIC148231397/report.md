# Planet-hunter report

Generated 2026-11-02 09:18 UTC by hunt.py v1.0.0.

## Stars processed

1 stars total: 1 done

Signals found: 3 (1 new and passing vetting, 2 new but failing vetting, 0 matching known planets/TOIs/CTOIs).

## New candidates that passed the automatic checks

These are the ones to look at first. Passing the automatic checks does **not** make something a planet.
Open each plot and follow the eyeball checklist in BOT_BRIEF.md before telling anyone about it.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 148231397 | 1 | 12.10413 | 342 | 2.88 | 18.0 | 10.2 | 13 | 2.86 | - | no catalogued planet/TOI on this star | [png](plots/TIC148231397_s1.png) |

## New signals that failed vetting

Usually eclipsing binaries, stellar variability or instrument noise. Worth a glance, rarely more.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 148231397 | 2 | 4.58594 | 215 | 3.77 | 21.1 | 9.7 | 34 | 2.27 | VARIABLE_STAR_SHAPE | no catalogued planet/TOI on this star | [png](plots/TIC148231397_s2.png) |
| 148231397 | 3 | 12.54097 | 327 | 4.82 | 20.9 | 10.7 | 11 | 2.8 | ODD_EVEN_MISMATCH | no catalogued planet/TOI on this star | [png](plots/TIC148231397_s3.png) |

## Signals matching something already catalogued

A good sanity check: if the pipeline recovers known planets, it is working.

_none_

## Stars with errors

_none_

## Caveat

A NEW_CANDIDATE here is only a candidate. Most automatic detections in TESS data turn out to be
eclipsing binaries (often a nearby star blended into the same pixels), stellar activity or systematics.
Confirming a planet needs pixel-level checks, follow-up photometry, and usually spectroscopy.
Promising, carefully checked signals can be shared on ExoFOP (as a CTOI) or with Planet Hunters TESS.
