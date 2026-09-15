# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.26 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-058 — Human visual correction pass / dev.26 candidate

- Required bootstrap completed from `PROJECT_CONTRACT.md` + `ACTIVE_CONTEXT.md`, then only the routed presentation files needed for this correction. Protected conversion/framing/adaptive areas were not reopened.
- Human review of run #84 supplied new visual evidence: alignment improved, but card icons remained blurry; the primary Polymorph action was too visually narrow/short; MB and resolution fields did not match; the UI still leaned too yellow/gold; the card fill looked like a low-quality warm gold-to-black fade; tool headings remained slightly oversized; and the Ready ring/helper scale did not match the mockup hierarchy.
- New candidate is `0.1.0-dev.26`. The patch is deliberately presentation-only and is installed before branded layout imports so the existing layout/state wiring remains authoritative.
- SVG icons are now rendered directly with Qt's SVG renderer at the final device-pixel size and only then tinted, including high-DPI scaling. This targets the observed icon softness without changing icon semantics or assets.
- Card painting is replaced by a smooth black/very-dark blue-charcoal gradient with restrained cool neutral borders. The old warm radial glow and synthesized grain are not used in this pass.
- Palette overrides move headings/icons/borders/hardware toward white-gold/champagne and cooler neutral grays while retaining the existing restrained crimson radio/action emphasis.
- Sizing fields are normalized to the same responsive width and dark surface treatment. Disabled resolution fields remain visually subdued by text/border rather than by a different panel fill.
- Section-heading typography is reduced slightly while keeping bundled Polymorph Bold.
- Primary action is enlarged, keeps the full rail width, loses the trailing spacer below it, remains deep crimson, and now renders small `CONVERT MEDIA` text below `POLYMORPH`.
- Ready status receives a larger painted crimson ring; status helper text is reduced.
- Static Python compilation of the new presentation module passed before commit assembly. This environment does not provide PySide6, so runtime/packaged validation is intentionally delegated to the canonical Windows CI pipeline.
- No GIF/MP4 encoding, adaptive policy, framing geometry, output sizing, updater, no-console subprocess, font payload, FFmpeg/gifski pin, `main` branch, or public-release behavior changed.
- Next gate: full Windows Dev Build CI, including the existing packaged UI smoke and 920×640 primary-action visibility gate, followed by Amanda's human visual check of the resulting installer.

## PFC-2026-09-14-057 — Chat-limit handoff / preserve self-contained Polymorph font boundary

- Handoff requested because the conversation reached its maximum length. `ACTIVE_CONTEXT.md` is refreshed as the authoritative next-chat baton; no runtime implementation work is performed in this handoff.
- Immediate user correction carried forward explicitly: Amanda's supplied Polymorph Regular/Bold display files came from a free/open-license font provider, are a Trajan-derived/version-based design, and are not Adobe's font distribution. Do not restart Adobe/system-font speculation unless Amanda explicitly asks for independent provenance verification.
- The repository already implements the required deployment model: `Polymorph-Regular.ttf.xz` and `Polymorph-Bold.ttf.xz` are packaged assets, decompressed losslessly in memory, and registered with Qt by `src/polymorph/ui/fonts.py`. Friends/users do not install a font separately.
- A closing-chat proposal to refuse bundling and convert display text to SVG/vector outlines was rejected by Amanda and was not implemented. The next chat must ignore that proposal and preserve the actual bundled font path.
- Run #84 dev.25 remains the active tested candidate and human visual gate. No code, font asset, version, package, CI, installer, conversion, framing, adaptive, updater, subprocess, or toolchain behavior changes in this documentation-only handoff.

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
