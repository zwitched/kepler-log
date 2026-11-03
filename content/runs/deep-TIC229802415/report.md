# Planet-hunter report

Generated 2026-11-03 10:18 UTC by hunt.py v1.0.0.

## Stars processed

1 stars total: 1 done

Signals found: 2 (0 new and passing vetting, 2 new but failing vetting, 0 matching known planets/TOIs/CTOIs).

## New candidates that passed the automatic checks

These are the ones to look at first. Passing the automatic checks does **not** make something a planet.
Open each plot and follow the eyeball checklist in BOT_BRIEF.md before telling anyone about it.

_none_

## New signals that failed vetting

Usually eclipsing binaries, stellar variability or instrument noise. Worth a glance, rarely more.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 229802415 | 2 | 13.05117 | 1035 | 3.79 | 12.9 | 9.6 | 5 | 6.13 | ODD_EVEN_MISMATCH ONE_EVENT_DOMINATES | no catalogued planet/TOI on this star | [png](plots/TIC229802415_s2.png) |
| 229802415 | 1 | 6.79032 | 1178 | 1.17 | 7.8 | 11.7 | 4 | 6.54 | ONE_EVENT_DOMINATES NEAR_SYSTEMATIC_PERIOD | no catalogued planet/TOI on this star | [png](plots/TIC229802415_s1.png) |

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
