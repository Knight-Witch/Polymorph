# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-15-064 — Motion Lab Elder Futhark transmutation rebuild FULL PASS

### Summary

- Rebuilt the standalone loader around Amanda's annotated Fullmetal Alchemist-inspired transmutation-circle motion study; the original simple rotating-line treatment is no longer the active direction.
- Switched rune content to real Elder Futhark and added a dedicated Noto Sans Runic bundle step to the standalone Motion Lab workflow.
- Added opposed rune motion families: clockwise outer rune band with six larger designated glyphs, counter-clockwise inner band, and three counter-clockwise rune rings clipped to partial visible arcs.
- Added a stationary middle rune band whose glyphs asynchronously glimmer/change only while dim, plus three large rune spheres that independently cycle glyphs without matching each other on a frame.
- Added clockwise triangle/rune-sphere motion, two offset counter-clockwise hexagons, grouped structural flicker and a four-stage outside-in cascade pulse.
- Replaced stub traces with six synchronized radial comet tracers that move outer→center→outer with bright heads, long gradient tails and explicit no-go clipping behind rune spheres, the center circle and partial rune bands.
- Reworked line glow into a tight ivory core plus multiple wide low-opacity gold/crimson passes for a smoother soft falloff.
- The two outermost rings are now opposite-direction real progress arcs. At 100% they pulse, the inner ritual fades, a radial flash fires and the Knight Witch emblem materializes.
- Added four study emphasis modes: Transmutation, Dense Runes, Tracer Ritual and Fractal Echo.
- Added bundled `assets/kw_emblem.svg`, derived from Amanda's supplied SVG with path-coordinate simplification only and visually checked against the source; the correct emblem no longer depends on the runtime SVG chooser.
- Clarified every motion control so each slider names the exact animated family it drives.
- Dedicated `Polymorph Motion Lab Build` run #3 / run ID `34944466899` is FULL PASS on implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd`.
- PASS: Windows source offscreen smoke, PyInstaller portable build, packaged Windows launch smoke and artifact upload.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10386399042`, size 50,819,549 bytes, digest `sha256:ca12e0e0bcf2f239c8e2acd75046443e4016bdefb7df11bb040625390bc6b767`.
- The same implementation also triggered the normal Windows Dev Build run #103 / run ID `34944466940`, which passed all production unit/toolchain/adaptive/GIF-reference/frozen-app/installer gates, confirming the isolated lab work did not regress the protected production app.
- Production Polymorph remains dev.27 unchanged; no conversion, framing, adaptive, updater, production UI, installer or public-release behavior changed.

## POLY-2026-09-14-063 — Standalone Motion Lab prototype FULL PASS

### Summary

- Added a standalone PySide6 Motion Lab for the deferred loader/working animation and animated primary action; production Polymorph behavior and runtime remain dev.27 unchanged.
- Added four loader compositions with independent rune/counter rotation, energy traces, glow, real 0–100% progress, and a swappable SVG center-emblem layer.
- Added black, Polymorph blue-black, procedural textured, busy stress-test, and custom-image preview backgrounds so animation legibility can be judged over different surfaces.
- Added an animated POLYMORPH button prototype that behaves as a clipped window into an oversized arcane mechanism, wakes on hover, carries a moving text-light tracer, and produces a short cast burst on click.
- Added a debug reveal mode that expands the button preview canvas and shows the full mechanism outside the cyan button clipping boundary.
- Added runtime `Load emblem SVG…`; basic emblem rendering does not rely on SVG path direction. A future contour-following tracer, if selected, should use a normalized animation path instead of rewriting canonical emblem artwork.
- Added a dedicated Windows Motion Lab workflow with source smoke, PyInstaller package, packaged smoke, and portable artifact upload.
- Motion Lab Build run #1 / run ID `34931411518` is FULL PASS on implementation commit `0341ea270fb88495cde7f102e155e8ddd44680cc`.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10381886805`, digest `sha256:b96ff563b952c411614417df483c1996de51d128895b39692f9bf933c12583b6`.
- No conversion, framing, adaptive, updater, production UI, runtime-version, installer, or public-release behavior changed.

## Documentation note

- This follow-up records completed CI/artifact identities only; no runtime, package, production UI, conversion, or release behavior changed in the documentation-only update.
