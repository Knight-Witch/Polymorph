# Changelog

## POLY-2026-09-11-026 — 2026-09-11 17:30 PDT — Trace adaptive fallback decisions

### Summary

- Recorded successful human validation of dev.14 presentation: the default window now sizes correctly and the new hover tooltips work well on the user's Windows setup.
- Inspected the user-supplied dev.13 Viper result and confirmed source-frame decimation did not survive the adaptive gates. The output is again the exact Preserve-motion baseline: `1552x1552`, 93,630,962 bytes, 375 frames at 40 ms over 15.0 s, SHA-256 `dbfd1be7211b801f3a3a8d0ffaaf1058a1974f6b27141ef5f3be5ce55452e5af`.
- Stopped blind adaptive-policy changes. The final fallback file alone cannot distinguish whether stride 2/3 failed the measured-byte gain gate, failed the completed >=8% realized-gain gate, or hit an adaptive encode/integrity error that was caught before fallback.
- Added `DiagnosticAdaptiveConverter`, a development-only observation wrapper over the existing `AdaptiveConverter`. It records the source/native geometry, byte ceiling, every baseline/adaptive encode result, stride metadata, sample byte cost, predicted linear gain, full adaptive-fit result/error, and final selection/fallback without changing the underlying planning or encode decisions.
- Dev.15 Favor-resolution jobs write a compact `*_ADAPTIVE_DIAGNOSTIC.json` sidecar beside the GIF; the completion line reports that sidecar filename. Preserve-motion and MP4 jobs do not emit the trace, and a diagnostic-write failure is non-fatal.
- Added direct unit coverage for measured-gain rejection, successful selected-candidate classification, and JSON sidecar output.
- Added `build/verify_adaptive_converter.py`, a process-level integration gate using the actual `Converter`/`AdaptiveConverter` plus pinned FFmpeg/gifski. It creates a deterministic high-entropy 25 FPS animated WebP, measures full-resolution and stride-2 costs, chooses a cap that forces a meaningful trade, and fails unless Favor resolution really returns fewer frames, stays under the same cap, and gains at least 8% linear resolution over Preserve motion.
- Added the integration gate and its JSON artifact to Windows CI before packaging. This separates a real control-flow/toolchain defect from a workload such as Viper whose GIF byte economics may simply not justify decimation.
- Carried the human-validated dev.14 UI geometry/tooltips forward unchanged and incremented the tester to `0.1.0-dev.15`.
- Actual conversion policy is unchanged from dev.13: same stride order, 8% predicted/final gain floors, 2048px/native soft target, exact loop-delay correction, gifski 1.32.0, quality 100, dev.8 smart-fit sizing, and Preserve-motion/MP4 behavior.

### Touched files

- `src/polymorph/diagnostic_adaptive_converter.py`
- `src/polymorph/ui/adaptive_main_window.py`
- `tests/test_adaptive_diagnostics.py`
- `build/verify_adaptive_converter.py`
- `.github/workflows/windows-dev-build.yml`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `build/README.md`
- `docs/ARCHITECTURE.md`
- `docs/UX_SPEC.md`
- `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to dev.14: the same dev.13 adaptive conversion policy plus the human-validated UI pass, without JSON decision tracing or the process-level adaptive integration gate.

### Test notes

- Unit tests must cover diagnostic outcome classification and sidecar serialization in addition to all existing adaptive/planner/timing tests.
- Windows CI must pass the new process-level adaptive-selection gate with the exact pinned FFmpeg 9.0.1/gifski 1.32.0 toolchain, then the existing reference diagnostic, packaged-app smoke, installer compilation, checksum generation, and artifact uploads.
- The next human Viper test should use GIF / Original / 99 MB / Favor resolution and return the generated `*_ADAPTIVE_DIAGNOSTIC.json`; no additional adaptive-policy change should be made before that trace is inspected.

## POLY-2026-09-11-025 — 2026-09-11 17:05 PDT — Fix first-launch layout compression and add hover tooltips

### Summary

- Responded to the user-reported first-launch UI defect where the old 1080x720 default window height compressed the right-side settings rail after the GIF-priority section was added; values and radio-label text rendered clipped until the user manually made the window taller.
- Kept the existing three-column layout and visual palette, but changed the adaptive UI's normal opening size to 1080x800 with a 900x700 resize floor and slightly tighter right-rail spacing.
- Added minimum visual heights for section headings, radio buttons, combo boxes, and spin boxes so controls do not collapse into unreadable rows near the lower resize range.
- Improved disabled-state styling for radio/input controls without changing their enabled/disabled logic.
- Added concise hover tooltips to the file queue, live preview, GIF/MP4 choices, sizing modes and fields, GIF priority controls, framing controls, output folder, primary conversion action, Add Files, Remove Selected, and Cancel. Existing footer/aspect-guide/output-folder tooltips remain.
- Extended the packaged-app smoke gate to require the new default geometry, minimum height, and primary-control tooltip coverage before an installer is accepted.
- Updated UX/status documentation and incremented the development tester to `0.1.0-dev.14`.
- Conversion behavior is intentionally untouched: dev.14 carries dev.13 exact source-frame-decimation Favor-resolution logic verbatim, along with Preserve-motion GIF, MP4, framing math, updater, dependencies, and file-size behavior.

### Touched files

- `src/polymorph/ui/adaptive_main_window.py`
- `src/polymorph/ui/styles.py`
- `src/polymorph/smoke_test.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/UX_SPEC.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.13's 1080x720 first-launch geometry and prior control styling/tooltips. Conversion output is independent of this UI-only change.

### Test notes

- Packaged-app smoke coverage now fails if the adaptive window initializes below 1080x800, if its minimum height falls below 700, or if the primary settings controls lose their hover tooltip text.
- Full Windows CI must pass unit tests, the dev.13 exact source-decimation toolchain smoke, standalone-reference diagnostic, packaged UI smoke, installer compilation, checksum generation, and artifact upload before dev.14 is handed to the user.
- Human UI validation should confirm that the first-launch control rail renders normally at the user's Windows DPI/scaling without manually increasing the window height and that hover tooltips appear as expected.

## POLY-2026-09-11-024 — 2026-09-11 05:55 PDT — Use exact source-frame decimation for Favor resolution

### Summary

- Recorded the dev.12 Viper human result: `1552x1552 • 93.6 MB • 25 FPS`, identical in the UI to dev.11 despite the interpolation-method change.
- Compared the supplied dev.11 and dev.12 outputs directly and confirmed they are byte-for-byte identical: 93,630,962 bytes, SHA-256 `dbfd1be7211b801f3a3a8d0ffaaf1058a1974f6b27141ef5f3be5ce55452e5af`, 1552x1552, 375 frames, 40 ms per frame, 15.0 s. The adaptive candidate was being discarded and the exact Preserve-motion baseline copied back out.
- Concluded the synthetic even-timestamp branch is exhausted for this Viper workload: both optical-flow and linear-blend synthesized frames fail to create enough gifski byte savings for the desired resolution trade.
- Identified and fixed a separate adaptive orchestration defect: dev.10-dev.12 could stop after a candidate passed the measured prediction gate but failed the completed 8% realized-gain veto, returning the baseline without testing deeper candidates. Dev.13 continues to the next candidate instead.
- Replaced only the experimental Favor-resolution synthesis path with deterministic source-frame decimation. Polymorph now tests exact integer strides nearest the source motion first, retaining every second original decoded frame and then every third frame while the effective rate remains above the automatic 8 FPS floor.
- Added `gif_timing.py` to inspect GIF Graphic Control Extension delays and losslessly patch only the final frame delay when the source frame count is not divisible by the selected stride.
- Viper stride 2 retains 188 original frames: 187 ordinary 80 ms intervals plus one 40 ms loop-closure interval, totaling the original 15.0 s and preserving constant source angular speed without synthesized images or periodic 1/2-step frame deletion.
- Kept real gifski sample cost authoritative, retained the ~8% predicted and final linear-gain thresholds, the 2048 px/native soft target, dev.8 GIF smart-fit search, true 99 MB ceiling, gifski 1.32.0, quality 100, `--extra`, explicit width, yuv420p, and infinite repeat.
- Added regression tests for Viper stride/remainder math, lossless final-delay patching, measured decimation planning, and the previously missing continue-to-deeper-candidate behavior after a failed final-gain veto.
- Reworked Windows toolchain smoke coverage to verify every-second-frame source decimation and exact closure-delay correction on an odd five-frame 25 FPS source.
- Preserve-motion GIF, MP4, framing, updater, preview, general UI layout, and public release state remain unchanged. Favor-resolution tooltip wording was updated to match the new original-source-frame strategy.
- Incremented the development tester to `0.1.0-dev.13`.

### Touched files

- `src/polymorph/adaptive_converter.py`
- `src/polymorph/motion_planner.py`
- `src/polymorph/gif_timing.py`
- `src/polymorph/ui/adaptive_main_window.py`
- `tests/test_motion_planner.py`
- `tests/test_gif_timing.py`
- `tests/test_adaptive_converter.py`
- `build/verify_toolchain.py`
- `build/README.md`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/UX_SPEC.md`
- `docs/ARCHITECTURE.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.12's synthetic exact-timestamp temporal-blend Favor-resolution experiment. Preserve-motion GIF, MP4, framing, updater, and the dev.8 GIF smart-fit search are independent of this adaptive change.

### Test notes

- Pure tests cover Viper stride-2/stride-3 frame/timing math, measured decimation gain gates, byte-level final GIF delay patching, and continuing to a deeper stride after a higher candidate fails the final realized-gain test.
- Windows CI must pass the exact source-decimation/closure-timing smoke, existing Preserve-motion GIF and MP4 gates, standalone-reference timing diagnostic, packaged-app smoke, installer compilation, checksum generation, and artifact upload before dev.13 is handed to the user.
- Human Viper validation should now produce a materially different result if source-frame decimation earns the spatial gain. For stride 2, expected temporal shape is 188 retained original frames over 15.0 s (~12.53 average FPS); user validation should focus on recovered dimensions and whether the lower motion rate/loop seam are acceptable.

## POLY-2026-09-11-023 — 2026-09-11 03:05 PDT — Test lower-complexity uniform temporal blending

### Summary

- Recorded the dev.11 Viper human result: `1552x1552 • 93.6 MB • 25 FPS` with Favor resolution selected.
- Independently inspected the supplied dev.11 GIF and confirmed it is 1552x1552, 93,630,962 bytes, 375 frames, exactly 40 ms per frame, and 15.0 s total; Preserve motion was retained exactly after every measured 20/16.67/14.29/12.5 FPS optical-flow candidate failed the existing ~8% spatial-gain gate.
- Stopped extending the optical-flow FPS ladder. The evidence now shows that motion-compensated synthesized frames remain too expensive for gifski on this workload even after a 50% nominal frame-rate reduction.
- Ran an isolated local comparison using the dev.11 Viper output as a 25 FPS source surrogate. At 20 FPS, `minterpolate=mi_mode=blend` produced essentially the same uniform adjacent-frame cadence energy as the prior MCI path, and 768 px crop/contact-sheet checks showed the blend and MCI frames to be visually extremely close around face, hair/fur, torso, cape and sword over the sampled segment.
- Changed only Favor-resolution reduced-FPS synthesis from motion-compensated optical flow to exact-timestamp linear temporal blending. No periodic frame deletion is introduced; every chosen GIF cadence remains uniform.
- Kept the dev.11 candidate ladder (`20 -> 16.67 -> 14.29 -> 12.5 FPS`), real encoded candidate-cost measurement, ~8% predicted linear-gain requirement, ~8% final realized-gain veto, 2048 px soft target, dev.8 smart-fit size search, exact planned frame-count verification, gifski 1.32.0, quality 100, `--extra`, explicit width, and infinite repeat unchanged.
- Updated the Windows toolchain smoke gate so the deepest 12.5 FPS adaptive path verifies `minterpolate=mi_mode=blend` with exact planned frame count.
- Preserve-motion GIF, MP4, framing, updater, preview, UI layout, and public release state remain unchanged.
- Incremented the development tester to `0.1.0-dev.12`.

### Touched files

- `src/polymorph/adaptive_converter.py`
- `build/verify_toolchain.py`
- `build/README.md`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/UX_SPEC.md`
- `docs/ARCHITECTURE.md`
- `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.11's motion-compensated MCI adaptive synthesis. Preserve-motion GIF behavior and all non-adaptive conversion paths are independent of this change.

### Test notes

- Local Viper surrogate cadence comparison at 20 FPS showed MCI phase energy `[0.53750, 0.54245, 0.54592, 0.53687]` versus blend `[0.53751, 0.54239, 0.54587, 0.53700]`, indicating the uniform cadence is retained.
- Windows CI must pass unit tests, the 12.5 FPS blend-resampling toolchain smoke, standalone-reference timing diagnostic, packaged-app smoke, installer compilation, checksum generation, and artifact upload before dev.12 is handed to the user.
- Human Viper validation is only meaningful if dev.12 actually selects a reduced FPS and larger image; if it again returns 25 FPS, the synthesized-even-timestamp branch should be considered exhausted for this workload and the next investigation should be exact source-frame decimation cadences rather than lower interpolated FPS.

## POLY-2026-09-11-022 — 2026-09-11 00:22 PDT — Extend measured Favor resolution cadence ladder

### Summary

- Recorded the dev.10 Viper human result: `1552x1552 • 93.6 MB • 25 FPS` with Favor resolution selected.
- Confirmed dev.10 behaved correctly: neither measured 20 FPS nor 16.67 FPS candidate predicted enough real byte savings to earn the existing ~8% linear-resolution threshold, so Polymorph kept the original 25 FPS Preserve-motion result.
- Kept real encoded sample cost as the authority; no return to frame-count-only FPS prediction.
- Extended only the clean uniform cadence search floor for the explicit Favor-resolution mode. A 25 FPS source now tests `20 -> 16.67 -> 14.29 -> 12.5 FPS`, corresponding to fixed 50/60/70/80 ms GIF frame delays.
- The first/highest cadence whose measured sample predicts at least ~8% linear spatial gain is still selected; if none earns that gain, Polymorph still returns the 25 FPS baseline.
- Preserved the final actual-gain veto, so even a selected lower cadence is discarded unless the completed adaptive fit really achieves the promised spatial increase.
- No interpolation algorithm change: FFmpeg `minterpolate` motion compensation, end lookahead padding, exact planned frame trimming, gifski quality 100, gifski 1.32.0, `--extra`, explicit width, infinite repeat, dev.8 smart-fit sizing, and integrity verification remain unchanged.
- Updated the Windows toolchain smoke gate to exercise the deepest permitted 12.5 FPS / 80 ms cadence.
- Preserve-motion GIF, MP4, framing, updater, preview, UI layout, and public release state remain unchanged.
- Incremented the development tester to `0.1.0-dev.11`.

### Touched files

- `src/polymorph/motion_planner.py`
- `tests/test_motion_planner.py`
- `build/verify_toolchain.py`
- `build/README.md`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/UX_SPEC.md`
- `docs/ARCHITECTURE.md`
- `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.10's measured 20/16.67 FPS search floor. Preserve-motion behavior and all non-adaptive conversion paths are independent of this change.

### Test notes

- Planner tests now require the 25 FPS uniform-cadence ladder to include 20, 16.67, 14.29, and 12.5 FPS in nearest-first order and cover exact 15-second expected frame counts for all four cadences.
- Windows CI must pass the 12.5 FPS `minterpolate` toolchain smoke, standard Preserve-motion GIF/MP4 gates, packaged app smoke, installer build, checksum generation, and artifact upload before dev.11 is handed to the user.
- Human Viper validation is only needed for the final chosen result. If dev.11 again reports 25 FPS, treat the interpolation strategy as unable to buy a worthwhile spatial gain on this workload under current quality/size constraints rather than continuing to lower FPS automatically.

## POLY-2026-09-10-021 — 2026-09-10 23:05 PDT — Measure adaptive GIF gains before reducing FPS

### Summary

- Recorded the dev.9 full-resolution Viper human test: motion-interpolated Favor resolution looked really good, but the result remained `1552x1552`, identical to Preserve motion.
- Recorded that dev.9 displayed `89.2 MB` using the then-existing binary-MiB completion calculation; that corresponds to roughly 93.5 decimal MB, placing the result immediately in the GIF optimizer's 93 MB acceptance region rather than indicating large unused headroom.
- Diagnosed the adaptive-planning regression: dev.9 selected 20 FPS from the theoretical `sqrt(source_fps / target_fps)` frame-count relationship, but motion-interpolated frames are materially more expensive for gifski than untouched source frames. Reducing frame count therefore did not produce the predicted byte savings or spatial gain.
- Reworked Favor resolution planning so real encoded byte cost is authoritative. Polymorph now makes the normal Preserve-motion fit, then tests lower uniform GIF cadences nearest the source FPS by encoding each candidate once at the Preserve-motion dimensions and measuring its actual gifski size.
- Candidate samples project achievable spatial size against the patched-Python `97/99` byte target and must predict roughly 8% or greater linear-resolution gain before Polymorph performs the full adaptive size search.
- For a 25 FPS source, the clean automatic cadence ladder now tests 20 FPS / 50 ms first, then 16.67 FPS / 60 ms if 20 FPS does not earn the required real gain. The current automatic floor is 16.67 FPS.
- Added a final actual-gain veto: even after a cadence passes the measured sample gate, Polymorph discards the completed reduced-FPS result and returns Preserve motion unless the final dimensions are actually about 8% larger linearly.
- Kept motion-compensated `minterpolate`, even frame cadence, exact planned frame trimming, quality 100, gifski 1.32.0, `--extra`, explicit width, infinite repeat, dev.8 smart-fit sizing, and post-encode integrity checks unchanged.
- Updated the adaptive completion line to show decimal MB and the actual effective output FPS, removing the remaining MiB-labeled-as-MB display mismatch for the development adaptive UI.
- Extended the Windows toolchain smoke test to exercise the new 16.67 FPS / 60 ms clean cadence.
- Preserve-motion GIF, MP4, framing, updater, preview, and visual skin remain unchanged.
- Incremented the development tester to `0.1.0-dev.10`.

### Touched files

- `src/polymorph/motion_planner.py`
- `src/polymorph/adaptive_converter.py`
- `src/polymorph/ui/adaptive_main_window.py`
- `tests/test_motion_planner.py`
- `build/verify_toolchain.py`
- `build/README.md`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/UX_SPEC.md`
- `docs/ARCHITECTURE.md`
- `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.9's 20-FPS theoretical adaptive planner and prior completion readout. Preserve-motion GIF, MP4, framing, updater hardening, and the dev.8 smart-fit optimizer are independent of this change.

### Test notes

- Planner regression tests cover rejection of a dev.9-like ~93.5 MB 20 FPS sample at 1552 px, acceptance of a lower uniform cadence when measured byte cost genuinely supports >=8% gain, the 25 FPS clean-cadence ladder, final actual-gain veto, and expected 20/16.67 FPS Viper frame counts.
- Full Windows CI must pass the 16.67 FPS `minterpolate` toolchain smoke, standard Preserve-motion GIF/MP4 gates, packaged adaptive UI smoke, installer compilation, checksum generation, and artifact upload before dev.10 is handed to the user.
- Human dev.10 Viper validation should report the completion line directly; it now exposes final dimensions, decimal MB, and selected effective FPS.

## POLY-2026-09-10-020 — 2026-09-10 21:12 PDT — Add adaptive Favor resolution GIF mode

### Summary

- Added an explicit experimental GIF priority choice: `Preserve motion` remains the default proven path, while `Favor resolution` may trade some temporal samples for a larger spatial result only when the user selects it.
- Validated the design against the real Viper source before wiring production: 2048x2048, 375 frames, 25 FPS, 15.0 s. Ordinary 25 -> 20 frame selection produced a strong repeating motion-change spike, while motion-compensated interpolation removed that periodic cadence pattern in the 512px diagnostic and produced exactly 300 intended frames after end lookahead + trimming.
- Added `src/polymorph/motion_planner.py` with a 2048 px soft preferred long edge, 20 FPS automatic floor, roughly 8% minimum predicted linear-resolution gain, uniform GIF-centisecond cadence candidates, and highest-FPS-first selection until 95% of the soft spatial target is reached.
- Added `src/polymorph/adaptive_converter.py` as a surgical layer over the proven converter. Preserve-motion/MP4/fixed-resolution jobs still call the existing converter behavior unchanged. Favor-resolution GIF file-size jobs first measure the full-frame fitted result, then only run the reduced-FPS pass if the planner predicts a worthwhile gain.
- Adaptive output uses FFmpeg motion-compensated `minterpolate` (`mci`, `aobmc`, bidirectional estimation, variable-size block compensation), cloned end lookahead, exact frame trimming, and explicit target FPS into gifski instead of uneven periodic frame deletion.
- Extended output integrity checks to accept an explicit planned frame count/FPS for intentional adaptive resampling while retaining exact source-frame verification for Preserve motion.
- Added a minimal dev.9 UI extension with `Preserve motion` / `Favor resolution`; adaptive controls are enabled only for GIF + `Fit under file size` and disabled for fixed-resolution output.
- Added unit coverage for motion planning and adaptive integrity expectations, bundled Windows `minterpolate` toolchain smoke coverage, and packaged-app UI smoke checks.
- Kept gifski 1.32.0, quality 100, `--extra`, infinite repeat, explicit width, `yuv420p`, dev.8 GIF smart-fit search, framing behavior, MP4, updater, preview behavior, and visual skin unchanged.
- Incremented the development tester to `0.1.0-dev.9`.

### Touched files

- `src/polymorph/motion_planner.py`
- `src/polymorph/adaptive_converter.py`
- `src/polymorph/models.py`
- `src/polymorph/integrity.py`
- `src/polymorph/app.py`
- `src/polymorph/smoke_test.py`
- `src/polymorph/ui/adaptive_main_window.py`
- `tests/test_motion_planner.py`
- `tests/test_integrity.py`
- `build/verify_toolchain.py`
- `build/README.md`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/UX_SPEC.md`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to dev.8, which exposes only the proven full-frame behavior. MP4, framing, updater hardening, and the dev.8 GIF size optimizer are independent of the adaptive layer.

### Test notes

- Local motion-planner + integrity suite: 13/13 tests pass.
- Python syntax compilation passes for all new/modified Python modules and the Windows toolchain verifier.
- Real-Viper 512px diagnostic removed the repeating four-interval cadence spike and showed no obvious interpolation corruption in spot checks around sword, hair, cape, silhouette, front/side/back views.
- Full Windows CI must still verify the pinned Gyan FFmpeg 9.0.1 build's `minterpolate` path, normal GIF/MP4 smoke behavior, packaged adaptive UI, installer build, and checksum before the tester is handed to the user.
- Full-resolution human Viper validation remains required before Favor resolution can be considered stable.

## POLY-2026-09-10-019 — 2026-09-10 04:40 PDT — Port patched-Python GIF smart-fit optimizer

### Summary

- Recorded the completed Windows timing diagnostic against the only canonical OG source: the patched Python converter actually run by the user.
- Controlled 25 FPS A/B retained 41/50 frames under patched-Python timing versus 50/50 with explicit full-frame gifski timing, while using 82.1878% of the bytes; the derived 1.10305x linear scale maps 1592px to 1756.06px and quantitatively explains the OG 1756px spatial advantage.
- Explicitly removed the later, unvalidated Discord distribution package from behavioral parity decisions.
- Diagnosed the remaining legitimate optimizer difference: current Polymorph can accept a GIF around 90.27 MB under a 99 MB ceiling, while the patched Python uses a 97 MB target and 93 MB acceptance floor plus a different pass/fail-bracketing search.
- Added `src/polymorph/size_optimizer.py`, a pure port of the patched Python scale-selection math generalized to arbitrary user ceilings using the exact 97/99 target and 93/99 acceptance ratios.
- GIF file-size mode now uses the patched Python measured-size square-root prediction, 0.985 safety factor, guaranteed 4% downward move after failure, pass/fail midpoint reclamation, six normal attempts, and 128px emergency long-edge fallback without source upscaling.
- Kept GIF quality 100, gifski 1.32.0, `--extra`, infinite repeat, explicit output width, `yuv420p`, explicit source FPS, exact frame-count/timing verification, and framing behavior unchanged.
- Preserved the previously validated MP4 file-size optimizer exactly by routing only GIF file-size mode through the new reference search.
- Added unit tests for reference thresholds, downward prediction, midpoint reclamation, acceptance stopping, full-size stopping, and no-upscale emergency floor.
- Incremented the development tester to `0.1.0-dev.8`.

### Touched files

- `src/polymorph/size_optimizer.py`
- `src/polymorph/converter.py`
- `tests/test_size_optimizer.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.7's GIF size search. MP4, encoder settings, updater hardening, framing, and UI behavior are independent of this optimizer change.

### Test notes

- Pure optimizer tests encode the patched Python's exact 99M -> 97M/93M thresholds and scale-selection rules.
- Windows CI must pass unit tests, normal GIF/MP4 toolchain smoke, patched-Python timing diagnostic, frozen-EXE smoke, installer compilation, checksum generation, and artifact upload before dev.8 is handed to the user.
- Human dev.8 validation should use the same Viper source at GIF / Original / 99 MB and compare final dimensions and decimal file size; expected result is only safe full-frame reclamation, not a return to the frame-resampled OG 1756px target.

## POLY-2026-09-10-018 — 2026-09-10 03:20 PDT — Add controlled standalone GIF parity diagnostic

### Summary

- Reopened the `1756x1756` standalone-vs-Polymorph resolution gap as an active diagnostic question after the current decimal-MB/full-frame Viper conversion produced `1552x1552` with otherwise good quality/smoothness.
- Re-read the user-supplied known-good standalone Python reference and recorded its exact visible behavior: Lanczos scaling, FFmpeg `-r <source fps>`, YUV4MPEG streaming, gifski quality 100/extra/repeat 0/explicit width, no gifski `--fps`, and 99,000,000/97,000,000/93,000,000-byte smart-fit thresholds.
- Recorded the supplied SHA-256 for the separately shared `HeroForge_WebP_to_Reddit_GIF_v1.0.0.zip` as provenance, while explicitly not treating the checksum as evidence of the ZIP's internal FFmpeg/gifski builds or Y4M pixel format.
- Corrected earlier documentation that overstated the standalone pixel format as definitely 4:2:0 and the omitted gifski `--fps` behavior as the fully proven cause of the `1756x1756` result.
- Added `build/compare_gif_reference.py`, a CI-only 25 FPS animated-WebP diagnostic that holds output dimensions, gifski quality, extra effort, looping, and Y4M pixel format constant while comparing reference-style omission of gifski `--fps` against explicit 25 FPS.
- The diagnostic also records literal automatic-pixel-format behavior plus explicit `yuv420p` and `yuv444p` pairs, along with FFmpeg/ffprobe/gifski versions, output frame count, duration, dimensions, byte size, and comparison ratios.
- Added the diagnostic to the Windows dev workflow and upload its JSON/log/media output as `Polymorph-gif-reference-diagnostic` before packaging.
- Updated current status to record that dev.7 updater hardening already passed the complete Windows CI pipeline.
- No installed application version bump: production Polymorph remains `0.1.0-dev.7`.
- No production converter, GIF/MP4 settings, file-size optimizer, framing, preview, UI, updater runtime, or installer behavior changed.

### Touched files

- `build/compare_gif_reference.py`
- `.github/workflows/windows-dev-build.yml`
- `build/README.md`
- `MASTER.md`
- `docs/ARCHITECTURE.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to remove only the CI/reference diagnostic and restore the previous documentation wording. Installed dev.7 behavior is unchanged either way.

### Test notes

- The new diagnostic intentionally requires the controlled `yuv420p` explicit-25-FPS variant to preserve all 50 synthetic source frames and requires the otherwise matched no-gifski-`--fps` variant to produce fewer than 50 frames.
- Automatic pixel-format and `yuv444p` variants are recorded as evidence when supported but are not required for the timing-control assertion.
- Windows CI must produce and upload `reference-timing.json` before its measurements are treated as confirmed.
- Documentation/build-only update; no human media-quality retest is required for the commit itself.

## POLY-2026-09-10-017 — 2026-09-10 03:02 PDT — Harden verified update downloads

### Summary

- Hardened the automatic updater without changing the visible update flow or any conversion behavior.
- Automatic installation now requires the exact canonical installer asset `Polymorph_Setup_v<version>.exe` and its exact `.exe.sha256` companion from the same official GitHub release.
- Restricted automatic update downloads to HTTPS release URLs under `github.com/Knight-Witch/Polymorph/releases/download/`.
- Replaced whole-file installer hashing with bounded streaming download plus incremental SHA-256 hashing, avoiding an unnecessary ~85 MB in-memory buffer.
- Added explicit maximum download sizes for checksum and installer assets and delete partial downloads on failure.
- Added strict checksum parsing: valid 64-character SHA-256 required; when the checksum line includes a filename, it must match the selected installer exactly.
- Added unit coverage for exact asset pairing, wrong checksum assets, official URL restriction, checksum filename validation, streamed hashing, and oversized-download rejection.
- GIF, MP4, file-size optimizer, framing, preview, UI layout, and installer privilege behavior were not changed.
- Incremented the development tester to `0.1.0-dev.7`.

### Touched files

- `src/polymorph/update_service.py`
- `tests/test_update_service.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the dev.6 updater behavior while leaving the decimal-MB conversion fix intact.

### Test notes

- New updater tests are network-independent and use in-memory fake responses for streaming behavior.
- Windows unit/toolchain/frozen-EXE/installer gates must pass before dev.7 becomes the current development tester.
- No human media-quality retest is required because conversion code is untouched.

## POLY-2026-09-10-016 — 2026-09-10 02:48 PDT — Normalize file-size ceilings to decimal MB

### Summary

- Corrected the user-defined file-size ceiling so `MB` now means decimal megabytes: 1 MB = 1,000,000 bytes.
- The prior calculation used `1024 * 1024`, so a displayed `99 MB` ceiling actually allowed 103,809,024 bytes and could exceed a platform's decimal 100 MB upload limit.
- Added a small centralized size-unit helper and direct unit tests for decimal MB conversion.
- Kept the file-size optimizer search strategy unchanged; only the byte ceiling supplied to it changes.
- Kept GIF quality 100, gifski 1.32.0, `yuv420p`, explicit source FPS/frame preservation, infinite looping, output-dimension verification, MP4 encoding, framing, and UI layout unchanged.
- Incremented the development tester to `0.1.0-dev.6`.

### Touched files

- `src/polymorph/size_units.py`
- `src/polymorph/converter.py`
- `tests/test_size_units.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore binary-MiB interpretation of the `MB` ceiling and the dev.5 version metadata.

### Test notes

- Pure unit conversion is covered directly: `99 MB -> 99,000,000 bytes` and fractional decimal MB values round deterministically.
- Because the corrected ceiling is stricter than prior builds, size-constrained outputs may be slightly smaller in spatial resolution; that is expected and not a GIF-quality regression.
- Windows run #12 completed successfully through unit tests, pinned toolchain verification, frozen application smoke test, installer compilation, checksum generation, and artifact upload.
- Dev.6 installer SHA-256 was independently recomputed after artifact download and matched the generated checksum.

## POLY-2026-09-10-015 — 2026-09-10 02:20 PDT — Restore gifski 1.32.0 and confirm frame-preservation tradeoff

### Summary

- Human dev.4 retest produced `1532x1532`, regressing from dev.3's `1592x1592`; gifski 1.34.0 is therefore not retained for this workload.
- Re-read the exact standalone converter and gifski's Y4M implementation. The standalone used FFmpeg `-r <source fps>` but omitted gifski `--fps`; gifski defaults Y4M/video input to 20 FPS and its Y4M decoder skips frames when required to meet that target.
- This confirms the main reason the standalone converter could produce a larger `1756x1756` GIF under the same byte ceiling: it was not preserving the complete source frame sequence.
- Preserving source FPS/frame count is a hard Polymorph requirement, so the standalone `1756x1756` result is no longer treated as the correct spatial-resolution parity target.
- Restored the bundled development gifski dependency from 1.34.0 to the better-performing, previously human-validated 1.32.0 build.
- Kept `yuv420p`, explicit source FPS, gifski quality 100, extra effort, infinite repeat, explicit width, post-encode dimension/frame/timing verification, file-size optimizer, and MP4 path unchanged.
- Updated architecture/history/status documentation to distinguish standalone visual-quality parity from Polymorph's stricter frame-preservation requirement.
- Incremented the development tester to `0.1.0-dev.5`.

### Touched files

- `.github/workflows/windows-dev-build.yml`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `THIRD_PARTY.md`
- `build/README.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to the gifski 1.34.0 dev.4 experiment. Converter and MP4 logic are identical across dev.4 and dev.5.

### Test notes

- Root-cause diagnosis is supported by the exact standalone command and gifski's Y4M decoder source.
- No converter code or optimizer code changed in this update.
- Windows unit/toolchain/frozen-EXE/installer gates passed for dev.5; no further Viper quality retest is required solely to re-establish the already human-validated dev.3 GIF engine behavior.

## POLY-2026-09-10-014 — 2026-09-10 01:12 PDT — Test stable gifski 1.34.0

### Summary

- Human dev.3 retest reported good animation smoothness and a `1592x1592` Viper GIF, only slightly above the prior `1570x1570` result and still materially below the canonical standalone `1756x1756` output.
- Color remained too subtle to judge reliably.
- Re-read the standalone converter and confirmed it only enforces gifski `>=1.32.0`; it does not establish that the successful standalone output used exactly 1.32.0.
- Identified Polymorph's exact 1.32.0 pin as the next isolated upstream mismatch.
- Updated only the bundled development gifski dependency to stable 1.34.0. The 1.34.0 release notes document palette-quality improvements from a newer `libimagequant`.
- Converter code, GIF command line, `yuv420p` Y4M handoff, source-FPS safeguard, explicit gifski width, quality 100, extra effort, repeat behavior, post-encode integrity checks, size optimizer, and MP4 path were not changed.
- Updated development packaging/documentation and incremented the tester to `0.1.0-dev.4`.

### Touched files

- `.github/workflows/windows-dev-build.yml`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `THIRD_PARTY.md`
- `build/README.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore gifski 1.32.0 and the dev.3 tester metadata. Converter/MP4 code is identical across the two builds.

### Test notes

- This is an isolated dependency A/B, not an optimizer change.
- Windows unit/toolchain/frozen-EXE/installer gates passed before dev.4 was handed to the user.
- Human retest used the same Viper source and established that 1.34.0 was worse for this workload.

## POLY-2026-09-10-013 — 2026-09-10 00:45 PDT — Pin GIF Y4M to yuv420p

### Summary

- Windows CI run #8 proved that literal removal of GIF `-pix_fmt` is not reliable on the pinned FFmpeg 9.0.1 Windows build: after Polymorph's filter graph, FFmpeg retained a non-Y4M-compatible intermediate and `yuv4mpegpipe` refused to write its header.
- Replaced the failed auto-negotiation experiment with explicit `yuv420p`, reproducing the canonical standalone converter's effective 4:2:0 Y4M handoff deterministically.
- Kept the validated GIF settings unchanged: source FPS handoff, gifski quality 100, extra effort, infinite repeat, explicit output width, and post-encode dimension/frame/timing verification.
- Kept the file-size optimizer unchanged so the Viper retest isolates the pixel-format difference.
- Kept the human-validated MP4 path unchanged.
- Fixed the Windows smoke test's failure-cleanup pipe handling so it no longer asks `communicate()` to read an already closed FFmpeg stdout pipe.
- Updated the durable GIF reference history with the failed no-pixel-format probe and deterministic `yuv420p` decision.
- Incremented the development tester to `0.1.0-dev.3`; dev.2 never produced an installer because its smoke gate failed.

### Touched files

- `src/polymorph/converter.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `build/verify_toolchain.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to the failed `0.1.0-dev.2` auto-negotiation experiment. The prior validated tester remains commit `3305139` / dev.1.

### Test notes

- Run #8 failure was diagnosed from the exact Windows job log before editing.
- New unit/toolchain/frozen-EXE/installer gates passed before dev.3 was handed to the user.
- Human A/B validation confirmed smoothness remained good and recovered only a small amount of spatial resolution.

## POLY-2026-09-10-012 — 2026-09-10 00:30 PDT — Restore canonical Y4M handoff for GIF

### Summary

- Recorded the successful human retest of the width-corrected GIF: visual quality now matches the standalone converter and may be slightly smoother framewise.
- Recorded the remaining measured scale difference: Polymorph `1570x1570` versus standalone `1756x1756` at the same nominal size target, plus only a possible subtle red/pink color difference.
- Rechecked the actual size context before editing: the Polymorph result shown in Windows Explorer is already about `93.8 MB`, so the remaining scale difference is not plausibly explained by simple unused file-size headroom alone.
- Compared the GIF pixel handoff against the canonical standalone converter and found the remaining material difference: Polymorph forced `yuv444p`; the standalone FFmpeg command did not force a YUV pixel format before `yuv4mpegpipe`.
- Removed only the forced GIF-path `yuv444p` so the Y4M handoff again matches the validated standalone pipeline.
- Preserved Polymorph's explicit source-FPS handoff, gifski quality 100, extra effort, infinite repeat, explicit output width, post-encode dimensions, exact frame count, and timing verification.
- Updated the Windows toolchain smoke test to exercise the same negotiated Y4M handoff and verify both dimensions and frame count.
- Left file-size optimizer logic and the already human-validated MP4 path unchanged so the next Viper comparison isolates this variable.
- Added `HISTORY/REFERENCE_GIF_CONVERTER.md` as the durable canonical standalone reference record.
- Incremented the development tester to `0.1.0-dev.2` so the replacement installer is distinguishable from the prior build.

### Touched files

- `src/polymorph/converter.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `build/verify_toolchain.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the forced `yuv444p` GIF handoff and the `0.1.0-dev.1` tester metadata. MP4 behavior is unchanged by this commit.

### Test notes

- The canonical standalone script was re-read before editing.
- Current dev conversion optimizer was reviewed and deliberately left unchanged for isolation.
- Windows unit/toolchain/frozen-EXE/installer gates passed for the working follow-up build.

## POLY-2026-09-09-011 — 2026-09-09 23:57 PDT — Restore canonical gifski output width

### Summary

- First hands-on HeroForge media comparison validated MP4 visually with no reported issue.
- The same test found the Polymorph GIF substantially blurrier, grainier in gradients, and much smaller in actual pixel dimensions than the immediately preceding standalone converter result.
- Compared Polymorph against the validated standalone `HeroForge_WebP_to_Reddit_GIF.py` and confirmed Polymorph had omitted the reference converter's explicit gifski `--width` argument.
- Restored explicit gifski width control so gifski cannot apply its default conservative automatic animation downsize.
- Extended output integrity validation to require actual encoded dimensions to exactly match the dimensions Polymorph requested, in addition to existing exact frame-count and bounded-duration checks.
- Added regression coverage for output-dimension mismatch.
- Retained Polymorph's explicit source-FPS handoff and temporal integrity checks; those protect the no-frame-loss requirement and are not part of the confirmed quality regression.
- MP4 encoding settings, framing behavior, UI, updater, and installer architecture were not changed.
- Logged the separate binary-MiB-vs-decimal-MB ceiling issue for a later isolated fix.

### Touched files

- `src/polymorph/converter.py`
- `src/polymorph/integrity.py`
- `tests/test_integrity.py`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the pre-fix GIF path; MP4 remains unaffected either way.

### Test notes

- Root cause is directly supported by the standalone converter and gifski CLI behavior.
- Windows gates passed before the replacement installer was handed back for Viper retest.
- Human visual validation confirmed the corrected GIF quality was excellent.

## POLY-2026-09-09-010 — 2026-09-09 19:45 PDT — Record successful Windows smoke-gated build

### Summary

- Recorded successful Windows run #6 for commit `b3cfdda`.
- The frozen `Polymorph.exe` smoke gate passed before installer compilation.
- Inno Setup, SHA-256 generation, and artifact uploads also passed.
- The dev installer is 88,997,108 bytes and its recomputed local SHA-256 matches the generated checksum: `ef1ba4562be7d81ac70a4b261ad204e98f8da2c114cdc836b0ee972df1675177`.
- Marked the current dev build ready for hands-on HeroForge animated-WebP testing.
- Documentation-only update; no Python, workflow, installer definition, JavaScript, manifest, or runtime behavior changed.

### Touched files

- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this documentation commit only; the validated `b3cfdda` tester binary remains unchanged.

### Test notes

- Windows CI run #6 completed successfully from checkout through artifact upload.
- Packaged-app smoke test passed bundled-tool discovery, SVG resource loading, Qt animated-WebP live preview, and linked 16:9 resolution controls.
- Human Windows validation with real HeroForge animated WebP media followed successfully.

## POLY-2026-09-09-009 — 2026-09-09 19:34 PDT — Gate installer on packaged application smoke test

### Summary

- Added a hidden CI-only `--smoke-test` application path.
- The actual frozen `Polymorph.exe` now must prove it can resolve bundled FFmpeg/ffprobe/gifski, load packaged footer SVGs, construct the main window, decode an animated WebP into the live preview, and maintain linked 16:9 resolution controls.
- Reused the synthetic animated WebP from the existing toolchain smoke test rather than introducing a second media generator.
- Installer compilation is blocked if the packaged-app smoke test fails.
- Normal GUI/drag-to-open behavior is unchanged unless the hidden smoke-test flag is explicitly supplied.

### Touched files

- `src/polymorph/app.py`
- `src/polymorph/smoke_test.py`
- `build/verify_toolchain.py`
- `.github/workflows/windows-dev-build.yml`
- `build/README.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to remove the packaged-EXE gate and restore the prior build workflow.

### Test notes

- Unit/toolchain tests remain upstream of PyInstaller.
- Packaged-app gate passed on Windows run #6 before Inno Setup compiled the installer.
- Human HeroForge media validation was subsequently completed.

## POLY-2026-09-09-008 — 2026-09-09 19:25 PDT — First-pass UI usability polish

### Summary

- Linked fixed-resolution width and height automatically to the active framed aspect ratio, while retaining no-upscale limits.
- Changed Crop preview dragging so the visible image follows the user's drag direction; Fit offset semantics remain unchanged.
- Replaced development footer text placeholders with monochrome GitHub, Ko-fi, Patreon, Discord, and update icons plus hover tooltips.
- Added packaged SVG resource lookup for source and frozen builds and documented Simple Icons attribution.
- Final Polymorph application emblem remains deferred; the generated development app icon is unchanged.

### Touched files

- `src/polymorph/geometry.py`
- `src/polymorph/resources.py`
- `src/polymorph/assets/*.svg`
- `src/polymorph/ui/main_window.py`
- `src/polymorph/ui/preview.py`
- `src/polymorph/ui/resolution_linker.py`
- `src/polymorph/ui/styles.py`
- `tests/test_geometry.py`
- `pyproject.toml`
- `build/Polymorph.spec`
- `THIRD_PARTY.md`
- `docs/UX_SPEC.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore independent resolution fields, prior Crop drag semantics, and text-placeholder footer controls.

### Test notes

- Linked-dimension math is covered by unit tests for 16:9 width/height driving and native-size clamping.
- SVG resource inclusion is declared both as Python package data and explicit PyInstaller data.
- Packaged Qt smoke tests subsequently confirmed resource and preview loading.

## POLY-2026-09-09-007 — 2026-09-09 19:22 PDT — Pin and smoke-test smaller FFmpeg Essentials build

### Summary

- Replaced the mutable/latest full BtbN FFmpeg download in the dev build workflow with the exact Gyan FFmpeg 9.0.1 Essentials archive.
- Added verification against the provider-published SHA-256 before extraction.
- Added a build-time animated WebP smoke test covering ffprobe frame counting, Crop/Scale/Pad filters, YUV4MPEG streaming into gifski, infinite-loop GIF encoding, H.264 MP4 encoding, and output frame-count preservation.
- Recorded the exact development FFmpeg bundle/source reference in third-party documentation.
- No application conversion settings or UI behavior changed.

### Touched files

- `.github/workflows/windows-dev-build.yml`
- `build/verify_toolchain.py`
- `build/README.md`
- `THIRD_PARTY.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the previous BtbN master GPL build acquisition.

### Test notes

- Provider documentation confirms the Essentials build includes libwebp and libx264 and all internal Windows FFmpeg components.
- Exact bundled toolchain behavior is gated by the Windows smoke-test step; installer artifacts are not accepted if that step fails.

## POLY-2026-09-09-006 — 2026-09-09 19:12 PDT — Correct PyInstaller repository root

### Summary

- Fixed the Windows build failure in `build/Polymorph.spec` by resolving the repository root from PyInstaller's `SPECPATH` directory correctly.
- No converter, UI, dependency, installer, or runtime behavior changed.

### Touched files

- `build/Polymorph.spec`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the previous spec path calculation.

### Test notes

- Windows run #1 passed unit tests, FFmpeg acquisition, gifski 1.32.0 compilation, and placeholder icon generation before failing at PyInstaller with `script 'D:\a\Polymorph\run_polymorph.py' not found`.
- The corrected root resolves to the checked-out repository directory `D:\a\Polymorph\Polymorph`.
- Windows run #3 subsequently passed all build, installer, checksum, and artifact-upload steps.

## POLY-2026-09-09-005 — 2026-09-09 19:09 PDT — Verify frame/timing integrity after encoding

### Summary

- Made source probing tolerant of ffprobe decoder failure when animated WebP RIFF metadata already supplies valid dimensions, frame count, and duration.
- Added explicit nominal FPS storage instead of relying only on frame-count/duration reconstruction.
- Added post-encode integrity verification requiring exact frame-count preservation and bounded duration drift.
- Added tests for RIFF-only fallback and temporal integrity rules.

### Touched files

- `src/polymorph/models.py`
- `src/polymorph/probe.py`
- `src/polymorph/integrity.py`
- `src/polymorph/converter.py`
- `tests/test_probe_fallback.py`
- `tests/test_integrity.py`
- `docs/ARCHITECTURE.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to pre-verification probing/encoding behavior.

### Test notes

- Pure integrity/probe logic is covered by unit tests.
- Full output verification is also exercised in the Windows toolchain/frozen application pipeline.

## POLY-2026-09-09-004 — 2026-09-09 18:28 PDT — Windows development packaging

### Summary

- Wired the canonical Ko-fi, Patreon, and Discord destinations into the footer.
- Added PyInstaller one-directory packaging with bundled FFmpeg, ffprobe, and gifski binaries.
- Added a deliberately temporary generated `.ico` for development builds.
- Added a per-user Inno Setup installer targeting `%LOCALAPPDATA%\Programs\Polymorph` with optional desktop shortcut and no administrator requirement.
- Added a Windows GitHub Actions development build that runs tests, obtains the conversion toolchain, builds the app and installer, generates SHA-256, and uploads workflow artifacts.
- Development workflow does not publish a GitHub Release.

### Touched files

- `src/polymorph/constants.py`
- `build/**`
- `installer/Polymorph.iss`
- `.github/workflows/windows-dev-build.yml`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert the packaging commit; application/core dev code remains on the prior `dev` head.

### Test notes

- Packaging definitions reviewed for one-directory dependency placement and per-user install behavior.
- Windows run #3 produced a successful installer artifact (~126.6 MB) and unpacked application artifact (~435 MB before ZIP compression).

## POLY-2026-09-09-003 — 2026-09-09 18:28 PDT — Functional desktop UI and updater scaffold

### Summary

- Added PySide6 main window with multi-file queue, drag/drop, animated WebP preview, GIF/MP4 selection, mutually exclusive sizing modes, framing controls, output folder selection, and conversion progress.
- Added live Original / Crop / Fit preview with drag repositioning and Fit background color.
- Added aspect-ratio guide dialog and development footer controls for updates, GitHub, Ko-fi, Patreon, and Discord.
- Added automatic update checks while the app is open and verified installer download support; no background service/daemon.
- Added a lightweight placeholder arcane progress animation so final sigil styling can be swapped in without restructuring the UI.
- Preview uses non-caching animation playback so large source animations are not intentionally retained frame-by-frame in RAM.

### Touched files

- `src/polymorph/app.py`
- `src/polymorph/ui/**`
- `src/polymorph/update_service.py`
- `run_polymorph.py`
- `tests/test_update_service.py`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert the UI/updater commit; core conversion modules remain independently testable.

### Test notes

- 8/8 local non-GUI tests passed at the time.
- Python source syntax compilation passed.
- Packaged Qt/Windows interaction is now covered by the frozen-app smoke gate.

## POLY-2026-09-09-002 — 2026-09-09 18:28 PDT — Core conversion engine scaffold

### Summary

- Added modular media probe, WebP RIFF fallback parser, framing geometry, FFmpeg filter construction, tool discovery, and conversion orchestration.
- Preserved the canonical FFmpeg -> YUV4MPEG -> gifski path with quality 100, extra effort, infinite repeat, no PNG intermediates, and explicit source FPS handoff to avoid gifski's default 20 FPS resampling.
- Added H.264 MP4 output scaffold.
- Added file-size-constrained resolution optimization, fixed-resolution no-upscale validation, collision-safe output naming, and a variable-frame-duration safeguard that refuses silent GIF resampling.
- Added unit tests for framing geometry and RIFF parsing.

### Touched files

- `src/polymorph/{__init__,constants,models,probe,geometry,filters,tools,converter}.py`
- `tests/**`
- `pyproject.toml`
- `.gitignore`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`
- `MASTER.md`

### Rollback

- Revert the core scaffold commit; `main` remains documentation-only/unreleased.

### Test notes

- Core-engine unit tests pass.
- Actual output quality has since been human-validated against real HeroForge media.

## POLY-2026-09-09-001 — 2026-09-09 18:28 PDT — Repository bootstrap

### Summary

- Established Polymorph as a standalone public repository.
- Defined the project contract, canonical conversion priorities, v1 UX scope, architecture boundaries, and third-party dependency notes.
- Witch Dock was not modified.

### Touched files

- `README.md`
- `PROJECT_CONTRACT.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`
- `THIRD_PARTY.md`
- `docs/ARCHITECTURE.md`
- `docs/UX_SPEC.md`

### Rollback

- Revert the bootstrap documentation commit.

### Test notes

- Documentation-only bootstrap; no public executable, installer, or runtime behavior released.
