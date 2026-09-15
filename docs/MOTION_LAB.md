# Polymorph Motion Lab

Standalone PySide6 design sandbox for Polymorph's deferred loading/working animation and animated primary action.

This is intentionally isolated from the production Polymorph window. It does not touch conversion, framing, updater, queue, or encoder behavior.

## Run from source

```powershell
python run_motion_lab.py
```

or, with the package installed/editable:

```powershell
python -m polymorph.motion_lab
```

## Current prototype controls

- Switch the preview surface between black, the Polymorph blue-black gradient, two procedural textures, a deliberately busy stress-test surface, or any custom image.
- Compare four loader compositions: Ritual, Concentric, Cipher, and Hybrid.
- Scrub real loader progress or auto-loop 0–100%.
- Tune loader glow, rune rotation, counter-rotation, and energy-trace speed.
- Load any SVG as the center emblem at runtime. The canonical Knight Witch/Polymorph emblem can be dropped in without changing loader geometry.
- Hover the real button to wake its oversized clipped arcane mechanism and text tracer.
- Force Rest/Hover/Pressed states for inspection.
- Click the button to preview a short cast/activation burst.
- Reveal the full oversized button mechanism around the cyan clipping boundary to tune the “window into a larger sigil” behavior.

## SVG path-direction note

The center emblem is rendered as normal SVG artwork rather than relying on CSS `stroke-dasharray` traversal, so source subpath direction is not required for the basic emblem reveal. If a later approved effect needs a tracer to travel along the emblem's actual contours in a prescribed order, that tracer should use a normalized animation path layer rather than mutating the canonical emblem artwork.

## Acceptance boundary

This lab is exploratory visual tooling. None of its motion is part of the shipping Polymorph UI until Amanda selects/approves a treatment and it is deliberately integrated behind a separate human visual gate.
