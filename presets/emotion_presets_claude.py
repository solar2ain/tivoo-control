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
    3: (2, 13),
    4: (2, 13), 5: (2, 13), 6: (2, 13),
    7: (1, 14), 8: (1, 14), 9: (1, 14), 10: (2, 13),
}
_LEGS = [
    (11, 3), (11, 5), (11, 10), (11, 12),
    (12, 3), (12, 5), (12, 10), (12, 12),
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
                p[5 + dy][4 + dx] = _BLACK
                p[5 + dy][10 + dx] = _BLACK
    elif style == "open_wide":
        # 2x3 rectangular eyes
        for dy in (0, 1):
            for dx in range(3):
                p[5 + dy][4 + dx] = _BLACK
                p[5 + dy][10 + dx] = _BLACK
    elif style == "squint":
        for dx in range(3):
            p[6][4 + dx] = _BLACK
            p[6][10 + dx] = _BLACK
    elif style == "closed":
        p[6][4] = _BLACK; p[6][5] = _BLACK; p[6][6] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][12] = _BLACK
    elif style == "half":
        p[6][4] = _BLACK; p[6][5] = _BLACK
        p[5][4] = _DARK_O; p[5][5] = _DARK_O
        p[6][10] = _BLACK; p[6][11] = _BLACK
        p[5][10] = _DARK_O; p[5][11] = _DARK_O
    elif style == "wide":
        for dy in range(3):
            for dx in range(3):
                p[4 + dy][4 + dx] = _WHITE
                p[4 + dy][9 + dx] = _WHITE
        p[5][5] = _BLACK
        p[5][10] = _BLACK
    elif style == "wider":
        for dy in range(3):
            for dx in range(3):
                p[4 + dy][3 + dx] = _WHITE
                p[4 + dy][9 + dx] = _WHITE
        for dy in (0, 1):
            for dx in (0, 1):
                p[4 + dy][4 + dx] = _BLACK
                p[4 + dy][10 + dx] = _BLACK
    elif style == "hearts":
        h = _RED
        # Left heart centered at col 5
        p[5][4] = h; p[5][6] = h
        p[6][4] = h; p[6][5] = h; p[6][6] = h
        p[7][5] = h
        # Right heart centered at col 10
        p[5][9] = h; p[5][11] = h
        p[6][9] = h; p[6][10] = h; p[6][11] = h
        p[7][10] = h
    elif style == "hearts_big":
        h = _RED
        w = _PINK
        # Left heart centered at col 5
        p[4][4] = h; p[4][6] = h
        p[5][3] = h; p[5][4] = w; p[5][5] = h; p[5][6] = w; p[5][7] = h
        p[6][4] = h; p[6][5] = h; p[6][6] = h
        p[7][5] = h
        # Right heart centered at col 10
        p[4][9] = h; p[4][11] = h
        p[5][8] = h; p[5][9] = w; p[5][10] = h; p[5][11] = w; p[5][12] = h
        p[6][9] = h; p[6][10] = h; p[6][11] = h
        p[7][10] = h
    elif style == "dizzy":
        p[5][4] = _BLACK; p[5][6] = _BLACK
        p[6][5] = _BLACK
        p[7][4] = _BLACK; p[7][6] = _BLACK
        p[5][9] = _BLACK; p[5][11] = _BLACK
        p[6][10] = _BLACK
        p[7][9] = _BLACK; p[7][11] = _BLACK
    elif style == "one_closed":
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][12] = _BLACK
    elif style == "angry":
        # 2-row diagonal — outer high, inner low
        # Left eye
        p[5][3] = _BLACK; p[5][4] = _BLACK; p[5][5] = _BLACK
        p[6][4] = _BLACK; p[6][5] = _BLACK; p[6][6] = _BLACK
        # Right eye
        p[5][10] = _BLACK; p[5][11] = _BLACK; p[5][12] = _BLACK
        p[6][9] = _BLACK; p[6][10] = _BLACK; p[6][11] = _BLACK
    elif style == "angry_deep":
        # Thicker 2-row diagonal
        p[4][3] = _BLACK; p[5][3] = _BLACK; p[5][4] = _BLACK; p[5][5] = _BLACK
        p[6][4] = _BLACK; p[6][5] = _BLACK; p[6][6] = _BLACK; p[7][6] = _BLACK
        p[4][12] = _BLACK; p[5][10] = _BLACK; p[5][11] = _BLACK; p[5][12] = _BLACK
        p[6][9] = _BLACK; p[6][10] = _BLACK; p[6][11] = _BLACK; p[7][9] = _BLACK
    elif style == "lookup":
        # Eyes shifted up one row (thinking)
        for dy in (0, 1):
            for dx in (0, 1):
                p[4 + dy][4 + dx] = _BLACK
                p[4 + dy][10 + dx] = _BLACK


# --- Mouth (only for specific emotions) ---

def _draw_mouth(p, style):
    """Draw mouth in body area — most emotions don't use this."""
    if style == "smile":
        # Upward curve — corners high, center low
        p[8][5] = _BLACK; p[8][10] = _BLACK
        p[9][6] = _BLACK; p[9][7] = _BLACK; p[9][8] = _BLACK; p[9][9] = _BLACK
    elif style == "grin":
        # Wide grin with teeth
        p[8][5] = _BLACK; p[8][6] = _BLACK; p[8][7] = _BLACK
        p[8][8] = _BLACK; p[8][9] = _BLACK; p[8][10] = _BLACK
        p[8][6] = _WHITE; p[8][7] = _WHITE; p[8][8] = _WHITE; p[8][9] = _WHITE
        p[9][5] = _BLACK; p[9][6] = _BLACK; p[9][7] = _BLACK
        p[9][8] = _BLACK; p[9][9] = _BLACK; p[9][10] = _BLACK
    elif style == "laugh":
        for x in range(5, 11):
            p[8][x] = _BLACK
        p[9][5] = _BLACK; p[9][10] = _BLACK
        for x in range(6, 10):
            p[9][x] = _RED
    elif style == "open":
        p[8][7] = _BLACK; p[8][8] = _BLACK
        p[9][7] = _BLACK; p[9][8] = _BLACK
    elif style == "open_big":
        for x in range(6, 10):
            p[8][x] = _BLACK
        p[9][6] = _BLACK; p[9][9] = _BLACK
        p[9][7] = _RED; p[9][8] = _RED
    elif style == "wavy":
        # _--_ shape: middle stays level, sides droop down
        p[9][7] = _BLACK; p[9][8] = _BLACK
        p[10][6] = _BLACK; p[10][9] = _BLACK
    elif style == "flat":
        for x in range(6, 10):
            p[9][x] = _BLACK
    elif style == "kiss":
        p[8][7] = _RED; p[8][8] = _RED
        p[9][7] = _RED; p[9][8] = _RED


# --- Brows ---

def _draw_brows(p, style):
    """Draw eyebrows — only angry_deep fits the compact shape."""
    if style == "angry_deep":
        p[4][3] = _BLACK; p[4][4] = _BLACK; p[4][5] = _BLACK; p[5][6] = _BLACK
        p[4][12] = _BLACK; p[4][11] = _BLACK; p[4][10] = _BLACK; p[5][9] = _BLACK


# --- Effects ---

def _draw_tear(p, side="both", heavy=False):
    lb = _BLUE
    lw = (150, 200, 255)
    if side in ("left", "both"):
        p[7][4] = lb; p[8][4] = lb; p[9][4] = lb
        if heavy:
            p[10][4] = lb
            p[8][3] = lw; p[9][3] = lw
            p[8][5] = lw
    if side in ("right", "both"):
        p[7][12] = lb; p[8][12] = lb; p[9][12] = lb
        if heavy:
            p[10][12] = lb
            p[8][13] = lw; p[9][13] = lw
            p[8][11] = lw


def _draw_sweat(p, side="left"):
    if side == "left":
        p[3][1] = _BLUE; p[4][1] = _BLUE
    elif side == "both":
        p[3][1] = _BLUE; p[4][1] = _BLUE
        p[3][14] = _BLUE; p[4][14] = _BLUE


def _draw_zzz(p):
    z = _WHITE
    p[1][11] = z; p[1][12] = z; p[1][13] = z
    p[2][13] = z
    p[3][12] = z
    p[4][11] = z
    p[5][11] = z; p[5][12] = z; p[5][13] = z


def _draw_sunglasses(p):
    g = _BLACK
    b = (60, 60, 60)
    for x in range(3, 13):
        p[5][x] = g
    for dy in (0, 1):
        for dx in range(4):
            p[6 + dy][3 + dx] = b
            p[6 + dy][9 + dx] = b


def _draw_sunglasses_shine(p):
    _draw_sunglasses(p)
    p[6][4] = _WHITE; p[6][5] = _WHITE
    p[6][10] = _WHITE; p[6][11] = _WHITE


def _draw_exclaim(p):
    e = _RED
    p[1][14] = e; p[2][14] = e; p[3][14] = e
    p[5][14] = e


def _draw_dots(p, count=3):
    """Draw thinking dots above head."""
    d = _WHITE
    positions = [(1, 6), (1, 8), (1, 10)]
    for i in range(min(count, 3)):
        y, x = positions[i]
        p[y][x] = d


def _draw_code_tag(p, stage=1):
    """Draw </> code tag above head. stage 1: < , 2: <>, 3: </>"""
    c = _WHITE
    if stage >= 1:
        # < at row 1, cols 4-5
        p[1][5] = c; p[0][4] = c; p[2][4] = c
    if stage >= 2:
        # > at row 1, cols 10-11
        p[1][10] = c; p[0][11] = c; p[2][11] = c
    if stage >= 3:
        # / at row 1, cols 7-8
        p[0][8] = c; p[2][7] = c


def _draw_checkmark(p, y, x, color=None):
    """Draw small ✓ at position. 3x2 check shape."""
    c = color or _GREEN
    p[y + 1][x] = c
    p[y][x + 1] = c
    p[y + 1][x + 1] = c
    p[y][x + 2] = c


def _draw_question_mark(p, y, x):
    """Draw ? mark at position. 4 rows tall."""
    c = _WHITE
    p[y][x] = c; p[y][x + 1] = c
    p[y + 1][x + 1] = c
    p[y + 2][x] = c
    p[y + 3][x] = c


def _draw_gear(p, rotated=False):
    """Draw gear below Claude (rows 13-15, cols 6-9). Cross or X shape."""
    g = (160, 160, 160)  # gray
    cy, cx = 14, 7  # center
    p[cy][cx] = g; p[cy][cx + 1] = g
    if not rotated:
        # + cross
        p[cy - 1][cx] = g; p[cy - 1][cx + 1] = g
        p[cy + 1][cx] = g; p[cy + 1][cx + 1] = g
        p[cy][cx - 1] = g; p[cy][cx + 2] = g
    else:
        # X cross (rotated 45°)
        p[cy - 1][cx - 1] = g; p[cy - 1][cx + 2] = g
        p[cy + 1][cx - 1] = g; p[cy + 1][cx + 2] = g


def _draw_squares(p, count=1):
    """Draw small squares on right side for tasklist."""
    sq = _WHITE
    positions = [(5, 15), (7, 15), (9, 15)]
    for i in range(min(count, 3)):
        y, x = positions[i]
        p[y][x] = sq


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
    _draw_flying_heart(f2, 12, 1)

    f3 = _claude_base()
    _draw_eyes(f3, "one_closed")
    _draw_mouth(f3, "kiss")
    _draw_flying_heart(f3, 13, 0)

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
    for r, c in [(11, 4), (11, 6), (11, 9), (11, 11),
                 (12, 4), (12, 6), (12, 9), (12, 11)]:
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


def working():
    """Working/coding — </> tag builds up above head."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "squint")
    _draw_code_tag(f2, 1)

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_code_tag(f3, 2)

    f4 = _claude_base()
    _draw_eyes(f4, "squint")
    _draw_code_tag(f4, 3)

    return [f1, f2, f3, f4], [600, 400, 400, 400]


def subagent():
    """Subagent — Claude splits into two."""
    # F1: normal Claude centered
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    # F2: body shifts left 2px + dim outline on right
    f2 = _empty()
    c = _ORANGE
    dim = _DARK_O
    for row, (s, e) in _BODY.items():
        for col in range(s - 2, e - 1):
            if 0 <= col < 16:
                f2[row][col] = c
    for r, col in _LEGS:
        if 0 <= col - 2 < 16:
            f2[r][col - 2] = c
    # Eyes on shifted body
    for dy in (0, 1):
        for dx in (0, 1):
            f2[5 + dy][2 + dx] = _BLACK
            f2[5 + dy][8 + dx] = _BLACK
    # Dim outline on right side
    for row, (s, e) in _BODY.items():
        for col in range(s + 6, e + 7):
            if 0 <= col < 16:
                f2[row][col] = dim
    for r, col in _LEGS:
        if 0 <= col + 6 < 16:
            f2[r][col + 6] = dim

    # F3: left Claude + right small full Claude
    f3 = _empty()
    # Left Claude (shifted left 2)
    for row, (s, e) in _BODY.items():
        for col in range(s - 2, e - 1):
            if 0 <= col < 16:
                f3[row][col] = c
    for r, col in _LEGS:
        if 0 <= col - 2 < 16:
            f3[r][col - 2] = c
    for dy in (0, 1):
        for dx in (0, 1):
            f3[5 + dy][2 + dx] = _BLACK
            f3[5 + dy][8 + dx] = _BLACK
    # Right Claude (shifted right 6, bright)
    bright = (255, 170, 70)
    for row, (s, e) in _BODY.items():
        for col in range(s + 6, e + 7):
            if 0 <= col < 16:
                f3[row][col] = bright
    for r, col in _LEGS:
        if 0 <= col + 6 < 16:
            f3[r][col + 6] = bright
    # Eyes on right clone
    for dy in (0, 1):
        f3[5 + dy][10] = _BLACK
        f3[5 + dy][14] = _BLACK

    return [f1, f2, f3], [600, 400, 400]


def done():
    """Done/success — squint + smile + green checkmark."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "smile")

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "smile")
    _draw_checkmark(f3, 0, 6, _GREEN)

    return [f1, f2, f3], [400, 400, 500]


def notify():
    """Notify — wide eyes with flashing red exclamation mark."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "wide")
    _draw_exclaim(f2)  # red !

    f3 = _claude_base()
    _draw_eyes(f3, "wide")
    # White ! flash
    p = f3
    p[1][14] = _WHITE; p[2][14] = _WHITE; p[3][14] = _WHITE
    p[5][14] = _WHITE

    f4 = _claude_base()
    _draw_eyes(f4, "wide")
    _draw_exclaim(f4)  # red ! again

    return [f1, f2, f3, f4], [400, 300, 300, 300]


def tooluse():
    """Tool use — gear spinning below Claude."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "squint")
    _draw_gear(f2, rotated=False)

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_gear(f3, rotated=True)

    return [f1, f2, f3], [400, 400, 400]


def oops():
    """Oops/error — dizzy eyes + sweat + red tint."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "dizzy")
    _draw_sweat(f2, "left")

    f3 = _claude_base()
    _tint_red(f3)
    _draw_eyes(f3, "dizzy")
    _draw_sweat(f3, "both")

    return [f1, f2, f3], [500, 500, 500]


def tasklist():
    """Tasklist — squares appear on right side."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "lookup")
    _draw_squares(f2, 1)

    f3 = _claude_base()
    _draw_eyes(f3, "lookup")
    _draw_squares(f3, 2)

    f4 = _claude_base()
    _draw_eyes(f4, "lookup")
    _draw_squares(f4, 3)

    return [f1, f2, f3, f4], [500, 400, 400, 400]


def taskdone():
    """Task done — green checkmarks appear."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_checkmark(f1, 1, 12, _GREEN)

    f2 = _claude_base()
    _draw_eyes(f2, "squint")
    _draw_checkmark(f2, 1, 12, _GREEN)
    _draw_checkmark(f2, 1, 7, _GREEN)

    return [f1, f2], [500, 500]


def question():
    """Question/waiting — dots build up then ? appears."""
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    f2 = _claude_base()
    _draw_eyes(f2, "open")
    p = f2
    p[1][6] = _WHITE  # .

    f3 = _claude_base()
    _draw_eyes(f3, "open")
    p = f3
    p[1][6] = _WHITE; p[1][8] = _WHITE  # ..

    f4 = _claude_base()
    _draw_eyes(f4, "open")
    p = f4
    p[1][6] = _WHITE; p[1][8] = _WHITE; p[1][10] = _WHITE  # ...
    _draw_question_mark(f4, 0, 12)  # ?

    return [f1, f2, f3, f4], [600, 400, 400, 400]


def haiku():
    """Easter egg — Claude composes a haiku. 5-7-5 dots appear line by line."""
    _LAV = (180, 140, 255)   # lavender
    _SPK = (255, 150, 180)   # soft pink
    _SCY = (100, 220, 240)   # soft cyan

    def _line(p, row, count, color):
        """Draw centered dots: count pixels on row."""
        start = (16 - count) // 2
        for i in range(count):
            p[row][start + i] = color

    # F1: contemplation
    f1 = _claude_base()
    _draw_eyes(f1, "open")

    # F2: eyes up + first line (5)
    f2 = _claude_base()
    _draw_eyes(f2, "lookup")
    _line(f2, 0, 5, _LAV)

    # F3: + second line (7)
    f3 = _claude_base()
    _draw_eyes(f3, "lookup")
    _line(f3, 0, 5, _LAV)
    _line(f3, 1, 7, _SPK)

    # F4: + third line (5) — poem complete
    f4 = _claude_base()
    _draw_eyes(f4, "lookup")
    _line(f4, 0, 5, _LAV)
    _line(f4, 1, 7, _SPK)
    _line(f4, 2, 5, _SCY)

    # F5: satisfied — squint, all lines shimmer brighter
    _LAV2 = (210, 180, 255)
    _SPK2 = (255, 180, 210)
    _SCY2 = (140, 240, 255)
    f5 = _claude_base()
    _draw_eyes(f5, "squint")
    _line(f5, 0, 5, _LAV2)
    _line(f5, 1, 7, _SPK2)
    _line(f5, 2, 5, _SCY2)

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
