"""
Claude Emotion Presets — Orange Claude-shaped face expressions for Tivoo 16x16.

Usage: python3 tivoo_macos.py preset happy --load emotion_presets_claude.py
"""

import copy

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


# --- Base ---

_BODY = {
    2: (5, 10), 3: (4, 11), 4: (2, 13),
    5: (1, 14), 6: (1, 14), 7: (1, 14),
    8: (1, 14), 9: (1, 14), 10: (2, 13), 11: (4, 11),
}
_FEET = [(12, 5), (12, 6), (12, 9), (12, 10)]


def _empty():
    return [[_BG] * 16 for _ in range(16)]


def _claude_base(color=None):
    """Orange Claude-shaped face base."""
    p = _empty()
    c = color or _ORANGE
    for row, (s, e) in _BODY.items():
        for col in range(s, e + 1):
            p[row][col] = c
    for r, col in _FEET:
        p[r][col] = c
    return p


def _claude_base_sick():
    """Green-tinted Claude for sick emoji."""
    return _claude_base(_SICK_G)


# --- Eyes ---

def _draw_eyes(p, style):
    """Draw eyes on face. Same positions as standard emotions."""
    if style == "open":
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = _BLACK
                p[5 + dy][10 + dx] = _BLACK
    elif style == "squint":
        for dx in range(3):
            p[6][4 + dx] = _BLACK
            p[6][10 + dx] = _BLACK
    elif style == "closed":
        p[6][4] = _BLACK; p[6][5] = _BLACK; p[6][6] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][9] = _BLACK
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
        p[5][4] = h; p[5][6] = h
        p[6][3] = h; p[6][4] = h; p[6][5] = h; p[6][6] = h; p[6][7] = h
        p[7][4] = h; p[7][5] = h; p[7][6] = h
        p[8][5] = h
        p[5][10] = h; p[5][12] = h
        p[6][9] = h; p[6][10] = h; p[6][11] = h; p[6][12] = h; p[6][13] = h
        p[7][10] = h; p[7][11] = h; p[7][12] = h
        p[8][11] = h
    elif style == "hearts_big":
        h = _RED
        w = _PINK
        p[4][4] = h; p[4][6] = h
        p[5][3] = h; p[5][4] = w; p[5][5] = h; p[5][6] = w; p[5][7] = h
        p[6][3] = h; p[6][4] = h; p[6][5] = h; p[6][6] = h; p[6][7] = h
        p[7][4] = h; p[7][5] = h; p[7][6] = h
        p[8][5] = h
        p[4][10] = h; p[4][12] = h
        p[5][9] = h; p[5][10] = w; p[5][11] = h; p[5][12] = w; p[5][13] = h
        p[6][9] = h; p[6][10] = h; p[6][11] = h; p[6][12] = h; p[6][13] = h
        p[7][10] = h; p[7][11] = h; p[7][12] = h
        p[8][11] = h
    elif style == "dizzy":
        p[5][4] = _BLACK; p[5][6] = _BLACK
        p[6][5] = _BLACK
        p[7][4] = _BLACK; p[7][6] = _BLACK
        p[5][10] = _BLACK; p[5][12] = _BLACK
        p[6][11] = _BLACK
        p[7][10] = _BLACK; p[7][12] = _BLACK
    elif style == "one_closed":
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][9] = _BLACK


# --- Mouth ---

def _draw_mouth(p, style):
    """Draw mouth on face."""
    if style == "smile":
        p[10][5] = _BLACK; p[10][6] = _BLACK; p[10][7] = _BLACK
        p[10][8] = _BLACK; p[10][9] = _BLACK; p[10][10] = _BLACK
        p[9][4] = _BLACK; p[9][11] = _BLACK
    elif style == "grin":
        p[10][5] = _BLACK; p[10][6] = _BLACK; p[10][7] = _BLACK
        p[10][8] = _BLACK; p[10][9] = _BLACK; p[10][10] = _BLACK
        p[9][4] = _BLACK; p[9][11] = _BLACK
        p[10][6] = _WHITE; p[10][7] = _WHITE; p[10][8] = _WHITE; p[10][9] = _WHITE
        p[11][5] = _BLACK; p[11][6] = _BLACK; p[11][7] = _BLACK
        p[11][8] = _BLACK; p[11][9] = _BLACK; p[11][10] = _BLACK
    elif style == "laugh":
        p[9][5] = _BLACK; p[9][6] = _BLACK; p[9][7] = _BLACK
        p[9][8] = _BLACK; p[9][9] = _BLACK; p[9][10] = _BLACK
        p[10][5] = _BLACK; p[10][6] = _RED; p[10][7] = _RED
        p[10][8] = _RED; p[10][9] = _RED; p[10][10] = _BLACK
        p[11][5] = _BLACK; p[11][6] = _RED; p[11][7] = _RED
        p[11][8] = _RED; p[11][9] = _RED; p[11][10] = _BLACK
        p[12][6] = _BLACK; p[12][7] = _BLACK; p[12][8] = _BLACK; p[12][9] = _BLACK
    elif style == "sad":
        p[11][5] = _BLACK; p[11][6] = _BLACK; p[11][7] = _BLACK
        p[11][8] = _BLACK; p[11][9] = _BLACK; p[11][10] = _BLACK
        p[10][4] = _BLACK; p[10][11] = _BLACK
    elif style == "frown":
        p[11][5] = _BLACK; p[11][6] = _BLACK; p[11][7] = _BLACK
        p[11][8] = _BLACK; p[11][9] = _BLACK; p[11][10] = _BLACK
        p[10][5] = _BLACK; p[10][10] = _BLACK
    elif style == "open":
        for dy in range(2):
            for dx in range(2):
                p[10 + dy][7 + dx] = _BLACK
    elif style == "open_big":
        for dy in range(3):
            for dx in range(4):
                p[9 + dy][6 + dx] = _BLACK
        p[10][7] = _RED; p[10][8] = _RED
    elif style == "wavy":
        p[10][5] = _BLACK; p[10][6] = _BLACK
        p[11][7] = _BLACK; p[11][8] = _BLACK
        p[10][9] = _BLACK; p[10][10] = _BLACK
    elif style == "flat":
        for x in range(5, 11):
            p[10][x] = _BLACK
    elif style == "kiss":
        p[9][7] = _RED; p[9][8] = _RED
        p[10][6] = _RED; p[10][9] = _RED
        p[11][7] = _RED; p[11][8] = _RED


# --- Brows ---

def _draw_brows(p, style):
    """Draw eyebrows."""
    if style == "angry":
        p[3][3] = _BLACK; p[3][4] = _BLACK; p[4][5] = _BLACK; p[4][6] = _BLACK
        p[3][12] = _BLACK; p[3][11] = _BLACK; p[4][10] = _BLACK; p[4][9] = _BLACK
    elif style == "angry_deep":
        p[4][3] = _BLACK; p[4][4] = _BLACK; p[4][5] = _BLACK; p[5][6] = _BLACK
        p[4][12] = _BLACK; p[4][11] = _BLACK; p[4][10] = _BLACK; p[5][9] = _BLACK
    elif style == "worried":
        p[4][4] = _BLACK; p[4][5] = _BLACK; p[3][6] = _BLACK
        p[4][11] = _BLACK; p[4][10] = _BLACK; p[3][9] = _BLACK


# --- Effects ---

def _draw_tear(p, side="left"):
    if side == "left":
        p[7][3] = _BLUE; p[8][3] = _BLUE; p[9][3] = _BLUE
    elif side == "right":
        p[7][12] = _BLUE; p[8][12] = _BLUE; p[9][12] = _BLUE
    elif side == "both":
        p[7][3] = _BLUE; p[8][3] = _BLUE; p[9][3] = _BLUE
        p[7][12] = _BLUE; p[8][12] = _BLUE; p[9][12] = _BLUE


def _draw_sweat(p, side="left"):
    if side == "left":
        p[3][2] = _BLUE; p[4][2] = _BLUE
    elif side == "both":
        p[3][2] = _BLUE; p[4][2] = _BLUE
        p[3][13] = _BLUE; p[4][13] = _BLUE


def _draw_zzz(p):
    z = _WHITE
    p[1][11] = z; p[1][12] = z; p[1][13] = z
    p[2][12] = z
    p[3][11] = z; p[3][12] = z; p[3][13] = z
    p[4][13] = z; p[4][14] = z
    p[5][14] = z


def _draw_sunglasses(p):
    g = _BLACK
    b = (60, 60, 60)
    for x in range(3, 13):
        p[5][x] = g
    for dy in (0, 1, 2):
        for dx in range(4):
            p[6 + dy][3 + dx] = b
            p[6 + dy][9 + dx] = b


def _draw_sunglasses_shine(p):
    _draw_sunglasses(p)
    p[6][4] = _WHITE; p[6][5] = _WHITE
    p[6][10] = _WHITE; p[6][11] = _WHITE


def _draw_exclaim(p):
    e = _RED
    p[1][14] = e; p[2][14] = e; p[3][14] = e; p[4][14] = e
    p[6][14] = e


def _draw_confetti(p, density=1):
    colors = [_RED, _BLUE, _GREEN, _PURPLE, _CYAN, (255, 150, 0), _PINK]
    spots_1 = [(1, 2), (2, 13), (1, 8), (3, 0), (2, 5), (0, 11)]
    spots_2 = spots_1 + [(0, 4), (1, 10), (3, 7), (0, 14), (2, 1), (1, 6),
                          (14, 3), (14, 10), (13, 7), (15, 1), (15, 13)]
    spots = spots_1 if density == 1 else spots_2
    for i, (y, x) in enumerate(spots):
        p[y][x] = colors[i % len(colors)]


def _tint_red(p):
    """Add red tint to the Claude face (angry)."""
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


# --- Emotion Animations ---

def happy():
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    f2 = _claude_base()
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "grin")

    f3 = _claude_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "laugh")

    return [f1, f2, f3], [500, 500, 500]


def sad():
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "sad")
    _draw_brows(f1, "worried")

    f2 = _claude_base()
    _draw_eyes(f2, "closed")
    _draw_mouth(f2, "sad")
    _draw_brows(f2, "worried")

    f3 = _claude_base()
    _draw_eyes(f3, "closed")
    _draw_mouth(f3, "sad")
    _draw_brows(f3, "worried")
    _draw_tear(f3, "left")

    return [f1, f2, f3], [600, 600, 600]


def angry():
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "frown")
    _draw_brows(f1, "angry")

    f2 = _claude_base()
    _draw_eyes(f2, "open")
    _draw_mouth(f2, "frown")
    _draw_brows(f2, "angry_deep")

    f3 = _claude_base()
    _tint_red(f3)
    _draw_eyes(f3, "open")
    _draw_mouth(f3, "frown")
    _draw_brows(f3, "angry_deep")

    return [f1, f2, f3], [500, 500, 500]


def love():
    f1 = _claude_base()
    _draw_eyes(f1, "hearts")
    _draw_mouth(f1, "smile")

    f2 = _claude_base()
    _draw_eyes(f2, "hearts_big")
    _draw_mouth(f2, "smile")

    f3 = _claude_base()
    _draw_eyes(f3, "hearts")
    _draw_mouth(f3, "smile")

    return [f1, f2, f3], [400, 400, 400]


def cool():
    f1 = _claude_base()
    _draw_sunglasses(f1)
    _draw_mouth(f1, "smile")

    f2 = _claude_base()
    _draw_sunglasses_shine(f2)
    _draw_mouth(f2, "smile")

    return [f1, f2], [600, 600]


def cry():
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "sad")

    f2 = _claude_base()
    _draw_eyes(f2, "closed")
    _draw_mouth(f2, "sad")
    _draw_tear(f2, "left")

    f3 = _claude_base()
    _draw_eyes(f3, "closed")
    _draw_mouth(f3, "sad")
    _draw_tear(f3, "right")

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
    _draw_tear(f3, "left")

    return [f1, f2, f3], [400, 400, 400]


def sleepy():
    f1 = _claude_base()
    _draw_eyes(f1, "half")
    _draw_mouth(f1, "flat")

    f2 = _claude_base()
    _draw_eyes(f2, "closed")
    _draw_mouth(f2, "flat")

    f3 = _claude_base()
    _draw_eyes(f3, "closed")
    _draw_mouth(f3, "flat")
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
    _draw_mouth(f1, "smile")

    f2 = _claude_base()
    _draw_eyes(f2, "one_closed")
    _draw_mouth(f2, "smile")

    f3 = _claude_base()
    _draw_eyes(f3, "open")
    _draw_mouth(f3, "smile")

    return [f1, f2, f3], [500, 500, 500]


def sick():
    f1 = _claude_base_sick()
    _draw_eyes(f1, "dizzy")
    _draw_mouth(f1, "wavy")

    f2 = _claude_base_sick()
    _draw_eyes(f2, "dizzy")
    _draw_mouth(f2, "wavy")
    _draw_sweat(f2, "left")

    f3 = _claude_base_sick()
    _draw_eyes(f3, "dizzy")
    _draw_mouth(f3, "wavy")
    _draw_sweat(f3, "both")

    return [f1, f2, f3], [600, 600, 600]


def party():
    f1 = _claude_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "grin")

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
    _draw_mouth(f1, "kiss")

    f2 = _claude_base()
    _draw_eyes(f2, "one_closed")
    _draw_mouth(f2, "kiss")
    _draw_flying_heart(f2, 12, 4)

    f3 = _claude_base()
    _draw_eyes(f3, "one_closed")
    _draw_mouth(f3, "kiss")
    _draw_flying_heart(f3, 13, 1)

    return [f1, f2, f3], [400, 400, 400]


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
}
