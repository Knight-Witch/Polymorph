# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Current development version: `0.1.0-dev.21`
- Public release: not yet published.
- Core conversion machine is considered functionally complete for the current v1 scope: MP4 is human-validated; Preserve-motion GIF quality/smoothness is human-validated; decimal-MB ceiling behavior is validated; updater hardening is validated; Favor-resolution GIF behavior is diagnostically and visually validated on Viper plus two kitbash/decal-heavy HeroForge variants; Crop/Fit preview and real exported output are human-validated end to end; Windows probe/encode console flashes are eliminated.
- UI work is now the active development phase. dev.18 established the black/gold/red visual language; dev.19 replaced the old three-column scaffold; dev.20 moved much closer to the approved mockup; dev.21 is the fidelity pass driven by the user's direct side-by-side markup: Trajan-preferred display typography, aligned card content, supplied icon artwork, simplified preview chrome, playback/timeline controls, responsive shrink behavior, and a rebuilt two-level status/footer.
- The loading/working animation and final application emblem remain separate design work.

## Canonical conversion behavior

### GIF — Preserve motion

- Default mode.
- Input focus: animated WebP.
- Decode/process through FFmpeg.
- Stream YUV4MPEG directly to gifski 1.32.0.
- gifski quality 100, `--extra`, explicit width, infinite repeat.
- Production uses explicit `yuv420p` for deterministic compatibility on bundled FFmpeg 9.0.1.
- Explicitly pass source FPS to gifski and verify exact source frame count/timing.
- Do not intentionally drop, duplicate, or lower frames to meet a size target.
- In file-size mode, reduce spatial resolution only as needed to fit the user ceiling.
- User-entered MB ceilings are decimal; default `99 MB` means exactly 99,000,000 bytes.
- GIF file-size search uses the patched-Python smart-fit resolution algorithm introduced in dev.8.

### GIF — Favor resolution

- Explicit opt-in; Preserve motion remains the default.
- Available only for GIF + Fit under file size.
- Starts from the Preserve-motion fitted result.
- Preferred long edge remains native resolution capped at 2048 px; never upscale.
- dev.13+ tests exact original-source-frame decimation rather than synthesizing frames.
- Candidate order is stride 2 first, then stride 3 while effective motion remains above the automatic 8 FPS floor.
- Candidate byte cost is measured at the Preserve baseline dimensions using real gifski output.
- A candidate must predict roughly 8% or greater linear spatial gain before the full adaptive size search runs.
- A full candidate must realize the same gain threshold or Polymorph continues to the next stride.
- If source frame count is not divisible by stride, only the final GIF delay is shortened to preserve exact source duration/angular speed.
- Keeps quality 100, `--extra`, explicit width, infinite repeat, smart-fit sizing, and post-encode integrity verification.
- Development diagnostics write `*_ADAPTIVE_DIAGNOSTIC.json` only for Favor-resolution/file-size GIF runs; this sidecar is temporary developer instrumentation.

### MP4

- Output: H.264 MP4 for broad compatibility.
- Preserve source timing/frame sequence.
- High-quality encoder settings remain internal and hidden from the novice UI.
- MP4 file-size search remains the previously human-validated implementation.
- Produced video is cleanly loop-ready; actual repeat playback is controlled by the player/platform.

## Human validation and OG reference

- The only canonical OG behavioral reference is the patched Python `HeroForge_WebP_to_Reddit_GIF.py` actually run by the user.
- The separately packaged Discord build is unvalidated and excluded from parity decisions.
- Width-corrected Polymorph Preserve GIF is visually on par with OG and was reported slightly smoother.
- True-decimal 99 MB Preserve-motion Viper output is `1552x1552`; quality/smoothness remained good.
- OG Viper result was `1756x1756` but contains 300 frames from a 375-frame / 25 FPS / 15 s source, i.e. exactly 20 FPS. Its spatial advantage is therefore partly a hidden temporal tradeoff and is not a valid Preserve-motion parity target.
- Possible slight red/pink difference remains visually inconclusive and is not treated as a blocker.

## Adaptive motion validation

- Real Viper source: 2048x2048, 375 frames, 25 FPS, 15.0 s, every source frame 40 ms.
- A confirmed Viper Favor-resolution run selected stride 2 and returned full native `2048x2048`, 188 frames, exactly 15.0 s, ~12.53 effective FPS, and 82,147,387 bytes. The user reported the motion/frame rate looked consistent.
- Viper stride-2 sample at the Preserve baseline dimensions was 51,558,287 bytes versus 93,630,962 bytes for the full-frame baseline.
- A harder 2048px kitbash/decal-heavy 500-frame / 20 s variant selected stride 2 and produced `1810x1810`, 250 frames at exactly 80 ms each, ~97.22 MB.
- A 3072px version of the same complex scene selected stride 2 and produced `1752x1752`, 250 frames at exactly 80 ms each, ~94.69 MB.
- These real workloads support keeping the current adaptive policy unchanged.

## Framing behavior

- Original preserves source framing.
- Crop trims to the selected aspect ratio without distortion; preview and encoder share the same geometry resolver.
- Crop supports drag repositioning plus 100-300% zoom. Zoom shrinks the retained source window rather than upscaling.
- Fit preserves the complete source aspect ratio and expands the canvas with user-selectable padding color; drag repositioning moves the source inside available padding.
- Human desktop validation confirmed Crop/Fit behavior in the viewer and one real Crop export plus one real Fit export matched expectations. Framing preview/export parity is therefore closed for current scope.

## Branded UI state

- Branded runtime composition is two columns: left workspace with compact media queue + dominant preview, and a right settings rail. The rail no longer depends on vertical scrolling; below the 1260×820 design size, the UI enters responsive shrink mode and scales typography, card density, control widths, preview minimums, and rail width down to the supported 920×640 floor.
- Queue header follows the approved mockup: `FILES` and count share one row, while Add Files / supplied trash icon / separator / red-hover `Clear All` stay aligned at the right edge. Queue rows retain thumbnail, source size, dimensions, runtime, and the real Open / Open file location / Remove overflow menu; the overflow dots are larger in dev.21.
- Busy settings cards use supplied/reworked gold icons, Trajan Pro Bold-preferred headings, a separator, and content indented to the same visual column as the heading text. Crop Zoom and Output Folder intentionally omit the heading divider.
- `OUTPUT FORMAT` remains side-by-side; `SIZING` uses editable fields without ticker arrows; `FRAMING` and `ASPECT RATIO` remain paired. The dev.20 Fit-only `Fill` control is removed from the branded UI so choosing Fit cannot expand the card.
- The preview card no longer has a redundant `PREVIEW` header or inner gray panel. Media is drawn against the preview-card background with a tight square/near-square border, playback controls beneath it, a seekable source-frame timeline, seconds readout, and in-view `FRAME n / total` timing readout. A divider separates playback from the source/framed-max metadata line.
- Header lockup is `POLYMORPH` plus mixed-case `Media conversion magic — by Knight Witch™`; the version moves out of the title line. Trajan Pro is the preferred system display family, with bundled Cinzel retained only as the legal packaged fallback and Inter as the body/UI family. Trajan font binaries supplied by the user are not committed to the public repository.
- Primary conversion copy is back to `POLYMORPH`; its label uses the same Trajan-preferred tracking language as the application title, centered over static sigil/line decoration that remains separate from the later loader animation.
- Status + link footer is now one concept-matched two-level panel: top row carries Ready/status plus spaced Check for Updates / GitHub / Ko-fi / Patreon / Discord links and separators; a divider leads to `Polymorph v…` at bottom-left and `Polymorph 2026, Knight Witch™` at bottom-right.
- Current palette remains near-black/charcoal, ivory, champagne gold and restrained crimson, with layered gradients and a faint deterministic runtime grain overlay; no external grain texture is required.
- The later loader animation remains open between the arcane/magic-circle concept and the user's D20 roll/spin concept.

## Windows subprocess behavior

- FFmpeg and gifski encoding subprocesses use `CREATE_NO_WINDOW`.
- ffprobe uses the same flag for initial probing and post-encode integrity checks.
- Human testing confirmed the focus-stealing popup windows are gone.

## Update policy

- Check only official GitHub releases from `Knight-Witch/Polymorph`.
- Require exact versioned installer plus matching `.sha256` companion.
- Download only official repository HTTPS release assets.
- Verify SHA-256 before launching installer.
- No background service, startup daemon, unattended updater, or silent install.

## Known follow-ups

- Human-review dev.21 directly against the approved concept side-by-side: Trajan rendering/tracking, vertical option alignment, supplied icons, preview/player treatment, primary action centering, footer spacing/meta row, and responsive shrink behavior at default and minimum window sizes.
- Design and implement the working/loading animation after the structural UI is accepted.
- Decide final application emblem/icon.
- Favor resolution performs extra measurement encodes by design; conversion-time optimization can be investigated later but must not change selected outputs.
- First public release still requires a deliberate project-license choice and final packaging/release-workflow review.
- Code-signing / SmartScreen strategy remains a release decision.

## Deferred

- User-configurable advanced FPS floor/target controls.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
- macOS/Linux packaging.
