# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.25 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-055 — Mockup fidelity continuation after run #79 human visual review

- Required bootstrap completed before material editing: `PROJECT_CONTRACT.md`, `ACTIVE_CONTEXT.md`, canonical `docs/UX_SPEC.md`, current font/style/layout/widget/fidelity files, packaged smoke because presentation/package assertions are relevant, and `THIRD_PARTY.md` for the new icon source.
- New human evidence supersedes the prior wait state: the run-#79 tester is technically PASS but visually still too far from the approved mockup in container rhythm, text scale, right-rail alignment, palette nuance, footer icon/text spacing, and icon quality/semantics.
- Preserve the confirmed bundled Polymorph Regular/Bold display family and bundled Inter body/UI family. No system-font dependency is introduced.
- Presentation correction is intentionally isolated in the branded fidelity layer: smaller/denser normal-size body/control/helper type, mockup-like dark/gold/ivory/red palette tuning, more compact normal-size card geometry, and a single optical content axis beneath section headings.
- Output Format, Sizing, GIF Priority, Framing, Aspect Ratio, Crop Zoom, and Output Folder are aligned to the section-title text column. Helper copy no longer receives the oversized legacy indent.
- Use coherent Lucide SVG section glyphs at a larger design size. Required semantic corrections: `FRAMING` = crop icon; `CROP ZOOM` = hourglass. Existing social links remain Simple Icons SVGs, enlarged and spaced farther from their labels.
- The minimum-size rail compaction is protected: fidelity container-geometry overrides do not run at scale `<= 0.76`, preserving the accepted 920×640 primary-action budget.
- Add `LUCIDE_LICENSE.txt`, package text notices, and document Lucide in `THIRD_PARTY.md`.
- Five accidental temporary staging files created during this edit are explicitly removed in the same final candidate tree; they must not survive on `dev`.
- Runtime remains `0.1.0-dev.25`. No conversion, adaptive GIF, framing/export geometry, output sizing, updater, subprocess, or pinned toolchain behavior changes.
- Next gate: full Windows CI. Only a full PASS artifact becomes the new visual tester; then Amanda checks alignment, density, colors, body/helper typography, larger crisp icons, Framing/Crop Zoom semantics, footer rhythm, and minimum-size balance.
