"""
Emotion Preset Animations for Tivoo

Animated emoji presets built from composable face components.
Each emotion returns (frames, delays) for multi-frame animation.
"""

import copy

# --- Colors ---

_BG = (0, 0, 0)
_YELLOW = (255, 220, 50)
_DARK_Y = (220, 180, 30)
_BLACK = (40, 30, 20)
_WHITE = (255, 255, 255)
_RED = (255, 50, 50)
_PINK = (255, 140, 160)
_BLUE = (80, 150, 255)
_GREEN = (100, 200, 80)
_SICK_G = (140, 200, 80)
_SICK_D = (120, 170, 60)
_ORANGE = (255, 150, 0)
_PURPLE = (180, 100, 255)
_CYAN = (0, 220, 255)


# --- Base ---

def _empty():
    return [[_BG] * 16 for _ in range(16)]


def _circle(cx, cy, r, pixels, color):
    for y in range(16):
        for x in range(16):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                pixels[y][x] = color


def _face_base(color=None):
    """Yellow circle face base."""
    p = _empty()
    c = color or _YELLOW
    _circle(7.5, 7.5, 6.5, p, c)
    return p


def _face_base_sick():
    """Green-tinted face for sick emoji."""
    p = _empty()
    _circle(7.5, 7.5, 6.5, p, _SICK_G)
    return p


# --- Eyes ---

def _draw_eyes(p, style):
    """Draw eyes on face.

    Styles: open, squint, closed, half, wide, hearts, hearts_big, dizzy, one_closed
    """
    if style == "open":
        # 2x2 dot eyes
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = _BLACK
                p[5 + dy][10 + dx] = _BLACK
    elif style == "squint":
        # Horizontal line eyes (happy squint)
        p[6][4] = _BLACK; p[6][5] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK
    elif style == "closed":
        # Closed eyes (3px, one wider than open on right)
        p[6][4] = _BLACK; p[6][5] = _BLACK; p[6][6] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][12] = _BLACK
    elif style == "half":
        # Half-closed (sleepy)
        p[6][4] = _BLACK; p[6][5] = _BLACK
        p[5][4] = _DARK_Y; p[5][5] = _DARK_Y
        p[6][10] = _BLACK; p[6][11] = _BLACK
        p[5][10] = _DARK_Y; p[5][11] = _DARK_Y
    elif style == "wide":
        # Wide open (shocked) — 3x3
        for dy in range(3):
            for dx in range(3):
                p[4 + dy][4 + dx] = _WHITE
                p[4 + dy][9 + dx] = _WHITE
        p[5][5] = _BLACK
        p[5][10] = _BLACK
    elif style == "wider":
        # Even wider (more shocked)
        for dy in range(3):
            for dx in range(3):
                p[4 + dy][3 + dx] = _WHITE
                p[4 + dy][9 + dx] = _WHITE
        for dy in (0, 1):
            for dx in (0, 1):
                p[4 + dy][4 + dx] = _BLACK
                p[4 + dy][10 + dx] = _BLACK
    elif style == "hearts":
        # Small heart eyes (3x3) — symmetric
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
        # Bigger heart eyes (4x4) — symmetric
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
        # X-shaped eyes (symmetric about 7.5)
        p[5][4] = _BLACK; p[5][6] = _BLACK
        p[6][5] = _BLACK
        p[7][4] = _BLACK; p[7][6] = _BLACK
        p[5][9] = _BLACK; p[5][11] = _BLACK
        p[6][10] = _BLACK
        p[7][9] = _BLACK; p[7][11] = _BLACK
    elif style == "one_closed":
        # Left open, right wink
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][9] = _BLACK
    elif style == "lookup":
        # Looking up (thinking)
        for dx in (0, 1):
            p[4][4 + dx] = _BLACK; p[4][10 + dx] = _BLACK
        p[5][4] = _BLACK; p[5][10] = _BLACK
    elif style == "focused":
        # Focused/determined narrow eyes
        p[6][4] = _BLACK; p[6][5] = _BLACK; p[6][6] = _BLACK
        p[5][4] = _BLACK; p[5][6] = _BLACK
        p[6][10] = _BLACK; p[6][11] = _BLACK; p[6][9] = _BLACK
        p[5][9] = _BLACK; p[5][11] = _BLACK
    elif style == "cross":
        # X eyes (error)
        p[5][4] = _RED; p[5][6] = _RED; p[6][5] = _RED; p[7][4] = _RED; p[7][6] = _RED
        p[5][10] = _RED; p[5][12] = _RED; p[6][11] = _RED; p[7][10] = _RED; p[7][12] = _RED


# --- Mouth ---

def _draw_mouth(p, style):
    """Draw mouth on face.

    Styles: smile, grin, laugh, sad, frown, open, wavy, flat, open_big
    """
    if style == "smile":
        # Simple smile curve
        p[10][5] = _BLACK; p[10][6] = _BLACK; p[10][7] = _BLACK
        p[10][8] = _BLACK; p[10][9] = _BLACK; p[10][10] = _BLACK
        p[9][4] = _BLACK; p[9][11] = _BLACK
    elif style == "grin":
        # Wide grin
        p[10][5] = _BLACK; p[10][6] = _BLACK; p[10][7] = _BLACK
        p[10][8] = _BLACK; p[10][9] = _BLACK; p[10][10] = _BLACK
        p[9][4] = _BLACK; p[9][11] = _BLACK
        # Show teeth
        p[10][6] = _WHITE; p[10][7] = _WHITE; p[10][8] = _WHITE; p[10][9] = _WHITE
        p[11][5] = _BLACK; p[11][6] = _BLACK; p[11][7] = _BLACK
        p[11][8] = _BLACK; p[11][9] = _BLACK; p[11][10] = _BLACK
    elif style == "laugh":
        # Open mouth laughing
        p[9][5] = _BLACK; p[9][6] = _BLACK; p[9][7] = _BLACK
        p[9][8] = _BLACK; p[9][9] = _BLACK; p[9][10] = _BLACK
        p[10][5] = _BLACK; p[10][6] = _RED; p[10][7] = _RED
        p[10][8] = _RED; p[10][9] = _RED; p[10][10] = _BLACK
        p[11][5] = _BLACK; p[11][6] = _RED; p[11][7] = _RED
        p[11][8] = _RED; p[11][9] = _RED; p[11][10] = _BLACK
        p[12][6] = _BLACK; p[12][7] = _BLACK; p[12][8] = _BLACK; p[12][9] = _BLACK
    elif style == "sad":
        # Small frown
        p[10][6] = _BLACK; p[10][7] = _BLACK; p[10][8] = _BLACK; p[10][9] = _BLACK
        p[11][5] = _BLACK; p[11][10] = _BLACK
    elif style == "frown":
        # Angry frown
        p[10][5] = _BLACK; p[10][6] = _BLACK; p[10][7] = _BLACK
        p[10][8] = _BLACK; p[10][9] = _BLACK; p[10][10] = _BLACK
        p[11][5] = _BLACK; p[11][10] = _BLACK
    elif style == "open":
        # Small open mouth (surprise)
        for dy in range(2):
            for dx in range(2):
                p[10 + dy][7 + dx] = _BLACK
    elif style == "open_big":
        # Big open mouth (shock)
        for dy in range(3):
            for dx in range(4):
                p[9 + dy][6 + dx] = _BLACK
        p[10][7] = _RED; p[10][8] = _RED
    elif style == "wavy":
        # Wavy mouth (sick/uneasy)
        p[10][5] = _BLACK; p[10][6] = _BLACK
        p[11][7] = _BLACK; p[11][8] = _BLACK
        p[10][9] = _BLACK; p[10][10] = _BLACK
    elif style == "flat":
        # Flat line mouth
        for x in range(5, 11):
            p[10][x] = _BLACK
    elif style == "kiss":
        # Puckered lips
        p[9][7] = _RED; p[9][8] = _RED
        p[10][6] = _RED; p[10][9] = _RED
        p[11][7] = _RED; p[11][8] = _RED
    elif style == "determined":
        # Tight determined mouth
        p[10][6] = _BLACK; p[10][7] = _BLACK; p[10][8] = _BLACK; p[10][9] = _BLACK
    elif style == "small":
        p[10][7] = _BLACK; p[10][8] = _BLACK


# --- Brows ---

def _draw_brows(p, style):
    """Draw eyebrows.

    Styles: angry, angry_deep, worried
    """
    if style == "angry":
        # Angry V brows
        p[3][3] = _BLACK; p[3][4] = _BLACK; p[4][5] = _BLACK; p[4][6] = _BLACK
        p[3][12] = _BLACK; p[3][11] = _BLACK; p[4][10] = _BLACK; p[4][9] = _BLACK
    elif style == "angry_deep":
        # More intense angry brows (lower)
        p[4][3] = _BLACK; p[4][4] = _BLACK; p[4][5] = _BLACK; p[5][6] = _BLACK
        p[4][12] = _BLACK; p[4][11] = _BLACK; p[4][10] = _BLACK; p[5][9] = _BLACK
    elif style == "flat":
        # Flat horizontal brows — wide
        p[4][3] = _BLACK; p[4][4] = _BLACK; p[4][5] = _BLACK; p[4][6] = _BLACK
        p[4][9] = _BLACK; p[4][10] = _BLACK; p[4][11] = _BLACK; p[4][12] = _BLACK
    elif style == "worried":
        # Worried brows (opposite angle)
        p[4][4] = _BLACK; p[4][5] = _BLACK; p[3][6] = _BLACK
        p[4][11] = _BLACK; p[4][10] = _BLACK; p[3][9] = _BLACK


# --- Extras / Effects ---

def _draw_tear(p, side="both", heavy=False):
    """Draw teardrops below eyes."""
    lb = _BLUE
    lw = (150, 200, 255)
    if side in ("left", "both"):
        p[7][4] = lb; p[8][4] = lb; p[9][4] = lb
        if heavy:
            p[10][4] = lb
            p[8][3] = lw; p[9][3] = lw
            p[8][5] = lw
    if side in ("right", "both"):
        p[7][11] = lb; p[8][11] = lb; p[9][11] = lb
        if heavy:
            p[10][11] = lb
            p[8][12] = lw; p[9][12] = lw
            p[8][10] = lw


def _draw_sweat(p, side="left"):
    """Draw sweat drops."""
    if side == "left":
        p[3][2] = _BLUE; p[4][2] = _BLUE
    elif side == "both":
        p[3][2] = _BLUE; p[4][2] = _BLUE
        p[3][13] = _BLUE; p[4][13] = _BLUE


def _draw_zzz(p):
    """Draw Z for sleepy."""
    z = _WHITE
    p[1][11] = z; p[1][12] = z; p[1][13] = z
    p[2][13] = z
    p[3][12] = z
    p[4][11] = z
    p[5][11] = z; p[5][12] = z; p[5][13] = z
    p[5][14] = z


def _draw_sunglasses(p):
    """Draw sunglasses."""
    g = _BLACK
    b = (60, 60, 60)
    # Bridge
    for x in range(3, 13):
        p[5][x] = g
    # Left lens
    for dy in (0, 1, 2):
        for dx in range(4):
            p[6 + dy][3 + dx] = b
    # Right lens
    for dy in (0, 1, 2):
        for dx in range(4):
            p[6 + dy][9 + dx] = b


def _draw_sunglasses_shine(p):
    """Draw sunglasses with shine effect."""
    _draw_sunglasses(p)
    p[6][4] = _WHITE; p[6][5] = _WHITE
    p[6][10] = _WHITE; p[6][11] = _WHITE


def _draw_exclaim(p):
    """Draw exclamation mark."""
    e = _RED
    p[1][14] = e; p[2][14] = e; p[3][14] = e; p[4][14] = e
    p[6][14] = e


def _draw_dots(p, count=3):
    """Draw thinking dots above head."""
    d = _WHITE
    positions = [(1, 5), (1, 7), (1, 9)]
    for i in range(min(count, 3)):
        y, x = positions[i]
        p[y][x] = d


def _draw_confetti(p, density=1):
    """Draw confetti particles."""
    import random
    random.seed(42)  # Deterministic
    colors = [_RED, _BLUE, _GREEN, _PURPLE, _CYAN, _ORANGE, _PINK]
    spots_1 = [(1, 2), (2, 13), (1, 8), (3, 0), (2, 5), (0, 11)]
    spots_2 = spots_1 + [(0, 4), (1, 10), (3, 7), (0, 14), (2, 1), (1, 6),
                          (14, 3), (14, 10), (13, 7), (15, 1), (15, 13)]
    spots = spots_1 if density == 1 else spots_2
    for i, (y, x) in enumerate(spots):
        p[y][x] = colors[i % len(colors)]


def _tint_red(p):
    """Add red tint to the face (for angry)."""
    for y in range(16):
        for x in range(16):
            r, g, b = p[y][x]
            if (r, g, b) == _YELLOW:
                p[y][x] = (255, 160, 30)
            elif (r, g, b) == _DARK_Y:
                p[y][x] = (230, 130, 20)


# --- Emotion Animations ---
# Each returns (frames_list, delays_list)

def happy():
    """Happy face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    f2 = _face_base()
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "grin")

    f3 = _face_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "laugh")

    return [f1, f2, f3], [500, 500, 500]


def sad():
    """Sad face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "sad")

    f2 = _face_base()
    _draw_eyes(f2, "closed")
    _draw_mouth(f2, "sad")

    f3 = _face_base()
    _draw_eyes(f3, "closed")
    _draw_mouth(f3, "sad")
    _draw_tear(f3)

    return [f1, f2, f3], [600, 600, 600]


def angry():
    """Angry face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "flat")
    _draw_brows(f1, "flat")

    f2 = _face_base()
    _draw_eyes(f2, "open")
    _draw_mouth(f2, "frown")
    _draw_brows(f2, "angry_deep")

    f3 = _face_base()
    _tint_red(f3)
    _draw_eyes(f3, "open")
    _draw_mouth(f3, "frown")
    _draw_brows(f3, "angry_deep")

    return [f1, f2, f3], [500, 500, 500]


def love():
    """Love face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "hearts")
    _draw_mouth(f1, "smile")

    f2 = _face_base()
    _draw_eyes(f2, "hearts_big")
    _draw_mouth(f2, "smile")

    f3 = _face_base()
    _draw_eyes(f3, "hearts")
    _draw_mouth(f3, "smile")

    return [f1, f2, f3], [400, 400, 400]


def cool():
    """Cool face animation."""
    f1 = _face_base()
    _draw_sunglasses(f1)
    _draw_mouth(f1, "smile")

    f2 = _face_base()
    _draw_sunglasses_shine(f2)
    _draw_mouth(f2, "smile")

    return [f1, f2], [600, 600]


def cry():
    """Crying face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "closed")
    _draw_mouth(f1, "sad")
    _draw_tear(f1, "both")

    f2 = _face_base()
    _draw_eyes(f2, "closed")
    _draw_mouth(f2, "sad")
    _draw_tear(f2, "both", heavy=True)

    f3 = _face_base()
    _draw_eyes(f3, "open")
    _draw_mouth(f3, "sad")
    _draw_tear(f3, "both")

    return [f1, f2, f3], [500, 500, 500]


def laugh():
    """Laughing face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "grin")

    f2 = _face_base()
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "laugh")

    f3 = _face_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "laugh")

    return [f1, f2, f3], [400, 400, 400]


def sleepy():
    """Sleepy face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "half")
    _draw_mouth(f1, "flat")

    f2 = _face_base()
    _draw_eyes(f2, "closed")
    _draw_mouth(f2, "flat")

    f3 = _face_base()
    _draw_eyes(f3, "closed")
    _draw_mouth(f3, "flat")
    _draw_zzz(f3)

    return [f1, f2, f3], [700, 700, 700]


def shock():
    """Shocked face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "wide")
    _draw_mouth(f1, "open")

    f2 = _face_base()
    _draw_eyes(f2, "wider")
    _draw_mouth(f2, "open_big")

    f3 = _face_base()
    _draw_eyes(f3, "wide")
    _draw_mouth(f3, "open_big")
    _draw_exclaim(f3)

    return [f1, f2, f3], [400, 400, 400]


def wink():
    """Winking face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    f2 = _face_base()
    _draw_eyes(f2, "one_closed")
    _draw_mouth(f2, "smile")

    f3 = _face_base()
    _draw_eyes(f3, "open")
    _draw_mouth(f3, "smile")

    return [f1, f2, f3], [500, 500, 500]


def sick():
    """Sick face animation."""
    _MID_SICK = (198, 210, 65)

    f1 = _face_base()
    _draw_eyes(f1, "dizzy")
    _draw_mouth(f1, "wavy")

    f2 = _face_base(_MID_SICK)
    _draw_eyes(f2, "dizzy")
    _draw_mouth(f2, "wavy")
    _draw_sweat(f2, "left")

    f3 = _face_base_sick()
    _draw_eyes(f3, "dizzy")
    _draw_mouth(f3, "wavy")
    _draw_sweat(f3, "both")

    return [f1, f2, f3], [600, 600, 600]


def party():
    """Party face animation."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "grin")

    f2 = _face_base()
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "laugh")
    _draw_confetti(f2, density=1)

    f3 = _face_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "laugh")
    _draw_confetti(f3, density=2)

    return [f1, f2, f3], [400, 400, 400]


def _draw_flying_heart(p, x, y):
    """Draw a small 3x3 heart at position."""
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


def kiss():
    """Flying kiss animation."""
    f1 = _face_base()
    _draw_eyes(f1, "one_closed")
    _draw_mouth(f1, "small")

    f2 = _face_base()
    _draw_eyes(f2, "one_closed")
    _draw_mouth(f2, "kiss")
    _draw_flying_heart(f2, 12, 4)

    f3 = _face_base()
    _draw_eyes(f3, "one_closed")
    _draw_mouth(f3, "kiss")
    _draw_flying_heart(f3, 13, 1)

    return [f1, f2, f3], [400, 400, 400]


def standby():
    """Standby blink animation with subtle expression change."""
    # Standing smile
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    # Blink
    f2 = _face_base()
    _draw_eyes(f2, "half")
    _draw_mouth(f2, "smile")

    f3 = _face_base()
    _draw_eyes(f3, "closed")
    _draw_mouth(f3, "smile")

    f4 = _face_base()
    _draw_eyes(f4, "open")
    _draw_mouth(f4, "smile")

    # Look up briefly
    f5 = _face_base()
    _draw_eyes(f5, "lookup")
    _draw_mouth(f5, "smile")

    f6 = _face_base()
    _draw_eyes(f6, "open")
    _draw_mouth(f6, "smile")

    return [f1, f2, f3, f4, f5, f6], [2000, 200, 200, 1500, 500, 300]


def thinking():
    """Thinking face — eyes look up, dots appear."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "small")

    f2 = _face_base()
    _draw_eyes(f2, "lookup")
    _draw_mouth(f2, "small")

    f3 = _face_base()
    _draw_eyes(f3, "lookup")
    _draw_mouth(f3, "small")
    _draw_dots(f3, 1)

    f4 = _face_base()
    _draw_eyes(f4, "lookup")
    _draw_mouth(f4, "small")
    _draw_dots(f4, 2)

    f5 = _face_base()
    _draw_eyes(f5, "lookup")
    _draw_mouth(f5, "small")
    _draw_dots(f5, 3)

    return [f1, f2, f3, f4, f5], [600, 400, 400, 400, 400]


# --- Workflow Helpers ---

def _face_base_at(cx=7.5, cy=7.5, color=None):
    """Yellow circle face at custom center position."""
    p = _empty()
    _circle(cx, cy, 6.5, p, color or _YELLOW)
    return p


def _mini_face(p, cx, cy, color=None):
    """Draw small circle face with dot eyes and smile mouth."""
    c = color or _YELLOW
    _circle(cx, cy, 3.5, p, c)
    iy = int(cy)
    ix = int(cx)
    # eyes: moved outward
    if 0 <= iy - 1 < 16 and 0 <= ix - 2 < 16:
        p[iy - 1][ix - 2] = _BLACK
    if 0 <= iy - 1 < 16 and 0 <= ix + 2 < 16:
        p[iy - 1][ix + 2] = _BLACK
    # smile mouth: 3px wide
    if 0 <= iy + 1 < 16:
        for dx in (-1, 0, 1):
            if 0 <= ix + dx < 16:
                p[iy + 1][ix + dx] = _BLACK


def _draw_gear(p, phase=0):
    """Draw gear at top-right with clockwise chase highlight."""
    g = (170, 170, 170)
    h = (80, 80, 80)
    bright = (240, 240, 240)
    base = (110, 110, 110)

    def px(r, c, color=g):
        if 0 <= r < 16 and 0 <= c < 16:
            p[r][c] = color

    # Center body (2-4-4-2)
    px(1, 11); px(1, 12)
    px(2, 10); px(2, 11); px(2, 12); px(2, 13)
    px(3, 10); px(3, 11); px(3, 12); px(3, 13)
    px(4, 11); px(4, 12)
    # Axle hole
    px(2, 11, h); px(2, 12, h)
    px(3, 11, h); px(3, 12, h)
    # 8 teeth clockwise
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
    lit = {phase * 2 % 8, (phase * 2 + 1) % 8}
    for i, positions in enumerate(teeth):
        color = bright if i in lit else base
        for r, c in positions:
            px(r, c, color)


def _draw_bell_default(p, cx, tilt=0):
    """Draw narrow rounded bell for default emoji — silver to contrast yellow face."""
    g = (200, 200, 210)   # silver
    d = (150, 150, 160)   # dark silver
    w = _WHITE
    x = cx + tilt

    def px(r, c, color):
        if 0 <= r < 16 and 0 <= c < 16:
            p[r][c] = color

    px(0, x, w)
    px(1, x - 1, d); px(1, x, g); px(1, x + 1, d)
    for row in (2, 3, 4, 5):
        for dx in range(-2, 3):
            px(row, x + dx, d if abs(dx) == 2 else g)
    for dx in range(-3, 4):
        px(6, x + dx, d if abs(dx) == 3 else g)
    px(7, x + tilt, w)


def _draw_checkbox_default(p, y, x, checked=False):
    """Draw 3x3 checkbox. Checked = green center dot."""
    w = _WHITE
    p[y][x] = w;     p[y][x+1] = w;     p[y][x+2] = w
    p[y+1][x] = w;   p[y+1][x+1] = _BG; p[y+1][x+2] = w
    p[y+2][x] = w;   p[y+2][x+1] = w;   p[y+2][x+2] = w
    if checked:
        p[y+1][x+1] = _GREEN


def _draw_question_mark_default(p, y, x):
    """Draw ? mark. 3 wide, 6 tall."""
    c = _WHITE
    p[y][x] = c; p[y][x+1] = c; p[y][x+2] = c
    p[y+1][x+2] = c
    p[y+2][x+1] = c
    p[y+3][x+1] = c
    p[y+5][x+1] = c


def _draw_checkmark_default(p, y, x, color=None):
    """Draw ✓ at right side — same shape as Claude done."""
    c = color or _GREEN
    #   col: x  x+1 x+2 x+3 x+4 x+5
    # y+0: .   .    .    .    .    X
    # y+1: .   .    .    .    X    .
    # y+2: X   .    .    X    .    .
    # y+3: .   X    X    .    .    .
    p[y][x+5] = c
    p[y+1][x+4] = c
    p[y+2][x+3] = c; p[y+2][x] = c
    p[y+3][x+2] = c; p[y+3][x+1] = c


# --- Workflow Emotions ---

def working():
    """Working — focused expression, mumbling mouth, steam rising."""
    _STEAM = (200, 200, 220)  # light gray-blue

    f1 = _face_base()
    _draw_eyes(f1, "focused")
    _draw_mouth(f1, "determined")

    f2 = _face_base()
    _draw_eyes(f2, "focused")
    _draw_mouth(f2, "open")
    f2[1][6] = _STEAM

    f3 = _face_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "flat")
    f3[0][7] = _STEAM
    f3[1][9] = _STEAM

    f4 = _face_base()
    _draw_eyes(f4, "focused")
    _draw_mouth(f4, "open")
    f4[0][8] = _STEAM
    f4[1][6] = _STEAM

    return [f1, f2, f3, f4], [600, 400, 400, 400]


def subagent():
    """Subagent — face fades left, two mini faces split up and down."""
    _DIM = (200, 180, 40)    # dimmed yellow
    _FADE = (150, 130, 25)   # very faded yellow

    # F1: normal face
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    # F2: face shifts left + dims, two dim mini faces appear
    f2 = _face_base_at(4.5, 7.5, _DIM)
    # eyes shifted left (cx 4.5 vs normal 7.5 = -3)
    for dy in (0, 1):
        f2[5 + dy][1] = _BLACK; f2[5 + dy][2] = _BLACK
        f2[5 + dy][7] = _BLACK; f2[5 + dy][8] = _BLACK
    # small mouth shifted left
    f2[10][4] = _BLACK; f2[10][5] = _BLACK
    _mini_face(f2, 12, 5, _DIM)
    _mini_face(f2, 12, 11, _DIM)

    # F3: face almost off-screen, bright mini faces split further apart
    f3 = _face_base_at(1.5, 7.5, _FADE)
    # eyes on faded face (cx 1.5 = shift -6)
    for dy in (0, 1):
        f3[5 + dy][0] = _BLACK
        f3[5 + dy][4] = _BLACK; f3[5 + dy][5] = _BLACK
    _mini_face(f3, 11, 3)
    _mini_face(f3, 11, 12)

    return [f1, f2, f3], [600, 400, 400]


def done():
    """Done — bounce + checkmark + sparkles."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    # Bounce up (cy=6.5, shift -1)
    f2 = _face_base_at(7.5, 6.5)
    # squint eyes shifted up 1
    f2[5][4] = _BLACK; f2[5][5] = _BLACK
    f2[5][10] = _BLACK; f2[5][11] = _BLACK
    # grin mouth shifted up 1 (matches _draw_mouth "grin" exactly)
    f2[8][4] = _BLACK; f2[8][11] = _BLACK
    for x in range(5, 11):
        f2[9][x] = _BLACK
    f2[9][6] = _WHITE; f2[9][7] = _WHITE; f2[9][8] = _WHITE; f2[9][9] = _WHITE
    for x in range(5, 11):
        f2[10][x] = _BLACK

    # Settle + checkmark
    f3 = _face_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "grin")
    _draw_checkmark_default(f3, 2, 10)

    # Sparkles
    f4 = _face_base()
    _draw_eyes(f4, "squint")
    _draw_mouth(f4, "laugh")
    _draw_checkmark_default(f4, 2, 10)
    _draw_confetti(f4, density=2)

    return [f1, f2, f3, f4], [400, 300, 400, 500]


def notify():
    """Notify — bell sways, face reacts."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    f2 = _face_base()
    _draw_eyes(f2, "open")
    _draw_mouth(f2, "open")
    _draw_bell_default(f2, 12, tilt=0)

    f3 = _face_base()
    _draw_eyes(f3, "half")
    _draw_mouth(f3, "open_big")
    _draw_bell_default(f3, 12, tilt=-1)

    f4 = _face_base()
    _draw_eyes(f4, "open")
    _draw_mouth(f4, "open")
    _draw_bell_default(f4, 12, tilt=1)

    f5 = _face_base()
    _draw_eyes(f5, "closed")
    _draw_mouth(f5, "open_big")
    _draw_bell_default(f5, 12, tilt=0)

    return [f1, f2, f3, f4, f5], [500, 300, 300, 300, 400]


def tooluse():
    """Tool use — gear rotates at top-right."""
    f1 = _face_base()
    _draw_eyes(f1, "focused")
    _draw_mouth(f1, "determined")
    _draw_gear(f1, phase=0)

    f2 = _face_base()
    _draw_eyes(f2, "focused")
    _draw_mouth(f2, "determined")
    _draw_gear(f2, phase=1)

    f3 = _face_base()
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "determined")
    _draw_gear(f3, phase=2)

    f4 = _face_base()
    _draw_eyes(f4, "focused")
    _draw_mouth(f4, "determined")
    _draw_gear(f4, phase=3)

    return [f1, f2, f3, f4], [300, 300, 300, 300]


def oops():
    """Oops — dizzy eyes + exclamation + face shakes."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    f2 = _face_base()
    _draw_eyes(f2, "dizzy")
    _draw_mouth(f2, "open")
    _draw_exclaim(f2)

    # Shake left (cx=6.5, shift -1)
    f3 = _face_base_at(6.5, 7.5)
    _tint_red(f3)
    # dizzy eyes shifted left
    f3[5][3] = _BLACK; f3[5][5] = _BLACK; f3[6][4] = _BLACK
    f3[7][3] = _BLACK; f3[7][5] = _BLACK
    f3[5][8] = _BLACK; f3[5][10] = _BLACK; f3[6][9] = _BLACK
    f3[7][8] = _BLACK; f3[7][10] = _BLACK
    # mouth shifted left
    f3[10][6] = _BLACK; f3[10][7] = _BLACK
    f3[11][6] = _BLACK; f3[11][7] = _BLACK
    _draw_exclaim(f3)

    # Shake right (cx=8.5, shift +1)
    f4 = _face_base_at(8.5, 7.5)
    _tint_red(f4)
    # dizzy eyes shifted right
    f4[5][5] = _BLACK; f4[5][7] = _BLACK; f4[6][6] = _BLACK
    f4[7][5] = _BLACK; f4[7][7] = _BLACK
    f4[5][10] = _BLACK; f4[5][12] = _BLACK; f4[6][11] = _BLACK
    f4[7][10] = _BLACK; f4[7][12] = _BLACK
    # mouth shifted right
    f4[10][8] = _BLACK; f4[10][9] = _BLACK
    f4[11][8] = _BLACK; f4[11][9] = _BLACK
    _draw_exclaim(f4)

    f5 = _face_base()
    _draw_eyes(f5, "dizzy")
    _draw_mouth(f5, "sad")
    _draw_exclaim(f5)

    return [f1, f2, f3, f4, f5], [500, 400, 200, 200, 400]


def tasklist():
    """Tasklist — face shifts left, checkboxes appear."""
    f1 = _face_base_at(5.5, 7.5)
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")

    f2 = _face_base_at(5.5, 7.5)
    _draw_eyes(f2, "lookup")
    _draw_mouth(f2, "small")
    _draw_checkbox_default(f2, 3, 13)

    f3 = _face_base_at(5.5, 7.5)
    _draw_eyes(f3, "lookup")
    _draw_mouth(f3, "small")
    _draw_checkbox_default(f3, 3, 13)
    _draw_checkbox_default(f3, 7, 13)

    f4 = _face_base_at(5.5, 7.5)
    _draw_eyes(f4, "lookup")
    _draw_mouth(f4, "small")
    _draw_checkbox_default(f4, 3, 13)
    _draw_checkbox_default(f4, 7, 13)
    _draw_checkbox_default(f4, 11, 13)

    return [f1, f2, f3, f4], [500, 400, 400, 400]


def taskdone():
    """Task done — checkbox gets checked + confetti."""
    f1 = _face_base_at(5.5, 7.5)
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "smile")
    _draw_checkbox_default(f1, 3, 13, checked=True)
    _draw_checkbox_default(f1, 7, 13)
    _draw_checkbox_default(f1, 11, 13)

    f2 = _face_base_at(5.5, 7.5)
    _draw_eyes(f2, "squint")
    _draw_mouth(f2, "grin")
    _draw_checkbox_default(f2, 3, 13, checked=True)
    _draw_checkbox_default(f2, 7, 13, checked=True)
    _draw_checkbox_default(f2, 11, 13)

    f3 = _face_base_at(5.5, 7.5)
    _draw_eyes(f3, "squint")
    _draw_mouth(f3, "laugh")
    _draw_checkbox_default(f3, 3, 13, checked=True)
    _draw_checkbox_default(f3, 7, 13, checked=True)
    _draw_checkbox_default(f3, 11, 13)
    _draw_confetti(f3, density=2)

    return [f1, f2, f3], [500, 400, 600]


def question():
    """Question — thinking dots then ? sways."""
    f1 = _face_base()
    _draw_eyes(f1, "open")
    _draw_mouth(f1, "small")

    f2 = _face_base()
    _draw_eyes(f2, "lookup")
    _draw_mouth(f2, "small")
    f2[1][7] = _WHITE

    f3 = _face_base()
    _draw_eyes(f3, "lookup")
    _draw_mouth(f3, "small")
    f3[1][6] = _WHITE; f3[1][8] = _WHITE

    f4 = _face_base()
    _draw_eyes(f4, "lookup")
    _draw_mouth(f4, "small")
    f4[1][5] = _WHITE; f4[1][7] = _WHITE; f4[1][9] = _WHITE

    f5 = _face_base()
    _draw_eyes(f5, "open")
    _draw_mouth(f5, "open")
    _draw_question_mark_default(f5, 0, 12)

    f6 = _face_base()
    _draw_eyes(f6, "open")
    _draw_mouth(f6, "open")
    _draw_question_mark_default(f6, 0, 11)

    f7 = _face_base()
    _draw_eyes(f7, "open")
    _draw_mouth(f7, "open")
    _draw_question_mark_default(f7, 0, 12)

    return [f1, f2, f3, f4, f5, f6, f7], [500, 350, 350, 400, 400, 400, 400]

    return [f1, f2, f3, f4, f5, f6], [500, 350, 400, 400, 400, 400]

EMOTION_PRESETS = {
    "happy": ("Happy face", happy),
    "sad": ("Sad face", sad),
    "angry": ("Angry face", angry),
    "love": ("Love face", love),
    "cool": ("Cool face", cool),
    "cry": ("Crying face", cry),
    "laugh": ("Laughing face", laugh),
    "sleepy": ("Sleepy face", sleepy),
    "shock": ("Shocked face", shock),
    "wink": ("Winking face", wink),
    "sick": ("Sick face", sick),
    "party": ("Party face", party),
    "kiss": ("Flying kiss", kiss),
    "standby": ("Standby face", standby),
    "thinking": ("Thinking face", thinking),
    # Workflow emotions
    "working": ("Working face", working),
    "subagent": ("Subagent face", subagent),
    "done": ("Done face", done),
    "notify": ("Notify face", notify),
    "tooluse": ("Tool use face", tooluse),
    "oops": ("Oops face", oops),
    "tasklist": ("Tasklist face", tasklist),
    "taskdone": ("Task done face", taskdone),
    "question": ("Question face", question),
}
