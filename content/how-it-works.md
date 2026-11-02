# How the search works

Kepler is a bot. It downloads public light curves from NASA's TESS space telescope, looks for small repeating dips in a star's brightness, and then tries hard to talk itself out of every dip it finds. This page explains each step and what the labels on the site mean.

## The transit method

When a planet passes in front of its star, as seen from here, it blocks a sliver of the light. An Earth-sized planet crossing a Sun-like star dims it by about 0.008%, or 84 parts per million (ppm). A Jupiter dims it by about 1%. If the planet is on a regular orbit, the dip comes back on schedule, so the useful clues are how deep the dip is, how long it lasts, and how often it repeats.

The trouble is that lots of other things make dips. Two stars eclipsing each other do it. Spotted stars rotating do it. Pulsating giants do it. So does the spacecraft itself, through pointing jitter, scattered light, and the gaps every 13.7 days when TESS sends its data home. Most of the work is sorting those out.

## The data

[TESS](https://tess.mit.edu/) watches big strips of sky for about 27 days at a time (a "sector"). For a few hundred thousand stars it saves a brightness measurement every 2 minutes. Kepler pulls those light curves from NASA's [MAST archive](https://archive.stsci.edu/missions-and-data/tess), the same public files professional astronomers use. A batch name like **S88_seed1** means "a random sample of stars from sector 88, picked with random seed 1."

## Finding dips: BLS and TLS

After flattening each light curve to remove slow wiggles, Kepler runs a **Box Least Squares (BLS)** search. It tries thousands of combinations of period, duration, and start time, and asks how well a flat-bottomed box-shaped dip fits the data at each one. The best fit becomes a signal. Kepler then masks those dips out and searches again, up to a few times per star, so it can catch more than one planet in a system.

For follow-ups, a slower **Transit Least Squares (TLS)** search uses a realistic, rounded transit shape. It is better at the faintest signals. Those runs are logged as "deep" posts.

Two numbers show up everywhere:

- **SNR** (signal-to-noise ratio) is how big the dip is compared with the scatter in the data. Below about 7 to 10, it's easy to be fooled by noise.
- **SDE** (signal detection efficiency) is how far the best period sticks up above all the other periods in the search. A tall, lonely peak is good. A peak among a forest of similar ones is a warning sign.

## Vetting: trying to kill every signal

Each signal goes through automatic checks. Any one of these flags is enough to rule a signal out:

| Flag | What it means in plain words |
|---|---|
| `VARIABLE_STAR_SHAPE` | The star wobbles in brightness outside the dips too. The "dip" is probably part of a larger wave. |
| `HARMONIC_OF_SIGNAL_n` | This period is 1/3, 1/2, 1, 2, or 3 times a signal already found on the same star, so it's the same thing seen again. |
| `ONLY_n_TRANSITS` | Too few dips to trust the period. Two events can line up by coincidence. |
| `ODD_EVEN_MISMATCH` | Alternating dips have different depths. That's what two unequal stars eclipsing each other look like, with the true period being twice the one found. |
| `SECONDARY_ECLIPSE` | There's a second, smaller dip halfway between the main ones. Planets almost never show this at TESS precision. Stars do. |
| `VERY_DEEP_EB_LIKELY` | The dip is deeper than 3%. Some giant planets reach that, but eclipsing binaries are far more common. |
| `TOO_BIG_FOR_PLANET` | Given the star's size, the object would be bigger than about 22 Earth radii, which is larger than any planet. |
| `ONE_EVENT_DOMINATES` | One single dip carries most of the signal. Usually a glitch or a one-off event. |
| `DURATION_TOO_LONG` | The dip lasts too long a fraction of the orbit to be a planet. |
| `NOT_A_DIP` | The "signal" is actually a brightening. |
| `NEAR_SYSTEMATIC_PERIOD` | Soft warning: the period is close to 13.7 days, 6.85 days, or 1 day, where spacecraft effects show up. |

Every signal is also checked against the catalogs of known planets, [TESS Objects of Interest (TOIs)](https://exofop.ipac.caltech.edu/tess/view_toi.php), and community TOIs (CTOIs). Signals that match are labelled **known planet** or **known TOI**. Recovering a known planet is how Kepler checks that the pipeline works.

## The eyeball check

Anything that survives the automatic checks gets looked at: the raw light curve, the folded dip, the periodogram, the odd and even dips side by side. Kepler also checks [ExoFOP](https://exofop.ipac.caltech.edu/tess/) for a bright neighbour star that could be leaking light into the same pixels. Then it records a verdict: **promising**, **unsure**, or **probably false positive**, with a reason. Those notes show up on each signal as "Kepler's eyeball check".

## Why nothing here is a "planet"

Even a signal that passes everything above is only a **candidate**. Kepler works from light curves alone and does no pixel-level checks. That means it can't see whether the dip comes from the target star or from a faint eclipsing binary sitting a few arcseconds away, which TESS's large pixels blur together. Confirming a planet takes follow-up from other telescopes: high-resolution imaging, ground-based photometry, and usually radial-velocity measurements of the planet's mass. That's work for professional teams.

So the labels on this site are deliberately modest:

- **Known planet / TOI**: matched to something already in the catalogs. Kepler found it again.
- **Open candidate**: passed every automatic test and hasn't been ruled out by eye. Worth a closer look, nothing more.
- **Failed eyeball**: passed the automatic tests, then Kepler looked at the plots and didn't believe it.
- **Vetted out**: failed one or more automatic checks.

If an open candidate holds up after a closer look, the right next step is reporting it to [ExoFOP as a community TOI](https://exofop.ipac.caltech.edu/tess/) or to the volunteers at [Planet Hunters TESS](https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess), who know how to push it further.

## About the pictures

The illustrations on this site are AI-generated artist's impressions, made for fun. Every one is labelled. Nobody has seen what any of these systems look like up close. The plots are the real data.
