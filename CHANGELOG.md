# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.26 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-14-059 — Restore minimum-size rail budget after run #85 smoke failure

### Summary

- Windows Dev Build run #85 / run ID `34914748497` validated the dev.26 presentation code through unit tests, pinned fonts/toolchain, adaptive integration, GIF reference comparison, and frozen application build, then correctly failed the packaged UI smoke at the protected 920×640 gate.
- Failure was isolated to the primary action geometry: `POLYMORPH action is clipped at minimum size: button bottom 505, rail 467`. No conversion/runtime gate failed.
- Diagnosis: the initial dev.26 visual patch forced the larger normal-size button height at every responsive scale and permanently removed the rail spacer. That overrode the already-proven compact rail behavior protected at scale `<= 0.76`.
- Fix keeps the substantial 82px-class crimson action at normal/design scale, restores the proven compact 68px-scaled/49px-floor behavior at `<= 0.76`, and no longer removes the rail spacer. The full-width red action and `CONVERT MEDIA` secondary line remain unchanged.
- Runtime remains `0.1.0-dev.26`; no conversion, framing, adaptive, updater, subprocess, font asset, toolchain, or public-release behavior changed. Canonical Windows CI is rerun before human review.

## POLY-2026-09-14-058 — Correct mockup palette, button weight, icon sharpness, and status scale

### Summary

- Human review of the technically passing run-#84/dev.25 tester accepted the improved alignment but identified concrete remaining presentation defects: section icons still looked blurry, the primary `POLYMORPH` action was too visually narrow/short for its rail slot, the MB field did not match the resolution fields, the palette remained too yellow/gold, card surfaces had a warm/grainy gold-to-black fade instead of the mockup's clean dark gradient, tool headings were still slightly too large, and the Ready indicator/helper hierarchy was too small/large respectively.
- Bumped the development candidate to `0.1.0-dev.26`; this pass is presentation-only.
- SVG icons now render directly at final device-pixel resolution before tinting, card surfaces use smooth black-to-blue-black gradients, palette accents shift toward cool white-gold/champagne, sizing fields use matched geometry/surfaces, tool headings are smaller, the Ready ring is larger, and helper copy is smaller.
- Primary action is deep crimson, visually substantial at normal size, and renders small `CONVERT MEDIA` beneath `POLYMORPH`.
- No conversion, framing, adaptive GIF, file-size fitting, MP4, updater, subprocess, toolchain, font asset, or public-release behavior changed.

## POLY-2026-09-14-057 — Record chat handoff and exact bundled-font boundary

### Summary

- Preserved Amanda's explicit typography boundary: the supplied Polymorph Regular/Bold faces remain bundled/self-contained and are not replaced by system-font dependencies or vector-outline text.
- Run #84/dev.25 remained the protected technical baseline entering the current visual-fidelity pass.
