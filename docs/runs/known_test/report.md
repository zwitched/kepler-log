# Planet-hunter report

Generated 2026-11-01 12:53 UTC by hunt.py v1.0.0.

## Stars processed

2 stars total: 2 done

Signals found: 4 (0 new and passing vetting, 0 new but failing vetting, 4 matching known planets/TOIs/CTOIs).

## New candidates that passed the automatic checks

These are the ones to look at first. Passing the automatic checks does **not** make something a planet.
Open each plot and follow the eyeball checklist in BOT_BRIEF.md before telling anyone about it.

_none_

## New signals that failed vetting

Usually eclipsing binaries, stellar variability or instrument noise. Worth a glance, rarely more.

_none_

## Signals matching something already catalogued

A good sanity check: if the pipeline recovers known planets, it is working.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 261136679 | 1 | 6.26784 | 274 | 3.00 | 170.4 | 153.6 | 88 | 2.07 | - | matches pi Men c P=6.26784 d | [png](plots/TIC261136679_s1.png) |
| 150428135 | 1 | 16.05108 | 2586 | 0.97 | 55.1 | 268.2 | 42 | 2.33 | - | matches TOI-700 c P=16.05110 d | [png](plots/TIC150428135_s1.png) |
| 150428135 | 2 | 9.97720 | 478 | 2.02 | 20.1 | 65.1 | 80 | 1.0 | - | matches TOI-700 b P=9.97722 d | [png](plots/TIC150428135_s2.png) |
| 150428135 | 3 | 18.71175 | 379 | 3.00 | 14.0 | 28.5 | 41 | 0.89 | ODD_EVEN_MISMATCH | matches TOI-700 d P=37.42346 d (found 1/2 known period) | [png](plots/TIC150428135_s3.png) |

## Stars with errors

_none_

## Caveat

A NEW_CANDIDATE here is only a candidate. Most automatic detections in TESS data turn out to be
eclipsing binaries (often a nearby star blended into the same pixels), stellar activity or systematics.
Confirming a planet needs pixel-level checks, follow-up photometry, and usually spectroscopy.
Promising, carefully checked signals can be shared on ExoFOP (as a CTOI) or with Planet Hunters TESS.
