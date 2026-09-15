# Active Context — Polymorph `dev`

**Updated:** 2026-09-15  
**Current task:** Motion Lab v3 geometry/masking correction pass from Amanda's v2 visual review. `B — Dense Runes` is the review baseline. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

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
- Windows Dev Build run #103 / run ID `34944466940`: **FULL PASS** on the v2 lab implementation commit.
- Production UI/conversion behavior is unchanged by Motion Lab work.
- No public release exists; `main` remains non-experimental.

## Motion Lab v3 candidate — CI PENDING

- v2 FULL PASS remains protected at implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd`, dedicated run #3 / `34944466899`.
- Amanda selected `B — Dense Runes` as the closest baseline and supplied a geometry/masking correction pass.
- Outer rune ring now uses six designated white runes as true replacements for six small-rune slots and is shifted inward.
- Two white outer progress rings remain the only non-red geometry.
- All structural geometry is red; ordinary runes use warmer yellow-orange gold; all large runes are white.
- Twin hexagons and the triangle now share one circumradius; the fourth ring is tangent to the hexagon flats.
- The triangle's three large rune spheres move to edge midpoints and use opaque interiors.
- Partial rune sections become fixed opaque windows ending at the fourth ring; only the complete rune circles behind those windows rotate.
- The stationary/glimmering middle rune ring intersects only the inner portion of the large rune spheres.
- The innermost rune system is rebuilt as an opaque annulus bounded by the fifth/seventh rings, leaving only tracer convergence visible inside the central opening.
- Radial comet tails are approximately tripled in length.
- Dedicated Windows Motion Lab source/package smoke is required before this candidate becomes a human-review build.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening, Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Build v3 through the dedicated Motion Lab Windows workflow.
2. Require source smoke, PyInstaller packaging, packaged smoke, and artifact upload to pass.
3. Give Amanda the portable v3 build for visual review of corrected spacing, masks, rune placement, palette, and tracer length.
4. Iterate only inside the standalone lab.
5. Do not integrate animation into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
