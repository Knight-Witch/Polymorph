# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** human animation review of the isolated Polymorph Motion Lab. The standalone Windows Motion Lab build is FULL PASS; production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `docs/MOTION_LAB.md`
5. `src/polymorph/motion_lab.py`
6. `src/polymorph/ui/fonts.py` and `src/polymorph/ui/brand_widgets.py` only when typography/shared brand behavior is implicated
7. `.github/workflows/motion-lab-build.yml` only when the standalone Windows artifact/build is implicated

Do not preload engine/history files unless the current task actually needs them.

## Production Dev candidate — protected

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- Production implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Windows Dev Build run #100 / run ID `34926765260`: **FULL PASS**.
- Production dev.27 UI/conversion behavior is unchanged by Motion Lab work.
- No public release exists; `main` remains non-experimental.

## Motion Lab candidate — FULL PASS

- Implementation commit: `0341ea270fb88495cde7f102e155e8ddd44680cc`.
- Workflow: `Polymorph Motion Lab Build` run #1 / run ID `34931411518`: **FULL PASS**.
- PASS: Windows source offscreen smoke.
- PASS: PyInstaller portable build.
- PASS: packaged Windows offscreen launch smoke.
- Artifact: `Polymorph-motion-lab`, artifact ID `10381886805`, 50,767,525 bytes.
- Artifact digest: `sha256:b96ff563b952c411614417df483c1996de51d128895b39692f9bf933c12583b6`.
- Standalone entry point remains `run_motion_lab.py` / `python -m polymorph.motion_lab`.
- Loader has four deliberately different compositions, real 0–100% progress, independent rune/counter/trace motion, glow and a swappable SVG center emblem.
- Preview background can switch among black, current Polymorph blue-black, procedural dark textures, a busy contrast stress test, or a custom image.
- Primary-action prototype treats the button as a clipping window into a larger rotating arcane mechanism; hover wakes it, POLYMORPH receives a moving light tracer, click produces a short cast burst, and debug reveal shows the full mechanism outside the button boundary.
- Canonical emblem SVG has not yet been committed because the recent attachment was not exposed to the available file tools. The lab exposes `Load emblem SVG…` so the exact artwork can still be tested immediately without code changes.
- Basic SVG rendering does not depend on source path direction. If a later contour-following tracer is approved, use a normalized animation path layer instead of mutating the canonical emblem artwork.
- Motion Lab is visual/prototype-only and does not alter production runtime version, installer, conversion behavior, or release state.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening, and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and the 920×640 supported minimum.
- Bundled Polymorph Regular/Bold and Inter application is confirmed.

## Next gate

1. Amanda opens the portable Motion Lab and reviews the four loader treatments, speeds/glow, background contrast, button hover/tracer/cast behavior, and clipping-debug visualization.
2. Load Amanda's exact emblem SVG through `Load emblem SVG…` for visual confirmation if the canonical source asset is not yet committed.
3. Iterate only inside the standalone lab until a loader treatment and button behavior are selected.
4. Do not integrate animation into the production Polymorph UI, promote to `main`, or create a public release without a separate explicit decision.
