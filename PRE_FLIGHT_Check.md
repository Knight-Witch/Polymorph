# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.25 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-056 — Run #84 technical PASS / human visual gate next

- Windows Dev Build run #84 / run ID `34890815616` from implementation commit `e76f88808f471c74ae100469ed4452a5095560b0` is FULL PASS.
- All configured gates passed: bundled Polymorph/Inter fonts, unit tests, pinned FFmpeg/gifski verification, adaptive integration, GIF reference comparison, frozen app build, packaged UI smoke, Inno Setup, checksum generation, and both artifact uploads.
- The same frozen packaged smoke retained the existing `mockup-v2`, applied bundled display typography, two-column composition, FILES grouping, 920×640 primary-action visibility, preview/adaptive/framing/crop-zoom/linked-resolution/footer assertions. The presentation changes therefore did not regress the protected package/runtime gates.
- Installer artifact `Polymorph-dev-installer`: ID `10366663850`, digest `sha256:a3ccd6e2d1a131fe0ef66f70d3a3781605ea4b9be2e6e09362f29c366f3f4c38`.
- Retrieved installer `Polymorph_Setup_v0.1.0-dev.25.exe` SHA-256: `5dc38ba315cb274fee8db9377db93d10f532c4ba39784187d16b69a891496c29`; matches its generated `.sha256` file.
- Next gate is human visual review of the installed run-#84 candidate. Do not continue UI retuning until Amanda judges section/content/helper alignment, spacing/density, body/helper typography, color balance, icon crispness/semantics, footer icon-label rhythm, and normal/minimum-size balance.
- Preserve all protected conversion/framing/adaptive/updater/subprocess/toolchain behavior. Runtime remains dev.25; no `main` promotion or public release is authorized.

## PFC-2026-09-14-055 — Mockup fidelity continuation after run #79 human visual review

- Required bootstrap completed before material editing: `PROJECT_CONTRACT.md`, `ACTIVE_CONTEXT.md`, canonical `docs/UX_SPEC.md`, current font/style/layout/widget/fidelity files, packaged smoke because presentation/package assertions are relevant, and `THIRD_PARTY.md` for the new icon source.
- New human evidence superseded the prior wait state: the run-#79 tester was technically PASS but visually still too far from the approved mockup in container rhythm, text scale, right-rail alignment, palette nuance, footer icon/text spacing, and icon quality/semantics.
- Preserve the confirmed bundled Polymorph Regular/Bold display family and bundled Inter body/UI family. No system-font dependency is introduced.
- Presentation correction is isolated in the branded fidelity layer: smaller/denser normal-size body/control/helper type, mockup-like dark/gold/ivory/red palette tuning, normal-size card rhythm, and a single optical content axis beneath section headings.
- Output Format, Sizing, GIF Priority, Framing, Aspect Ratio, Crop Zoom, and Output Folder are aligned to the section-title text column. Helper copy no longer receives the oversized legacy indent.
- Use coherent Lucide SVG section glyphs at a larger design size. Required semantic corrections: `FRAMING` = crop icon; `CROP ZOOM` = hourglass. Existing social links remain Simple Icons SVGs, enlarged and spaced farther from their labels.
- The minimum-size rail compaction is protected: fidelity container-geometry overrides do not run at scale `<= 0.76`, preserving the accepted 920×640 primary-action budget.
- Added `LUCIDE_LICENSE.txt`, package text notices, and documented Lucide in `THIRD_PARTY.md`.
- Five accidental temporary staging files created during assembly were removed from the final candidate tree.
- Runtime remains `0.1.0-dev.25`. No conversion, adaptive GIF, framing/export geometry, output sizing, updater, subprocess, or pinned toolchain behavior changes.
