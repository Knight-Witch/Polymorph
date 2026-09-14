# Active Context — Polymorph `dev`

**Updated:** 2026-09-13  
**Current task:** dev.25 repair of branded display typography after human visual rejection of dev.24.  
**Runtime posture:** conversion/framing/adaptive behavior remains closed/validated for current v1 scope; UI fidelity is the active development phase.

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

Read `docs/ARCHITECTURE.md` and relevant engine files only if the task actually touches conversion, framing, adaptive GIF behavior, updater, subprocesses, packaging, or toolchain behavior. Do not preload full changelog/pre-flight/history archives.

## Current Dev candidate

- Branch: `dev`
- Runtime version: `0.1.0-dev.25`
- dev.24 technical candidate `c4f9e1962716a56650366964acff806f61ae38b0` / Windows run #57 / run ID `34805017987` passed CI end to end, but Amanda's installed visual check **REJECTED** dev.24 because the custom Polymorph face appeared only on the custom-painted primary action.
- Human evidence: title, subtitle/byline, `FILES`, and right-rail card headings rendered in Inter/fallback styling even though packaged smoke had confirmed the Polymorph font assets registered.
- Confirmed root cause: `build_brand_stylesheet()` applied `font-family: "Inter"` and a body `font-size` in the generic `QWidget` rule. Qt stylesheet precedence overrode the explicit `tracked_font(...)` QFonts used by `BrandTitle`, `BrandSubtitle`, and `CardHeading`. The custom-painted `PolymorphButton` bypassed that stylesheet path, explaining why it alone visibly used the intended face.
- dev.25 repair: remove font family/size from the generic `QWidget` stylesheet; apply the responsive Inter body font through the window's inherited QFont instead; keep the existing explicit Polymorph tracked QFonts for title/subtitle/card headings. Existing typography point sizes, letter spacing, layout geometry and control spacing are otherwise unchanged.
- Regression coverage: packaged smoke now fails if the generic QWidget rule reintroduces a font family/size override and verifies the applied title/subtitle/card-heading families/tracking/bold state. A fast unit test also protects the generic rule.
- Exact dev.25 implementation commit/run/artifact identity must be recorded here after the full Windows workflow completes.
- dev.24 successful installer artifact remains `Polymorph-dev-installer`, artifact ID `10332274291`, digest `sha256:6e18bc546f065b29bf7b193e8bd84a6972c434f6a3c672bdf7a8572dd1bcbf26`, but it is **not visually accepted** and must not be promoted.
- No public Polymorph release exists yet. `main` is not the experimental branch.

Amanda's supplied custom font files identify as one `Polymorph` family with `Regular` and `Bold` faces. Polymorph ships display-only subsets generated from those exact supplied TTFs, preserving the original glyph outlines, metrics, family/subfamily naming and kerning for all characters currently used by branded display text. The subsets are losslessly compressed as XZ assets and registered directly with Qt before the UI is created. Friends running the installer do **not** need the font installed separately. Inter remains the body/UI face; Cinzel is emergency fallback only.

Original supplied source identities:

- Polymorph Regular SHA-256: `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`
- Polymorph Bold SHA-256: `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`

Shipped subset identities remain unchanged in dev.25:

- Regular XZ Git blob SHA-1: `e868cf74e450f2e3b69c2d3116d05f18d1499e15`; decompressed subset SHA-256: `5aeb68e5a95011f9a21c1c19d81514f04ad8ff23623f6e54ec20921d2ad2ef2c`
- Bold XZ Git blob SHA-1: `a794e9faebeb424e783ba1de4028a350e929113f`; decompressed subset SHA-256: `d437ef4599771311a175d3e7832c041eb76058e26a7e826dc1ea09547a111e3a`

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

1. Commit the dev.25 stylesheet-precedence repair + regression checks + aligned dev.25 version metadata on `dev`.
2. Run the full canonical Windows workflow. Do not claim visual correctness from CI.
3. On PASS, record the exact implementation commit, run and installer artifact identity here and hand Amanda the installer directly.
4. Amanda visually confirms that the app title, subtitle/byline, `FILES`, every right-rail section heading, and the primary action all use the intended Polymorph faces.
5. Only after the face is visibly correct should size/tracking be adjusted, and only where Amanda requests it.
6. Preserve all protected conversion/framing/adaptive behavior above.
7. After typography/layout fidelity is accepted, move to the working/loading animation phase.

## Historical routing

- Canonical engine architecture and validated algorithms: `docs/ARCHITECTURE.md`.
- Canonical UI behavior/specification: `docs/UX_SPEC.md`.
- Patched-Python GIF reference: `HISTORY/REFERENCE_GIF_CONVERTER.md`.
- GIF timing evidence: `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`.
- Adaptive motion evidence: `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`.
- Detailed tracking through dev.23 is archived under `HISTORY/PROJECT_LOGS/`; use it only when a current question needs that history.
