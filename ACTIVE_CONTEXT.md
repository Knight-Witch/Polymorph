# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** dev.26 branded-presentation HUMAN VISUAL REVIEW. Windows Dev Build run #93 is FULL PASS and the correctly labeled dev.26 installer artifact has been retrieved and checksum-verified.  
**Runtime posture:** conversion/framing/adaptive behavior remains closed/validated for current v1 scope; do not reopen it without new evidence. Branded presentation fidelity is awaiting Amanda's visual acceptance.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `src/polymorph/app.py`
5. `src/polymorph/ui/fonts.py`
6. `src/polymorph/ui/styles.py`
7. `src/polymorph/ui/branded_layout.py`
8. `src/polymorph/ui/brand_widgets.py`
9. `src/polymorph/ui/fidelity_pass.py`
10. `src/polymorph/ui/visual_patch.py`
11. `src/polymorph/ui/compact_status_patch.py`
12. `src/polymorph/smoke_test.py` only if a package assertion itself is implicated

Do not preload engine/history files unless the current task actually needs them.

## Current Dev candidate

- Branch: `dev`.
- Runtime version: `0.1.0-dev.26`.
- Final implementation/package-label commit: `1927f88264786ea2b568bb98a87653571ab7168d`.
- Windows Dev Build run #93 / run ID `34923465313`: **FULL PASS**.
- Run #92 / `34923070361` first proved the responsive geometry correction with a full technical PASS; its installer was intentionally not handed off because `installer/Polymorph.iss` still named the package dev.25.
- Run #93 corrected the installer identity to dev.26 and re-passed every technical/build/package gate.
- Tester artifact: `Polymorph-dev-installer`, artifact ID `10378963848`.
- Artifact ZIP SHA-256: `465caa8821f642a5e3139ffc4a0d803e8803cd70beb2a7809d1ce05257bef2b5`.
- Installer inside artifact: `Polymorph_Setup_v0.1.0-dev.26.exe`.
- Installer SHA-256: `203013ebc65c1dc99321c25b9c6143db98f8a6aaed1ce99b053a1bc751e8c6fe`.
- Companion `.sha256` file was checked and matches the installer.
- No public release exists; `main` remains non-experimental.

## dev.26 presentation state

Preserve these implemented features unless Amanda explicitly asks to change them:

- supplied Polymorph Regular/Bold display fonts, self-contained and Qt-registered;
- direct final-device-pixel SVG rendering for high-DPI sharpness;
- smooth black-to-blue-black card gradients without warm glow/grain;
- cooler white-gold/champagne headings, icons, borders, and hardware;
- slightly smaller Polymorph Bold tool headings;
- equal max-MB / resolution-field widths and matching dark surfaces;
- horizontally full-width deep-crimson primary action with small `CONVERT MEDIA` beneath `POLYMORPH`;
- larger Ready ring and smaller Ready helper/detail text at normal size;
- compact scale `<= 0.76`: primary action height applied synchronously through `RefinedPolymorphButton.apply_scale` as `max(42, round(55 * scale))`, and Ready ring returns to 24 px.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening, and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and the 920×640 supported minimum.
- Preserve minimum-only rail compaction at responsive scale `<= 0.76`; presentation geometry must not override it.
- Bundled Polymorph Regular/Bold and Inter application is confirmed.
- Packaged application smoke now passes unchanged at minimum size.

## Next gate

1. Give Amanda the run #93 `Polymorph-dev-installer` artifact for human visual review.
2. Human review should focus on icon sharpness, cooler white-gold color balance, smooth dark gradients, equal sizing fields, normal-size primary-action weight/full width and `CONVERT MEDIA`, smaller tool headings, larger Ready ring, smaller Ready helper copy, and normal/minimum-size balance.
3. If Amanda reports a visual issue, change only the implicated presentation layer; do not reopen engine/adaptive/framing work without concrete evidence.
4. If dev.26 is visually accepted, record visual-fidelity **HUMAN PASS** and proceed to the deferred working/loading animation phase.
5. Deferred animation direction already approved conceptually: multi-ring arcane/alchemic circle, rotating rune ring, counter-rotating outer geometry, restrained orbiting sparks, and progressive center-emblem reveal tied to progress; final behavior can be tuned during that phase.
6. Do not promote to `main` or create a public release without explicit approval.
