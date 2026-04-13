# Tivoo Control

Control a [Divoom Tivoo](https://divoom.com) 16x16 pixel screen from macOS via Bluetooth RFCOMM.

## Features

- **Brightness, clock, light effects** — basic device control
- **Images** — send any PNG/JPG/GIF, auto-resized to 16x16 (configurable resample algorithm)
- **Scrolling text** — with Unifont pixel font, supports CJK characters, configurable font/size/speed, custom font file
- **Animations** — from image directories or GIF files
- **33 animated presets** — pixel art with multi-frame animations (heart, weather, animals, workflow icons, etc.)
- **24 emotion presets** — animated face expressions (happy, sad, angry, love, workflow emotions, etc.)
- **Character presets** — Claude (orange logo), Luna (magic girl) emotion sets via `--load`
- **AI pixel art** — generate pixel art via Claude CLI, Anthropic API, or OpenAI API with extended thinking
- **AI animation** — generate multi-frame animations, supports first-frame input
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

# Optional: AI pixel art providers
pip3 install anthropic      # Anthropic API
pip3 install openai         # OpenAI API

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
python3 tivoo_macos.py preset happy --load luna
python3 tivoo_macos.py preset happy --load claude

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
| `image <path>` | Display image (--duration 12s, --resample) |
| `text <text>` | Scrolling text (--loop, --speed, --size, --font, --font-file, --step) |
| `anim <path>` | Animation from directory or GIF (--loop, --delay) |
| `preset [name]` | Preset pixel art (--duration 12s, --load; no args = list all) |
| `ai <prompt>` | AI-generated pixel art (--provider, --no-thinking) |
| `ai-anim <prompt>` | AI-generated animation (--frames, --first-frame, --provider, --no-thinking) |
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
# Apply default hooks (7 events: Stop, StopFailure, Notification, PermissionRequest, Elicitation, TeammateIdle, UserPromptSubmit)
./hooks/configure-claude-hooks.sh

# English TTS
./hooks/configure-claude-hooks.sh --lang en

# Enable all 13 events
./hooks/configure-claude-hooks.sh --all
```

## Protocol

See [protocol-reference.md](skills/tivoo/protocol-reference.md) for the full Divoom Bluetooth protocol documentation.

## License

MIT
