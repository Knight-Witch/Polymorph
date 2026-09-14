# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.25 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-14-055 — Mockup alignment, density, palette, and vector-icon fidelity after run #79 human review

### Summary

- Human review of the installed run-#79 dev.25 tester rejected the remaining presentation fidelity: card/container rhythm, body/control text scale, right-rail content alignment, footer icon/label spacing, icon sharpness, and some icon semantics still differ materially from the approved mockup.
- Keep the proven bundled Polymorph Regular/Bold display typography and Inter body/UI family. This pass does not re-open font registration or provenance.
- Tighten normal-size card padding/gaps and body/control/helper typography toward the mockup while preserving the accepted 1260×820 design geometry. The proven compact rail at `<= 0.76` scale is explicitly left untouched so the 920×640 primary action remains visible.
- Align right-rail section content to the same optical text axis as each section title: Output Format, Sizing, GIF Priority, Framing, Aspect Ratio, Crop Zoom, and Output Folder now use one consistent title/content/helper column system rather than accumulated large per-widget indents.
- Reduce the over-indented helper copy under GIF/MP4 and Preserve/Favor so subtitles sit under their labels instead of drifting far right.
- Refine the presentation palette toward the approved mockup: darker inputs/surfaces, softer ivory body copy, more muted helper copy, restrained champagne-gold headings/dividers, and the existing crimson selection accent.
- Increase branded section icons to about 18 px at design scale and replace the mixed/soft section glyphs with a coherent Lucide thin-line SVG set. `FRAMING` explicitly uses the crop glyph; `CROP ZOOM` explicitly uses an hourglass per Amanda's direction. Files, Output Format, Sizing, GIF Priority, Aspect Ratio, and Output Folder also use purpose-specific Lucide vectors.
- Keep the existing Simple Icons social SVGs, but enlarge footer icons and increase icon-to-label spacing so the service row reads more like the mockup. The update glyph also stays vector-backed.
- Add the upstream Lucide ISC/MIT notice to packaged assets and record Lucide in `THIRD_PARTY.md`.
- Runtime remains `0.1.0-dev.25`; this is presentation-only. No GIF/MP4 encoding, adaptive GIF selection, Crop/Fit geometry, output sizing, updater, subprocess, or pinned FFmpeg/gifski behavior changes.
- Clean up five accidental temporary staging files created while assembling this pass; they are not part of the candidate tree.

### Validation plan

- Run the complete Windows pipeline unchanged: bundled fonts, all unit tests, pinned toolchain, adaptive integration, GIF reference comparison, frozen build, packaged UI smoke, Inno Setup, checksum, and artifact uploads.
- If CI passes, retrieve the installer directly and require human visual review of title/content axes, normal-size card density, body/helper scale, icon crispness/semantics, footer icon-label rhythm, colors, and the preserved 920×640 minimum-size balance.
- Do not promote to `main` or create a public release without explicit approval.
