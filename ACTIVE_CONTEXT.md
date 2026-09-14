# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** human visual validation of the dev.25 presentation-polish tester from Windows Dev Build run #79. The requested heading/icon/alignment/playback/button-centering pass is technically complete; do not continue changing presentation until Amanda evaluates the installed tester.  
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
8. `src/polymorph/ui/fidelity_pass.py`
9. `src/polymorph/smoke_test.py` only if a UI/package assertion is being changed

Do not preload engine/history files unless the current task actually needs them.

## Current Dev candidate

- Branch: `dev`
- Runtime version: `0.1.0-dev.25`
- Current tested implementation commit: `06ad854d3cab7c1f249b253673e99ce18196cee5` (`Restore proven packaged smoke harness for mockup v2`).
- Windows Dev Build run #79 / run ID `34821077711`: **FULL PASS**.
- Run #79 passed bundled custom-font verification, all 56 unit tests, pinned FFmpeg/gifski toolchain checks, adaptive integration, GIF reference comparison, frozen application build, complete packaged UI smoke, Inno Setup compilation, SHA-256 generation, unpacked-app upload, and installer upload.
- Packaged smoke passed the restored bundled Polymorph font checks, `mockup-v2` presentation tag, applied Polymorph title/subtitle/card-heading typography, two-column shell, FILES grouping, 920×640 primary-action visibility, concept field/alignment/slider styling, animated WebP preview, adaptive GIF controls, framing/crop zoom mapping, linked resolution controls, and footer metadata in the same frozen application.
- Installer artifact: `Polymorph-dev-installer`, artifact ID `10338840830`, digest `sha256:5f15f4246c1a6fa254b86b7977a0716ad2e385c6abb4135b7f66a8a0bb79cb7e`.
- The tester was retrieved directly as `Polymorph-dev.25-visual-polish-installer.zip`.
- Human-requested visual changes included in this candidate:
  - smaller FILES/right-rail section headings while preserving Polymorph Bold;
  - coherent thin-line SVG section icons with distinct Framing and Crop Zoom symbols;
  - one aligned radio-bubble column for Output Format, Sizing and GIF Priority;
  - Preserve/Favor helper copy aligned with radio-label text;
  - smaller Browse/Add Files text;
  - real SVG play/pause playback control;
  - primary `POLYMORPH` label centered against the full action-button bounds.
- Implementation is presentation-only: `fidelity_pass.py` reapplies optical adjustments after responsive scaling; `brand_widgets.py` centers the primary-action title; SVG assets provide the section/playback icons.
- Run #75 / ID `34820011338` and run #77 / ID `34820591656` are failed CI evidence only. Their failures were smoke-harness/version-assertion issues and produced no installer. Do not treat them as current candidates.
- The accepted compact-rail logic from run #62 remains unchanged.
- dev.24 remains technical PASS / human visual FAIL and must not be promoted.
- No public release exists; `main` remains non-experimental.

## Intended typography

Amanda's supplied custom files register as one Polymorph family with Regular and Bold faces. They are bundled/self-contained; users do not install them separately.

- Brand title, subtitle/byline, primary action: Polymorph Regular.
- FILES and every right-rail CardHeading: Polymorph Bold.
- Body/control/footer text: Inter.
- Run #79 retains the smaller card-heading optical size requested in the latest human review.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum; run #79 again cleared the minimum-size packaged gate.
- Preserve the current responsive minimum-only rail compaction unless new evidence shows a regression.
- Bundled Polymorph font application is confirmed both technically and visually from the earlier run #62 review and technically again in run #79.

## Next gate

1. Amanda installs/runs the run-#79 tester and visually checks heading scale, section icons, radio/helper alignment, playback control, Browse/Add Files sizing, centered primary action, and overall full/minimum-window balance.
2. If she finds visual issues, change only the branded presentation/UI layer implicated by that evidence; do not reopen protected conversion/runtime areas.
3. If she accepts the visual pass, mark dev.25 UI polish human-PASS and proceed to the deferred working/loading animation phase.
4. Do not promote to `main` or create a public release without Amanda's explicit approval.
