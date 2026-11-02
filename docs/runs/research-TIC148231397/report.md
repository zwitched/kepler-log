# Research follow-up: TIC 148231397

Generated 2026-11-02 11:59 UTC by Kepler (follow-up analysis, not a batch run). 1 stars total.

Signal under review: 12.104131 d, 342 ppm, 2.88 h, TLS SDE 10.19, 13 transits, from post deep-TIC148231397.
Verdict changed: **unsure -> probably false positive**.

## Star (TIC v8.2 / Gaia DR3 5576393122591566720)

| Property | Value |
|---|---|
| Teff | 6946 K (TIC), 6781 K (Gaia) |
| Radius / mass | 1.42 R_sun / 1.52 M_sun (TIC); 1.43 / 1.37 (Gaia FLAME) |
| logg, [M/H] | 4.32, -0.30 |
| Distance | 168 pc |
| Tmag / V / G | 9.03 / 9.37 / 9.31 |
| Gaia RUWE | 0.94 |
| Gaia binarity | non_single_star = 0, no NSS orbit or acceleration solution |
| Gaia line broadening (vbroad) | 65 km/s |
| Gaia variability table | no entry |
| Light-curve variability | weak periodicity at about 0.87 to 0.93 d in every sector |
| ExoFOP | no TOI, no CTOI, no imaging, spectra or notes |
| NASA Exoplanet Archive | no planets, no TOI rows |

SPOC 2-minute sectors on MAST: 6, 7, 33, 34, 61, 87, 88 (all already used by the deep run; no new sectors).

## Tests

| Test | Result |
|---|---|
| Scrambled-data false alarm (TLS, 12 trials, each sector circularly shifted) | best SDE 8.85 to 12.35; 6 of 12 trials reach SDE >= 10.19 |
| Flipped light curve (search for brightenings) | SDE 9.03 at 1.74 d |
| Scatter of a random 2.9 h window | 170 ppm (about 2.4x the formal error); 3% of windows dip deeper than 300 ppm |
| Event-to-event depth consistency (PDCSAP, formal errors) | chi2 = 72 for 12 dof |
| Mean depth by sector (PDCSAP) | S6 331, S7 517, S33 380, S34 365, S61 477 (1 event), S87 88 (1 event), S88 158 ppm |
| SAP-only events | E123 +358, E124 -184, E182 +29 ppm; mean depth falls from 330 to 278 ppm |
| Momentum dumps | deepest event (E3, 614 ppm) is 1.1 h from a dump; E0 is 0.1 h from one |
| BLS fine grid, 12.10 d | SDE 7.7 (PDCSAP), 5.3 (SAP, peak shifts to 12.123 d) |
| BLS fine grid, 12.54 d / 24.2 d / 6.05 d | SDE 11.0 / about 9.1 / 5.6 |
| Injection-recovery (30 fake 330 ppm transits, 10 to 14 d) | 53% recovered, median SDE 5.6 at injected period; real 12.104 d scores 3.2 in the same search |
| Expected duration at 12.1 d for this star | 5.2 h for a central transit; 2.9 h needs impact parameter about 0.85 |
| Pixel check (S7, S33, S34; 2 events each) | aperture depth about 3 sigma per sector, brightest pixel about 2.5 sigma: inconclusive |

## Neighbours (Gaia DR3, within 2 arcmin; 68 sources)

| Separation | G | Delta G | Eclipse depth needed to fake 330 ppm |
|---|---|---|---|
| 16.2" | 13.98 | 4.67 | 2.5% |
| 114.5" | 14.22 | 4.91 | 3.1% |
| 100.0" | 14.64 | 5.33 | 4.5% |
| 86.2" | 15.17 | 5.86 | 7.3% |

The pixel check can't tell the target from the 16" neighbour: they sit less than one TESS pixel apart and the signal is too faint.

## Caveat

A probably-false-positive verdict is a judgment, not a proof. More TESS data would settle it.
