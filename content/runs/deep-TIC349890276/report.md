# Planet-hunter report

Generated 2026-11-02 02:36 UTC by hunt.py v1.0.0.

## Stars processed

1 stars total: 1 done

Signals found: 2 (1 new and passing vetting, 1 new but failing vetting, 0 matching known planets/TOIs/CTOIs).

## New candidates that passed the automatic checks

These are the ones to look at first. Passing the automatic checks does **not** make something a planet.
Open each plot and follow the eyeball checklist in BOT_BRIEF.md before telling anyone about it.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 349890276 | 1 | 0.89736 | 38 | 2.58 | 14.0 | 20.0 | 242 | 1.3 | - | no catalogued planet/TOI on this star | [png](plots/TIC349890276_s1.png) |

## New signals that failed vetting

Usually eclipsing binaries, stellar variability or instrument noise. Worth a glance, rarely more.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 349890276 | 2 | 0.89736 | 33 | 2.55 | 12.1 | 27.3 | 245 | 1.21 | HARMONIC_OF_SIGNAL_1 | no catalogued planet/TOI on this star | [png](plots/TIC349890276_s2.png) |

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
