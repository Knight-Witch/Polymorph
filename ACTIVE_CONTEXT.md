# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** human visual follow-up on dev.25 after run #62. The custom Polymorph font is now correct; the active pass is presentation-only polish from Amanda's installed screenshot/feedback.  
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
- Last technical-PASS baseline: code commit `112f2e2efb128ef806cb6f44ed650b9753a5471e`; Windows Dev Build run #62 / run ID `34809405250`; installer artifact ID `10334421612`; digest `sha256:c77908691be09782951a52d8537e7c629681a3f6638e5a48e09b7880966b9384`.
- Human review of that installed tester confirms the custom Polymorph face is finally applied correctly. Do not reopen font provenance, asset transport, registration, or direct-label ownership.
- Human-requested visual changes for the next candidate:
  - shrink FILES/right-rail section headings optically;
  - replace low-quality/mixed section icons with a coherent thin-line SVG family;
  - Framing and Crop Zoom must use distinct icons;
  - align Output Format/Sizing/GIF Priority radio bubbles to one content column;
  - align helper copy under Preserve/Favor with the radio-label text column;
  - reduce Browse/Add Files button text;
  - replace the effectively missing text playback glyph with real play/pause icons;
  - center the primary `POLYMORPH` label against the full action-button bounds.
- Implementation is presentation-only: `fidelity_pass.py` reapplies optical adjustments after responsive scaling; `brand_widgets.py` centers the primary-action title; new SVG assets provide the section/playback icons.
- The accepted compact-rail logic from run #62 remains unchanged.
- The next exact implementation commit/run/artifact identity must replace this paragraph after CI completes.
- dev.24 remains technical PASS / human visual FAIL and must not be promoted.
- No public release exists; `main` remains non-experimental.

## Intended typography

Amanda's supplied custom files register as one Polymorph family with Regular and Bold faces. They are bundled/self-contained; users do not install them separately.

- Brand title, subtitle/byline, primary action: Polymorph Regular.
- FILES and every right-rail CardHeading: Polymorph Bold.
- Body/control/footer text: Inter.
- Human review specifically requests smaller card-heading optical size while preserving the correct Polymorph Bold face.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum; run #62 cleared the minimum-size packaged gate.
- Preserve the current responsive minimum-only rail compaction unless new evidence shows a regression.
- Bundled Polymorph font application is confirmed both technically and visually.

## Next gate

1. Consolidate the visual-polish edits and required tracking docs into one clean `dev` commit.
2. Run the full canonical Windows workflow; packaged smoke must still pass bundled font application and 920×640 primary-action visibility.
3. On full PASS, retrieve the new `Polymorph-dev-installer` artifact directly and record commit/run/artifact identity here.
4. Amanda visually checks heading scale, section icons, radio/helper alignment, playback control, button text sizing, centered primary action, and overall full/minimum-window balance.
5. Only after that visual PASS proceed to the deferred working/loading animation phase.
