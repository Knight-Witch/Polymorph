# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-15-066 — Motion Lab v4 element editor FULL PASS

- PASS architecture: all work remains isolated to the standalone Motion Lab; production conversion/framing/updater/encoder/release behavior is untouched.
- PASS source smoke: the v4 editor instantiates under Qt offscreen and exercises static triangle, linked hex spread and rune-transition state.
- PASS design: triangle and three large rune circles default to static.
- PASS design: every selectable element exposes only relevant controls; unsupported controls are disabled.
- PASS design: element editor supports span/radius, scale, manual base rotation, color, link group, brightness and glow spread.
- PASS design: signed rotation slider maps left to CCW, center to zero, right to CW; Static disables rotational animation.
- PASS design: pulse-array membership plus global pulse speed, trail/hold and dark-end controls are implemented using outside-to-inside current radius ordering.
- PASS design: rune-bearing elements expose transition speed with zero meaning no glyph identity cycling.
- PASS design: linked families propagate span, scale, base rotation, brightness and glow edits where supported.
- PASS export: `Export motion spec…` writes UTF-8 JSON containing exact element state, pulse timing, selected study and global light/tracer settings.
- PASS preservation: v3 opaque partial windows, outer large-rune placement/size, large-circle masking, inner annulus masking and long tracer tails remain in the loader path.
- PASS CI: dedicated `Polymorph Motion Lab Build` run #7 / run ID `34972811122` completed successfully on implementation head `8f68d4003be672de93cb5ae576abb1c8fb642a39`.
- PASS CI: Windows source offscreen smoke, PyInstaller portable build, packaged Windows offscreen launch smoke and portable artifact upload.
- Artifact `Polymorph-motion-lab`, artifact ID `10398081397`, size 50,856,993 bytes, digest `sha256:4f49ffffcfbcf8b96d8a3ef418fb72e67e51641237f08203bb6b0d87b60651a0`.
- PENDING isolation check: normal Windows Dev Build run #107 / run ID `34972810969` was still running when this pre-flight entry was written. Production runtime source was not changed by v4.
- Next gate: Amanda uses the v4 portable Motion Lab to tune the composition and exports the resulting `polymorph-motion-spec.json` for implementation.

## PFC-2026-09-15-065 — Motion Lab v3 correction FULL PASS

- v3 implementation commit `5b265c7bd1e21f58753f5cfd13d7a0cf19f3bc30`.
- Dedicated Motion Lab run #4 / `34964398114`: FULL PASS.
- Normal Windows Dev Build run #104 / `34964398145`: FULL PASS.

## PFC-2026-09-15-064 — Elder Futhark transmutation Motion Lab FULL PASS

- v2 implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd`.
- Dedicated Motion Lab run #3 / `34944466899`: FULL PASS.
