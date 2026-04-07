#!/usr/bin/env python3
"""
Tivoo macOS Control Script

Control a Divoom Tivoo 16x16 pixel screen via macOS IOBluetooth framework.
Uses compiled tivoo_cmd binary to send RFCOMM commands.

Usage:
    python3 tivoo_macos.py brightness 50        # Set brightness 0-100
    python3 tivoo_macos.py clock                # Clock mode
    python3 tivoo_macos.py light red            # Light effect
    python3 tivoo_macos.py image photo.png      # Send image
    python3 tivoo_macos.py text Hello           # Scrolling text
    python3 tivoo_macos.py anim frames/         # Send animation
    python3 tivoo_macos.py preset heart         # Preset pixel art
    python3 tivoo_macos.py ai "a cat"           # AI-generated pixel art
    python3 tivoo_macos.py raw 74 64            # Raw hex command
"""
import subprocess
import sys
import os
import math
import time
import json

import click

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TIVOO_CMD = os.path.join(SCRIPT_DIR, "tivoo_cmd")
SCREEN_SIZE = 16
ANIM_CHUNK_SIZE = 200

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
    args = [TIVOO_CMD] + [
        f"{b:02x}" if isinstance(b, int) else str(b) for b in hex_bytes
    ]
    ok, _ = _run_tivoo_cmd(args)
    return ok


def send_session(payloads, timeout=30):
    """
    Session mode: keep connection open, send multiple payloads.
    payloads: list of list[int], each is a payload byte list.
    """
    args = [TIVOO_CMD, "-s"]
    for i, payload in enumerate(payloads):
        if i > 0:
            args.append("--")
        for b in payload:
            args.append(f"{b:02x}")

    ok, _ = _run_tivoo_cmd(args, timeout=timeout)
    return ok


def _restore_clock():
    """Switch back to default clock (style 1, calendar on)."""
    time.sleep(1)
    r, g, b = parse_color("white")
    print("  Restoring clock mode")
    send_cmd(0x45, 0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x01, r, g, b)


def _wait_and_restore(duration_s):
    """Wait then restore clock. duration_s=0 means stay forever."""
    if duration_s <= 0:
        return
    print(f"  Waiting {duration_s:.1f}s before restoring clock...")
    time.sleep(duration_s)
    _restore_clock()


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


def image_file_to_pixels(path):
    """Load image file and resize to 16x16, return pixel 2D array."""
    from PIL import Image

    img = Image.open(path).convert("RGBA")
    img = img.resize((SCREEN_SIZE, SCREEN_SIZE), Image.LANCZOS)

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
    print("Requesting device status")
    send_cmd(0x46)


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
def image(path, duration):
    """Send image file to Tivoo (PNG/JPG/GIF)."""
    print(f"Sending image: {path}")
    pixels = image_file_to_pixels(path)
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
@click.option("--size", default=12, type=click.IntRange(8, 16), help="Font size (8-16)")
@click.option("--loop", default=3, type=int, help="Loop count (0=infinite)")
def text(text, color, bg, speed, step, size, loop):
    """Display scrolling text."""
    print(f"Generating text animation: \"{text}\"")
    frames, delays = _gen_text_frames(text, color, bg, speed, step, font_size=size)
    print(f"  {len(frames)} frames, step {step}px, speed {speed}ms/step")
    duration_ms = _send_animation(frames, speed, delays)
    _wait_and_restore(duration_ms * loop / 1000 if loop > 0 else 0)


# --- Animation Command ---

@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-d", "--delay", default=100, type=int, help="Frame delay (ms)")
@click.option("--loop", default=3, type=int, help="Loop count (0=infinite)")
def anim(path, delay, loop):
    """Send animation (image directory or GIF file)."""
    from PIL import Image

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
            img = img.resize((SCREEN_SIZE, SCREEN_SIZE), Image.LANCZOS)
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
                (SCREEN_SIZE, SCREEN_SIZE), Image.LANCZOS
            )
            frame = []
            for y in range(SCREEN_SIZE):
                row = []
                for x in range(SCREEN_SIZE):
                    r, g, b, a = img.getpixel((x, y))
                    row.append((r, g, b) if a >= 32 else (0, 0, 0))
                frame.append(row)
            frames.append(frame)
            per_frame_delays.append(gif.info.get('duration', delay))
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

@cli.command()
@click.argument("prompt")
def ai(prompt):
    """AI-generate 16x16 pixel art and send."""
    print(f"AI pixel art: \"{prompt}\"")
    print("  Requesting AI...")

    system_msg = (
        "You are a pixel art artist. Based on the user's description, generate a 16x16 pixel image. "
        "Output a JSON array with 16 rows, each containing 16 [R,G,B] color values. "
        "Output ONLY JSON, nothing else. "
        "Color values 0-255. Use black [0,0,0] for background. "
        "Keep the art clean and use vivid colors."
    )

    json_str = _call_ai(system_msg, prompt)
    if not json_str:
        print("  AI generation failed")
        return

    pixels = _parse_pixel_json(json_str)
    if not pixels:
        return

    print("  Pixel art ready, sending to Tivoo...")
    _preview_ascii(pixels)
    frame = build_image_frame(pixels, timecode=0)
    payload = [0x44, 0x00, 0x0A, 0x0A, 0x04] + frame
    send_cmd(*payload)
    print("  Sent")


@cli.command("ai-anim")
@click.argument("prompt")
@click.option("-n", "--frames", default=10, type=int, help="Number of frames")
@click.option("-d", "--delay", default=100, type=int, help="Frame delay (ms)")
def ai_anim(prompt, frames, delay):
    """AI-generate pixel animation and send."""
    print(f"AI pixel animation: \"{prompt}\" ({frames} frames)")

    system_msg = (
        f"You are a pixel animation artist. Based on the user's description, generate a {frames}-frame "
        "16x16 pixel animation. Output a JSON array of frames, each frame is 16 rows x 16 columns of "
        "[R,G,B] color arrays. Structure: [[[R,G,B], ...16...], ...16 rows...] per frame. "
        "Output ONLY JSON, nothing else. "
        "Color values 0-255. Use black [0,0,0] for background. "
        "Animation should be smooth with small changes between adjacent frames."
    )

    json_str = _call_ai(system_msg, prompt)
    if not json_str:
        print("  AI generation failed")
        return

    all_frames = _parse_json_response(json_str)
    if all_frames is None:
        return

    if not isinstance(all_frames, list) or len(all_frames) == 0:
        print("  Format error: expected frame array")
        return

    clean_frames = [f for f in (_clean_frame(frame) for frame in all_frames) if f]

    if not clean_frames:
        print("  No usable frames")
        return

    print(f"  Generated {len(clean_frames)} frames, sending animation...")
    _send_animation(clean_frames, delay)


@cli.command()
@click.argument("hex_bytes", nargs=-1, required=True)
def raw(hex_bytes):
    """Send raw hex command."""
    print(f"Raw command: {' '.join(hex_bytes)}")
    send_cmd(*hex_bytes)


@cli.command()
@click.argument("name", required=False)
@click.option("--duration", default=12, type=int, help="Display seconds (0=forever)")
def preset(name, duration):
    """Send preset pixel art pattern.

    Run without arguments to list all presets.
    """
    from presets import PRESETS

    if not name:
        print("Available presets:\n")
        for key, (desc, _) in PRESETS.items():
            print(f"  {key:12s}  {desc}")
        return

    if name not in PRESETS:
        print(f"Unknown preset: {name}")
        print(f"Available: {', '.join(PRESETS.keys())}")
        return

    desc, func = PRESETS[name]
    print(f"Sending preset: {desc}")
    pixels = func()
    _preview_ascii(pixels)
    frame = build_image_frame(pixels, timecode=0)
    payload = [0x44, 0x00, 0x0A, 0x0A, 0x04] + frame
    send_cmd(*payload)
    print("  Sent")
    _wait_and_restore(duration)


def _parse_json_response(json_str):
    """Clean and parse AI-returned JSON."""
    json_str = json_str.strip()
    if json_str.startswith("```"):
        json_str = json_str.split("\n", 1)[1]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    json_str = json_str.strip()
    try:
        return json.loads(json_str)
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


def _parse_pixel_json(json_str):
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


def _call_ai(system_msg, user_msg):
    """Try calling an AI model to generate content."""
    # Method 1: claude CLI
    try:
        result = subprocess.run(
            ["claude", "--print", "-p", user_msg, "--system-prompt", system_msg],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Method 2: anthropic SDK
    try:
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_msg,
            messages=[{"role": "user", "content": user_msg}],
        )
        return response.content[0].text
    except ImportError:
        pass
    except Exception:
        pass

    print("  No AI backend available:")
    print("    Option 1: Install Claude CLI (https://claude.ai/code)")
    print("    Option 2: pip3 install anthropic && set ANTHROPIC_API_KEY")
    return None


def _preview_ascii(pixels):
    """Write ASCII preview of pixel art to log file."""
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
        _log(f"  {line}")


# --- Frame Generation (shared by prepare and direct commands) ---

STAGE_FILE = os.path.join(SCRIPT_DIR, ".tivoo_stage.json")


def _load_font(size=16):
    """Load pixel font (prefer Unifont for crisp 16x16 rendering)."""
    from PIL import ImageFont
    for font_path in [
        os.path.expanduser("~/.tivoo/fonts/unifont.otf"),
        os.path.join(SCRIPT_DIR, "fonts", "unifont.otf"),
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _gen_static_frames(pixels, duration_ms):
    """Generate a single frame for static content.

    Only 1 frame needed; timecode controls display duration.
    """
    return [pixels], [duration_ms]


def _gen_text_frames(text, color="white", bg="black", speed=100, step=2, font_size=12):
    """Generate scrolling text frames. Returns (frames, delays)."""
    from PIL import Image, ImageDraw
    fg = parse_color(color)
    bg_rgb = parse_color(bg)
    font = _load_font(font_size)

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
@click.option("-o", "--output", default=None, help="Stage file path")
def prepare_preset(name, duration, output):
    """Append preset pattern frames."""
    from presets import PRESETS
    if name not in PRESETS:
        print(f"Unknown preset: {name}")
        return

    path = output or STAGE_FILE
    stage = _load_stage(path)

    desc, func = PRESETS[name]
    pixels = func()
    frames, delays = _gen_static_frames(pixels, duration)

    stage["frames"].extend(frames)
    stage["delays"].extend(delays)
    _save_stage(path, stage)
    print(f"Appended: {desc} ({len(frames)} frame, {duration}ms) -> {os.path.basename(path)}")


@prepare.command("text")
@click.argument("text")
@click.option("--color", default="white", help="Text color")
@click.option("--bg", default="black", help="Background color")
@click.option("--speed", default=100, type=int, help="Scroll speed (ms/step)")
@click.option("--step", default=2, type=click.IntRange(1, 8), help="Pixels per step")
@click.option("--size", default=12, type=click.IntRange(8, 16), help="Font size (8-16)")
@click.option("-o", "--output", default=None, help="Stage file path")
def prepare_text(text, color, bg, speed, step, size, output):
    """Append scrolling text frames."""
    path = output or STAGE_FILE
    stage = _load_stage(path)

    frames, delays = _gen_text_frames(text, color, bg, speed, step, font_size=size)

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
@click.option("--loop", default=3, type=int, help="Loop count (0=infinite)")
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


if __name__ == "__main__":
    cli()
