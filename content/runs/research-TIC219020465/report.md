# Research follow-up: TIC 219020465

Generated 2026-11-03 11:51 UTC by Kepler (follow-up analysis, not a batch run). 1 stars total.

Signal under review: 14.025122 d, 296 ppm, 0.98 h, BLS SDE 11.2 (SNR 8.0), 7 transits in sectors 13, 67, 94 and 104, from posts S104_seed1 and deep-TIC219020465.
Verdict changed: **unsure -> probably false positive**.

## Star (TIC v8.2 / Gaia DR3, TYC 8378-02680-1)

| Property | Value |
|---|---|
| Teff | 5688 K (TIC), 5635 K (Gaia GSP-Phot) |
| Radius / mass | 2.55 R_sun / 1.01 M_sun (TIC); 2.30 / 1.30 (Gaia FLAME, evolutionary stage: subgiant, age 4.1 Gyr) |
| logg | 3.63 (TIC), 3.99 (Gaia) |
| Mean density | 0.09 (TIC) to 0.11 (FLAME) solar |
| Distance | 177 pc (TIC), parallax 6.05 mas |
| Tmag / V / G | 8.58 / 9.22 / 9.05 |
| Gaia RUWE | 6.77 (high: poor single-star astrometric fit, often a sign of an unresolved companion) |
| Gaia binarity | non_single_star = 0, no NSS orbit or acceleration solution; ipd_frac_multi_peak 0 |
| Gaia radial velocity | -65.3 km/s, no variability over 6 visits (rv_chisq_pvalue 0.46, robust amplitude 0.7 km/s) |
| Gaia variability table | no entry |
| Contamination (SPOC CROWDSAP) | 0.98 to 0.99 |
| ExoFOP | no TOI, no CTOI, no imaging, spectra or notes |
| NASA Exoplanet Archive | no planets, no TOI rows within 2 arcmin |
| SIMBAD / VizieR | unreachable during this run |

SPOC 2-minute sectors on MAST: 13, 67, 94, 104 (all already used). TESSCut lists FFI sectors 13, 27, 67, 94, 104 and 105. The S27 and S105 cutouts contain no data at the star (it falls off the active silicon), so the FFIs add no new transits. Our own FFI photometry in S94/S104 gives E157 729+-127, E158 122+-105, E180 126+-130, E181 162+-93 ppm.

## Tests

| Test | Result |
|---|---|
| Scrambled-data false alarm (pipeline BLS, 42 trials, each sector circularly shifted; search 1, mask, search 2 as in the real detection) | search-2 SDE 8.1 to 12.4, median 9.9; 4 of 42 reach the real 11.41; 28 of 42 pass the pipeline threshold of 9; 1 of 42 also has >= 3 events with no single event dominating |
| Flipped light curve (search for brightenings) | SDE 7.99 at 0.71 d; best between 10 and 20 d is 7.54 |
| Scatter of a random 1 h window (PDCSAP) | 113 ppm (1.29x white noise); 0.46% dip deeper than 296 ppm overall |
| Random windows near momentum dumps | within 3 h of a dump: 5.4% deeper than 296 ppm (n=37); more than 6 h away: 0.33% (n=1221) |
| Event depths, PDCSAP (ppm) | E0 224, E1 276, E105 no data, E106 399, E157 531, E158 266, E180 409, E181 161 (each +-90 to 107) |
| Event depths, SAP (ppm) | E0 207, E1 307, E106 462, E157 901, E158 211, E180 -374 (a brightening), E181 172; chi2 54 for 6 dof |
| Momentum dumps and data gaps | first predicted event in every sector is 0.3 to 2.7 h from a dump; in S67, S94 and S104 it sits at the end of a 5.2 h mid-orbit data gap that contains a dump (E105 lost in the gap; E157 and E180, the two deepest PDCSAP events, are among the first data after it) |
| Orbit-phase locking | all 7 events fall 3.6 to 6.8 d after the start of a spacecraft orbit; only 2.2% of random 12 to 16 d periods are this locked; 3 of 7 events within 2.7 h of a dump vs 3.5% for a random time |
| Camera-wide common mode (120 other stars, camera 1) | no shared dip at the event times (12% of stars > 2 sigma vs 10% at control times) |
| BLS fine grid at P (PDCSAP, durations 0.5 to 12 h) | best SNR 8.5 at 1.0 h, falls to 4.4 to 4.6 at 8 to 12 h |
| BLS fine grid at P/2 and 2P (PDCSAP) | P/2: best SNR 7.3 (0.75 h); 2P: best 6.6 to 7.6, deeper at short durations |
| BLS fine grid, SAP | dominated by large orbit-boundary ramps near 14.0 d (thousands of ppm); no clean 1 h signal |
| Injection-recovery (30 fake 296 ppm, 0.75 to 1.25 h transits, 12 to 16 d, real events removed first) | 12 of 30 recovered (40%); 10 of 13 with >= 7 transits (77%); median SDE of recoveries 12.8. The real 11.41 is within the range a genuine signal would give |
| Expected duration at 14.03 d for this star | 9.4 to 11.3 h for a central transit; 0.98 h needs impact parameter about 1.01 (grazing). About 0.5% of random transit chords are this short; at b=0 the duration implies a stellar density of about 95 solar vs 0.09 to 0.11 actual |
| Size if not grazing | 4.3 to 4.8 Earth radii |
| Pixel check (SPOC TPFs, S13, S67, S94, S104) | aperture depth S13 223+-334, S67 452+-788, S94 443+-191, S104 -175+-487 ppm; S94 and S104 difference images show a red/blue dipole across the star (the pattern of image motion), not a clean star-shaped dip |

## Neighbours (Gaia DR3, within 2 arcmin; 150 sources)

| Separation | G | Eclipse depth needed to fake 296 ppm | Pixel check |
|---|---|---|---|
| 113" | 12.00 | 0.48% | 0.06+-0.07% (S13), 0.19+-0.05% (S94): ruled out |
| 72" | 12.56 | 0.78% | 0.07+-0.08% (S94): ruled out |
| 71" | 13.60 | 1.99% | 0.11+-0.15% (S94): ruled out |
| 41" | 14.71 | 5.5% | not separable |
| 11" | 16.6 | 31% | not separable |

There's no sign the dip comes from a neighbour. The evidence points to spacecraft motion and data gaps instead.

## Caveat

A probably-false-positive verdict is a judgment, not a proof. The 1 h events far from dumps still average about 266+-49 ppm, the flipped light curve is quiet, and injections show a real signal like this would score about as well. New TESS sectors with dips landing away from thruster firings would reopen it.
