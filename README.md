# Tivoo Control

Control a [Divoom Tivoo](https://divoom.com) 16x16 pixel screen from macOS via Bluetooth RFCOMM.

## Features

- **Brightness, clock, light effects** — basic device control
- **Images** — send any PNG/JPG/GIF, auto-resized to 16x16
- **Scrolling text** — with Unifont pixel font, supports CJK characters
- **Animations** — from image directories or GIF files
- **Preset pixel art** — 23 built-in patterns (heart, smiley, weather, animals, etc.)
- **AI pixel art** — generate pixel art via Claude CLI or Anthropic API
- **Compose animations** — stage multiple segments (preset + text + image) and send as one animation
- **Auto-restore clock** — display content for a set duration/loops, then switch back to clock mode

## Requirements

- macOS (uses IOBluetooth framework)
- Python 3 + [click](https://click.palletsprojects.com/)
- [Pillow](https://pillow.readthedocs.io/) (for image/text/animation features)
- Xcode Command Line Tools (for compiling the Bluetooth bridge)

## Quick Start

```bash
# Install dependencies
pip3 install click Pillow

# Compile Bluetooth bridge (one-time)
clang -framework Foundation -framework IOBluetooth -o tivoo_cmd tivoo_cmd.m -fobjc-arc

# Basic commands
python3 tivoo_macos.py brightness 50
python3 tivoo_macos.py clock 1
python3 tivoo_macos.py preset heart
python3 tivoo_macos.py text "Hello World" --color cyan
python3 tivoo_macos.py image photo.png

# Compose multi-segment animation
python3 tivoo_macos.py prepare clear
python3 tivoo_macos.py prepare preset star --duration 2000
python3 tivoo_macos.py prepare text "Hello!" --color yellow
python3 tivoo_macos.py send
```

## Commands

Run `python3 tivoo_macos.py -h` for full help. Every subcommand supports `-h`.

| Command | Description |
|---------|-------------|
| `brightness <0-100>` | Set screen brightness |
| `clock [style]` | Clock mode (styles 0-6, options: --calendar, --weather, --color) |
| `light <color>` | Light effect (color name or #RRGGBB) |
| `off` / `on` | Turn screen off/on |
| `image <path>` | Display image (--duration 12s, then restore clock) |
| `text <text>` | Scrolling text (--loop 3, --speed, --size 8-16, --font) |
| `anim <path>` | Animation from directory or GIF (--loop 3, --delay) |
| `preset [name]` | Preset pixel art (--duration 12s; no args = list all) |
| `ai <prompt>` | AI-generated pixel art |
| `prepare <sub>` | Stage animation: `preset`, `text`, `image`, `clear`, `info` |
| `send [file]` | Send staged animation (--loop 3, --clean) |
| `raw <hex...>` | Send raw Bluetooth command |

## Configuration

The device MAC address is hardcoded in `tivoo_cmd.m` line 130. Edit and recompile for a different device:

```objc
IOBluetoothDevice *dev = [IOBluetoothDevice deviceWithAddressString:@"11:75:58:8C:5B:0C"];
```

## Claude Code Skill

The `skills/tivoo/` directory contains a [Claude Code](https://claude.ai/code) skill that lets Claude control the Tivoo directly in conversation. See [SKILL.md](skills/tivoo/SKILL.md) for setup instructions.

## Protocol

See [protocol-reference.md](skills/tivoo/protocol-reference.md) for the full Divoom Bluetooth protocol documentation.

## License

MIT
