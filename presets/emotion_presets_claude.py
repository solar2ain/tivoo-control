"""
Claude Emotion Presets — Orange Claude character expressions for Tivoo 16x16.

Claude is a short, wide character with no mouth — emotions are conveyed
through eyes and effects only. 4 thin legs, 12-14 wide, 7 rows tall.

Usage: python3 tivoo_macos.py preset happy --load emotion_presets_claude.py
"""

# --- Colors ---

_BG = (0, 0, 0)
_ORANGE = (232, 140, 55)
_DARK_O = (200, 115, 40)
_BLACK = (40, 30, 20)
_WHITE = (255, 255, 255)
_RED = (255, 50, 50)
_PINK = (255, 140, 160)
_BLUE = (80, 150, 255)
_GREEN = (100, 200, 80)
_SICK_G = (140, 200, 80)
_PURPLE = (180, 100, 255)
_CYAN = (0, 220, 255)


# --- Base: short & wide Claude ---

_BODY = {
    4: (2, 13),
    5: (2, 13), 6: (2, 13), 7: (2, 13),
    8: (1, 14), 9: (1, 14), 10: (1, 14), 11: (2, 13),
}
_LEGS = [
    (12, 3), (12, 5), (12, 10), (12, 12),
    (13, 3), (13, 5), (13, 10), (13, 12),
]


def _empty():
    return [[_BG] * 16 for _ in range(16)]


def _claude_base(color=None):
    """Orange Claude body — compact rectangle + 4 thin legs."""
    p = _empty()
    c = color or _ORANGE
    for row, (s, e) in _BODY.items():
        for col in range(s, e + 1):
            p[row][col] = c
    for r, col in _LEGS:
        p[r][col] = c
    return p


def _claude_base_sick():
    """Green-tinted Claude for sick emoji."""
    return _claude_base(_SICK_G)


# --- Eyes ---

def _draw_eyes(p, style):
    """Draw eyes on Claude. No mouth — eyes carry the emotion."""
    if style == "open":
        for dy in (0, 1):
            for dx in (0, 1):
                p[6 + dy][4 + dx] = _BLACK
                p[6 + dy][10 + dx] = _BLACK
    elif style == "open_wide":
        # 2x3 rectangular eyes
        for dy in (0, 1):
            for dx in range(3):
                p[6 + dy][4 + dx] = _BLACK
                p[6 + dy][10 + dx] = _BLACK
    elif style == "squint":
        for dx in range(3):
            p[7][4 + dx] = _BLACK
            p[7][10 + dx] = _BLACK
    elif style == "closed":
        p[7][4] = _BLACK; p[7][5] = _BLACK; p[7][6] = _BLACK
        p[7][10] = _BLACK; p[7][11] = _BLACK; p[7][12] = _BLACK
    elif style == "half":
        p[7][4] = _BLACK; p[7][5] = _BLACK
        p[6][4] = _DARK_O; p[6][5] = _DARK_O
        p[7][10] = _BLACK; p[7][11] = _BLACK
        p[6][10] = _DARK_O; p[6][11] = _DARK_O
    elif style == "wide":
        for dy in range(3):
            for dx in range(3):
                p[5 + dy][4 + dx] = _WHITE
                p[5 + dy][9 + dx] = _WHITE
        p[6][5] = _BLACK
        p[6][10] = _BLACK
    elif style == "wider":
        for dy in range(3):
            for dx in range(3):
                p[5 + dy][3 + dx] = _WHITE
                p[5 + dy][9 + dx] = _WHITE
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = _BLACK
                p[5 + dy][10 + dx] = _BLACK
    elif style == "hearts":
        h = _RED
        # Left heart centered at col 5
        p[6][4] = h; p[6][6] = h
        p[7][4] = h; p[7][5] = h; p[7][6] = h
        p[8][5] = h
        # Right heart centered at col 10
        p[6][9] = h; p[6][11] = h
        p[7][9] = h; p[7][10] = h; p[7][11] = h
        p[8][10] = h
    elif style == "hearts_big":
        h = _RED
        w = _PINK
        # Left heart centered at col 5
        p[5][4] = h; p[5][6] = h
        p[6][3] = h; p[6][4] = w; p[6][5] = h; p[6][6] = w; p[6][7] = h
        p[7][4] = h; p[7][5] = h; p[7][6] = h
        p[8][5] = h
        # Right heart centered at col 10
        p[5][9] = h; p[5][11] = h
        p[6][8] = h; p[6][9] = w; p[6][10] = h; p[6][11] = w; p[6][12] = h
        p[7][9] = h; p[7][10] = h; p[7][11] = h
        p[8][10] = h
    elif style == "dizzy":
        p[6][4] = _BLACK; p[6][6] = _BLACK
        p[7][5] = _BLACK
        p[8][4] = _BLACK; p[8][6] = _BLACK
        p[6][9] = _BLACK; p[6][11] = _BLACK
        p[7][10] = _BLACK
        p[8][9] = _BLACK; p[8][11] = _BLACK
    elif style == "one_closed":
        for dy in (0, 1):
            for dx in (0, 1):
                p[6 + dy][4 + dx] = _BLACK
        p[7][10] = _BLACK; p[7][11] = _BLACK; p[7][12] = _BLACK
    elif style == "angry":
        # 2-row diagonal — outer high, inner low
        # Left eye
        p[6][3] = _BLACK; p[6][4] = _BLACK; p[6][5] = _BLACK
        p[7][4] = _BLACK; p[7][5] = _BLACK; p[7][6] = _BLACK
        # Right eye
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][12] = _BLACK
        p[7][9] = _BLACK; p[7][10] = _BLACK; p[7][11] = _BLACK
    elif style == "angry_deep":
        # Thicker 2-row diagonal
        p[5][3] = _BLACK; p[6][3] = _BLACK; p[6][4] = _BLACK; p[6][5] = _BLACK
        p[7][4] = _BLACK; p[7][5] = _BLACK; p[7][6] = _BLACK; p[8][6] = _BLACK
        p[5][12] = _BLACK; p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][12] = _BLACK
        p[7][9] = _BLACK; p[7][10] = _BLACK; p[7][11] = _BLACK; p[8][9] = _BLACK
    elif style == "lookup":
        # Eyes shifted up one row (thinking)
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = _BLACK
                p[5 + dy][10 + dx] = _BLACK


# --- Mouth (only for specific emotions) ---

def _draw_mouth(p, style):
    """Draw mouth in body area — most emotions don't use this."""
    if style == "smile":
        # Upward curve — corners high, center low
        p[9][5] = _BLACK; p[9][10] = _BLACK
        p[10][6] = _BLACK; p[10][7] = _BLACK; p[10][8] = _BLACK; p[10][9] = _BLACK
    elif style == "grin":
        # Wide grin with teeth
        p[9][5] = _BLACK; p[9][6] = _BLACK; p[9][7] = _BLACK
        p[9][8] = _BLACK; p[9][9] = _BLACK; p[9][10] = _BLACK
        p[9][6] = _WHITE; p[9][7] = _WHITE; p[9][8] = _WHITE; p[9][9] = _WHITE
        p[10][5] = _BLACK; p[10][6] = _BLACK; p[10][7] = _BLACK
        p[10][8] = _BLACK; p[10][9] = _BLACK; p[10][10] = _BLACK
    elif style == "laugh":
        for x in range(5, 11):
            p[9][x] = _BLACK
        p[10][5] = _BLACK; p[10][10] = _BLACK
        for x in range(6, 10):
            p[10][x] = _RED
    elif style == "open":
        p[9][7] = _BLACK; p[9][8] = _BLACK
        p[10][7] = _BLACK; p[10][8] = _BLACK
    elif style == "open_big":
        for x in range(6, 10):
            p[9][x] = _BLACK
        p[10][6] = _BLACK; p[10][9] = _BLACK
        p[10][7] = _RED; p[10][8] = _RED
    elif style == "wavy":
        # _--_ shape: middle stays level, sides droop down
        p[10][7] = _BLACK; p[10][8] = _BLACK
        p[11][6] = _BLACK; p[11][9] = _BLACK
    elif style == "flat":
        for x in range(6, 10):
            p[10][x] = _BLACK
    elif style == "kiss":
        p[9][7] = _RED; p[9][8] = _RED
        p[10][7] = _RED; p[10][8] = _RED


# --- Brows ---

def _draw_brows(p, style):
    """Draw eyebrows — only angry_deep fits the compact shape."""
    if style == "angry_deep":
        p[5][3] = _BLACK; p[5][4] = _BLACK; p[5][5] = _BLACK; p[6][6] = _BLACK
        p[5][12] = _BLACK; p[5][11] = _BLACK; p[5][10] = _BLACK; p[6][9] = _BLACK


# --- Effects ---

def _draw_tear(p, side="both", heavy=False):
    lb = _BLUE
    lw = (150, 200, 255)
    if side in ("left", "both"):
        p[8][4] = lb; p[9][4] = lb; p[10][4] = lb
        if heavy:
            p[11][4] = lb
            p[9][3] = lw; p[10][3] = lw
            p[9][5] = lw
    if side in ("right", "both"):
        p[8][12] = lb; p[9][12] = lb; p[10][12] = lb
        if heavy:
            p[11][12] = lb
            p[9][13] = lw; p[10][13] = lw
            p[9][11] = lw


def _draw_sweat(p, side="left"):
    if side == "left":
        p[4][1] = _BLUE; p[5][1] = _BLUE
    elif side == "both":
        p[4][1] = _BLUE; p[5][1] = _BLUE
        p[4][14] = _BLUE; p[5][14] = _BLUE


def _draw_zzz(p):
    z = _WHITE
    p[2][11] = z; p[2][12] = z; p[2][13] = z
    p[3][13] = z
    p[4][12] = z
    p[5][11] = z
    p[6][11] = z; p[6][12] = z; p[6][13] = z


def _draw_sunglasses(p):
    g = _BLACK
    b = (60, 60, 60)
    for x in range(3, 13):
        p[6][x] = g
    for dy in (0, 1):
        for dx in range(4):
            p[7 + dy][3 + dx] = b
            p[7 + dy][9 + dx] = b


def _draw_sunglasses_shine(p):
    _draw_sunglasses(p)
    p[7][4] = _WHITE; p[7][5] = _WHITE
    p[7][10] = _WHITE; p[7][11] = _WHITE


def _draw_exclaim(p):
    e = _RED
    p[2][14] = e; p[3][14] = e; p[4][14] = e
    p[6][14] = e


def _draw_dots(p, count=3):
    """Draw thinking dots above head."""
    d = _WHITE
    positions = [(2, 6), (2, 8), (2, 10)]
    for i in range(min(count, 3)):
        y, x = positions[i]
        p[y][x] = d


def _draw_code_tag(p, stage=1):
    """Draw </> code tag above head (rows 1-3). stage 1: <, 2: </, 3: </>"""
    c = _WHITE
    if stage >= 1:
        # < at cols 4-5
        p[1][5] = c
        p[2][4] = c
        p[3][5] = c
    if stage >= 2:
        # / at cols 7-8
        p[1][8] = c
        p[2][7] = c; p[2][8] = c
        p[3][7] = c
    if stage >= 3:
        # > at cols 10-11
        p[1][10] = c
        p[2][11] = c
        p[3][10] = c


def _draw_checkmark(p, y, x, color=None):
    """Draw small ✓ at position. 3x2 check shape."""
    c = color or _GREEN
    p[y + 1][x] = c
    p[y][x + 1] = c
    p[y + 1][x + 1] = c
    p[y][x + 2] = c


def _draw_question_mark(p, y, x):
    """Draw ? mark at position. 5 rows tall, 3 wide."""
    c = _WHITE
    # Top curve
    p[y][x] = c; p[y][x+1] = c; p[y][x+2] = c
    p[y+1][x+2] = c
    # Middle bend
    p[y+2][x+1] = c
    # Stem
    p[y+3][x+1] = c
    # Dot
    p[y+5][x+1] = c


def _draw_gear(p, phase=0):
    """Draw gear at top-right, rotating highlight chases clockwise."""
    g = (170, 170, 170)  # gear body
    h = (80, 80, 80)     # axle hole
    bright = (240, 240, 240)  # highlighted tooth
    base = (110, 110, 110)    # normal tooth

    def px(r, c, color=g):
        if 0 <= r < 16 and 0 <= c < 16:
            p[r][c] = color

    # Center body (2-4-4-2 rounded rect)
    px(1, 11); px(1, 12)
    px(2, 10); px(2, 11); px(2, 12); px(2, 13)
    px(3, 10); px(3, 11); px(3, 12); px(3, 13)
    px(4, 11); px(4, 12)

    # Axle hole (2x2)
    px(2, 11, h); px(2, 12, h)
    px(3, 11, h); px(3, 12, h)

    # 8 teeth positions clockwise: N, NE, E, SE, S, SW, W, NW
    teeth = [
        [(0, 11), (0, 12)],   # N
        [(1, 13)],             # NE
        [(2, 14), (3, 14)],   # E
        [(4, 13)],             # SE
        [(5, 11), (5, 12)],   # S
        [(4, 10)],             # SW
        [(2, 9), (3, 9)],     # W
        [(1, 10)],             # NW
    ]

    # Highlight 2 adjacent teeth per phase (clockwise chase)
    lit = {phase * 2 % 8, (phase * 2 + 1) % 8}

    for i, positions in enumerate(teeth):
        color = bright if i in lit else base
        for r, c in positions:
            px(r, c, color)


def _draw_checkbox(p, y, x, checked=False):
    """Draw a 3x3 checkbox at (y,x). Checked = white box with green center dot."""
    w = _WHITE
    p[y][x] = w;     p[y][x+1] = w;     p[y][x+2] = w
    p[y+1][x] = w;   p[y+1][x+1] = _BG; p[y+1][x+2] = w
    p[y+2][x] = w;   p[y+2][x+1] = w;   p[y+2][x+2] = w
    if checked:
        p[y+1][x+1] = _GREEN


def _draw_confetti(p, density=1):
    colors = [_RED, _BLUE, _GREEN, _PURPLE, _CYAN, (255, 150, 0), _PINK]
    spots_1 = [(1, 2), (2, 13), (1, 8), (3, 0), (2, 5), (0, 11)]
    spots_2 = spots_1 + [(0, 4), (1, 10), (3, 7), (0, 14), (2, 1), (1, 6),
                          (14, 3), (14, 10), (13, 7), (15, 1), (15, 13)]
    spots = spots_1 if density == 1 else spots_2
    for i, (y, x) in enumerate(spots):
        p[y][x] = colors[i % len(colors)]


def _tint_red(p):
    """Add red tint to Claude (angry)."""
    for y in range(16):
        for x in range(16):
            r, g, b = p[y][x]
            if (r, g, b) == _ORANGE:
                p[y][x] = (255, 110, 40)
            elif (r, g, b) == _DARK_O:
                p[y][x] = (230, 90, 30)


def _draw_flying_heart(p, x, y):
    h = _RED
    if 0 <= y < 16 and 0 <= x < 15:
        p[y][x] = h; p[y][x + 1] = h
    if 0 <= y + 1 < 16 and 0 <= x - 1 < 16 and x + 2 < 16:
        p[y + 1][x - 1] = h; p[y + 1][x] = h; p[y + 1][x + 1] = h; p[y + 1][x + 2] = h
    if 0 <= y + 2 < 16 and 0 <= x < 15:
        p[y + 2][x] = h; p[y + 2][x + 1] = h
    if 0 <= y + 3 < 16:
        cx = x if (x + 1) < 16 else x
        p[y + 3][cx] = h


# --- Emotion Animations (eyes + effects, no mouth) ---

def happy():
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "open")
    _draw_mouth(f2, "smile")

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "smile")

    f4 = _claude_base()
    _draw_eyes(f4, "open")
    _draw_mouth(f4, "smile")

    f5 = _claude_base()
    _draw_eyes(f5, "open")

    return [f1, f2, f3, f4, f5], [400, 400, 500, 400, 400]


def sad():
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "closed")

    f3 = _claude_base()
    _draw_eyes(f3, "closed")
    _draw_tear(f3)

    return [f1, f2, f3], [600, 600, 600]


def angry():
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "angry")

    f3 = _claude_base()
    _tint_red(f3)
    _draw_eyes(f3, "angry")

    return [f1, f2, f3], [500, 500, 500]


def love():
    f1 = _claude_base()
    _draw_eyes(f1, "hearts")

    f2 = _claude_base()
    _draw_eyes(f2, "hearts_big")

    f3 = _claude_base()
    _draw_eyes(f3, "hearts")

    return [f1, f2, f3], [400, 400, 400]


def cool():
    f1 = _claude_base()
    _draw_sunglasses(f1)

    f2 = _claude_base()
    _draw_sunglasses_shine(f2)

    return [f1, f2], [600, 600]


def cry():
    f1 = _claude_base()
    _draw_eyes(f1, "closed")
    _draw_tear(f1, "both")

    f2 = _claude_base()
    _draw_eyes(f2, "closed")
    _draw_tear(f2, "both", heavy=True)

    f3 = _claude_base()
    _draw_eyes(f3, "open")
    _draw_tear(f3, "both")

    return [f1, f2, f3], [500, 500, 500]


def laugh():
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "grin")

    f2 = _claude_base()
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "laugh")

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "laugh")

    return [f1, f2, f3], [400, 400, 400]


def sleepy():
    f1 = _claude_base()
    _draw_eyes(f1, "half")

    f2 = _claude_base()
    _draw_eyes(f2, "closed")

    f3 = _claude_base()
    _draw_eyes(f3, "closed")
    _draw_zzz(f3)

    return [f1, f2, f3], [700, 700, 700]


def shock():
    f1 = _claude_base()
    _draw_eyes(f1, "wide")
    _draw_mouth(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "wider")
    _draw_mouth(f2, "open_big")

    f3 = _claude_base()
    _draw_eyes(f3, "wide")
    _draw_mouth(f3, "open_big")
    _draw_exclaim(f3)

    return [f1, f2, f3], [400, 400, 400]


def wink():
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "one_closed")

    f3 = _claude_base()
    _draw_eyes(f3, "open")

    return [f1, f2, f3], [500, 500, 500]


def sick():
    # Gradient: orange → mid → green
    _MID_SICK = (186, 170, 68)

    f1 = _claude_base()
    _draw_eyes(f1, "dizzy")
    _draw_mouth(f1, "flat")

    f2 = _claude_base(_MID_SICK)
    _draw_eyes(f2, "dizzy")
    _draw_mouth(f2, "flat")
    _draw_sweat(f2, "left")

    f3 = _claude_base_sick()
    _draw_eyes(f3, "dizzy")
    _draw_mouth(f3, "flat")
    _draw_sweat(f3, "both")

    return [f1, f2, f3], [600, 600, 600]


def party():
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "laugh")
    _draw_confetti(f2, density=1)

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "laugh")
    _draw_confetti(f3, density=2)

    return [f1, f2, f3], [400, 400, 400]


def kiss():
    f1 = _claude_base()
    _draw_eyes(f1, "one_closed")

    f2 = _claude_base()
    _draw_eyes(f2, "one_closed")
    _draw_mouth(f2, "kiss")
    _draw_flying_heart(f2, 12, 2)

    f3 = _claude_base()
    _draw_eyes(f3, "one_closed")
    _draw_mouth(f3, "kiss")
    _draw_flying_heart(f3, 13, 1)

    return [f1, f2, f3], [400, 400, 400]


def standby():
    # Standing
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    # Blink
    f2 = _claude_base()
    _draw_eyes(f2, "half")

    f3 = _claude_base()
    _draw_eyes(f3, "closed")

    f4 = _claude_base()
    _draw_eyes(f4, "open")

    # Legs shuffle inward
    f5 = _claude_base()
    _draw_eyes(f5, "open")
    for r, c in _LEGS:
        f5[r][c] = _BG
    for r, c in [(12, 4), (12, 6), (12, 9), (12, 11),
                 (13, 4), (13, 6), (13, 9), (13, 11)]:
        f5[r][c] = _ORANGE

    # Legs back to normal
    f6 = _claude_base()
    _draw_eyes(f6, "open")

    return [f1, f2, f3, f4, f5, f6], [2000, 200, 200, 1500, 300, 300]


def thinking():
    """Thinking Claude — eyes look up, dots appear."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "lookup")

    f3 = _claude_base()
    _draw_eyes(f3, "lookup")
    _draw_dots(f3, 1)

    f4 = _claude_base()
    _draw_eyes(f4, "lookup")
    _draw_dots(f4, 2)

    f5 = _claude_base()
    _draw_eyes(f5, "lookup")
    _draw_dots(f5, 3)

    return [f1, f2, f3, f4, f5], [600, 400, 400, 400, 400]


def _shuffle_legs(p):
    """Shift legs inward — gives a 'busy' fidget look."""
    for r, c in _LEGS:
        p[r][c] = _BG
    for r, c in [(12, 4), (12, 6), (12, 9), (12, 11),
                 (13, 4), (13, 6), (13, 9), (13, 11)]:
        p[r][c] = _ORANGE


def working():
    """Working/coding — </> tag builds up, eyes lookup, legs fidget."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "lookup")
    _draw_code_tag(f2, 1)
    _shuffle_legs(f2)

    f3 = _claude_base()
    _draw_eyes(f3, "lookup")
    _draw_code_tag(f3, 2)

    f4 = _claude_base()
    _draw_eyes(f4, "lookup")
    _draw_code_tag(f4, 3)
    _shuffle_legs(f4)

    return [f1, f2, f3, f4], [600, 400, 400, 400]


def _draw_mini_claude(p, top, left, color=None):
    """Draw a small Claude: 4-row body + 2 legs, ~6 wide."""
    c = color or _ORANGE
    # Body: 4 rows × 6 cols
    for dy in range(4):
        for dx in range(6):
            x = left + dx
            if 0 <= top + dy < 16 and 0 <= x < 16:
                p[top + dy][x] = c
    # Eyes: 1px each at row 1
    ey = top + 1
    if 0 <= ey < 16:
        if 0 <= left + 1 < 16:
            p[ey][left + 1] = _BLACK
        if 0 <= left + 4 < 16:
            p[ey][left + 4] = _BLACK
    # Legs: 2 at row 4
    ly = top + 4
    if 0 <= ly < 16:
        if 0 <= left + 1 < 16:
            p[ly][left + 1] = c
        if 0 <= left + 4 < 16:
            p[ly][left + 4] = c


def subagent():
    """Subagent — Claude fades left, two mini clones split up and down."""
    _FADE = (100, 65, 25)  # very faded orange

    # F1: normal Claude
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    # F2: Claude shifts left 5 + dims, two dim mini Claudes appear
    f2 = _empty()
    for row, (s, e) in _BODY.items():
        for col in range(s - 5, e - 4):
            if 0 <= col < 16:
                f2[row][col] = _DARK_O
    for r, col in _LEGS:
        if 0 <= col - 5 < 16:
            f2[r][col - 5] = _DARK_O
    # Eyes on shifted Claude (-5): left eye at col 0; right at cols 5-6
    f2[6][0] = _BLACK; f2[7][0] = _BLACK
    for dy in (0, 1):
        for dx in (0, 1):
            f2[6 + dy][5 + dx] = _BLACK
    _draw_mini_claude(f2, 3, 10, _DARK_O)
    _draw_mini_claude(f2, 9, 10, _DARK_O)

    # F3: Claude fades off-screen, bright mini Claudes split apart
    f3 = _empty()
    for row, (s, e) in _BODY.items():
        for col in range(s - 9, e - 8):
            if 0 <= col < 16:
                f3[row][col] = _FADE
    for r, col in _LEGS:
        if 0 <= col - 9 < 16:
            f3[r][col - 9] = _FADE
    # Eyes on shifted Claude (-9): left eye off-screen; right at cols 1-2
    for dy in (0, 1):
        for dx in (0, 1):
            f3[6 + dy][1 + dx] = _BLACK
    _draw_mini_claude(f3, 1, 10)
    _draw_mini_claude(f3, 11, 10)

    return [f1, f2, f3], [600, 400, 400]


def _claude_base_at(y_offset=0, x_offset=0, color=None):
    """Orange Claude body at a vertical/horizontal offset from default position."""
    p = _empty()
    c = color or _ORANGE
    for row, (s, e) in _BODY.items():
        r = row + y_offset
        if 0 <= r < 16:
            for col in range(s + x_offset, e + 1 + x_offset):
                if 0 <= col < 16:
                    p[r][col] = c
    for r, col in _LEGS:
        rr = r + y_offset
        cc = col + x_offset
        if 0 <= rr < 16 and 0 <= cc < 16:
            p[rr][cc] = c
    return p


def done():
    """Done/success — bounce up, land with smile + checkmark + sparkles."""
    g = _GREEN

    # F1: normal Claude
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    # F2: bounce up 1 row, squint
    f2 = _claude_base_at(-1)
    for dx in range(3):
        f2[6][4 + dx] = _BLACK
        f2[6][10 + dx] = _BLACK

    # F3: land back, squint + smile
    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "smile")

    # F4: checkmark appears on right (overlaps body)
    #   col: 10 11 12 13 14 15
    # row2: .  .  .  .  .  X
    # row3: .  .  .  .  X  .
    # row4: X  .  .  X  .  .
    # row5: .  X  X  .  .  .
    f4 = _claude_base()
    _draw_eyes(f4, "squint")
    _draw_mouth(f4, "smile")
    f4[2][15] = g
    f4[3][14] = g
    f4[4][13] = g; f4[4][10] = g
    f4[5][12] = g; f4[5][11] = g

    # F5: hold + top sparkles
    f5 = _claude_base()
    _draw_eyes(f5, "squint")
    _draw_mouth(f5, "smile")
    f5[2][15] = g
    f5[3][14] = g
    f5[4][13] = g; f5[4][10] = g
    f5[5][12] = g; f5[5][11] = g
    # Sparkles — mostly top, a few around body
    f5[0][2] = _CYAN; f5[0][6] = _RED; f5[0][10] = _PINK; f5[0][14] = _PURPLE
    f5[1][4] = (255, 150, 0); f5[1][8] = _BLUE; f5[1][12] = _GREEN
    f5[2][1] = _PINK; f5[2][9] = _CYAN
    f5[6][0] = _RED; f5[8][15] = _PURPLE; f5[14][2] = _BLUE

    return [f1, f2, f3, f4, f5], [400, 250, 350, 400, 500]


def _draw_bell(p, cx, tilt=0):
    """Draw narrow rounded bell. cx=center col, tilt: -1/0/1."""
    g = (255, 210, 60)   # gold
    d = (200, 165, 40)   # dark gold edge
    w = _WHITE
    x = cx + tilt

    def px(r, c, color):
        if 0 <= r < 16 and 0 <= c < 16:
            p[r][c] = color

    # Handle (row 0)
    px(0, x, w)
    # Dome start (row 1): 3px — round top
    px(1, x - 1, d); px(1, x, g); px(1, x + 1, d)
    # Body (rows 2-5): 5px same width = round barrel
    for row in (2, 3, 4, 5):
        for dx in range(-2, 3):
            px(row, x + dx, d if abs(dx) == 2 else g)
    # Rim (row 6): 7px
    for dx in range(-3, 4):
        px(6, x + dx, d if abs(dx) == 3 else g)
    # Clapper swings extra (row 7)
    px(7, x + tilt, w)


def notify():
    """Notify — bell sways, Claude shouts."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "open")
    _draw_mouth(f2, "open")
    _draw_bell(f2, 11, tilt=0)

    f3 = _claude_base()
    _draw_eyes(f3, "half")
    _draw_mouth(f3, "open_big")
    _draw_bell(f3, 11, tilt=-1)

    f4 = _claude_base()
    _draw_eyes(f4, "open")
    _draw_mouth(f4, "open")
    _draw_bell(f4, 11, tilt=1)

    f5 = _claude_base()
    _draw_eyes(f5, "closed")
    _draw_mouth(f5, "open_big")
    _draw_bell(f5, 11, tilt=0)

    return [f1, f2, f3, f4, f5], [500, 300, 300, 300, 400]


def tooluse():
    """Tool use — gear with rotating highlight at top-right."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_gear(f1, phase=0)

    f2 = _claude_base()
    _draw_eyes(f2, "open")
    _draw_gear(f2, phase=1)

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_gear(f3, phase=2)

    f4 = _claude_base()
    _draw_eyes(f4, "open")
    _draw_gear(f4, phase=3)
    _shuffle_legs(f4)

    return [f1, f2, f3, f4], [300, 300, 300, 300]


def oops():
    """Oops/error — dizzy eyes + exclamation + body shake."""
    def _dizzy_at(p, xo):
        """Draw dizzy X-eyes with horizontal offset."""
        b = _BLACK
        p[6][4+xo] = b; p[6][6+xo] = b
        p[7][5+xo] = b
        p[8][4+xo] = b; p[8][6+xo] = b
        p[6][9+xo] = b; p[6][11+xo] = b
        p[7][10+xo] = b
        p[8][9+xo] = b; p[8][11+xo] = b

    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "dizzy")
    _draw_exclaim(f2)

    # Shake left
    f3 = _claude_base_at(0, -1)
    _tint_red(f3)
    _dizzy_at(f3, -1)
    _draw_exclaim(f3)

    # Shake right
    f4 = _claude_base_at(0, 1)
    _tint_red(f4)
    _dizzy_at(f4, 1)
    _draw_exclaim(f4)

    f5 = _claude_base()
    _draw_eyes(f5, "dizzy")
    _draw_exclaim(f5)

    return [f1, f2, f3, f4, f5], [500, 400, 200, 200, 400]


def tasklist():
    """Tasklist — 3x3 checkboxes appear on right side, Claude shifts left."""
    xo = -3  # Claude shifts left by 3

    def _eyes_lookup(p):
        """Lookup eyes with x offset."""
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + xo + dx] = _BLACK
                p[5 + dy][10 + xo + dx] = _BLACK

    def _eyes_open(p):
        for dy in (0, 1):
            for dx in (0, 1):
                p[6 + dy][4 + xo + dx] = _BLACK
                p[6 + dy][10 + xo + dx] = _BLACK

    f1 = _claude_base_at(0, xo)
    _eyes_open(f1)

    f2 = _claude_base_at(0, xo)
    _eyes_lookup(f2)
    _draw_checkbox(f2, 3, 13)

    f3 = _claude_base_at(0, xo)
    _eyes_lookup(f3)
    _draw_checkbox(f3, 3, 13)
    _draw_checkbox(f3, 7, 13)

    f4 = _claude_base_at(0, xo)
    _eyes_lookup(f4)
    _draw_checkbox(f4, 3, 13)
    _draw_checkbox(f4, 7, 13)
    _draw_checkbox(f4, 11, 13)

    return [f1, f2, f3, f4], [500, 400, 400, 400]


def taskdone():
    """Task done — second checkbox gets checked + confetti."""
    xo = -3

    def _eyes_open(p):
        for dy in (0, 1):
            for dx in (0, 1):
                p[6 + dy][4 + xo + 1 + dx] = _BLACK
                p[6 + dy][10 + xo + 1 + dx] = _BLACK

    def _eyes_squint(p):
        for dx in range(3):
            p[7][4 + xo + 1 + dx] = _BLACK
            p[7][10 + xo + 1 + dx] = _BLACK

    def _mouth_smile(p):
        p[9][5+xo] = _BLACK; p[9][10+xo] = _BLACK
        for x in range(6+xo, 10+xo):
            p[10][x] = _BLACK

    def _mouth_grin(p):
        for x in range(5+xo, 11+xo):
            p[9][x] = _BLACK
        p[9][6+xo] = _WHITE; p[9][7+xo] = _WHITE; p[9][8+xo] = _WHITE; p[9][9+xo] = _WHITE
        for x in range(5+xo, 11+xo):
            p[10][x] = _BLACK

    # First checked, second unchecked, third unchecked
    f1 = _claude_base_at(0, xo)
    _eyes_open(f1)
    _mouth_smile(f1)
    _draw_checkbox(f1, 3, 13, checked=True)
    _draw_checkbox(f1, 7, 13)
    _draw_checkbox(f1, 11, 13)

    # Second gets checked
    f2 = _claude_base_at(0, xo)
    _eyes_squint(f2)
    _mouth_smile(f2)
    _draw_checkbox(f2, 3, 13, checked=True)
    _draw_checkbox(f2, 7, 13, checked=True)
    _draw_checkbox(f2, 11, 13)

    # Confetti
    f3 = _claude_base_at(0, xo)
    _eyes_squint(f3)
    _mouth_smile(f3)
    _draw_checkbox(f3, 3, 13, checked=True)
    _draw_checkbox(f3, 7, 13, checked=True)
    _draw_checkbox(f3, 11, 13)
    _draw_confetti(f3, density=2)

    return [f1, f2, f3], [500, 400, 600]


def question():
    """Question/waiting — thinking dots then ? sways, eyes look around."""
    def _eyes_left(p):
        for dy in (0, 1):
            p[6+dy][4] = _BLACK; p[6+dy][5] = _BLACK
            p[6+dy][10] = _BLACK; p[6+dy][11] = _BLACK

    def _eyes_right(p):
        for dy in (0, 1):
            p[6+dy][5] = _BLACK; p[6+dy][6] = _BLACK
            p[6+dy][11] = _BLACK; p[6+dy][12] = _BLACK

    # Dots build up
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "lookup")
    f2[2][7] = _WHITE

    f3 = _claude_base()
    _draw_eyes(f3, "lookup")
    f3[2][6] = _WHITE; f3[2][8] = _WHITE

    f4 = _claude_base()
    _draw_eyes(f4, "lookup")
    f4[2][5] = _WHITE; f4[2][7] = _WHITE; f4[2][9] = _WHITE

    # ? appears, sways left/right
    f5 = _claude_base()
    _draw_eyes(f5, "open")
    _draw_question_mark(f5, 0, 12)

    f6 = _claude_base()
    _draw_eyes(f6, "open")
    _draw_question_mark(f6, 0, 11)

    f7 = _claude_base()
    _draw_eyes(f7, "open")
    _draw_question_mark(f7, 0, 12)

    return [f1, f2, f3, f4, f5, f6, f7], [500, 350, 350, 400, 400, 400, 400]


def haiku():
    """Easter egg — Claude composes a haiku. 5-7-5 dots appear line by line."""
    _LAV = (180, 140, 255)   # lavender
    _SPK = (255, 150, 180)   # soft pink
    _SCY = (100, 220, 240)   # soft cyan
    yo = 2  # body shifts down to make room

    def _line(p, row, count, color):
        start = (16 - count) // 2
        for i in range(count):
            p[row][start + i] = color

    def _eyes(p, style):
        if style == "open":
            for dy in (0, 1):
                for dx in (0, 1):
                    p[6+yo+dy][4+dx] = _BLACK
                    p[6+yo+dy][10+dx] = _BLACK
        elif style == "lookup":
            for dy in (0, 1):
                for dx in (0, 1):
                    p[5+yo+dy][4+dx] = _BLACK
                    p[5+yo+dy][10+dx] = _BLACK
        elif style == "squint":
            for dx in range(3):
                p[7+yo][4+dx] = _BLACK
                p[7+yo][10+dx] = _BLACK

    def _legs_shuffle(p):
        for r, c in _LEGS:
            p[r+yo][c] = _BG
        for r, c in [(12, 4), (12, 6), (12, 9), (12, 11),
                     (13, 4), (13, 6), (13, 9), (13, 11)]:
            p[r+yo][c] = _ORANGE

    # F1: contemplation
    f1 = _claude_base_at(yo)
    _eyes(f1, "open")

    # F2: first line (5)
    f2 = _claude_base_at(yo)
    _eyes(f2, "lookup")
    _line(f2, 0, 5, _LAV)
    _legs_shuffle(f2)

    # F3: + second line (7)
    f3 = _claude_base_at(yo)
    _eyes(f3, "lookup")
    _line(f3, 0, 5, _LAV)
    _line(f3, 2, 7, _SPK)

    # F4: + third line (5)
    f4 = _claude_base_at(yo)
    _eyes(f4, "lookup")
    _line(f4, 0, 5, _LAV)
    _line(f4, 2, 7, _SPK)
    _line(f4, 4, 5, _SCY)
    _legs_shuffle(f4)

    # F5: satisfied — shimmer
    _LAV2 = (210, 180, 255)
    _SPK2 = (255, 180, 210)
    _SCY2 = (140, 240, 255)
    f5 = _claude_base_at(yo)
    _eyes(f5, "squint")
    _line(f5, 0, 5, _LAV2)
    _line(f5, 2, 7, _SPK2)
    _line(f5, 4, 5, _SCY2)

    return [f1, f2, f3, f4, f5], [600, 500, 500, 500, 600]


# --- Registry ---

EMOTIONS = {
    "happy": ("Claude happy", happy),
    "sad": ("Claude sad", sad),
    "angry": ("Claude angry", angry),
    "love": ("Claude love", love),
    "cool": ("Claude cool", cool),
    "cry": ("Claude cry", cry),
    "laugh": ("Claude laugh", laugh),
    "sleepy": ("Claude sleepy", sleepy),
    "shock": ("Claude shock", shock),
    "wink": ("Claude wink", wink),
    "sick": ("Claude sick", sick),
    "party": ("Claude party", party),
    "kiss": ("Claude kiss", kiss),
    "standby": ("Claude standby", standby),
    "thinking": ("Claude thinking", thinking),
    # Workflow emotions
    "working": ("Claude working", working),
    "subagent": ("Claude subagent", subagent),
    "done": ("Claude done", done),
    "notify": ("Claude notify", notify),
    "tooluse": ("Claude tooluse", tooluse),
    "oops": ("Claude oops", oops),
    "tasklist": ("Claude tasklist", tasklist),
    "taskdone": ("Claude taskdone", taskdone),
    "question": ("Claude question", question),
    # Easter egg
    "haiku": ("Claude haiku", haiku),
}

# Hidden from help listing
HIDDEN_EMOTIONS = {"haiku"}
