# Tivoo Control

Control a [Divoom Tivoo](https://divoom.com) 16x16 pixel screen from macOS via Bluetooth RFCOMM.

## Features

- **Brightness, clock, light effects** — basic device control
- **Images** — send any PNG/JPG/GIF, auto-resized to 16x16
- **Scrolling text** — with Unifont pixel font, supports CJK characters, configurable font/size/speed
- **Animations** — from image directories or GIF files
- **39 animated presets** — pixel art with multi-frame animations (heart, weather, animals, workflow icons, etc.)
- **13 emotion presets** — animated face expressions (happy, sad, angry, love, etc.)
- **Custom preset loading** — load external preset files via `--load`
- **AI pixel art** — generate pixel art via Claude CLI or Anthropic API
- **Compose animations** — stage multiple segments (preset + text + image) and send as one animation
- **Auto-restore clock** — display content for a set duration/loops, then switch back to clock mode
- **Claude Code hooks** — show Tivoo animations on Claude Code events (task done, errors, notifications)

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

# Emotion presets
python3 tivoo_macos.py preset happy
python3 tivoo_macos.py preset happy --load emotion_presets_luna.py

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
| `text <text>` | Scrolling text (--loop, --speed, --size, --font, --step) |
| `anim <path>` | Animation from directory or GIF (--loop 3, --delay) |
| `preset [name]` | Preset pixel art (--duration 12s, --load; no args = list all) |
| `ai <prompt>` | AI-generated pixel art |
| `prepare <sub>` | Stage animation: `preset`, `text`, `image`, `clear`, `info` |
| `send [file]` | Send staged animation (--loop 3, --clean) |
| `raw <hex...>` | Send raw Bluetooth command |

## Configuration

Set the `TIVOO_MAC` environment variable to your device's Bluetooth MAC address:

```bash
export TIVOO_MAC="AA:BB:CC:DD:EE:FF"
```

Default: `11:75:58:8C:5B:0C`. The MAC is passed to `tivoo_cmd` via the `-a` flag.

## Claude Code Skill

The `skills/tivoo/` directory contains a [Claude Code](https://claude.ai/code) skill that lets Claude control the Tivoo directly in conversation. See [SKILL.md](skills/tivoo/SKILL.md) for setup instructions.

## Claude Code Hooks

The `hooks/` directory contains a configuration script to show Tivoo animations on Claude Code events. See [hooks/README.md](hooks/README.md) for details.

```bash
# Apply default hooks (6 events: Stop, StopFailure, Notification, PermissionRequest, Elicitation, TeammateIdle)
./hooks/configure-hooks.sh

# English TTS
./hooks/configure-hooks.sh --lang en

# Enable all 13 events
./hooks/configure-hooks.sh --all
```

## Protocol

See [protocol-reference.md](skills/tivoo/protocol-reference.md) for the full Divoom Bluetooth protocol documentation.

## License

MIT
