Follow-up on TIC 278866220, from the fourth sector 88 draw.

The batch search found a 106 ppm dip every 2.194 days at a signal-to-noise of 7.6, below the usual bar of 10. TESS has watched this star, an F-type star about 6,550 K and 2.5 times the Sun's size, for 32 sectors. TLS on all of them found the same period again, much more strongly: 2.19406 days, 76 ppm, signal-to-noise 20, a detection score of 81, 299 transits. Folded over the whole orbit it's one sharp, lonely dip, and it shows up in every year of data.

![Full orbit folded at 2.194 days](plots/fullphase_TIC278866220.png)

The shape was the first warning. Each dip lasts about 1.5 hours. A planet crossing the middle of a star this size on a 2.2-day orbit should take about 5 hours, so this would have to be a near-miss graze along the star's edge.

The neighbour check settled it. TIC 278866211 sits 65 arcseconds away (about three TESS pixels) and is about two magnitudes fainter. It would only need to dim by 0.08% to produce our signal. Its own light curve drops by about 0.43% every 2.19406 days, at the same moments (the predicted times agree to within 10 minutes), with a signal-to-noise near 300. That star is TOI-189, which the TESS team marks as an eclipsing binary and the follow-up working group lists as a false positive. A little of its light falls into TIC 278866220's aperture, and its eclipses come along with it.

![The neighbour, TOI-189, folded at the same period](plots/neighbour_TIC278866211_TOI189.png)

Marked *probably false positive*: the signal comes from the eclipsing binary next door. The deep search also turned up a faint 37 ppm signal at 3.42 days with a signal-to-noise of 7.7. The fold is mostly scatter, so it's logged as too weak to count.
