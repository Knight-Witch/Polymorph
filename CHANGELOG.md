# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.25 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-14-056 — Run #84 passes the complete mockup-fidelity candidate pipeline

### Summary

- Windows Dev Build run #84 / run ID `34890815616` from implementation commit `e76f88808f471c74ae100469ed4452a5095560b0` completed successfully.
- The full configured Windows pipeline passed: packaged Polymorph/Inter fonts, unit tests, pinned FFmpeg 9.0.1/gifski 1.32.0 verification, adaptive integration, GIF reference comparison, frozen application build, packaged UI smoke, Inno Setup compilation, checksum generation, and both artifact uploads.
- The existing packaged UI smoke still passes after the presentation changes, including bundled display-font application, `mockup-v2`, two-column composition, FILES grouping, 920×640 primary-action visibility, animated preview initialization, adaptive controls, Crop/Fit mapping, crop zoom, linked resolution, and footer metadata.
- Installer artifact `Polymorph-dev-installer`: ID `10366663850`, artifact digest `sha256:a3ccd6e2d1a131fe0ef66f70d3a3781605ea4b9be2e6e09362f29c366f3f4c38`.
- Retrieved artifact contains `Polymorph_Setup_v0.1.0-dev.25.exe`; independently computed installer SHA-256 is `5dc38ba315cb274fee8db9377db93d10f532c4ba39784187d16b69a891496c29`, matching the generated `.sha256` companion.
- The candidate now awaits human visual review only. Technical PASS does not determine whether the new alignment, density, palette, icon semantics, or footer rhythm visually match the approved mockup closely enough.
- Runtime remains `0.1.0-dev.25`; no conversion/framing/adaptive/updater/subprocess/toolchain behavior changed and no public release was created.

## POLY-2026-09-14-055 — Mockup alignment, density, palette, and vector-icon fidelity after run #79 human review

### Summary

- Human review of the installed run-#79 dev.25 tester rejected the remaining presentation fidelity: card/container rhythm, body/control text scale, right-rail content alignment, footer icon/label spacing, icon sharpness, and some icon semantics still differ materially from the approved mockup.
- Keep the proven bundled Polymorph Regular/Bold display typography and Inter body/UI family. This pass does not re-open font registration or provenance.
- Tighten normal-size presentation rhythm and body/control/helper typography toward the mockup while preserving the accepted 1260×820 design geometry. The proven compact rail at `<= 0.76` scale is explicitly left untouched so the 920×640 primary action remains visible.
- Align right-rail section content to the same optical text axis as each section title: Output Format, Sizing, GIF Priority, Framing, Aspect Ratio, Crop Zoom, and Output Folder now use one consistent title/content/helper column system rather than accumulated large per-widget indents.
- Reduce the over-indented helper copy under GIF/MP4 and Preserve/Favor so subtitles sit under their labels instead of drifting far right.
- Refine the presentation palette toward the approved mockup: darker inputs/surfaces, softer ivory body copy, more muted helper copy, restrained champagne-gold headings/dividers, and the existing crimson selection accent.
- Increase branded section icons to about 18 px at design scale and replace the mixed/soft section glyphs with a coherent Lucide thin-line SVG set. `FRAMING` explicitly uses the crop glyph; `CROP ZOOM` explicitly uses an hourglass per Amanda's direction. Files, Output Format, Sizing, GIF Priority, Aspect Ratio, and Output Folder also use purpose-specific Lucide vectors.
- Keep the existing Simple Icons social SVGs, but enlarge footer icons and increase icon-to-label spacing so the service row reads more like the mockup. The update glyph also stays vector-backed.
- Add the upstream Lucide ISC/MIT notice to packaged assets and record Lucide in `THIRD_PARTY.md`.
- Runtime remains `0.1.0-dev.25`; this is presentation-only. No GIF/MP4 encoding, adaptive GIF selection, Crop/Fit geometry, output sizing, updater, subprocess, or pinned FFmpeg/gifski behavior changes.
- Cleaned five accidental temporary staging files from the final candidate tree.
