# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-15-065 — Motion Lab v3 correction FULL PASS

- PASS static: rewritten Motion Lab source parses without syntax errors.
- PASS architecture: changes remain isolated from production `PolymorphWindow`, conversion, framing, updater, encoder and release behavior.
- PASS source design: six large white outer runes replace exact small-rune slots; outer rune band is shifted inward.
- PASS source design: outer progress rings are white; structural geometry is red; ordinary runes are warmer yellow-orange gold; large runes are white.
- PASS source design: triangle and twin hexagons share one circumradius; fourth ring is tangent to hexagon flats.
- PASS source design: triangle rune spheres are anchored to edge midpoints and use opaque masks.
- PASS source design: three partial rune sections are fixed opaque windows clipped at the fourth ring; only full rune circles behind them rotate.
- PASS source design: stationary/glimmering middle rune ring and innermost opaque rune annulus are separated into non-overlapping zones.
- PASS source design: radial tracer tails are extended from 20% to 60% of spoke travel while retaining bright comet heads.
- PASS CI: dedicated `Polymorph Motion Lab Build` run #4 / run ID `34964398114` completed successfully on implementation commit `5b265c7bd1e21f58753f5cfd13d7a0cf19f3bc30`.
- PASS CI: Windows source offscreen smoke, PyInstaller portable build, packaged Windows offscreen launch smoke and portable artifact upload.
- Artifact `Polymorph-motion-lab`, artifact ID `10394437743`, size 50,819,173 bytes, digest `sha256:ee9528c126987c26744032d0c144c32ebba0274002aae1c263c577598a2cc4c1`.
- PASS isolation check: normal Windows Dev Build run #104 / run ID `34964398145` also completed successfully on the same implementation commit, including unit tests, pinned toolchain verification, adaptive integration, GIF reference comparison, production PyInstaller build, packaged production smoke, installer compilation, checksum and artifact uploads.
- No production conversion, geometry semantics, adaptive, updater, subprocess, app-window, installer, runtime-version or public-release behavior changed.
- Next gate: Amanda's human visual review of the v3 portable Motion Lab, primarily Dense Runes.

## PFC-2026-09-15-064 — Elder Futhark transmutation Motion Lab FULL PASS

- v2 implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd`.
- Dedicated Motion Lab run #3 / `34944466899`: FULL PASS.
- Normal Windows Dev Build run #103 / `34944466940`: FULL PASS.
