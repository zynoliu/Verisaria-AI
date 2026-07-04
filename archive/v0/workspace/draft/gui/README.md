# Verisaria Pixel GUI Draft Assets

This directory is a standalone GUI draft area. It does not import from or modify
anything under `src/`.

The current asset pack is based on the Frostgate pixel GUI concept. Most assets
are generated as atlas sheets so the next prototype step can crop or slice them
into concrete sprites, panels, and icons.

## Structure

- `assets/backgrounds/`: full-scene background layers
- `assets/overlays/`: atmosphere, foreground, speech/focus marker overlays
- `assets/characters/`: character standees and dialogue portraits
- `assets/ui/`: panel, input box, button, gauge, and border atlas
- `assets/icons/`: icon, emblem, badge, and faction marker atlas
- `refs/`: full GUI reference mockup

Files ending in `_key.png` keep the original chroma-key green background.
Files ending in `_alpha.png` are transparent RGBA versions for compositing.

## Godot Prototype

This folder is also a standalone Godot 4 project.

Open:

```bash
godot4 --path draft/gui
```

Or open `draft/gui/project.godot` from the Godot editor.

Current prototype files:

- `project.godot`: Godot project root
- `scenes/main.tscn`: minimal root scene
- `scripts/main.gd`: mock-data GUI scene builder

Current mock interactions:

- Type into the bottom input and press Enter, or click `执行`.
- Tick, stamina, relationship meters, pressure, event log, and the `难民入营`
  world variable update from local mock state.
- No runtime connection to the engine exists yet.

## Suggested Next Steps

1. Crop individual sprites/icons from the atlas sheets into smaller PNGs.
2. Build a simple GUI mock canvas using the base background plus the transparent
   character and UI assets.
3. Decide a working viewport scale before pixel-perfect slicing; the generated
   sheets are high-resolution pixel art, so a 2x/3x rendering strategy will help
   keep the style crisp.
