# Active Context — Polymorph `dev`

**Updated:** 2026-09-13  
**Current task:** dev.23 human visual validation of the self-contained Trajan typography and current approved-mockup fidelity.  
**Runtime posture:** conversion/framing/adaptive behavior is closed/validated for current v1 scope; UI fidelity is the active development phase.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `src/polymorph/ui/fonts.py`
5. `src/polymorph/ui/styles.py`
6. `src/polymorph/ui/branded_layout.py`
7. `src/polymorph/ui/brand_widgets.py`
8. `src/polymorph/smoke_test.py` only if a UI/package assertion is being changed

Read `docs/ARCHITECTURE.md` and the relevant engine files only if the task actually touches conversion, framing, adaptive GIF behavior, updater, subprocesses, packaging, or toolchain behavior. Do not preload full changelog/pre-flight/history archives.

## Current Dev candidate

- Branch: `dev`
- Runtime version: `0.1.0-dev.23`
- Code head before this documentation-only handoff commit: `81150b0e7007969d260317c9383ed7bacb3362b9` (`Bundle approved Trajan typography in dev.23`)
- Windows Dev Build run #54 / run ID `34779195156`: **PASS**.
- Installer artifact: `Polymorph-dev-installer`, artifact ID `10324259742`, artifact ZIP digest `sha256:5ca0721234585cd1a364aa221965f0f6e2d0743bbdad9bb34b2744cea4b3bbb4`.
- No public Polymorph release exists yet. `main` is not the experimental branch.

The dev.23 change is complete technically: the approved Trajan Regular/Bold files are pinned by exact Git blob identity, downloaded in Windows CI, bundled into the frozen application/installer, registered with Qt before the UI is created, and required by packaged smoke. Friends running the installer do **not** need Trajan installed separately. Inter remains the body/UI face; Cinzel is only an emergency source-checkout fallback.

Do not restart the font-provenance/system-font investigation, substitute a system-font dependency, or replace the bundled face with vector-outline text unless Amanda explicitly changes direction. The requirement is a self-contained installed application using the approved display face.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing behavior, MP4 output, updater hardening, and Windows no-console subprocess behavior are validated.
- Favor-resolution GIF selection is validated on Viper plus two harder HeroForge variants. Keep exact source-frame decimation, measured-gain gating, loop-closure timing repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior unchanged unless a new diagnostic demonstrates a defect.
- Crop/Fit live preview and real exported output are human-validated end to end; preview/export geometry is shared.
- dev.21 proportional responsive behavior is human-accepted. Preserve the `1260x820` design geometry and `920x640` supported minimum unless later testing identifies a concrete regression.
- dev.22 added sharp SVG siblings for branded icons while keeping PNG fallback and all interaction wiring unchanged.

## Active UI specification

The approved mockup is the visual specification, not loose inspiration. Current composition is two columns: compact queue + dominant preview on the left, settings/action rail on the right. Header copy is `POLYMORPH` with `Media conversion magic — by Knight Witch™`; version stays in the footer. Primary action copy is `POLYMORPH`.

Current palette is near-black/charcoal, ivory, champagne gold and restrained crimson. Busy card headings use bundled Trajan Bold; title/subtitle/primary action use bundled Trajan Regular with the established wide tracking; body/control copy uses Inter. Existing queue actions, preview controls, framing radios, sizing modes, GIF priority, footer links and responsive behavior are real functionality and must not be replaced with decorative mockup-only controls.

The working/loading animation remains deliberately deferred. Arcane-circle and D20 concepts are still open; do not implement either until the structural/typography visual pass is accepted or Amanda explicitly changes priority.

## Next gate

1. If Amanda has not yet been handed the dev.23 installer, retrieve the run #54 `Polymorph-dev-installer` artifact and give her the installer directly rather than sending her to Actions.
2. She should run the normal installed tester **without separately installing Trajan** and visually confirm the `POLYMORPH` title, subtitle/byline, card headings and primary action use the intended face.
3. Compare the whole window against the approved mockup, especially typography scale/tracking, card density/alignment, icon sharpness, preview prominence, primary-action balance and footer rhythm.
4. If she reports visual issues, change only the branded UI/presentation layer unless evidence points elsewhere. Preserve the protected conversion/framing/adaptive state above.
5. After typography/layout fidelity is accepted, move to the working/loading animation phase.

## Historical routing

- Canonical engine architecture and validated algorithms: `docs/ARCHITECTURE.md`.
- Canonical UI behavior/specification: `docs/UX_SPEC.md`.
- Patched-Python GIF reference: `HISTORY/REFERENCE_GIF_CONVERTER.md`.
- GIF timing evidence: `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`.
- Adaptive motion evidence: `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`.
- Detailed tracking through dev.23 is archived under `HISTORY/PROJECT_LOGS/`; use it only when a current question needs that history.
