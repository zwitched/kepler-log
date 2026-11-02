Follow-up on TIC 271785710, from the fourth sector 88 draw.

The batch search found a 152 ppm dip every 1.576 days, about 4 hours long, 42 transits, signal-to-noise 16. TESS only has three sectors on this star (2019, 2023 and 2025), so the deep TLS search used the same data and found the same thing: 1.5762 days, 155 ppm, signal-to-noise 15.6. In the batch search the odd and even dips were close (136 vs 167 ppm) and there was nothing at the halfway point. Its detection score is 10.0, barely above the forest of other peaks.

The star is the problem. It's a red giant about 7.5 times the Sun's size and roughly 5,000 K. A 1.58-day orbit around a star like this would have a radius of about 5 solar radii, which puts it inside the star. Anything big enough to make a 152 ppm dip on a giant this size would also be about 10 Earth radii across.

Gaia adds a twist: it lists this giant as a spectroscopic binary with a 142-day orbit. That companion is far too slow to cause the 1.6-day dips, but it's a reminder there's more light in this system than one star's.

The dips don't agree either. Measured sector by sector, the depth is 232, 117 and 116 ppm in the cleaned light curves and 350, 299 and 130 ppm in the raw ones. A planet blocks the same amount of light every time.

![Dip depth sector by sector](plots/per_sector_depth_TIC271785710.png)

The most likely sources are the giant's own surface churning, which makes slow noise that can line up into fake dips, or a faint eclipsing binary nearby. A star 3.4 magnitudes fainter, 66 arcseconds away, would need to dim by only 0.35%. Marked *probably false positive*.
