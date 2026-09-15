# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-15-065 — Motion Lab v3 geometry/masking correction candidate

### Summary

- Selected `B — Dense Runes` as the active review baseline from Amanda's v2 visual review.
- Corrected the outer hierarchy to two white progress rings, an inward-shifted gold Elder Futhark ring, red third ring, rotating red hexagons/triangle, and a fourth red ring tangent to the hexagon flats.
- Kept six designated outer runes; each now replaces its small-rune slot exactly and renders white instead of overlapping a gold rune.
- Converted the three partial rune structures into fixed opaque annular windows clipped at the fourth ring. Their frames stay anchored; only complete Elder Futhark circles rotate behind the windows.
- Enlarged the triangle to the same circumradius as the hexagons and moved all three large rune spheres from triangle tips to edge midpoints.
- Made large rune spheres opaque foreground masks and switched their cycling glyphs to white.
- Repositioned the stationary/glimmering middle gold rune ring so it intersects only the inner portion of the large rune spheres.
- Rebuilt the innermost rune system as an opaque annulus bounded by red fifth/seventh rings, with the smallest gold Elder Futhark ring rotating inside and only tracer convergence visible in the central opening.
- Tripled radial comet-tail travel from roughly 20% to 60% of each spoke.
- Standardized palette: white outer progress geometry, red structural geometry, warmer yellow-orange gold ordinary runes, white large runes.
- Set Dense Runes as the Motion Lab's default review study and clarified partial-window/innermost-rune controls.
- Production Polymorph remains dev.27 unchanged; no conversion, framing, adaptive, updater, production UI, installer, or public-release behavior changed.
- Dedicated Windows Motion Lab CI/package validation is pending for this candidate.

## POLY-2026-09-15-064 — Motion Lab Elder Futhark transmutation rebuild FULL PASS

- v2 implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd`.
- Dedicated Motion Lab run #3 / `34944466899`: FULL PASS.
- Portable artifact `10386399042`, digest `sha256:ca12e0e0bcf2f239c8e2acd75046443e4016bdefb7df11bb040625390bc6b767`.
- Normal Windows Dev Build run #103 / `34944466940` also passed all protected production gates.
