# Planet-hunter report

Generated 2026-11-02 09:18 UTC by hunt.py v1.0.0.

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
| 184512118 | 1 | 1.12345 | 34 | 3.23 | 10.2 | 12.4 | 141 |  | SECONDARY_ECLIPSE | no catalogued planet/TOI on this star | [png](plots/TIC184512118_s1.png) |
| 184512118 | 2 | 19.54422 | 180 | 2.89 | 9.1 | 13.0 | 5 |  | ODD_EVEN_MISMATCH ONE_EVENT_DOMINATES | no catalogued planet/TOI on this star | [png](plots/TIC184512118_s2.png) |

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
