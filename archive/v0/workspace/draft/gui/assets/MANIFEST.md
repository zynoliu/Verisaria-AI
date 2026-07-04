# GUI Asset Manifest

Generated with built-in image generation, then copied into `draft/gui/assets/`.
Original generated files remain under Codex's generated image directory.

## Backgrounds

- `backgrounds/frostgate_gatehouse_base.png`
  - Size: 1672 x 941
  - Format: RGB
  - Use: base Frostgate gatehouse scene, no foreground characters or UI.

## Overlays

- `overlays/frostgate_overlay_atlas_key.png`
  - Size: 1672 x 941
  - Format: RGB, chroma-key source
  - Contains: snow particles, snow drift strips, lantern glow, moonlight beam,
    distant refugees, breath fog, shadows, speech bubbles, focus diamonds.

- `overlays/frostgate_overlay_atlas_alpha.png`
  - Size: 1672 x 941
  - Format: RGBA
  - Use: transparent compositing source; crop individual effects from here.

## Characters

- `characters/character_standee_atlas_key.png`
  - Size: 1881 x 836
  - Format: RGB, chroma-key source
  - Contains: player traveler, Captain Brann, Sentry Voss, Refugee Kaze, Old Sib,
    each with neutral and speaking/gesturing variants.

- `characters/character_standee_atlas_alpha.png`
  - Size: 1881 x 836
  - Format: RGBA
  - Use: transparent full-body standees for scene placement.

- `characters/portrait_expression_atlas_key.png`
  - Size: 1254 x 1254
  - Format: RGB, chroma-key source
  - Contains: five rows of dialogue portraits with four expressions each.

- `characters/portrait_expression_atlas_alpha.png`
  - Size: 1254 x 1254
  - Format: RGBA
  - Use: transparent portrait/emotion source for dialogue and NPC panels.

## UI

- `ui/ui_frame_atlas_key.png`
  - Size: 1672 x 941
  - Format: RGB, chroma-key source
  - Contains: dialogue panel, input box, sidebar modules, event log frame,
    portrait rings, status frame, buttons, tabs, gauge tracks, gauge fills,
    corner ornaments, and 9-slice-style border samples.

- `ui/ui_frame_atlas_alpha.png`
  - Size: 1672 x 941
  - Format: RGBA
  - Use: transparent source for cropping and slicing GUI chrome.

## Icons

- `icons/icon_emblem_atlas_key.png`
  - Size: 1672 x 941
  - Format: RGB, chroma-key source
  - Contains: Verisaria emblem, Frostgate banner, HP, stamina, tick, location,
    relationship, suspicion, trust, pressure, world-change, dialogue, combat,
    map, agenda, save, settings, close, plus/minus, check/cross, severity badges,
    and faction badges.

- `icons/icon_emblem_atlas_alpha.png`
  - Size: 1672 x 941
  - Format: RGBA
  - Use: transparent icon source.

## Reference

- `../refs/verisaria-pixel-gui-prototype-reference.png`
  - Size: 1672 x 941
  - Format: RGB
  - Use: target composition reference for the next GUI prototype.

## Generation Notes

- Background prompt requested a clean Frostgate gatehouse scene with no UI and no
  foreground characters, leaving space for sprite placement and bottom dialogue UI.
- Atlas prompts requested crisp 16-bit/32-bit pixel-art assets on flat `#00ff00`
  chroma-key backgrounds, with no text labels or watermarks.
- Chroma-key removal used Codex's imagegen helper with border auto-key,
  soft matte, and despill.

