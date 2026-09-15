# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** isolated Polymorph Motion Lab prototype for the deferred loading/working animation and animated primary action. The production app remains on dev.27; conversion/framing/adaptive behavior remains closed/validated. The Motion Lab is a standalone PySide6 sandbox so loader/button motion can be iterated without touching the shipping UI.

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
- Tester artifact: `Polymorph-dev-installer`, artifact ID `10379458708`.
- Installer: `Polymorph_Setup_v0.1.0-dev.27.exe`.
- dev.27 production visual corrections remain unchanged by Motion Lab work.
- No public release exists; `main` remains non-experimental.

## Motion Lab candidate

- Standalone entry point: `run_motion_lab.py` / `python -m polymorph.motion_lab`.
- Loader has four deliberately different compositions, real 0–100% progress, independent rune/counter/trace motion, glow and a swappable SVG center emblem.
- Preview background can switch among black, current Polymorph blue-black, procedural dark textures, a busy contrast stress test, or a custom image.
- Primary-action prototype treats the button as a clipping window into a larger rotating arcane mechanism; hover wakes it, the POLYMORPH glyphs receive a moving light tracer, click produces a short cast burst, and debug reveal shows the complete mechanism outside the button boundary.
- Canonical emblem SVG has not yet been committed. The lab exposes `Load emblem SVG…` so the exact supplied artwork can be tested without code changes. Do not approximate/redraw it.
- Dedicated Windows workflow: `.github/workflows/motion-lab-build.yml`; it source-smokes, packages, packaged-smokes, then uploads `Polymorph-motion-lab`.
- Motion Lab is visual/prototype-only and does not alter the production Polymorph window, conversion behavior, runtime version, installer, or release state.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening, and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and the 920×640 supported minimum.
- Preserve minimum-only rail compaction at responsive scale `<= 0.76`.
- Bundled Polymorph Regular/Bold and Inter application is confirmed.
- Packaged application smoke passes unchanged after dev.27.

## Next gate

1. Get the standalone Motion Lab Windows build to PASS.
2. Give Amanda the portable Motion Lab artifact for human animation review.
3. Use the exact supplied emblem SVG once it is available; basic SVG rendering does not depend on source path direction.
4. Iterate only inside the standalone lab until Amanda selects a loader treatment and button behavior.
5. Do not integrate animation into the production Polymorph UI, promote to `main`, or create a public release without a separate explicit decision.
