# Active Context — Polymorph `dev`

**Updated:** 2026-09-15  
**Current task:** human visual review of Motion Lab v3 geometry/masking corrections. `B — Dense Runes` is the review baseline. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/MOTION_LAB.md`
4. `src/polymorph/motion_lab.py`
5. `src/polymorph/motion_loader.py`
6. `src/polymorph/motion_loader_base.py`
7. `src/polymorph/motion_effects.py`
8. `.github/workflows/motion-lab-build.yml` only when the standalone Windows artifact/build is implicated

Do not preload engine/history files unless the current task actually needs them.

## Production Dev candidate — protected

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- Production implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Motion Lab v3 implementation commit `5b265c7bd1e21f58753f5cfd13d7a0cf19f3bc30` triggered Windows Dev Build run #104 / run ID `34964398145`: **FULL PASS**.
- PASS on run #104: unit tests, pinned FFmpeg/gifski checks, adaptive integration, GIF reference comparison, production PyInstaller build, packaged app smoke, Inno Setup installer, checksum and artifact uploads.
- Production UI/conversion behavior is unchanged by Motion Lab work.
- No public release exists; `main` remains non-experimental.

## Motion Lab v3 candidate — FULL PASS

- Implementation commit: `5b265c7bd1e21f58753f5cfd13d7a0cf19f3bc30`.
- Dedicated workflow: `Polymorph Motion Lab Build` run #4 / run ID `34964398114`: **FULL PASS**.
- PASS: Windows source offscreen smoke.
- PASS: PyInstaller portable build.
- PASS: packaged Windows offscreen launch smoke.
- PASS: portable artifact upload.
- Artifact: `Polymorph-motion-lab`, artifact ID `10394437743`, 50,819,173 bytes.
- Artifact digest: `sha256:ee9528c126987c26744032d0c144c32ebba0274002aae1c263c577598a2cc4c1`.
- `B — Dense Runes` opens as the default review study.
- Outer rune ring uses six designated white runes as true replacements for small-rune slots and is shifted inward.
- The two outer progress rings are white. Structural geometry is red; ordinary runes are warmer yellow-orange gold; large runes are white.
- Twin hexagons and triangle share one circumradius; the fourth ring is tangent to hexagon flats.
- Triangle rune spheres sit on edge midpoints and use opaque interiors.
- Partial rune sections are fixed opaque windows ending at the fourth ring; only full rune circles behind them rotate.
- The middle glimmer ring, inner gap and opaque innermost rune annulus occupy separate non-overlapping zones.
- Radial comet tails are approximately three times the v2 length.
- Motion Lab remains visual/prototype-only and does not alter production runtime version, installer, conversion behavior or release state.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Amanda visually reviews the v3 portable Motion Lab, primarily `B — Dense Runes`.
2. Prioritize spacing/order, fixed partial-window masking, triangle/sphere anchoring, inner annulus spacing, palette separation, designated outer rune placement and tracer-tail length.
3. Iterate only inside the standalone lab until the loader motion is accepted.
4. Review the animated POLYMORPH button separately; loader approval does not automatically approve button motion.
5. Do not integrate animation into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
