Follow-up on TIC 96796224 (HIP 33705), from the fifth sector 88 draw.

The batch search, using four sectors (2020-21 and 2024-25), found an 84 ppm dip every 18.207 days, three hours long, six transits, signal-to-noise 11.2. The star is a bright F dwarf, about 6,500 K and 1.3 times the Sun's size, so the dip would mean something about 1.3 Earth radii across. Odd and even dips were 98 and 77 ppm, close enough, and nothing showed at the halfway point. The detection score was only 9.5, and the periodogram climbs toward long periods, which makes an 18-day peak easier to fake.

The deep TLS search added sector 6 from 2018, five sectors in all, and came back empty. Its best peak was at 13.66 days with a score of 7.6 and signal-to-noise 6.4, both below the bar. The 18.2-day signal was not recovered.

Kepler then measured the dip directly at the predicted times, sector by sector. In the cleaned light curves the depths were 75, 58, 114 and 65 ppm in the four batch sectors, and -104 ppm in sector 6, a brightening. In the raw light curves they were 76, -2, -230 and 23 ppm, plus -15 ppm in sector 6. A real transit would show up at a steady depth in both. Folding the whole orbit shows a single narrow low point at the predicted time and nothing else.

![Dip depth sector by sector](plots/per_sector_depth_TIC96796224.png)

![Full orbit folded at 18.207 days](plots/fullphase_TIC96796224.png)

Neighbours don't explain it. Gaia lists 82 sources within 90 arcseconds, all at least 8.7 magnitudes fainter. The brightest, 77 arcseconds away, would need to lose 25% of its light to fake the dip; the next ones at 58 and 66 arcseconds would need 34% and 39%. Their FFI light curves are too noisy, sitting next to a 6th-magnitude star, to test. Gaia shows the star itself as single (RUWE 0.93, no binary solution), and ExoFOP and the NASA Exoplanet Archive have no TOI, CTOI or planet on it or nearby.

With no recovery in the deep search and depths that wander sector to sector and vanish in the raw flux, this looks like noise or a processing leftover. Marked *probably false positive*.
