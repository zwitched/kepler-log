# Planet-hunter report

Generated 2026-11-01 12:49 UTC by hunt.py v1.0.0.

## Stars processed

15 stars total: 5 done, 10 no_signal

Signals found: 11 (0 new and passing vetting, 11 new but failing vetting, 0 matching known planets/TOIs/CTOIs).

## New candidates that passed the automatic checks

These are the ones to look at first. Passing the automatic checks does **not** make something a planet.
Open each plot and follow the eyeball checklist in BOT_BRIEF.md before telling anyone about it.

_none_

## New signals that failed vetting

Usually eclipsing binaries, stellar variability or instrument noise. Worth a glance, rarely more.

| TIC | # | P (d) | depth (ppm) | dur (h) | SNR | SDE | N tr | Rp est (Re) | flags | note | plot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 302201252 | 1 | 1.10549 | 1528 | 3.98 | 332.1 | 29.9 | 72 |  | VARIABLE_STAR_SHAPE ODD_EVEN_MISMATCH | no catalogued planet/TOI on this star | [png](plots/TIC302201252_s1.png) |
| 113710966 | 1 | 19.28658 | 444 | 5.03 | 51.2 | 16.0 | 2 | 1.92 | VARIABLE_STAR_SHAPE ONLY_2_TRANSITS ONE_EVENT_DOMINATES | no catalogued planet/TOI on this star | [png](plots/TIC113710966_s1.png) |
| 369479378 | 2 | 1.23448 | 374 | 3.98 | 46.6 | 9.1 | 39 | 23.87 | ODD_EVEN_MISMATCH TOO_BIG_FOR_PLANET | no catalogued planet/TOI on this star | [png](plots/TIC369479378_s2.png) |
| 369479378 | 3 | 1.24273 | 317 | 3.98 | 36.8 | 10.4 | 32 | 21.97 | HARMONIC_OF_SIGNAL_2 ODD_EVEN_MISMATCH | no catalogued planet/TOI on this star | [png](plots/TIC369479378_s3.png) |
| 369479378 | 1 | 1.20787 | 345 | 3.98 | 35.1 | 9.2 | 27 | 22.92 | VARIABLE_STAR_SHAPE ODD_EVEN_MISMATCH TOO_BIG_FOR_PLANET | no catalogued planet/TOI on this star | [png](plots/TIC369479378_s1.png) |
| 113710966 | 2 | 19.14019 | 270 | 3.98 | 29.7 | 11.2 | 2 | 1.49 | HARMONIC_OF_SIGNAL_1 ONLY_2_TRANSITS ODD_EVEN_MISMATCH ONE_EVENT_DOMINATES | no catalogued planet/TOI on this star | [png](plots/TIC113710966_s2.png) |
| 17309322 | 1 | 19.17559 | 1067 | 3.00 | 19.8 | 14.8 | 2 | 137.18 | ONLY_2_TRANSITS TOO_BIG_FOR_PLANET ONE_EVENT_DOMINATES | no catalogued planet/TOI on this star | [png](plots/TIC17309322_s1.png) |
| 113710966 | 3 | 18.16704 | 150 | 3.00 | 18.8 | 11.3 | 3 | 1.11 | ODD_EVEN_MISMATCH ONE_EVENT_DOMINATES | no catalogued planet/TOI on this star | [png](plots/TIC113710966_s3.png) |
| 311128904 | 1 | 17.19771 | 420 | 2.02 | 10.9 | 9.2 | 5 | 6.47 | ODD_EVEN_MISMATCH | no catalogued planet/TOI on this star | [png](plots/TIC311128904_s1.png) |
| 302201252 | 2 | 2.21091 | -26 | 5.03 | -4.5 | 16.8 | 35 |  | VARIABLE_STAR_SHAPE HARMONIC_OF_SIGNAL_1 ODD_EVEN_MISMATCH NOT_A_DIP | no catalogued planet/TOI on this star | [png](plots/TIC302201252_s2.png) |
| 302201252 | 3 | 2.21086 | -363 | 5.03 | -65.0 | 19.0 | 39 |  | VARIABLE_STAR_SHAPE HARMONIC_OF_SIGNAL_1 HARMONIC_OF_SIGNAL_2 ODD_EVEN_MISMATCH NOT_A_DIP | no catalogued planet/TOI on this star | [png](plots/TIC302201252_s3.png) |

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
