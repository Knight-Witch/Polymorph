# Changelog

Historical entries through dev.15 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV15.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV15.md).

## POLY-2026-09-12-029 — 2026-09-12 04:20 PDT — Establish first branded visual skin

### Summary

- Closed the framing-validation loop before visual work: the user completed one real Crop export and one real Fit export after the dev.16/17 geometry fixes and reported that both matched expectations and worked great. Crop/Fit preview/export parity is now human-validated end to end.
- Replaced the generic gray development appearance with the first Polymorph visual system: near-black/charcoal surfaces, ivory text, muted champagne-gold borders/section hierarchy, and restrained crimson active/selection states.
- Increased the general UI type scale to `11pt`, enlarged the title treatment, and increased default window width so the larger text has room without compressing the controls.
- Changed the header subtitle from `Media Transmutation Utility` to `MEDIA CONVERSION MAGIC`.
- Changed the main action from `POLYMORPH` to `Cast Polymorph`.
- Added a dedicated gold-outlined `+ Add Files` treatment and strengthened file-selection, input-focus, slider, progress, tooltip, and footer hover states.
- Gave `Cast Polymorph` a deep-crimson/gold primary treatment with distinct hover and pressed states as immediate feedback. No looping or decorative button animation is introduced yet.
- Intentionally did not add the mockup-only slogans `Same motion. A brighter form.` or `Artifacts to new forms.`.
- The loading/working animation remains deliberately deferred. Both the previously discussed alchemic/magic-circle concept and the user's D20 roll/spin concept remain open for the next design phase.
- Kept the proven widget layout and every conversion/framing behavior unchanged; presentation changes are applied after the validated adaptive MainWindow has fully constructed.
- Extended the packaged smoke path so it applies the same branded skin as the normal app and fails if the new subtitle/action copy is missing.
- Incremented the development tester to `0.1.0-dev.18`.

### Touched files

- `src/polymorph/ui/styles.py`
- `src/polymorph/app.py`
- `src/polymorph/smoke_test.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.17's neutral gray development skin and previous `POLYMORPH`/`Media Transmutation Utility` copy. Conversion, framing, adaptive GIF behavior, updater behavior, and toolchain state are independent of this presentation-only pass.

### Test notes

- Full Windows CI must pass the unchanged unit suite, pinned FFmpeg/gifski smoke, adaptive integration, reference diagnostic, PyInstaller build, packaged-app smoke, installer compilation, checksum generation, and artifact uploads.
- The frozen-app smoke now applies the first branded skin and asserts `MEDIA CONVERSION MAGIC`, `Cast Polymorph`, and the skin marker before running the normal UI/preview/framing/adaptive checks.
- Human dev.18 review is visual: verify readability at normal Windows scaling, confirm the gold/red/black hierarchy feels right, confirm the larger default window is comfortable, and decide what should be pushed further before implementing the loader animation.

## POLY-2026-09-12-028 — 2026-09-12 03:45 PDT — Use conventional radio selection dots

### Summary

- Incorporated dev.16 human validation: console popup windows are gone in normal desktop use, and Crop/Fit behave correctly in the live viewer. End-to-end export parity still needs one real Crop export and one real Fit export.
- Replaced dev.16's thick-border checked-radio treatment with the conventional state users expect: hollow circle when unselected, small centered filled dot when selected.
- Added an equivalent dimmed centered-dot treatment for disabled selected radios so checked state remains visible without making disabled controls look active.
- Strengthened the frozen-app smoke gate so the packaged stylesheet must retain the centered-dot radio treatment.
- No conversion, framing, preview geometry, subprocess, encoder, adaptive-planning, optimizer, updater, or toolchain behavior changed.
- Incremented the development tester to `0.1.0-dev.17`.

### Touched files

- `src/polymorph/ui/styles.py`
- `src/polymorph/smoke_test.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `MASTER.md`
- `docs/UX_SPEC.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore dev.16's explicit thick-border checked indicator. All conversion/framing behavior is independent of this presentation-only change.

### Test notes

- Full Windows CI must pass the unchanged unit/toolchain/adaptive/reference/build/installer gates plus the packaged-app radio-dot style assertion before dev.17 is handed out.
- Human dev.17 check is visual only: selected radio controls should read as ordinary hollow-circle/filled-dot radio buttons.

## POLY-2026-09-12-027 — 2026-09-12 03:24 PDT — Unify framing preview and suppress console flashes

### Summary

- Recorded successful real-media Favor-resolution validation before touching framing: a confirmed Viper run selected stride 2 and returned `2048x2048`, 188 frames over exactly 15.0 s, 82,147,387 bytes, with visually consistent motion. Two additional kitbash/decal-heavy 500-frame HeroForge variants also selected stride 2 and produced 250 uniform 80 ms frames at `1810x1810` and `1752x1752`. No adaptive selection/timing/quality policy is changed in dev.16.
- Corrected the historical interpretation of earlier dev.13-era Viper baselines: because the prior radio stylesheet hid the checked indicator, those files alone do not prove that Favor resolution actually ran. Dev.15 diagnostics provide the authoritative confirmed adaptive results.
- Diagnosed the user's focus-stealing CMD/PowerShell flashes. FFmpeg and gifski already launched with Windows `CREATE_NO_WINDOW`; ffprobe did not. ffprobe now uses the same no-console creation flag while continuing to capture stdout/stderr for errors and metadata.
- Replaced the animated preview's duplicate Crop/Fit geometry implementation with the same shared `native_geometry_for_size()` resolver used by encoder framing. Preview and export now consume one source of truth for crop rectangle, canvas size, padding, and offsets instead of merely attempting to agree.
- Crop continues to preserve aspect ratio and now adds a 100–300% manual zoom slider. Zoom reduces the retained source crop window and therefore its native framed maximum; it does not upscale source pixels and preserves the project-wide no-upscale rule. Preview drag chooses which source area remains visible.
- Fit preserves the complete source aspect ratio and expands the canvas with background padding. The preview now derives content size and position from the same pad geometry that drives the FFmpeg export filter rather than stretching the source to the selected ratio.
- Added an explicit visible radio-button checked state so the selected GIF/sizing/priority option can no longer appear blank and be mistaken for the unselected choice.
- Hardened the Qt/PyInstaller framing boundary by converting combo item data through `FramingMode(...)` instead of depending on Python object identity; this was required after the first frozen-app smoke caught Crop item data round-tripping as the underlying string.
- Extended geometry tests for crop zoom/no-distortion, probe tests for the Windows no-console flag, and the packaged-app smoke gate for checked-radio styling, Crop zoom mapping, and framing state.
- Increased the development window slightly to `1080x820` to accommodate the Crop zoom row while retaining the `900x700` minimum.
- Rolled the growing tracking histories forward without deleting them: the exact pre-dev.16 `PRE_FLIGHT_Check.md` and `CHANGELOG.md` contents are preserved under `HISTORY/PROJECT_LOGS/`, and the active files begin with dev.16.
- Incremented the development tester to `0.1.0-dev.16`.

### Touched files

- `src/polymorph/models.py`
- `src/polymorph/geometry.py`
- `src/polymorph/probe.py`
- `src/polymorph/ui/preview.py`
- `src/polymorph/ui/adaptive_main_window.py`
- `src/polymorph/ui/styles.py`
- `src/polymorph/smoke_test.py`
- `tests/test_geometry.py`
- `tests/test_probe_fallback.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/UX_SPEC.md`
- `docs/ARCHITECTURE.md`
- `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- `HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV15.md`
- `HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV15.md`
- `HISTORY/PROJECT_LOGS/README.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert the dev.16 commit to return to dev.15's adaptive diagnostics and prior preview/subprocess behavior. The validated adaptive converter policy, Preserve-motion GIF path, MP4 path, optimizer, updater, and pinned toolchain are independent of these framing/UI/process fixes.

### Test notes

- Unit suite includes Crop zoom/no-distortion geometry and platform-specific ffprobe creation-flag coverage.
- Pinned Windows toolchain smoke and real adaptive-converter integration remain required to pass unchanged.
- Frozen `Polymorph.exe` smoke now gates explicit checked-radio styling, Crop zoom state mapping, adaptive priority state, animated WebP preview, and linked fixed-resolution controls.
- Intermediate Windows run #34 on the completed dev.16 code tree passed unit tests, pinned toolchain checks, adaptive integration, reference diagnostics, PyInstaller build, packaged-app smoke, installer compilation, checksum generation, and artifact uploads before the tracking-history rollover/squash.
- Human dev.16 validation should confirm: no console flash on media load or encode/optimization; Crop visually trims rather than stretches and exported framing matches preview; Crop drag and zoom work as expected; Fit preserves source proportions and adds padding rather than stretching; Fit drag/export match preview; checked radio state is immediately obvious.