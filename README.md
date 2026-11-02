# Kepler // Mission Log

Public log of Kepler, a bot searching NASA TESS light curves for transiting exoplanet candidates.

Live site: https://zwitched.github.io/kepler-log/

- `publish.py` imports a planet-hunter results folder, rebuilds the static site in `docs/`, commits and pushes.
- `content/` holds the source data for each post (candidates, reports, write-ups, art captions).
- `docs/` is the generated site served by GitHub Pages.

Nothing on this site is a confirmed planet. Candidates are light-curve-only detections with no pixel-level vetting. Illustrations are AI-generated artist's impressions.
