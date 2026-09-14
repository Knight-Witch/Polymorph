# Active Context — Polymorph `dev`

**Updated:** 2026-09-13  
**Current task:** dev.24 build + human visual validation of Amanda's supplied Polymorph Regular/Bold display typography using the already-approved dev.23 sizes, tracking and layout geometry.  
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
- Runtime version: `0.1.0-dev.24`
- dev.24 initial implementation commit: `706f20d79185071daef2de2c4fa9c5c147830e7e` (`Use custom Polymorph display font in dev.24`).
- Windows Dev Build run #55 / run ID `34797309292`: **FAILED before tests/runtime** in `Prepare pinned Polymorph UI fonts` because the first connector-created repository XZ blobs were not valid XZ byte streams. This failure is transport-only evidence; it does not implicate the supplied fonts, Qt registration or UI measurements.
- A repair commit replacing those invalid blobs with verified display-subset XZ assets is the immediate candidate; exact repair commit/run/artifact identity must be recorded here after the full Windows workflow completes.
- Previous validated fallback remains dev.23 code commit `81150b0e7007969d260317c9383ed7bacb3362b9`, Windows Dev Build run #54 / run ID `34779195156`, installer artifact ID `10324259742`.
- No public Polymorph release exists yet. `main` is not the experimental branch.

Amanda explicitly replaced the dev.23 Trajan direction with her supplied custom font files. The files identify as one `Polymorph` family with `Regular` and `Bold` faces. For dev.24, Polymorph ships display-only subsets generated from those exact supplied TTFs, preserving the original glyph outlines, metrics, family/subfamily naming and kerning for all characters currently used by branded display text. The subsets are losslessly compressed as XZ assets and registered directly with Qt before the UI is created. Friends running the installer do **not** need the font installed separately. Inter remains the body/UI face; Cinzel is emergency fallback only.

Original supplied source identities:

- Polymorph Regular SHA-256: `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`
- Polymorph Bold SHA-256: `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`

Correct shipped dev.24 subset identities:

- Regular XZ Git blob SHA-1: `e868cf74e450f2e3b69c2d3116d05f18d1499e15`; decompressed subset SHA-256: `5aeb68e5a95011f9a21c1c19d81514f04ad8ff23623f6e54ec20921d2ad2ef2c`
- Bold XZ Git blob SHA-1: `a794e9faebeb424e783ba1de4028a350e929113f`; decompressed subset SHA-256: `d437ef4599771311a175d3e7832c041eb76058e26a7e826dc1ea09547a111e3a`

The first dev.24 tester deliberately keeps the exact dev.23 title/subtitle/card/button point sizes and absolute letter spacing. `styles.py` was not changed for the font swap. Do not pre-emptively retune typography; Amanda wants to see the new face at the previously requested measurements first and adjust only if needed after visual review.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing behavior, MP4 output, updater hardening, and Windows no-console subprocess behavior are validated.
- Favor-resolution GIF selection is validated on Viper plus two harder HeroForge variants. Keep exact source-frame decimation, measured-gain gating, loop-closure timing repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior unchanged unless a new diagnostic demonstrates a defect.
- Crop/Fit live preview and real exported output are human-validated end to end; preview/export geometry is shared.
- dev.21 proportional responsive behavior is human-accepted. Preserve the `1260x820` design geometry and `920x640` supported minimum unless later testing identifies a concrete regression.
- dev.22 added sharp SVG siblings for branded icons while keeping PNG fallback and all interaction wiring unchanged.

## Active UI specification

The approved mockup is the visual specification, not loose inspiration. Current composition is two columns: compact queue + dominant preview on the left, settings/action rail on the right. Header copy is `POLYMORPH` with `Media conversion magic — by Knight Witch™`; version stays in the footer. Primary action copy is `POLYMORPH`.

Current palette is near-black/charcoal, ivory, champagne gold and restrained crimson. Busy card headings use bundled Polymorph Bold; title/subtitle/primary action use bundled Polymorph Regular with the established tracking; body/control copy uses Inter. Existing queue actions, preview controls, framing radios, sizing modes, GIF priority, footer links and responsive behavior are real functionality and must not be replaced with decorative mockup-only controls.

The working/loading animation remains deliberately deferred. Arcane-circle and D20 concepts are still open; do not implement either until the structural/typography visual pass is accepted or Amanda explicitly changes priority.

## Next gate

1. Commit the corrected verified subset font assets + verifier/tracking repair on `dev` and run the normal Windows dev workflow for dev.24, preserving all existing unit, toolchain, adaptive integration, GIF reference, frozen-app smoke, installer and checksum gates.
2. On PASS, record the exact repair commit, run and artifact identity here, retrieve the `Polymorph-dev-installer` artifact, and give Amanda the installer directly rather than sending her to Actions.
3. Amanda should run the installed tester without separately installing the custom font and visually confirm the `POLYMORPH` title, subtitle/byline, card headings and primary action use the intended face.
4. Compare the whole window against the approved mockup, especially typography scale/tracking, card density/alignment, icon sharpness, preview prominence, primary-action balance and footer rhythm.
5. If she reports visual issues, change only the branded UI/presentation layer unless evidence points elsewhere. Preserve the protected conversion/framing/adaptive state above.
6. After typography/layout fidelity is accepted, move to the working/loading animation phase.

## Historical routing

- Canonical engine architecture and validated algorithms: `docs/ARCHITECTURE.md`.
- Canonical UI behavior/specification: `docs/UX_SPEC.md`.
- Patched-Python GIF reference: `HISTORY/REFERENCE_GIF_CONVERTER.md`.
- GIF timing evidence: `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`.
- Adaptive motion evidence: `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`.
- Detailed tracking through dev.23 is archived under `HISTORY/PROJECT_LOGS/`; use it only when a current question needs that history.
