# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** dev.25 presentation-only polish from Amanda's installed screenshot/feedback. The visual-polish code itself continues to build cleanly; current CI repair work is only restoring the proven packaged-smoke harness after an accidental over-broad test-file replacement.  
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
- Consolidated visual-polish implementation: `b9196d17c67393ba79f509b107e30c08b55915ef`.
- Run #75 / ID `34820011338`: visual-polish code, unit suite, protected runtime/toolchain gates and frozen app build PASS; packaged smoke stopped on stale `mockup-v1` expectation.
- Run #77 / ID `34820591656`: updated `mockup-v2` expectation was accepted and all pre-package gates again PASS, but packaged smoke failed font-state validation because the first smoke repair accidentally replaced additional proven harness code. Comparison against `b9196d17` identified the accidental differences: wrong font-state property names/checks, lost offscreen window placement, lost bundled-converter readiness assertion, and lost final Qt event processing. This is test-harness drift, not evidence that the visual-polish runtime broke font registration.
- Immediate repair restores `src/polymorph/smoke_test.py` exactly from `b9196d17`, with one and only one intended delta: `polymorphFidelity` expects `mockup-v2` instead of `mockup-v1`.
- Human-requested visual changes in the candidate:
  - smaller FILES/right-rail section headings while preserving Polymorph Bold;
  - coherent thin-line SVG icons with distinct Framing and Crop Zoom symbols;
  - one aligned radio-bubble column for Output Format, Sizing and GIF Priority;
  - helper copy aligned with Preserve/Favor label text;
  - smaller Browse/Add Files text;
  - real play/pause SVG playback control;
  - primary `POLYMORPH` label centered against the full button bounds.
- Implementation remains presentation-only: `fidelity_pass.py` reapplies optical adjustments after responsive scaling; `brand_widgets.py` centers the primary-action title; new SVG assets provide section/playback icons.
- The accepted compact-rail logic from run #62 remains unchanged.
- The next exact successful implementation commit/run/artifact identity must replace this paragraph after CI completes.
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

1. Re-run the full canonical Windows workflow with the proven run-#75 smoke harness restored and only the `mockup-v2` expectation changed.
2. Packaged smoke must pass bundled font application, mockup-v2 presentation, Polymorph heading typography, two-column shell, FILES grouping, 920×640 primary-action visibility, preview decode, framing/adaptive/resolution mapping and footer metadata in the same frozen app.
3. On full PASS, retrieve the new `Polymorph-dev-installer` artifact directly and record commit/run/artifact identity here.
4. Amanda visually checks heading scale, section icons, radio/helper alignment, playback control, button text sizing, centered primary action, and overall full/minimum-window balance.
5. Only after that visual PASS proceed to the deferred working/loading animation phase.
