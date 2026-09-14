# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; older detail is not mandatory startup reading.

## PFC-2026-09-14-052 — Stale mockup-version assertion after run #75

- Run #75 / run ID `34820011338` from visual-polish commit `b9196d17c67393ba79f509b107e30c08b55915ef` passed font assets, all 56 unit tests, protected conversion/toolchain/adaptive/GIF-reference gates, and the frozen application build.
- Packaged smoke failed at its first presentation-version assertion because `fidelity_pass.py` intentionally advanced `polymorphFidelity` to `mockup-v2`, while smoke still demanded `mockup-v1`.
- This failure is stale test metadata, not a demonstrated runtime regression. Change only the expected fidelity tag to `mockup-v2`.
- Do not weaken or bypass the remaining packaged assertions. The rerun must still prove bundled Polymorph font application, two-column composition, FILES grouping, 920×640 primary-action visibility, preview decode, adaptive controls, framing geometry mapping, linked resolution, and footer metadata.
- Runtime remains dev.25. Run #75 produced no installer.
- No visual behavior, SVG asset, conversion/framing/adaptive/updater/subprocess/toolchain behavior changes in this repair.

## PFC-2026-09-14-051 — Human visual polish after run #62

- Human visual review of the installed run #62 tester confirms the custom Polymorph face is finally rendering correctly, so do not reopen font provenance/registration or the direct-label ownership repair.
- Remaining issues are presentation-only: right-rail section headings are optically too large; section icons are inconsistent/low quality; Framing and Crop Zoom incorrectly share a symbol; Output Format/Sizing radio bubbles sit left of GIF Priority; helper text under Preserve/Favor is over-indented; Browse/Add Files text is too large; playback's text glyph is effectively invisible; and the primary POLYMORPH label is right-shifted inside its button.
- Preserve the run #62 technical PASS, accepted 1260×820 / 920×640 geometry, minimum-size compact-rail fix, and all protected conversion/framing/adaptive/updater/subprocess/toolchain behavior.
- Presentation repair uses a post-responsive optical controller so heading size, radio/helper alignment, vector icons, playback icons, and small-button text remain correct after window resizes without changing the underlying layout engine.
- Use one coherent thin-line SVG family for FILES, Output Format, Sizing, GIF Priority, Framing, Aspect Ratio, Crop Zoom, and Output Folder. Framing and Crop Zoom must remain visually distinct.
- Playback uses real play/pause SVG icons tied to `playbackChanged`; do not rely on narrow text glyphs in the 28 px tool button.
- Primary action keeps its existing surface/sigil but centers `POLYMORPH` against the full button rectangle.
- Runtime remains dev.25 for this visual revision. No conversion, package-toolchain, updater, or public-release behavior changes.
- Next gate is the complete Windows pipeline, followed by another installed human visual check. CI can prove packaging/geometry/functionality, not appearance.

## PFC-2026-09-13-050 — dev.25 technical PASS / human visual gate next

- Run #62 / run ID `34809405250` from code commit `112f2e2efb128ef806cb6f44ed650b9753a5471e` passed the complete Windows technical pipeline.
- Required packaged smoke passed both the real Polymorph title/subtitle/card-heading typography assertion and the 920×640 primary-action visibility assertion in the same frozen application.
- Installer artifact `Polymorph-dev-installer`: ID `10334421612`, digest `sha256:c77908691be09782951a52d8537e7c629681a3f6638e5a48e09b7880966b9384`.
- Keep dev.25 behind the human visual gate. Amanda must inspect the normal installed tester and confirm BrandTitle, BrandSubtitle/byline, FILES, all right-rail headings, primary action, overall card density/alignment, and compact-minimum appearance before promotion or typography retuning.
- Do not reopen protected conversion/framing/adaptive/updater/subprocess/toolchain areas without new evidence.
- This record is documentation-only: no runtime, version, package contents, UI behavior, conversion behavior, or public-release state changed.

## PFC-2026-09-13-049 — Measured second compact pass after run #61

- Run #61 / run ID `34808985545` is failed evidence, not a tester to hand to Amanda.
- PASS before failure: custom Polymorph assets, all 56 unit tests including the real QLabel font-resolution test, protected conversion/adaptive/GIF gates, frozen app build, applied Polymorph typography, title/byline fidelity, and FILES grouping.
- Exact remaining failure: `POLYMORPH action is clipped at minimum size: button bottom 494, rail 482`.
- The first minimum-only compaction recovered 14 px relative to run #60. Preserve it and preserve the now-confirmed typography implementation.
- Recover the remaining 12 px without shrinking the primary action or changing normal-size geometry: at compact scale only, reduce top-level `ControlRailContent` spacing from 2 px to 1 px and reduce each top-level `ControlCard` bottom padding by one additional pixel.
- Keep 1260×820 full-size metrics, 920×640 supported minimum, FILES/preview/footer geometry, font sizes/tracking/assets, and all protected runtime/toolchain behavior unchanged.
- Runtime remains dev.25 because run #61 produced no installer.
- Re-run the full Windows pipeline; only hand over a tester if applied typography and minimum-size primary-action visibility pass in the same frozen build.

## PFC-2026-09-13-048 — Minimum-size rail compaction after run #60

- Run #60 / run ID `34807810638` is useful failed evidence, not a tester to hand to Amanda.
- PASS before failure: packaged Polymorph fonts, 56 unit tests including the real QLabel font-resolution test, protected conversion/adaptive/GIF gates, frozen app build, `PASS applied Polymorph title/subtitle/card-heading typography`, title/byline fidelity, and FILES grouping.
- Exact failure: `POLYMORPH action is clipped at minimum size: button bottom 508, rail 482` at the existing 920×640 supported minimum.
- This is no longer a typography-assignment failure. Preserve the direct widget-owned Polymorph fonts and do not weaken the smoke assertion.
- Keep 1260×820 full-size geometry unchanged. At responsive scale `<= 0.76`, compact only the top-level `ControlRailContent` spacing and top/bottom padding on top-level `ControlCard` layouts. Do not shrink the primary action or change FILES/preview/footer geometry.
- Runtime remains dev.25 because run #60 produced no installer.
- Preserve all protected conversion/framing/adaptive/updater/subprocess/toolchain behavior.
- Re-run the complete Windows pipeline. Only hand over a tester if both the applied-typography and 920×640 primary-action visibility gates pass in the same frozen build.

## PFC-2026-09-13-047 — Direct widget-owned Polymorph typography after run #59

- Run #59 / run ID `34807445345` failed packaged smoke with `Brand title is not using Polymorph Regular: 'Inter' != 'Polymorph'`; installer steps were correctly skipped.
- Do not weaken the smoke. App-level specific QSS still leaves the resolved QLabel font as Inter under the body stylesheet.
- Keep the restored QSS body/control sizing model from the responsive repair.
- Apply the branded face directly on each BrandTitle, BrandSubtitle and CardHeading widget with a local stylesheet, then set the tracked QFont for absolute letter spacing/bold state.
- Add an offscreen Qt unit test using the packaged font loader and real QLabel objects under the Inter body QSS; require resolved Polymorph family before the slow build proceeds.
- Runtime remains dev.25; no installer from run #59.
- Preserve font bytes, existing point sizes/tracking, 1260×820 / 920×640 geometry, and all protected conversion/framing/adaptive/updater/subprocess behavior.

## PFC-2026-09-13-046 — Restore responsive QSS metrics after run #58

- Run #58 proved applied Polymorph typography but failed the minimum-size primary-action visibility gate after body sizing moved into inherited QFont.
- Restore the accepted body/control QSS sizing mechanism without reverting the font-assignment repair.

## PFC-2026-09-13-045 — dev.24 visual rejection / root-cause repair

- dev.24 was technical PASS but human visual FAIL: only the custom-painted primary action visibly used Polymorph.
- Root cause was global Inter QWidget QSS overriding QLabel display fonts. dev.25 adds real applied-font gates.