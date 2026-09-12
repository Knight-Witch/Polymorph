# Changelog

Historical entries through dev.19 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV19.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV19.md). Earlier pre-dev.16 history also remains in the existing dev.15 archive.

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
