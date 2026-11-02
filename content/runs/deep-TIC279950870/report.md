# Planet-hunter report

Generated 2026-11-02 13:12 UTC by hunt.py v1.0.0.

## Stars processed

1 stars total: 1 done

Signals found: 3 (1 new and passing vetting, 2 new but failing vetting, 0 matching known planets/TOIs/CTOIs).

## New candidates that passed the automatic checks

These are the ones to look at first. Passing the automatic checks does **not** make something a planet.
Open each plot and follow the eyeball checklist in BOT_BRIEF.md before telling anyone about it.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 279950870 | 1 | 0.73115 | 394 | 1.72 | 46.9 | 95.6 | 816 | 2.23 | - | no catalogued planet/TOI on this star | [png](plots/TIC279950870_s1.png) |

## New signals that failed vetting

Usually eclipsing binaries, stellar variability or instrument noise. Worth a glance, rarely more.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 279950870 | 2 | 0.73115 | 365 | 2.08 | 47.8 | 116.3 | 815 | 2.15 | HARMONIC_OF_SIGNAL_1 | no catalogued planet/TOI on this star | [png](plots/TIC279950870_s2.png) |
| 279950870 | 3 | 0.73115 | 361 | 2.11 | 47.7 | 141.1 | 820 | 2.13 | HARMONIC_OF_SIGNAL_1 HARMONIC_OF_SIGNAL_2 | no catalogued planet/TOI on this star | [png](plots/TIC279950870_s3.png) |

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
