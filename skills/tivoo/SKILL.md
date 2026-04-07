---
name: tivoo
description: "Use when the user wants to control a Divoom Tivoo pixel screen - adjust brightness, display images, show animations, set clock mode, change light color, generate pixel art, or send raw Bluetooth commands to the device"
---

# Tivoo Pixel Screen Control

Control a Divoom Tivoo 16x16 pixel screen via Bluetooth.

## First-Time Setup

Check if `TIVOO_DIR` env var or `~/.tivoo/` directory exists to determine if setup is complete.

### 1. Determine Install Directory

Default: `~/.tivoo/`. Override with `TIVOO_DIR` env var.

```bash
mkdir -p ~/.tivoo
```

### 2. Copy Source Files

Copy files from the `scripts/` directory to the install directory:

```bash
cp scripts/tivoo_macos.py ~/.tivoo/
cp scripts/tivoo_cmd.m ~/.tivoo/
cp scripts/presets.py ~/.tivoo/
cp -r scripts/fonts ~/.tivoo/
```

### 3. Compile Bluetooth Tool

The user must compile `tivoo_cmd` locally (binaries are not distributed for security):

```bash
cd ~/.tivoo
clang -framework Foundation -framework IOBluetooth -o tivoo_cmd tivoo_cmd.m -fobjc-arc
```

Requires Xcode Command Line Tools. If not installed: `xcode-select --install`

### 4. Configure Device MAC Address

Default MAC is hardcoded as `11:75:58:8C:5B:0C`. For a different Tivoo device, edit the address in `tivoo_cmd.m` and recompile.

### 5. Install Python Dependencies

```bash
pip3 install click          # CLI framework (required)
pip3 install Pillow         # Image/animation/text (recommended)
pip3 install anthropic      # AI pixel art (optional)
```

### 6. macOS Bluetooth Permissions

On first run, macOS will prompt for Bluetooth access. Allow your terminal app (Terminal/iTerm/Warp) to access Bluetooth.

Check in: System Settings > Privacy & Security > Bluetooth

## Tool Path

After installation, the tool is at `~/.tivoo/tivoo_macos.py`:

```bash
TIVOO="${TIVOO_DIR:-$HOME/.tivoo}/tivoo_macos.py"
python3 "$TIVOO" <command>
```

## Command Reference

| Command | Example | Description |
|---------|---------|-------------|
| `brightness <0-100>` | `brightness 50` | Set brightness |
| `clock [style] [opts]` | `clock 1 --calendar` | Clock mode (style 0-6) |
| `light <color>` | `light #FF6600` | Light effect color |
| `off` / `on` | `off` | Turn screen off/on |
| `image <path>` | `image cat.png` | Send image (--duration 12) |
| `text <text>` | `text Hello` | Scrolling text (--loop 3) |
| `anim <dir\|gif>` | `anim frames/` | Send animation (--loop 3) |
| `preset <name>` | `preset heart` | Preset pixel art (--duration 12) |
| `ai <prompt>` | `ai "a cat"` | AI-generated pixel art |
| `ai-anim <prompt>` | `ai-anim "fire"` | AI-generated animation |
| `raw <hex...>` | `raw 74 64` | Raw hex command |
| `prepare <sub>` | `prepare preset heart` | Stage animation frames |
| `send [file]` | `send` | Send staged frames (--loop 3) |

All commands support `-h` / `--help` for detailed options.

### Auto-Restore Clock

By default, static commands (`image`, `preset`) display for 12 seconds then restore clock mode (`clock 1 --calendar`). Animation commands (`text`, `anim`, `send`) loop 3 times then restore.

Use `--duration 0` or `--loop 0` for permanent display (no auto-restore).

### Clock Options

```
clock [STYLE] [--12h] [--weather] [--temp] [--calendar] [--color COLOR]
```

Styles: 0=fullscreen, 1=rainbow, 2=boxed, 3=square, 4=fullscreen-inv, 5=round, 6=wide

### Text Options

```
text TEXT [--color white] [--bg black] [--speed 100] [--step 2] [--size 12] [--loop 3]
```

- `--size`: Font size 8-16 (uses Unifont pixel font)
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
sys.path.insert(0, os.path.expanduser("~/.tivoo"))
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
python3 ~/.tivoo/tivoo_macos.py preset heart      # Heart
python3 ~/.tivoo/tivoo_macos.py preset smiley     # Smiley
python3 ~/.tivoo/tivoo_macos.py preset gradient   # Gradient test
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
