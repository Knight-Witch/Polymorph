# Active Context — Polymorph `dev`

**Updated:** 2026-09-15  
**Current task:** human visual review of the Motion Lab transmutation-circle v2 candidate. The v2 standalone Windows Motion Lab build is FULL PASS. Amanda's annotated Fullmetal Alchemist-inspired direction is implemented with real Elder Futhark, layered line-only glow, opposed rune systems, grouped flicker, comet tracers with no-go masking, dual progress rings, and the real Knight Witch emblem. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `docs/MOTION_LAB.md`
5. `src/polymorph/motion_lab.py`
6. `src/polymorph/motion_loader.py` and `src/polymorph/motion_effects.py` for loader/glow/rune behavior
7. `src/polymorph/motion_button.py` only when button motion is implicated
8. `src/polymorph/motion_stage.py` only when preview backgrounds are implicated
9. `.github/workflows/motion-lab-build.yml` only when the standalone Windows artifact/build is implicated
10. `src/polymorph/assets/kw_emblem.svg` only when emblem rendering is implicated

Do not preload engine/history files unless the current task actually needs them.

## Production Dev candidate — protected

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- Production implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Original dev.27 Windows Dev Build run #100 / run ID `34926765260`: **FULL PASS**.
- Motion Lab v2 implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd` also triggered Windows Dev Build run #103 / run ID `34944466940`: **FULL PASS**.
- PASS on run #103: all unit tests, pinned FFmpeg/gifski checks, adaptive integration, GIF reference comparison, PyInstaller production app build, packaged app smoke, Inno Setup installer build and artifact upload.
- Production dev.27 UI/conversion behavior remains unchanged by Motion Lab work.
- No public release exists; `main` remains non-experimental.

## Motion Lab v2 candidate — FULL PASS

- Implementation commit: `be7939fabedc6c719b5500dd7578ab4b2d8534fd`.
- Dedicated workflow: `Polymorph Motion Lab Build` run #3 / run ID `34944466899`: **FULL PASS**.
- PASS: Windows source offscreen smoke.
- PASS: PyInstaller portable build.
- PASS: packaged Windows offscreen launch smoke.
- PASS: portable artifact upload.
- Artifact: `Polymorph-motion-lab`, artifact ID `10386399042`, 50,819,549 bytes.
- Artifact digest: `sha256:ca12e0e0bcf2f239c8e2acd75046443e4016bdefb7df11bb040625390bc6b767`.
- The v1 standalone lab FULL PASS remains historical at commit `0341ea270fb88495cde7f102e155e8ddd44680cc`, run #1 / `34931411518`; v2 supersedes it for current visual review.
- Elder Futhark is the chosen rune system. The standalone workflow downloads/bundles Noto Sans Runic so glyph rendering is not dependent on Windows fallback fonts.
- Architecture includes: opposed outer/inner rune rings; six larger designated outer glyphs; three clipped partial rune bands; a non-rotating glimmer/cycling rune band; three independently cycling rune spheres; clockwise triangle family; counter-clockwise offset hexagons; outside-in structural cascade; masked six-ray comet tracers; opposite-direction dual progress rings; completion flash/fade/emblem reveal.
- Glow uses a tight ivory core plus layered gold/crimson falloff. Tracers use a bright comet head plus gradient tail.
- Four study modes remain: balanced Transmutation, Dense Runes, Tracer Ritual, and Fractal Echo.
- `src/polymorph/assets/kw_emblem.svg` is the bundled center asset, derived from Amanda's supplied SVG by simplifying redundant path coordinates only; raster comparison was visually equivalent at review scale.
- Runtime override chooser remains optional for development comparison.
- Motion Lab remains visual/prototype-only and does not alter production runtime version, installer, conversion behavior, or release state.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening, and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and the 920×640 supported minimum.
- Bundled Polymorph Regular/Bold and Inter application is confirmed.

## Next gate

1. Amanda opens the portable Motion Lab v2 and visually reviews the transmutation behavior.
2. Prioritize feedback on rune readability, outer/inner opposed motion, partial-arc masking, rune-sphere cycling, tracer occlusion/tail length, glow spread/core, cascade timing, dual progress rings, completion reveal, and the four study variants.
3. Also review the animated POLYMORPH button separately; loader approval does not automatically approve button motion.
4. Iterate only inside the standalone lab until the loader/button motion is selected.
5. Do not integrate animation into the production Polymorph UI, promote to `main`, or create a public release without a separate explicit decision.
