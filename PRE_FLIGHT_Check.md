# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-15-066 — Motion Lab v5 scene builder FULL PASS

- PASS static: new Motion Lab editor/loader/rune modules parse without syntax errors.
- PASS architecture: changes remain isolated to standalone Motion Lab tooling; production conversion, framing, updater, encoder, installer and runtime version are unchanged.
- PASS source design: v4 preset JSON is migrated without discarding saved element/global values; new layer/rune fields use v5 defaults where the v4 schema had no equivalent.
- PASS source design: six large outer runes are the default frontmost layer above both outer progress rings.
- PASS source design: all rune renderers share one asynchronous transition/glimmer model with Fade/Snap, timing randomization, bright/dark holds, color/brightness range, and zero-transition radial/twinkle/pulse modes.
- PASS source design: exposed speed ranges extend to 2000% while underlying saved/imported values remain unchanged.
- PASS source design: geometry pulse capability is absent from rune elements.
- PASS source design: drag/drop layer order, duplicate/remove/group-copy/group-clear, study copy/rename, v4 preset load, v5 workspace export/load and checkpoint reset flows are implemented.
- PASS source design: background sparkle field is deterministic and independently configurable.
- PASS CI: dedicated `Polymorph Motion Lab Build` run #8 / run ID `35056008606` completed successfully on implementation commit `d6d694e59358e9507bba540d43c44fb1fe32abc2`.
- PASS CI: Windows source smoke, PyInstaller portable build, packaged Windows smoke and portable artifact upload.
- Artifact `Polymorph-motion-lab`, artifact ID `10430402445`, size 50,889,797 bytes, digest `sha256:4ae317285edc9a7fc821ea0374f2eb8ef1aacb4094e5e7a1abee9c2c08482ee4`.
- PASS isolation check: normal Windows Dev Build run #108 / run ID `35056008609` completed successfully on the same implementation commit, including unit tests, pinned FFmpeg/gifski checks, adaptive integration, GIF reference comparison, production PyInstaller build, packaged production smoke, installer compilation, checksum and artifact uploads.
- No production conversion, framing, adaptive, updater, subprocess, app-window, installer, runtime-version or public-release behavior changed.
- Next gate: Amanda loads her existing v4 export into v5, confirms the old tuning resumes, then visually tunes/reorders/duplicates as desired and exports the selected v5 workspace.

## Documentation note

- This follow-up records completed v5 CI/artifact identities only. It changes no runtime, package, production UI, conversion, installer, or public-release behavior.
