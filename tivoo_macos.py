#!/usr/bin/env python3
"""
Tivoo Control Script

Control a Divoom Tivoo 16x16 pixel screen via Bluetooth RFCOMM.
Uses compiled tivoo_cmd binary to send RFCOMM commands.

Configuration:
    Set TIVOO_MAC environment variable to your device's Bluetooth MAC address.
    Default: 11:75:58:8C:5B:0C

Usage:
    python3 tivoo_macos.py brightness 50           # Set brightness 0-100
    python3 tivoo_macos.py clock                   # Clock mode
    python3 tivoo_macos.py light red               # Light effect
    python3 tivoo_macos.py image photo.png         # Send image
    python3 tivoo_macos.py text Hello              # Scrolling text
    python3 tivoo_macos.py anim frames/            # Send animation
    python3 tivoo_macos.py preset heart            # Animated preset
    python3 tivoo_macos.py preset working          # Workflow animation
    python3 tivoo_macos.py preset happy            # Emotion animation
    python3 tivoo_macos.py preset happy --load luna
    python3 tivoo_macos.py ai "a cat"              # AI-generated pixel art
    python3 tivoo_macos.py raw 74 64               # Raw hex command
"""
import subprocess
import sys
import os
import math
import time
import json
import importlib.util

import click

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TIVOO_CMD = os.path.join(SCRIPT_DIR, "tivoo_cmd")
DEVICE_MAC = os.environ.get("TIVOO_MAC", "11:75:58:8C:5B:0C")
SCREEN_SIZE = 16
ANIM_CHUNK_SIZE = 200
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.local.json")

_DEFAULT_CONFIG = {
    "default": "clock 1",
    "ai": {
        "provider": "claude-cli",
        "api_url": None,
        "api_key": None,
        "model": None,
    },
}


def _load_config():
    """Load config from config.local.json, filling missing fields with defaults."""
    config = dict(_DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            user = json.load(f)
        for k, v in user.items():
            if k == "ai" and isinstance(v, dict):
                config["ai"] = {**_DEFAULT_CONFIG["ai"], **v}
            else:
                config[k] = v
    return config

COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 255),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0),
    "pink": (255, 105, 180),
}


LOG_FILE = os.path.join(SCRIPT_DIR, "tivoo.log")
AI_ART_DIR = os.path.join(SCRIPT_DIR, "ai_art")

FONTS = {
    "arial": ["/Library/Fonts/Arial Unicode.ttf"],
    "unifont": [
        os.path.join(SCRIPT_DIR, "fonts", "unifont.otf"),
    ],
    "stheiti": ["/System/Library/Fonts/STHeiti Medium.ttc"],
    "hiragino": ["/System/Library/Fonts/Hiragino Sans GB.ttc"],
    "gothic": ["/System/Library/Fonts/AppleSDGothicNeo.ttc"],
}
FONT_NAMES = list(FONTS.keys())


# --- Communication Layer ---

def _log(msg):
    """Write to log file."""
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")


def _run_tivoo_cmd(args, timeout=15):
    """
    Run tivoo_cmd and parse output.
    Returns (success: bool, lines: list[str]).
    """
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        print("  Connection timed out")
        return False, []
    except FileNotFoundError:
        print(f"  Not found: {args[0]}")
        return False, []

    success = True
    lines = []
    for line in result.stderr.split("\n"):
        if "TX:" in line:
            parts = line.split("TX:")
            if len(parts) > 1:
                msg = f"TX: {parts[1].strip()}"
                _log(msg)
                lines.append(msg)
        elif "RX:" in line:
            parts = line.split("RX:")
            if len(parts) > 1:
                msg = f"RX: {parts[1].strip()}"
                _log(msg)
                lines.append(msg)
        elif "FAIL" in line:
            print("  Connection failed")
            success = False
    return success, lines


def send_cmd(*hex_bytes):
    """Send a single command."""
    args = [TIVOO_CMD, "-a", DEVICE_MAC] + [
        f"{b:02x}" if isinstance(b, int) else str(b) for b in hex_bytes
    ]
    ok, _ = _run_tivoo_cmd(args)
    return ok


def send_session(payloads, timeout=30):
    """
    Session mode: keep connection open, send multiple payloads.
    payloads: list of list[int], each is a payload byte list.
    """
    args = [TIVOO_CMD, "-a", DEVICE_MAC, "-s"]
    for i, payload in enumerate(payloads):
        if i > 0:
            args.append("--")
        for b in payload:
            args.append(f"{b:02x}")

    ok, _ = _run_tivoo_cmd(args, timeout=timeout)
    return ok


def _restore_clock():
    """Switch back to default clock (style 1)."""
    time.sleep(1)
    r, g, b = parse_color("white")
    send_cmd(0x45, 0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, r, g, b)


def _wait_and_restore(duration_s):
    """Fork a background process to wait then restore clock. Returns immediately."""
    if duration_s <= 0:
        return
    pid = os.fork()
    if pid == 0:
        # Child process: detach, wait, restore, exit
        os.setsid()
        time.sleep(duration_s)
        _restore_clock()
        os._exit(0)
    else:
        print(f"  Will restore clock in {duration_s:.1f}s (background)")



# --- Color Utilities ---

def parse_color(color):
    """
    Parse color: name or #RRGGBB -> (R, G, B).
    Supports: red, green, blue, white, black, yellow, purple, cyan, orange, pink, #RRGGBB
    """
    if isinstance(color, (tuple, list)) and len(color) == 3:
        return tuple(color)
    if isinstance(color, str):
        color = color.strip()
        if color.startswith("#") and len(color) == 7:
            return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
        name = color.lower()
        if name in COLORS:
            return COLORS[name]
        print(f"  Unknown color: {color}, using white")
    return (255, 255, 255)


# --- Image Encoding ---

def encode_image(pixels_2d):
    """
    Encode 16x16 RGB pixel array to Divoom protocol format.
    pixels_2d: list[list[(R,G,B)]], 16x16 2D array
    Returns: (num_colors, palette_bytes, pixel_bytes)
    """
    colors = []
    pixels = []
    for row in pixels_2d:
        for r, g, b in row:
            color = (r & 0xFF, g & 0xFF, b & 0xFF)
            if color not in colors:
                colors.append(color)
            pixels.append(colors.index(color))

    palette = []
    for r, g, b in colors:
        palette.extend([r, g, b])

    num_colors = len(colors)
    if num_colors <= 1:
        return (num_colors if num_colors > 0 else 1,
                palette if palette else [0, 0, 0],
                [0] * 32)

    bits_per_pixel = max(1, math.ceil(math.log2(num_colors)))

    bit_string = ""
    for p in pixels:
        reversed_bits = format(p, '08b')[::-1]
        bit_string += reversed_bits[:bits_per_pixel]

    remainder = len(bit_string) % 8
    if remainder:
        bit_string += '0' * (8 - remainder)

    pixel_bytes = []
    for i in range(0, len(bit_string), 8):
        chunk = bit_string[i:i + 8]
        pixel_bytes.append(int(chunk[::-1], 2))

    return (num_colors, palette, pixel_bytes)


def build_image_frame(pixels_2d, timecode=0):
    """
    Build a single image frame (without 0x44 prefix).
    Returns: byte list.
    """
    num_colors, palette, pixel_data = encode_image(pixels_2d)

    frame_content = []
    frame_content.extend([timecode & 0xFF, (timecode >> 8) & 0xFF])
    frame_content.append(0x00)  # palette flag: reset
    frame_content.append(num_colors & 0xFF)  # 0 = 256
    frame_content.extend(palette)
    frame_content.extend(pixel_data)

    frame_size = len(frame_content) + 3
    frame = [0xAA]
    frame.extend([frame_size & 0xFF, (frame_size >> 8) & 0xFF])
    frame.extend(frame_content)
    return frame


RESAMPLE_METHODS = ["nearest", "lanczos", "bilinear"]


def _get_resample(name):
    from PIL import Image
    return {"nearest": Image.NEAREST, "lanczos": Image.LANCZOS, "bilinear": Image.BILINEAR}.get(name, Image.LANCZOS)


def image_file_to_pixels(path, resample="lanczos"):
    """Load image file and resize to 16x16, return pixel 2D array."""
    from PIL import Image

    img = Image.open(path).convert("RGBA")
    img = img.resize((SCREEN_SIZE, SCREEN_SIZE), _get_resample(resample))

    pixels = []
    for y in range(SCREEN_SIZE):
        row = []
        for x in range(SCREEN_SIZE):
            r, g, b, a = img.getpixel((x, y))
            row.append((0, 0, 0) if a < 32 else (r, g, b))
        pixels.append(row)
    return pixels


def solid_pixels(r, g, b):
    """Generate solid color 16x16 pixel array."""
    return [[(r, g, b)] * SCREEN_SIZE for _ in range(SCREEN_SIZE)]


# --- Basic Commands ---

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Tivoo macOS pixel screen control tool."""
    if not ensure_compiled():
        raise SystemExit(1)


@cli.command()
@click.argument("value", type=click.IntRange(0, 100))
def brightness(value):
    """Set brightness (0-100)."""
    print(f"Setting brightness: {value}%")
    send_cmd(0x74, value)


@cli.command()
@click.argument("style", type=click.IntRange(0, 15), default=0)
@click.option("--12h", "twelve_hour", is_flag=True, help="Use 12-hour format")
@click.option("--weather", is_flag=True, help="Show weather")
@click.option("--temp", is_flag=True, help="Show temperature")
@click.option("--calendar", is_flag=True, help="Show calendar")
@click.option("--color", default="white", help="Color name or #RRGGBB")
def clock(style, twelve_hour, weather, temp, calendar, color):
    """Switch to clock mode.

    Styles: 0=fullscreen, 1=rainbow, 2=boxed, 3=square, 4=fullscreen-inv, 5=round, 6=wide
    """
    r, g, b = parse_color(color)
    twentyfour = not twelve_hour
    print(f"Clock mode (style {style}, {'24' if twentyfour else '12'}h)")
    send_cmd(
        0x45, 0x00,
        0x01 if twentyfour else 0x00,
        style & 0x0F, 0x01,
        0x01 if weather else 0x00,
        0x01 if temp else 0x00,
        0x01 if calendar else 0x00,
        r, g, b,
    )


@cli.command()
@click.argument("color")
def light(color):
    """Set light effect color (name or #RRGGBB)."""
    r, g, b = parse_color(color)
    print(f"Light effect: RGB({r}, {g}, {b})")
    send_cmd(0x45, 0x01, r, g, b, 0x64, 0x00, 0x01, 0x00, 0x00, 0x00)


@cli.command()
@click.option("-n", "--count", default=5, help="Number of flashes")
def flash(count):
    """Flash test."""
    print(f"Flash test ({count}x)")
    for i in range(count):
        print(f"  [{i + 1}/{count}]")
        send_cmd(0x74, 0x00)
        time.sleep(0.4)
        send_cmd(0x74, 0x64)
        time.sleep(0.4)
    print("  Done")


@cli.command()
def status():
    """Query device status."""
    ok, lines = _run_tivoo_cmd([TIVOO_CMD, "-a", DEVICE_MAC, "46"])
    if not ok:
        return

    # Find the status response (command 0x46)
    for line in lines:
        if not line.startswith("RX:"):
            continue
        hex_str = line[3:].strip()
        raw = bytes(int(b, 16) for b in hex_str.split())
        # Packet: 01 [len_lo len_hi] 04 46 [payload...] [crc_lo crc_hi] 02
        if len(raw) < 7 or raw[4] != 0x46:
            continue
        # Payload starts after "04 46 55" = indices 5 onward (0x55 is response marker)
        d = raw[6:]  # skip 01 len_lo len_hi 04 46 55
        if len(d) < 21:
            continue

        CLOCK_STYLES = {
            0: "fullscreen", 1: "rainbow", 2: "boxed", 3: "square",
            4: "fullscreen-inv", 5: "round", 6: "wide",
        }
        mode_names = {0: "clock", 1: "light"}
        mode = d[0]
        r1, g1, b1 = d[3], d[4], d[5]
        brightness = d[6]
        fmt_24h = d[8]
        r2, g2, b2 = d[12], d[13], d[14]
        style = d[15]
        temp = d[16]
        weather = d[17]
        calendar = d[19]

        print(f"  Mode:       {mode_names.get(mode, f'unknown({mode})')}")
        print(f"  Brightness: {brightness}%")
        print(f"  Clock:      style {style} ({CLOCK_STYLES.get(style, '?')}), {'24h' if fmt_24h else '12h'}")
        print(f"  Color:      RGB({r2}, {g2}, {b2})")
        flags = []
        if weather: flags.append("weather")
        if temp: flags.append("temp")
        if calendar: flags.append("calendar")
        print(f"  Display:    {', '.join(flags) if flags else 'none'}")
        return

    print("  No status response received")


@cli.command()
def off():
    """Turn off screen."""
    print("Screen off")
    send_cmd(0x74, 0x00)


@cli.command()
def on():
    """Turn on screen."""
    print("Screen on")
    send_cmd(0x74, 0x64)


# --- Image Command ---

@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--duration", default=12, type=int, help="Display seconds (0=forever)")
@click.option("--resample", default="lanczos", type=click.Choice(RESAMPLE_METHODS, case_sensitive=False), help="Resize algorithm")
def image(path, duration, resample):
    """Send image file to Tivoo (PNG/JPG/GIF)."""
    print(f"Sending image: {path}")
    pixels = image_file_to_pixels(path, resample=resample)
    frame = build_image_frame(pixels, timecode=0)
    payload = [0x44, 0x00, 0x0A, 0x0A, 0x04] + frame
    if send_cmd(*payload):
        print("  Sent")
    _wait_and_restore(duration)


# --- Text Command ---

@cli.command()
@click.argument("text")
@click.option("--color", default="white", help="Text color")
@click.option("--bg", default="black", help="Background color")
@click.option("--speed", default=100, type=int, help="Scroll speed (ms/step)")
@click.option("--step", default=2, type=click.IntRange(1, 8), help="Pixels per scroll step")
@click.option("--size", default=None, type=click.IntRange(8, 16), help="Font size (auto: 9=EN, 12=CJK)")
@click.option("--font", default=None, type=click.Choice(FONT_NAMES, case_sensitive=False), help="Font name")
@click.option("--font-file", default=None, type=click.Path(exists=True), help="Custom font file path")
@click.option("--loop", default=5, type=int, help="Loop count (0=infinite)")
def text(text, color, bg, speed, step, size, font, font_file, loop):
    """Display scrolling text."""
    print(f"Generating text animation: \"{text}\"")
    frames, delays = _gen_text_frames(text, color, bg, speed, step, font_size=size, font_name=font, font_file=font_file)
    print(f"  {len(frames)} frames, step {step}px, speed {speed}ms/step")
    duration_ms = _send_animation(frames, speed, delays)
    _wait_and_restore(duration_ms * loop / 1000 if loop > 0 else 0)


# --- Animation Command ---

@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-d", "--delay", default=200, type=int, help="Frame delay (ms)")
@click.option("--loop", default=5, type=int, help="Loop count (0=infinite)")
@click.option("--resample", default="lanczos", type=click.Choice(RESAMPLE_METHODS, case_sensitive=False), help="Resize algorithm")
def anim(path, delay, loop, resample):
    """Send animation (image directory or GIF file)."""
    from PIL import Image
    method = _get_resample(resample)

    frames = []
    per_frame_delays = []

    if os.path.isdir(path):
        files = sorted([
            f for f in os.listdir(path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ])
        if not files:
            print(f"No images in directory: {path}")
            return

        print(f"Loading animation frames ({len(files)} images)")
        for f in files:
            img = Image.open(os.path.join(path, f)).convert("RGBA")
            img = img.resize((SCREEN_SIZE, SCREEN_SIZE), method)
            frame = []
            for y in range(SCREEN_SIZE):
                row = []
                for x in range(SCREEN_SIZE):
                    r, g, b, a = img.getpixel((x, y))
                    row.append((r, g, b) if a >= 32 else (0, 0, 0))
                frame.append(row)
            frames.append(frame)
            per_frame_delays.append(delay)

    elif path.lower().endswith('.gif'):
        print("Loading GIF animation")
        gif = Image.open(path)
        n_frames = getattr(gif, 'n_frames', 1)

        for i in range(n_frames):
            gif.seek(i)
            img = gif.convert("RGBA").resize(
                (SCREEN_SIZE, SCREEN_SIZE), method
            )
            frame = []
            for y in range(SCREEN_SIZE):
                row = []
                for x in range(SCREEN_SIZE):
                    r, g, b, a = img.getpixel((x, y))
                    row.append((r, g, b) if a >= 32 else (0, 0, 0))
                frame.append(row)
            frames.append(frame)
            per_frame_delays.append(delay)
    else:
        print(f"Unsupported path: {path}")
        return

    if not frames:
        print("No usable frames")
        return

    print(f"  {len(frames)} frames")
    duration_ms = _send_animation(frames, delay, per_frame_delays)
    _wait_and_restore(duration_ms * loop / 1000 if loop > 0 else 0)


def _send_animation(frames, default_delay_ms, per_frame_delays=None):
    """Encode frames to Divoom animation protocol and send. Returns single-loop duration (ms)."""
    all_frame_data = []
    total_duration_ms = 0

    for i, frame_pixels in enumerate(frames):
        d = per_frame_delays[i] if per_frame_delays and i < len(per_frame_delays) else default_delay_ms
        total_duration_ms += d
        # timecode = per-frame display duration (not cumulative absolute time)
        frame = build_image_frame(frame_pixels, timecode=d)
        all_frame_data.extend(frame)

    total_size = len(all_frame_data)
    num_chunks = math.ceil(total_size / ANIM_CHUNK_SIZE)

    print(f"  Animation data: {total_size} bytes, {num_chunks} chunks")

    payloads = []
    for i in range(num_chunks):
        start = i * ANIM_CHUNK_SIZE
        end = start + ANIM_CHUNK_SIZE
        chunk = all_frame_data[start:end]
        payload = [
            0x49,
            total_size & 0xFF,
            (total_size >> 8) & 0xFF,
            i,
        ] + chunk
        payloads.append(payload)

    send_session(payloads)
    print("  Animation sent")
    return total_duration_ms


# --- AI Pixel Art ---

def _auto_save_path(prompt, ext="png"):
    """Generate auto save path: ai_art/<timestamp>_<prompt>.<ext>"""
    from datetime import datetime
    os.makedirs(AI_ART_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize prompt for filename: take first 30 chars, replace non-alnum
    safe = "".join(c if c.isalnum() or c in "-_ " else "" for c in prompt[:30]).strip().replace(" ", "_")
    return os.path.join(AI_ART_DIR, f"{ts}_{safe}.{ext}")


_AI_SYSTEM_IMAGE = (
    "You are a pixel art artist. Generate a 16x16 pixel image based on the user's description. "
    "Use a palette-indexed format to keep output compact. "
    "Output ONLY a JSON object with:\n"
    '  "palette": {"0": [R,G,B], "1": [R,G,B], ...} — up to 36 colors (keys: 0-9, a-z)\n'
    '  "pixels": ["0123456789abcdef", ...] — 16 strings of 16 chars each, referencing palette keys\n'
    "Use \"0\" for black background [0,0,0]. Use vivid colors. Keep art clean and recognizable."
)

_AI_SYSTEM_ANIM = (
    "You are a pixel animation artist. Generate a {n}-frame 16x16 pixel animation. "
    "Use a palette-indexed format to keep output compact. "
    "Output ONLY a JSON object with:\n"
    '  "palette": {{"0": [R,G,B], "1": [R,G,B], ...}} — up to 36 colors (keys: 0-9, a-z)\n'
    '  "frames": [["0123...", ...16 rows...], ...{n} frames...] — each frame is 16 strings of 16 chars\n'
    "Use \"0\" for black background [0,0,0]. Use vivid colors. "
    "Animation should be smooth with small changes between frames."
)


@cli.command()
@click.argument("prompt")
@click.option("--save", default=None, type=click.Path(), help="Save pixel art to PNG file (default: auto)")
@click.option("--provider", default=None, type=click.Choice(["claude-cli", "anthropic", "openai"], case_sensitive=False), help="AI provider")
@click.option("--no-thinking", is_flag=True, default=False, help="Disable extended thinking")
def ai(prompt, save, provider, no_thinking):
    """AI-generate 16x16 pixel art and send."""
    print(f"AI pixel art: \"{prompt}\"")

    system_msg = _AI_SYSTEM_IMAGE

    print(f"  System: {system_msg[:80]}...")
    print(f"  Requesting AI...")

    json_str = _call_ai(system_msg, prompt, provider=provider, max_tokens=16384, thinking=not no_thinking)
    if not json_str:
        print("  AI generation failed")
        return

    pixels = _parse_palette_image(json_str)
    if not pixels:
        print(f"  Raw response (first 200 chars): {json_str[:200]}")
        return

    print("  Pixel art ready, sending to Tivoo...")
    _preview_ascii(pixels)
    save_path = save or _auto_save_path(prompt, "png")
    _save_pixels_png(pixels, save_path)
    frame = build_image_frame(pixels, timecode=0)
    payload = [0x44, 0x00, 0x0A, 0x0A, 0x04] + frame
    send_cmd(*payload)
    print("  Sent")


@cli.command("ai-anim")
@click.argument("prompt")
@click.option("-n", "--frames", default=4, type=int, help="Number of frames")
@click.option("-d", "--delay", default=200, type=int, help="Frame delay (ms)")
@click.option("--first-frame", default=None, type=click.Path(exists=True), help="Image file for the first frame")
@click.option("--save", default=None, type=click.Path(), help="Save animation as GIF file (default: auto)")
@click.option("--provider", default=None, type=click.Choice(["claude-cli", "anthropic", "openai"], case_sensitive=False), help="AI provider")
@click.option("--no-thinking", is_flag=True, default=False, help="Disable extended thinking")
def ai_anim(prompt, frames, delay, first_frame, save, provider, no_thinking):
    """AI-generate pixel animation and send."""
    first_frame_pixels = None
    if first_frame:
        first_frame_pixels = image_file_to_pixels(first_frame)
        gen_frames = frames - 1
        print(f"AI pixel animation: \"{prompt}\" (1 given + {gen_frames} generated)")
    else:
        gen_frames = frames
        print(f"AI pixel animation: \"{prompt}\" ({frames} frames)")

    system_msg = _AI_SYSTEM_ANIM.format(n=gen_frames)

    user_msg = prompt
    if first_frame_pixels:
        pal_str, rows_str = _pixels_to_palette_text(first_frame_pixels)
        user_msg = (
            f"{prompt}\n\n"
            f"Here is the first frame (use the same palette and style):\n"
            f"palette: {pal_str}\n"
            f"pixels:\n{rows_str}\n\n"
            f"Generate {gen_frames} more frames continuing from this frame."
        )

    print(f"  System: {system_msg[:80]}...")
    print(f"  Requesting AI...")

    # Per frame: ~1K output + ~1K thinking overhead
    max_tokens = 16384 + gen_frames * 2048
    json_str = _call_ai(system_msg, user_msg, provider=provider, max_tokens=max_tokens, thinking=not no_thinking)
    if not json_str:
        print("  AI generation failed")
        return

    clean_frames = _parse_palette_anim(json_str)
    if not clean_frames:
        print(f"  Raw response (first 200 chars): {json_str[:200]}")
        return

    # Prepend first frame if provided
    if first_frame_pixels:
        clean_frames = [first_frame_pixels] + clean_frames

    print(f"  Generated {len(clean_frames)} frames, sending animation...")
    for i, f in enumerate(clean_frames):
        _preview_ascii(f, label=f"Frame {i+1}/{len(clean_frames)}")
    save_path = save or _auto_save_path(prompt, "gif")
    _save_frames_gif(clean_frames, delay, save_path)
    _send_animation(clean_frames, delay)


@cli.command()
@click.argument("hex_bytes", nargs=-1, required=True)
def raw(hex_bytes):
    """Send raw hex command."""
    print(f"Raw command: {' '.join(hex_bytes)}")
    send_cmd(*hex_bytes)


def _resolve_load_path(name):
    """Resolve --load shorthand to file path.

    'default' → built-in (no file needed)
    'luna' → emotion_presets_luna.py
    'claude' → emotion_presets_claude.py
    Other → treat as file path directly
    """
    if name == "default":
        return None
    # Check shorthand: name → presets/emotion_presets_{name}.py
    shorthand = os.path.join(os.path.dirname(__file__) or ".", "presets", f"emotion_presets_{name}.py")
    if os.path.exists(shorthand):
        return shorthand
    # Treat as direct file path
    if os.path.exists(name):
        return name
    raise click.BadParameter(f"Cannot find preset '{name}' (tried {shorthand} and {name})")


def _load_from_files(paths):
    """Load presets from external .py files. Returns (presets, emotions, hidden)."""
    presets, emotions, hidden = {}, {}, set()
    for p in paths:
        resolved = _resolve_load_path(p)
        if resolved is None:
            continue  # 'default' — skip, built-in already loaded
        spec = importlib.util.spec_from_file_location("custom", os.path.abspath(resolved))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        presets.update(getattr(mod, "PRESETS", {}))
        emotions.update(getattr(mod, "EMOTIONS", {}))
        hidden.update(getattr(mod, "HIDDEN_EMOTIONS", set()))
    return presets, emotions, hidden


def _load_all_presets(load_files=None):
    """Load built-in + custom presets. Returns (presets, emotions)."""
    from presets.presets import PRESETS
    from presets.emotion_presets import EMOTION_PRESETS as EP

    presets = dict(PRESETS)
    emotions = dict(EP)
    hidden = set()

    if load_files:
        cp, ce, ch = _load_from_files(load_files)
        presets.update(cp)
        emotions.update(ce)
        hidden.update(ch)

    return presets, emotions, hidden


@cli.command()
@click.argument("name", required=False)
@click.option("--duration", default=12, type=int, help="Display seconds (0=forever)")
@click.option("--loop", default=5, type=int, help="Loop count for animations (0=infinite)")
@click.option("--load", "load_files", multiple=True, help="Load preset set: luna, claude, or file path")
@click.option("--restore", "restore_cmd", default=None, help="Tivoo command to run after loops finish (e.g. 'preset standby --loop 0 --load claude')")
def preset(name, duration, loop, load_files, restore_cmd):
    """Send preset pixel art pattern.

    Run without arguments to list all presets.
    Use --load to add custom presets from .py files.
    Use --restore to auto-run another command after loops finish.
    """
    presets, emotions, hidden = _load_all_presets(load_files or None)
    all_presets = {**presets, **emotions}

    if not name:
        print("Available presets:\n")
        print("  Presets:")
        for key, (desc, _) in presets.items():
            print(f"    {key:14s}  {desc}")
        print(f"\n  Emotions:")
        for key, (desc, _) in emotions.items():
            if key not in hidden:
                print(f"    {key:14s}  {desc}")
        return

    if name not in all_presets:
        print(f"Unknown preset: {name}")
        print(f"Available: {', '.join(k for k in all_presets if k not in hidden)}")
        return

    desc, func = all_presets[name]
    print(f"Sending preset: {desc}")
    frames, delays = func()

    print(f"  {len(frames)} frame(s)")
    duration_ms = _send_animation(frames, delays[0], delays)

    if restore_cmd and loop > 0:
        import shlex
        total_wait = duration_ms * loop / 1000
        restore_args = shlex.split(restore_cmd)
        pid = os.fork()
        if pid == 0:
            os.setsid()
            time.sleep(total_wait)
            subprocess.run([sys.executable, __file__] + restore_args,
                           stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os._exit(0)
        else:
            print(f"  Will run '{restore_cmd}' in {total_wait:.1f}s (background)")
    else:
        _wait_and_restore(duration_ms * loop / 1000 if loop > 0 else 0)


def _parse_json_response(json_str):
    """Clean and parse AI-returned JSON."""
    json_str = json_str.strip()
    # Strip markdown code fences
    if json_str.startswith("```"):
        json_str = json_str.split("\n", 1)[1]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    json_str = json_str.strip()
    # Try direct parse first
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    # Try to extract the outermost JSON array
    start = json_str.find("[")
    if start == -1:
        print("  JSON parse failed: no array found")
        return None
    depth = 0
    end = start
    for i in range(start, len(json_str)):
        if json_str[i] == "[":
            depth += 1
        elif json_str[i] == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    try:
        return json.loads(json_str[start:end])
    except json.JSONDecodeError as e:
        print(f"  JSON parse failed: {e}")
        return None


def _clean_frame(frame):
    """Validate and clean a single frame, return None if invalid."""
    if len(frame) != SCREEN_SIZE:
        return None
    clean = []
    for row in frame:
        if len(row) != SCREEN_SIZE:
            return None
        clean.append([
            (max(0, min(255, int(px[0]))),
             max(0, min(255, int(px[1]))),
             max(0, min(255, int(px[2]))))
            for px in row
        ])
    return clean


def _expand_palette_frame(palette, rows):
    """Convert palette-indexed rows to RGB pixel frame."""
    frame = []
    for row_str in rows:
        row = []
        for ch in str(row_str)[:SCREEN_SIZE]:
            rgb = palette.get(ch, [0, 0, 0])
            row.append((max(0, min(255, int(rgb[0]))),
                        max(0, min(255, int(rgb[1]))),
                        max(0, min(255, int(rgb[2])))))
        # Pad if short
        while len(row) < SCREEN_SIZE:
            row.append((0, 0, 0))
        frame.append(row)
    # Pad rows if short
    while len(frame) < SCREEN_SIZE:
        frame.append([(0, 0, 0)] * SCREEN_SIZE)
    return frame


def _parse_palette_image(json_str):
    """Parse palette-indexed single image. Returns pixel frame or None."""
    data = _parse_json_response(json_str)
    if not isinstance(data, dict):
        return None
    palette = data.get("palette")
    rows = data.get("pixels")
    if not palette or not rows:
        return None
    print(f"  Palette: {len(palette)} colors")
    return _expand_palette_frame(palette, rows)


def _parse_palette_anim(json_str):
    """Parse palette-indexed animation. Returns list of pixel frames or None."""
    data = _parse_json_response(json_str)
    if not isinstance(data, dict):
        return None
    palette = data.get("palette")
    frames_data = data.get("frames")
    if not palette or not frames_data:
        return None
    print(f"  Palette: {len(palette)} colors, {len(frames_data)} frames")
    result = []
    for rows in frames_data:
        if isinstance(rows, list) and len(rows) > 0:
            result.append(_expand_palette_frame(palette, rows))
    return result if result else None


def _pixels_to_palette_text(pixels):
    """Convert 16x16 RGB pixel frame to palette-indexed text for AI prompt.
    Returns (palette_str, rows_str) suitable for embedding in a prompt."""
    keys = "0123456789abcdefghijklmnopqrstuvwxyz"
    color_to_key = {}
    palette = {}
    rows = []
    for row in pixels:
        row_str = ""
        for r, g, b in row:
            color = (r, g, b)
            if color not in color_to_key:
                idx = len(color_to_key)
                if idx < len(keys):
                    k = keys[idx]
                else:
                    # Too many colors — find nearest existing
                    k = min(color_to_key, key=lambda c: sum((a - b) ** 2 for a, b in zip(c, color)))
                    k = color_to_key[k]
                color_to_key[color] = k
                palette[k] = list(color)
            row_str += color_to_key[color]
        rows.append(row_str)
    pal_str = ", ".join(f'"{k}": [{v[0]},{v[1]},{v[2]}]' for k, v in sorted(palette.items()))
    rows_str = "\n".join(f'  "{r}"' for r in rows)
    return f'{{{pal_str}}}', rows_str


    """Parse AI-generated single-frame pixel JSON."""
    data = _parse_json_response(json_str)
    if data is None:
        return None

    if len(data) != SCREEN_SIZE:
        print(f"  Wrong row count: {len(data)} (need {SCREEN_SIZE})")
        return None

    cleaned = _clean_frame(data)
    if cleaned is None:
        print(f"  Wrong column count (need {SCREEN_SIZE})")
        return None
    return cleaned


def _save_pixels_png(pixels, path, scale=16):
    """Save 16x16 pixel art to PNG, scaled up for visibility."""
    from PIL import Image
    size = len(pixels)
    img = Image.new("RGB", (size * scale, size * scale))
    for y in range(size):
        for x in range(size):
            r, g, b = pixels[y][x]
            for dy in range(scale):
                for dx in range(scale):
                    img.putpixel((x * scale + dx, y * scale + dy), (r, g, b))
    img.save(path)
    print(f"  Saved to {path} ({size * scale}x{size * scale})")


def _save_frames_gif(frames, delay_ms, path, scale=16):
    """Save animation frames as GIF, scaled up for visibility."""
    from PIL import Image
    size = len(frames[0])
    imgs = []
    for pixels in frames:
        img = Image.new("RGB", (size * scale, size * scale))
        for y in range(size):
            for x in range(size):
                r, g, b = pixels[y][x]
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((x * scale + dx, y * scale + dy), (r, g, b))
        imgs.append(img)
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=delay_ms, loop=0)
    print(f"  Saved to {path} ({len(imgs)} frames, {size * scale}x{size * scale})")


def _call_ai(system_msg, user_msg, provider=None, max_tokens=4096, thinking=True):
    """Call AI model based on config.local.json provider setting."""
    config = _load_config()
    ai = config["ai"]
    provider = provider or ai["provider"]
    print(f"  Provider: {provider}")
    print(f"  Prompt: {user_msg}")

    if provider == "claude-cli":
        print("  Model: claude (CLI default)")
        try:
            result = subprocess.run(
                ["claude", "--print", "-p", user_msg, "--system-prompt", system_msg],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0 and result.stdout.strip():
                resp = result.stdout.strip()
                print(f"  Response: {len(resp)} chars")
                return resp
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        print("  Claude CLI not available. Install: https://claude.ai/code")
        return None

    elif provider == "anthropic":
        try:
            import anthropic
            api_key = ai["api_key"] or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
            if not api_key:
                print("  No API key: set ai.api_key in config or ANTHROPIC_API_KEY env")
                return None
            kwargs = {"api_key": api_key}
            base_url = ai["api_url"] or os.environ.get("ANTHROPIC_BASE_URL")
            if base_url:
                kwargs["base_url"] = base_url
                print(f"  API URL: {base_url}")
            client = anthropic.Anthropic(**kwargs)
            model = ai["model"] or os.environ.get("ANTHROPIC_MODEL") or "claude-sonnet-4-20250514"
            print(f"  Model: {model}")
            create_kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "system": system_msg,
                "messages": [{"role": "user", "content": user_msg}],
            }
            if thinking:
                thinking_budget = max(max_tokens - 4096, 1024)
                create_kwargs["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
                print(f"  Max tokens: {max_tokens} (thinking {thinking_budget} + output {max_tokens - thinking_budget})")
            else:
                print(f"  Max tokens: {max_tokens}")
            response = client.messages.create(**create_kwargs, stream=True)
            # Stream response with spinner
            resp_parts = []
            thinking_chars = 0
            input_tokens = 0
            output_tokens = 0
            stop = None
            current_type = None
            spin_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
            spin_idx = 0
            import sys
            for event in response:
                if event.type == "message_start":
                    input_tokens = getattr(event.message.usage, "input_tokens", 0)
                elif event.type == "content_block_start":
                    current_type = event.content_block.type
                    if current_type == "thinking":
                        sys.stdout.write(f"\r  {spin_chars[0]} Thinking...")
                        sys.stdout.flush()
                    elif current_type == "text":
                        sys.stdout.write(f"\r  {spin_chars[0]} Generating...    ")
                        sys.stdout.flush()
                        spin_idx = 0
                elif event.type == "content_block_delta":
                    spin_idx = (spin_idx + 1) % len(spin_chars)
                    if current_type == "thinking":
                        t = getattr(event.delta, "thinking", "")
                        if t:
                            thinking_chars += len(t)
                        sys.stdout.write(f"\r  {spin_chars[spin_idx]} Thinking...")
                        sys.stdout.flush()
                    elif current_type == "text":
                        text = getattr(event.delta, "text", "")
                        if text:
                            resp_parts.append(text)
                        sys.stdout.write(f"\r  {spin_chars[spin_idx]} Generating...")
                        sys.stdout.flush()
                elif event.type == "message_delta":
                    stop = event.delta.stop_reason
                    output_tokens = getattr(event.usage, "output_tokens", 0)
            sys.stdout.write("\r                        \r")
            sys.stdout.flush()
            resp = "".join(resp_parts)
            if not resp:
                print("  ERROR: no text in response")
                return None
            usage_str = f"{input_tokens}in/{output_tokens}out"
            if thinking_chars:
                usage_str += f", thinking ~{thinking_chars} chars"
            print(f"  Response: {len(resp)} chars, stop: {stop}, usage: {usage_str}")
            if stop == "max_tokens":
                print("  WARNING: response truncated (max_tokens reached)")
            return resp
        except ImportError:
            print("  anthropic SDK not installed: pip3 install anthropic")
            return None

    elif provider == "openai":
        try:
            import openai
            api_key = ai["api_key"] or os.environ.get("OPENAI_API_KEY")
            if not api_key:
                print("  No API key: set ai.api_key in config or OPENAI_API_KEY env")
                return None
            kwargs = {"api_key": api_key}
            base_url = ai["api_url"] or os.environ.get("OPENAI_BASE_URL")
            if base_url:
                kwargs["base_url"] = base_url
                print(f"  API URL: {base_url}")
            client = openai.OpenAI(**kwargs)
            model = ai["model"] or os.environ.get("OPENAI_MODEL") or "gpt-4o"
            print(f"  Model: {model}")
            create_kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
            }
            if thinking:
                create_kwargs["max_completion_tokens"] = max_tokens
                create_kwargs["reasoning_effort"] = "high"
                print(f"  Max tokens: {max_tokens} (thinking + output)")
            else:
                create_kwargs["max_tokens"] = max_tokens
                print(f"  Max tokens: {max_tokens}")

            import sys, time, threading
            resp_parts = []
            reasoning_parts = []
            input_tokens = 0
            output_tokens = 0
            reasoning_tokens = 0
            stop = None

            # Background spinner — start BEFORE API call because create() may block during thinking
            spin_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
            spin_state = {"phase": "Thinking" if thinking else "Generating", "done": False}
            def _spin():
                idx = 0
                while not spin_state["done"]:
                    sys.stdout.write(f"\r  {spin_chars[idx]} {spin_state['phase']}...")
                    sys.stdout.flush()
                    idx = (idx + 1) % len(spin_chars)
                    time.sleep(0.15)
            t = threading.Thread(target=_spin, daemon=True)
            t.start()

            response = client.chat.completions.create(**create_kwargs, stream=True, stream_options={"include_usage": True})
            for chunk in response:
                if chunk.usage:
                    input_tokens = chunk.usage.prompt_tokens or 0
                    output_tokens = chunk.usage.completion_tokens or 0
                    details = getattr(chunk.usage, "completion_tokens_details", None)
                    if details:
                        reasoning_tokens = getattr(details, "reasoning_tokens", 0) or 0
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                finish = chunk.choices[0].finish_reason
                if finish:
                    stop = finish
                if delta and getattr(delta, "reasoning_content", None):
                    spin_state["phase"] = "Thinking"
                    reasoning_parts.append(delta.reasoning_content)
                elif delta and delta.content:
                    spin_state["phase"] = "Generating"
                    resp_parts.append(delta.content)

            spin_state["done"] = True
            t.join(timeout=1)
            sys.stdout.write("\r                        \r")
            sys.stdout.flush()
            resp = "".join(resp_parts)
            if not resp:
                print("  ERROR: no text in response")
                return None
            usage_str = f"{input_tokens}in/{output_tokens}out"
            if reasoning_tokens:
                usage_str += f"/{reasoning_tokens}think"
            elif reasoning_parts:
                usage_str += f", thinking ~{sum(len(p) for p in reasoning_parts)} chars"
            print(f"  Response: {len(resp)} chars, stop: {stop}, usage: {usage_str}")
            if stop == "length":
                print("  WARNING: response truncated (max_tokens reached)")
            return resp
        except ImportError:
            print("  openai SDK not installed: pip3 install openai")
            return None

    else:
        print(f"  Unknown AI provider: {provider}")
        print("  Supported: claude-cli, anthropic, openai")
        return None


def _preview_ascii(pixels, label=None):
    """Print ASCII preview of pixel art."""
    if label:
        print(f"  [{label}]")
    for row in pixels:
        line = ""
        for r, g, b in row:
            brightness = (r + g + b) / 3
            if brightness > 200:
                line += "##"
            elif brightness > 100:
                line += "++"
            elif brightness > 50:
                line += ".."
            else:
                line += "  "
        print(f"  {line}")


# --- Frame Generation (shared by prepare and direct commands) ---

STAGE_FILE = os.path.join(SCRIPT_DIR, ".tivoo_stage.json")


def _load_font(size=16, name=None, font_file=None):
    """Load pixel font by name or file path. Default: tries all fonts in order."""
    from PIL import ImageFont
    if font_file:
        try:
            return ImageFont.truetype(font_file, size)
        except Exception as e:
            print(f"Cannot load font file '{font_file}': {e}")
            sys.exit(1)
    if name:
        paths = FONTS.get(name)
        if not paths:
            print(f"Unknown font '{name}'. Available: {', '.join(FONT_NAMES)}")
            sys.exit(1)
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
        print(f"Font '{name}' not found on this system.")
        sys.exit(1)
    # Default: try all fonts in order
    for paths in FONTS.values():
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _has_cjk(text):
    """Check if text contains CJK characters."""
    for ch in text:
        cp = ord(ch)
        if (0x4E00 <= cp <= 0x9FFF or    # CJK Unified
            0x3400 <= cp <= 0x4DBF or    # CJK Extension A
            0x3000 <= cp <= 0x303F or    # CJK Symbols
            0x3040 <= cp <= 0x309F or    # Hiragana
            0x30A0 <= cp <= 0x30FF or    # Katakana
            0xAC00 <= cp <= 0xD7AF):     # Hangul
            return True
    return False


def _auto_font_size(text):
    """Auto-select font size: 12 for CJK text, 9 for ASCII-only."""
    return 12 if _has_cjk(text) else 9


def _gen_static_frames(pixels, duration_ms):
    """Generate a single frame for static content.

    Only 1 frame needed; timecode controls display duration.
    """
    return [pixels], [duration_ms]


def _gen_text_frames(text, color="white", bg="black", speed=100, step=2, font_size=None, font_name=None, font_file=None):
    """Generate scrolling text frames. Returns (frames, delays)."""
    from PIL import Image, ImageDraw
    fg = parse_color(color)
    bg_rgb = parse_color(bg)
    if font_size is None:
        font_size = _auto_font_size(text)
    font = _load_font(font_size, font_name, font_file=font_file)

    tmp = Image.new("1", (1, 1))
    bbox = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img_width = text_width + SCREEN_SIZE * 2
    # 1-bit rendering: no antialiasing, crisp pixels
    mask = Image.new("1", (img_width, SCREEN_SIZE), 0)
    draw = ImageDraw.Draw(mask)
    y_offset = max(0, (SCREEN_SIZE - text_height) // 2 - bbox[1])
    draw.text((SCREEN_SIZE, y_offset), text, fill=1, font=font)

    frames = []
    for x in range(0, img_width - SCREEN_SIZE, step):
        frame_pixels = []
        for row_y in range(SCREEN_SIZE):
            row = []
            for col_x in range(SCREEN_SIZE):
                row.append(fg if mask.getpixel((col_x + x, row_y)) else bg_rgb)
            frame_pixels.append(row)
        frames.append(frame_pixels)

    return frames, [speed] * len(frames)


def _load_stage(path):
    """Load stage file."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"frames": [], "delays": []}


def _save_stage(path, data):
    """Save stage file."""
    with open(path, "w") as f:
        json.dump(data, f)


# --- Prepare Command Group ---

@cli.group()
def prepare():
    """Prepare animation frames (append to stage file, use 'send' to transmit)."""
    pass


@prepare.command("preset")
@click.argument("name")
@click.option("--duration", default=2000, type=int, help="Duration (ms)")
@click.option("--load", "load_files", multiple=True, help="Load preset set: luna, claude, or file path")
@click.option("-o", "--output", default=None, help="Stage file path")
def prepare_preset(name, duration, load_files, output):
    """Append preset pattern frames."""
    presets, emotions, _hidden = _load_all_presets(load_files or None)
    all_presets = {**presets, **emotions}
    if name not in all_presets:
        print(f"Unknown preset: {name}")
        return

    path = output or STAGE_FILE
    stage = _load_stage(path)

    desc, func = all_presets[name]
    frames, delays = func()

    stage["frames"].extend(frames)
    stage["delays"].extend(delays)
    _save_stage(path, stage)
    print(f"Appended: {desc} ({len(frames)} frame(s)) -> {os.path.basename(path)}")


@prepare.command("text")
@click.argument("text")
@click.option("--color", default="white", help="Text color")
@click.option("--bg", default="black", help="Background color")
@click.option("--speed", default=100, type=int, help="Scroll speed (ms/step)")
@click.option("--step", default=2, type=click.IntRange(1, 8), help="Pixels per step")
@click.option("--size", default=None, type=click.IntRange(8, 16), help="Font size (auto: 9=EN, 12=CJK)")
@click.option("--font", default=None, type=click.Choice(FONT_NAMES, case_sensitive=False), help="Font name")
@click.option("--font-file", default=None, type=click.Path(exists=True), help="Custom font file path")
@click.option("-o", "--output", default=None, help="Stage file path")
def prepare_text(text, color, bg, speed, step, size, font, font_file, output):
    """Append scrolling text frames."""
    path = output or STAGE_FILE
    stage = _load_stage(path)

    frames, delays = _gen_text_frames(text, color, bg, speed, step, font_size=size, font_name=font, font_file=font_file)

    stage["frames"].extend(frames)
    stage["delays"].extend(delays)
    _save_stage(path, stage)
    print(f"Appended: \"{text}\" ({len(frames)} frames) -> {os.path.basename(path)}")


@prepare.command("image")
@click.argument("path", type=click.Path(exists=True))
@click.option("--duration", default=2000, type=int, help="Duration (ms)")
@click.option("-o", "--output", default=None, help="Stage file path")
def prepare_image(path, duration, output):
    """Append image frames."""
    out = output or STAGE_FILE
    stage = _load_stage(out)

    pixels = image_file_to_pixels(path)
    frames, delays = _gen_static_frames(pixels, duration)

    stage["frames"].extend(frames)
    stage["delays"].extend(delays)
    _save_stage(out, stage)
    print(f"Appended: {os.path.basename(path)} ({len(frames)} frame, {duration}ms) -> {os.path.basename(out)}")


@prepare.command("clear")
@click.option("-o", "--output", default=None, help="Stage file path")
def prepare_clear(output):
    """Clear stage file."""
    path = output or STAGE_FILE
    _save_stage(path, {"frames": [], "delays": []})
    print(f"Cleared: {os.path.basename(path)}")


@prepare.command("info")
@click.option("-o", "--output", default=None, help="Stage file path")
def prepare_info(output):
    """Show stage file info."""
    path = output or STAGE_FILE
    stage = _load_stage(path)
    n = len(stage["frames"])
    total_ms = sum(stage["delays"]) if stage["delays"] else 0
    print(f"Stage: {n} frames, total {total_ms}ms ({total_ms/1000:.1f}s)")


# --- Send Command ---

@cli.command()
@click.argument("file", default=None, required=False, type=click.Path())
@click.option("--clean", is_flag=True, help="Delete stage file after sending")
@click.option("--loop", default=5, type=int, help="Loop count (0=infinite)")
def send(file, clean, loop):
    """Send staged animation frames.

    Optionally specify a file path; defaults to the built-in stage file.
    Files are kept by default for reuse.
    """
    path = file or STAGE_FILE
    stage = _load_stage(path)

    if not stage["frames"]:
        print("Stage is empty, use 'prepare' to add content first")
        return

    frames = [[list(row) for row in frame] for frame in stage["frames"]]
    delays = stage["delays"]

    print(f"Sending {len(frames)} frames, total {sum(delays)}ms ({sum(delays)/1000:.1f}s)")
    duration_ms = _send_animation(frames, delays[0] if delays else 100, delays)

    if clean:
        os.remove(path)
        print("  Stage file cleaned")

    _wait_and_restore(duration_ms * loop / 1000 if loop > 0 else 0)


def ensure_compiled():
    """Ensure tivoo_cmd is compiled."""
    if os.path.exists(TIVOO_CMD):
        return True
    src = os.path.join(SCRIPT_DIR, "tivoo_cmd.m")
    if not os.path.exists(src):
        click.echo("tivoo_cmd.m source not found")
        return False
    click.echo("tivoo_cmd not found, compiling...")
    result = subprocess.run(
        ["clang", "-framework", "Foundation", "-framework", "IOBluetooth",
         "-o", TIVOO_CMD, src, "-fobjc-arc"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        click.echo(f"Compilation failed: {result.stderr}")
        return False
    return True


def _save_config(config):
    """Save config to config.local.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


@cli.command("default", context_settings=dict(
    ignore_unknown_options=True, allow_extra_args=True,
))
@click.argument("args", nargs=-1)
def set_default(args):
    """Get or set the default standby command.

    \b
    Examples:
        tivoo default                              # Show current default
        tivoo default clock 1                      # Set default to clock style 1
        tivoo default preset standby --load claude  # Set default to preset
    """
    config = _load_config()

    if not args:
        print(f"Current default: {config['default']}")
        return

    cmd_str = " ".join(args)
    config["default"] = cmd_str
    _save_config(config)
    print(f"Default set to: {cmd_str}")


def _run_default():
    """Execute the default command from config."""
    import shlex
    config = _load_config()
    cmd_str = config["default"]
    parts = shlex.split(cmd_str)
    if not parts:
        return

    subcmd = parts[0]
    sub_args = parts[1:]

    if subcmd == "clock":
        # Invoke clock command
        ctx = click.Context(clock)
        ctx.invoke(clock, **_parse_clock_args(sub_args))
    elif subcmd == "preset":
        # Invoke preset command with loop=0 (infinite)
        if not sub_args:
            print("  Default preset: no name specified")
            return
        name = sub_args[0]
        load_files = []
        i = 1
        while i < len(sub_args):
            if sub_args[i] == "--load" and i + 1 < len(sub_args):
                load_files.append(sub_args[i + 1])
                i += 2
            else:
                i += 1
        presets, emotions = _load_all_presets(load_files or None)
        all_presets = {**presets, **emotions}
        if name not in all_presets:
            print(f"  Unknown preset: {name}")
            return
        desc, func = all_presets[name]
        print(f"Default: {desc} (loop=infinite)")
        frames, delays = func()
        _send_animation(frames, delays[0], delays)
    else:
        print(f"  Unknown default command: {subcmd}")


def _parse_clock_args(args):
    """Parse clock sub-args into kwargs."""
    kwargs = {"style": 0, "twelve_hour": False, "weather": False,
              "temp": False, "calendar": False, "color": "white"}
    i = 0
    while i < len(args):
        if args[i] == "--12h":
            kwargs["twelve_hour"] = True
        elif args[i] == "--weather":
            kwargs["weather"] = True
        elif args[i] == "--temp":
            kwargs["temp"] = True
        elif args[i] == "--calendar":
            kwargs["calendar"] = True
        elif args[i] == "--color" and i + 1 < len(args):
            kwargs["color"] = args[i + 1]
            i += 1
        else:
            try:
                kwargs["style"] = int(args[i])
            except ValueError:
                pass
        i += 1
    return kwargs


if __name__ == "__main__":
    cli()
