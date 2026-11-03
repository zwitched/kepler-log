Follow-up on TIC 316341281, the strongest pass of the first sector 104 draw.

The star is magnitude 8.1, about 7,000 K and twice the Sun's size, in a crowded field with 277 Gaia sources within 90 arcseconds. The batch search found a 153 ppm dip every 1.5145 days, five hours long, 44 transits, signal-to-noise 28.7. Odd and even dips matched (149 and 157 ppm). On paper that's a planet about 2.7 Earth radii on a very tight orbit. The diagnostic plot told a different story. The panel at the halfway point shows a dip almost as deep as the main one. The second signal the batch found was the same period shifted by half a cycle, and the periodogram is a comb of peaks at 0.76, 1.51, 2.27 and 3.03 days.

The deep TLS search, on the same three sectors (13, 94 and 104), put its strongest peak at 0.7539 days, exactly half the batch period, and flagged its shape as stellar variability. Its second signal, 202 ppm every 6.3 days, has signal-to-noise 8.2 and folds into a broad, shallow sag. That's leftover wobble from the star rather than a transit.

Folding the whole 1.51-day cycle shows the problem plainly. There's a broad V-shaped dip of about 280 ppm lasting around nine hours and a smaller one of about 120 ppm half a cycle later, joined by a rolling baseline. A planet would make a short flat-bottomed dip and leave the rest flat. The depth also wanders a lot: 199, 412 and 100 ppm in the cleaned light curves for the three sectors, and 350, 461 and 135 ppm in the raw ones.

![Full orbit folded at 1.51 days](plots/fullphase_TIC316341281.png)

![Dip depth sector by sector](plots/per_sector_depth_TIC316341281.png)

This is a hot F star varying on a roughly 0.75-day rhythm, or a close pair of stars pulling each other out of shape. Neither makes it a planet host. No bright neighbour is close: the brightest within 90 arcseconds is G=13.7 at 84 arcseconds and would need a 2% eclipse. Gaia sees the star as well behaved (RUWE 0.84), and ExoFOP and the NASA Exoplanet Archive have nothing on or near it. Marked *probably false positive*.
