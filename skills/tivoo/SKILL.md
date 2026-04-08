---
name: tivoo
description: "Use when the user wants to control a Divoom Tivoo pixel screen - adjust brightness, display images, show animations, set clock mode, change light color, generate pixel art, or send raw Bluetooth commands to the device"
---

# Tivoo Pixel Screen Control

Control a Divoom Tivoo 16x16 pixel screen via Bluetooth.

## First-Time Setup

Check if the Bluetooth bridge binary `tivoo_cmd` exists in the skill's `scripts/` directory.

### 1. Compile Bluetooth Tool

The user must compile `tivoo_cmd` locally (binaries are not distributed for security):

```bash
cd scripts/
clang -framework Foundation -framework IOBluetooth -o tivoo_cmd tivoo_cmd.m -fobjc-arc
```

Requires Xcode Command Line Tools. If not installed: `xcode-select --install`

### 2. Configure Device MAC Address

Set the `TIVOO_MAC` environment variable to your device's Bluetooth MAC address:

```bash
export TIVOO_MAC="AA:BB:CC:DD:EE:FF"
```

Default: `11:75:58:8C:5B:0C`. No recompilation needed — the MAC is passed via `-a` flag at runtime.

### 3. Install Python Dependencies

```bash
pip3 install click          # CLI framework (required)
pip3 install Pillow         # Image/animation/text (recommended)
pip3 install anthropic      # AI pixel art (optional)
```

### 4. macOS Bluetooth Permissions

On first run, macOS will prompt for Bluetooth access. Allow your terminal app (Terminal/iTerm/Warp) to access Bluetooth.

Check in: System Settings > Privacy & Security > Bluetooth

## Tool Path

The tool is at `scripts/tivoo_macos.py` relative to the skill directory:

```bash
python3 scripts/tivoo_macos.py <command>
```

## Command Reference

| Command | Example | Description |
|---------|---------|-------------|
| `brightness <0-100>` | `brightness 50` | Set brightness |
| `clock [style] [opts]` | `clock 1` | Clock mode (style 0-6) |
| `light <color>` | `light #FF6600` | Light effect color |
| `off` / `on` | `off` | Turn screen off/on |
| `image <path>` | `image cat.png` | Send image (--duration 12) |
| `text <text>` | `text Hello` | Scrolling text (--loop 3, --font, --size) |
| `anim <dir\|gif>` | `anim frames/` | Send animation (--loop 3) |
| `preset <name>` | `preset heart` | Animated preset (--duration 12, --load) |
| `ai <prompt>` | `ai "a cat"` | AI-generated pixel art |
| `ai-anim <prompt>` | `ai-anim "fire"` | AI-generated animation |
| `raw <hex...>` | `raw 74 64` | Raw hex command |
| `prepare <sub>` | `prepare preset heart` | Stage animation frames |
| `send [file]` | `send` | Send staged frames (--loop 3) |

All commands support `-h` / `--help` for detailed options.

### Auto-Restore Clock

By default, static commands (`image`, `preset`) display for 12 seconds then restore clock mode (`clock 1`). Animation commands (`text`, `anim`, `send`) loop 3 times then restore.

Use `--duration 0` or `--loop 0` for permanent display (no auto-restore).

### Presets

41 animated presets (run `preset` without args to list all):

- **Emoji**: heart, smiley, star, thumbs-up
- **Weather**: sun, moon, cloud, rain, snow, lightning
- **Animals**: cat, dog, fish
- **Nature**: flower, tree, fire
- **Symbols**: check, cross, music, ghost, skull, gradient, rainbow
- **Workflow**: working, thinking, error, success, coding, loading, building, deploying, testing, searching, downloading, uploading, debugging, saving, syncing, done

13 built-in emotion presets: happy, sad, angry, love, cool, cry, laugh, sleepy, shock, wink, sick, party, kiss

#### Custom Presets (--load)

Load external preset files to override or add presets:

```bash
python3 scripts/tivoo_macos.py preset happy --load emotion_presets_luna.py
```

External files export `PRESETS` and/or `EMOTIONS` dicts. Same-name entries override built-in ones.

### Clock Options

```
clock [STYLE] [--12h] [--weather] [--temp] [--calendar] [--color COLOR]
```

Styles: 0=fullscreen, 1=rainbow, 2=boxed, 3=square, 4=fullscreen-inv, 5=round, 6=wide

### Text Options

```
text TEXT [--color white] [--bg black] [--speed 100] [--step 2] [--size 12] [--font unifont] [--loop 3]
```

- `--size`: Font size 8-16 (uses Unifont pixel font by default)
- `--font`: Font name (unifont, stheiti, hiragino, gothic, arial)
- `--speed`: Scroll speed in ms per step
- `--step`: Pixels to scroll per step (1-8)
- `--loop`: Loop count, 0 = infinite

### Prepare / Send Workflow

Compose multi-segment animations by staging frames:

```bash
python3 tivoo_macos.py prepare clear
python3 tivoo_macos.py prepare preset heart --duration 2000
python3 tivoo_macos.py prepare text "Hello World"
python3 tivoo_macos.py prepare image photo.png --duration 3000
python3 tivoo_macos.py send                    # Sends all staged frames
python3 tivoo_macos.py send --loop 0           # Infinite loop
python3 tivoo_macos.py send my_anim.json       # Reuse saved stage file
```

### Colors

Predefined: red, green, blue, white, black, yellow, purple, cyan, orange, pink

Custom: `#RRGGBB` format (e.g. `#FF6600`)

## Direct Pixel Art Generation

When the user wants custom patterns, generate pixel data inline:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from tivoo_macos import build_image_frame, send_cmd

B = (0, 0, 0)        # background
R = (255, 0, 0)      # foreground

# 16x16 pixel array, 16 rows of 16 (R,G,B) tuples
pixels = [
    [B,B,B,R,R,B,B,B,B,B,R,R,B,B,B,B],
    # ... 16 rows total
]

frame = build_image_frame(pixels, timecode=0)
payload = [0x44, 0x00, 0x0A, 0x0A, 0x04] + frame
send_cmd(*payload)
```

Or use preset patterns:

```bash
python3 scripts/tivoo_macos.py preset heart      # Heart
python3 scripts/tivoo_macos.py preset working    # Workflow
python3 scripts/tivoo_macos.py preset happy      # Emotion
```

## Protocol Extension

For building new commands, see [protocol-reference.md](protocol-reference.md) for the full protocol documentation.

Quick reference for raw commands:

| Code | Function | Parameters | Example |
|------|----------|------------|---------|
| `0x74` | Brightness | `[0-100]` | `raw 74 32` (50%) |
| `0x45` | View mode | See protocol docs | `raw 45 00 00` (clock) |
| `0x46` | Request status | None | `raw 46` |
| `0x44` | Send image | Pixel data | See code |
| `0x49` | Send animation | Frame data | See code |

## Notes

- Device uses classic Bluetooth RFCOMM (not BLE); must be paired in system Bluetooth first
- Each command opens a new connection; wait at least 1 second between commands
- Multiple commands in sequence use session mode to keep connection open
- macOS only (depends on IOBluetooth framework)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection failed | Check Bluetooth is on and device is paired |
| Connection timeout | Ensure device is in range, try restarting device Bluetooth |
| tivoo_cmd not found | Run compile command, or run `python3 tivoo_macos.py` to auto-compile |
| Bluetooth permission | System Settings > Privacy & Security > Bluetooth > Allow terminal |
| Compilation failed | Install Xcode CLI Tools: `xcode-select --install` |
