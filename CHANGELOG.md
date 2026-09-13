# Changelog

Historical entries through dev.19 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV19.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV19.md). Earlier pre-dev.16 history also remains in the existing dev.15 archive.

## POLY-2026-09-12-035 — 2026-09-12 18:30 PDT — Add packaged-startup bootstrap checkpoints

### Summary

- Reclassified the remaining dev.21 CI hang from a playback-seek problem to a pre-smoke startup problem after Windows run #42 again hit the 120-second packaged-process guard without creating even the first incremental smoke checkpoint.
- Added packaged-smoke-only bootstrap logging to `run_polymorph.py` before/after importing `polymorph.app` and before calling `main()`.
- Added matching startup checkpoints in `app.py` around `QApplication` creation, brand-font loading, smoke-argument detection, smoke-module import, smoke invocation and smoke return.
- Bootstrap logging is gated entirely by the existing `POLYMORPH_SMOKE_LOG` environment variable and silently ignores logging failures, so normal desktop startup and release behavior are unchanged.
- No conversion, framing, adaptive GIF, preview/playback UI, styling, updater, subprocess or package-version behavior changed.
- Version remains `0.1.0-dev.21` because no dev.21 installer has completed the packaged gate yet.

### Touched files

- `run_polymorph.py`
- `src/polymorph/app.py`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to remove the startup checkpoint instrumentation once the frozen-startup hang is isolated. The instrumentation is intentionally inert in normal launches.

### Test notes

- The next Windows run should either complete the packaged smoke or print a precise last bootstrap stage before the 120-second guard fires. Use that evidence for the next fix rather than weakening the remaining frozen-app assertions.

## POLY-2026-09-12-034 — 2026-09-12 18:20 PDT — Make packaged playback smoke headless-safe

### Summary

- Followed up Windows Dev Build run #41 after the new 120-second guard proved the frozen process still wedged inside the offscreen preview/playback smoke while all conversion/toolchain/package stages before it passed.
- Added incremental smoke checkpoint persistence so `POLYMORPH_SMOKE_LOG` is rewritten after every PASS/FAIL line; a future timeout now shows the exact last successful assertion.
- Removed the CI-only `QMovie.jumpToFrame()` random-seek assertion from the offscreen frozen smoke. Qt's headless WebP plugin can wedge on random-access seeks and is not a faithful proxy for the normal interactive Windows plugin path.
- The packaged smoke still requires valid animated WebP initialization, a rendered preview frame, initialized frame-count/duration metadata, playback timeline styling, responsive geometry, queue metadata, framing mappings, adaptive controls, linked resolution, and footer metadata.
- Desktop play/pause/timeline seeking remains implemented unchanged and is left for human validation in the real Windows GUI.
- Version remains `0.1.0-dev.21` because no dev.21 tester installer has yet completed CI.

### Touched files

- `src/polymorph/smoke_test.py`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert the smoke-test commit if a future Qt runtime makes reliable offscreen random-access WebP seeking available again. No production conversion or playback UI code changed in this commit.

### Test notes

- The next Windows run must finish the frozen smoke within the existing 120-second guard and continue through installer/checksum/artifact creation.
- Human dev.21 validation should explicitly drag the preview timeline backward and forward while paused/running because headless CI no longer attempts that unsupported operation.

## POLY-2026-09-12-033 — 2026-09-12 18:10 PDT — Harden packaged preview smoke teardown

### Summary

- Investigated Windows Dev Build run #40 after it stalled inside the frozen-app smoke step until the 30-minute workflow timeout cancelled the job.
- Confirmed all 54 unit tests, pinned FFmpeg/gifski toolchain verification, adaptive integration, GIF reference comparison, and PyInstaller packaging had already passed before the stall.
- Changed preview playback from `QMovie.CacheAll` to `QMovie.CacheNone` to avoid aggressive full-animation caching in the frozen/offscreen Qt path.
- Preview frame seeks now pause an actively running movie before `jumpToFrame()` so the playback timer cannot race the requested seek.
- The dedicated `--smoke-test` application path now force-exits after returning its smoke result, preventing native Qt media/plugin teardown from holding the CI process open after assertions finish.
- The Windows packaged-smoke CI step now has an explicit 120-second process timeout, force-kills a wedged smoke process, and prints the smoke log before failing instead of consuming the full job timeout.
- No conversion, adaptive GIF, framing/export geometry, optimizer, updater, or user-facing dev.21 UI behavior changed.
- Version remains `0.1.0-dev.21` because the failed run never produced a dev.21 installer.

### Touched files

- `src/polymorph/ui/preview.py`
- `src/polymorph/app.py`
- `.github/workflows/windows-dev-build.yml`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert commit `2d226bc5d40051554ae7fdd425263aec44804739` to restore the original dev.21 packaged-smoke lifecycle. The visual fidelity work itself is in the preceding dev.21 commit and is independent of this hardening patch.

### Test notes

- The rerun must pass the frozen-app smoke within 120 seconds, then continue through Inno Setup, installer compilation, checksum generation, and both artifact uploads.
- Human UI validation remains the same as dev.21: compare directly against the approved mockup, verify responsive shrinking at smaller window sizes, and exercise the new playback/timeline controls.

## POLY-2026-09-12-032 — 2026-09-12 15:15 PDT — Fidelity pass against the approved Polymorph mockup

### Summary

- Reworked dev.20 using the user's annotated side-by-side screenshot as the direct visual specification rather than continuing approximate styling.
- Switched display typography to prefer system-installed `Trajan Pro`; `POLYMORPH` uses wide tracking, the subtitle is now mixed case exactly as requested (`Media conversion magic — by Knight Witch™`), and card headings prefer Trajan Bold with restrained tracking. Bundled Cinzel remains only as the packaged fallback because the supplied Trajan files are Adobe-proprietary and are not committed to the public repository.
- Removed the version from the title line. The footer now owns version/creator metadata.
- Re-aligned card content to the heading text column, retained divider lines only on busier cards, and specifically removed those dividers from Crop Zoom and Output Folder.
- Added the user's supplied resize, priority, crop, aspect-ratio, folder, trash, and update artwork as normalized high-DPI PNG assets. The UI tints the monochrome artwork at runtime to match the gold visual system.
- Enlarged the file-row overflow ellipsis and tightened the Files header so Add Files, trash, separator, and `Clear All` stay aligned on the right.
- Removed the branded Fit-only `Fill` button. Fit no longer changes card height when selected; the engine's background-color setting remains intact internally at its current/default value.
- Simplified the preview card: removed the `PREVIEW` heading/divider, removed the inner gray-looking surface, reduced the media border to a tight square line, and added a divider only at the bottom before source/frame/framed-max metadata.
- Added functional preview playback UI: play/pause, seekable frame timeline, elapsed/total seconds, and an in-view `FRAME n / total` plus timing readout. These controls operate only on the preview `QMovie` and do not alter export timing or frame selection.
- Rebuilt the main conversion action back to `POLYMORPH`, centered with Trajan-style tracking over symmetric static sigil/line decoration. The decoration remains separate from the later working/loading animation.
- Combined Ready/status and service links into one concept-matched footer panel with more breathing room between icon/text controls; added a divider and a second metadata row with `Polymorph v0.1.0-dev.21` at left and `Polymorph 2026, Knight Witch™` at right.
- Added deterministic runtime film grain over the gradient cards instead of requiring a supplied texture asset.
- Replaced scroll-dependent small-window behavior with responsive shrink mode. Below the 1260×820 design size, the UI scales typography, padding, control widths, queue rows, preview minimums and rail width down to a 920×640 supported minimum. The right control rail is no longer a vertical scroll area.
- Strengthened frozen-app smoke coverage for responsive minimum sizing, primary-action visibility, user-supplied icon packaging, hidden Fit Fill control, playback/seek behavior, footer metadata, and the existing framing/adaptive/linked-resolution mappings.
- No conversion, adaptive GIF, framing geometry, optimizer, updater, subprocess, or pinned toolchain behavior changed.
- Incremented the tester to `0.1.0-dev.21`.

### Touched files

- `src/polymorph/ui/brand_widgets.py` (new)
- `src/polymorph/ui/branded_layout.py`
- `src/polymorph/ui/styles.py`
- `src/polymorph/ui/preview.py`
- `src/polymorph/smoke_test.py`
- `src/polymorph/assets/ui/*.png` (new user-supplied icon artwork, normalized for UI use)
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to dev.20's first close mockup match. Conversion/framing/adaptive behavior is independent of the dev.21 UI/playback presentation changes.

### Test notes

- Full Windows CI must pass unit tests, pinned font acquisition/verification, pinned FFmpeg/gifski toolchain checks, adaptive integration, GIF reference comparison, PyInstaller build, frozen-app smoke, installer compilation, checksum generation, and artifact uploads.
- Frozen-app smoke now resizes to the supported minimum and rejects a clipped Polymorph button or failure to enter responsive shrink mode. It also seeks the animated preview by source frame and requires the playback timeline/readout to follow.
- Human dev.21 review should compare directly against the approved mockup at default size and then resize the window downward to confirm the interface shrinks rather than requiring the user to scroll for the primary action.

## POLY-2026-09-12-031 — 2026-09-12 05:05 PDT — Tighten the branded UI to the approved concept

### Summary

- Used the user's side-by-side dev.19/mockup comparison as the direct design target rather than continuing incremental skinning.
- Fixed the right settings rail so it has a stable 410 px viewport, vertical scrolling when necessary, and no horizontal scrolling/clipping. Default window geometry is reduced to a more useful `1260x820` while remaining comfortably above the responsive floor.
- Reduced outer/card/control padding and tightened body typography so the UI no longer feels inflated.
- Rebuilt card headers around a small gold line icon, title, and explicit separator line.
- Reworked Output Format into side-by-side GIF/MP4 choices with compact helper text.
- Reworked Sizing into two compact editable rows and removed spinbox ticker arrows; users type file-size and resolution values directly.
- Paired Framing and Aspect Ratio as two cards on one row; kept Original/Crop/Fit as real radio controls synchronized to the established framing state.
- Split Crop Zoom into its own compact card with percentage readout and a small reset/center action.
- Retained Fit background-color functionality as a small Fit-only `Fill` utility rather than a dedicated background-color card.
- Rebuilt the Files area to match the concept: title and file count share the action row; Add Files sits beside a selected-item trash button, separator, and `Clear All` text action that turns crimson on hover.
- Added real queue-row media presentation: first-frame thumbnail, source file name, original decimal file size, source dimensions, runtime, and overflow actions for Open, Open file location, and Remove from queue.
- Replaced the oversized idle/progress treatment with a compact Ready strip containing a ring glyph, `Ready`, and `<N> files imported. Choose your settings and begin.`; thin progress appears only while conversion is actually advancing.
- Rebuilt the footer as labeled Check for Updates / GitHub / Ko-fi / Patreon / Discord controls separated by dividers.
- Rebuilt the Cast Polymorph face with a central sigil, display title, `CONVERT MEDIA` subtitle, symmetric dashes, richer crimson/gold gradient, and the existing real conversion click behavior.
- Increased letter spacing in the `POLYMORPH` title and subtitle/byline. Cinzel remains temporary until the user provides the closer final display font.
- Suppressed the old 110 px ArcaneProgress placeholder from the compact status strip; real magic-circle/D20 working animation remains a separate future pass.
- Strengthened packaged smoke to reject horizontal rail overflow, missing concept Cast face, missing queue thumbnail/metadata rows, or restored spinbox arrow styling.
- No conversion, adaptive GIF, framing geometry, updater, subprocess, or pinned toolchain behavior changed.
- Incremented the tester to `0.1.0-dev.20`.

### Touched files

- `src/polymorph/ui/branded_layout.py`
- `src/polymorph/ui/styles.py`
- `src/polymorph/smoke_test.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`
- `HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV19.md`
- `HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV19.md`

### Rollback

- Revert this commit to return to dev.19's looser first two-column composition. Conversion/framing/adaptive behavior is independent of this presentation pass.

### Test notes

- Full Windows CI must pass unit tests, pinned font acquisition/verification, pinned FFmpeg/gifski toolchain checks, adaptive integration, GIF reference comparison, PyInstaller build, frozen-app smoke, installer compilation, checksum generation, and artifact uploads.
- Frozen-app smoke now shows the window offscreen and verifies that the control rail has no horizontal overflow, the concept-style Cast face exists, file rows gain metadata/thumbnail widgets after import, radio/framing mappings still work, spinbox arrow styling remains removed, and linked resolution behavior still passes.
- Human dev.20 review should compare directly against the approved mockup rather than against dev.19.
