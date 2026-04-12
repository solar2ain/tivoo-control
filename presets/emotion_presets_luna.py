"""
Luna Emotion Preset Animations for Tivoo

Character Luna with composable face components.
Each emotion returns (frames, delays) for multi-frame animation.
"""

# --- Colors ---

_BG = (0, 0, 0)
_H = (140, 60, 200)       # hair purple
_Hd = (100, 40, 160)      # hair dark
_Hl = (180, 100, 240)     # hair highlight
_SK = (255, 230, 215)     # skin
_Sd = (245, 210, 195)     # skin shadow
_EV = (150, 80, 220)      # eye violet
_EP = (80, 30, 140)       # eye pupil
_EW = (255, 255, 255)     # eye white
_EK = (40, 20, 60)        # eyelash
_PK = (255, 150, 170)     # blush pink
_LP = (220, 100, 130)     # lip
_TG = (220, 200, 255)     # tiara silver
_TJ = (180, 80, 255)      # tiara jewel
_SP = (255, 240, 255)     # sparkle
_MG = (220, 160, 255)     # magic purple
_ST = (180, 120, 255)     # star purple
_BLUE = (80, 150, 255)    # tears
_RED = (255, 80, 80)      # angry tint
_GREEN = (140, 200, 80)   # sick
_WHITE = (255, 255, 255)


# --- Luna Base ---

def _blank():
    return [[_BG] * 16 for _ in range(16)]


def _luna_base(skin=None):
    """Build Luna's face base: hair, tiara, face shape, hair curls."""
    sk = skin or _SK
    f = _blank()
    # Hair top
    for x in range(4, 12): f[0][x] = _H
    for x in range(3, 13): f[1][x] = _H
    for x in range(3, 13): f[2][x] = _H
    for x in range(3, 13): f[3][x] = _H
    # Tiara
    f[1][6] = _TG; f[1][7] = _TJ; f[1][8] = _TJ; f[1][9] = _TG
    # Bangs
    f[4][3] = _H; f[4][4] = _Hl; f[4][5] = _H
    f[4][6] = sk; f[4][7] = sk; f[4][8] = sk; f[4][9] = sk
    f[4][10] = _H; f[4][11] = _Hl; f[4][12] = _H
    f[3][4] = _Hl; f[3][11] = _Hl
    # Face
    for y in range(5, 13):
        for x in range(4, 12):
            f[y][x] = sk
    for y in range(6, 12):
        f[y][3] = sk; f[y][12] = sk
    # Hair sides
    for y in range(2, 15):
        f[y][2] = _H; f[y][13] = _H
    for y in range(7, 15):
        f[y][1] = _Hd; f[y][14] = _Hd
    # Lower hair curls inward
    f[12][3] = _H; f[12][12] = _H
    f[13][2] = _H; f[13][3] = _H; f[13][12] = _H; f[13][13] = _H
    f[14][2] = _Hd; f[14][3] = _H; f[14][4] = _Hd
    f[14][11] = _Hd; f[14][12] = _H; f[14][13] = _Hd
    f[15][2] = _Hd; f[15][3] = _Hd; f[15][4] = _H; f[15][5] = _Hl
    f[15][10] = _Hl; f[15][11] = _H; f[15][12] = _Hd; f[15][13] = _Hd
    # Highlights
    f[6][2] = _Hl; f[9][13] = _Hl
    return f


# --- Eyes ---

def _draw_eyes(p, style):
    """Draw Luna's eyes.

    Styles: open, squint, closed, wide, hearts, one_closed, half, dizzy
    """
    if style == "open":
        # Lashes
        p[6][4] = _EK; p[6][5] = _EK; p[6][6] = _EK
        p[6][9] = _EK; p[6][10] = _EK; p[6][11] = _EK
        # Left eye
        p[7][4] = _EW; p[7][5] = _EV; p[7][6] = _EP
        p[8][4] = _EW; p[8][5] = _EV; p[8][6] = _EV
        # Right eye
        p[7][9] = _EP; p[7][10] = _EV; p[7][11] = _EW
        p[8][9] = _EV; p[8][10] = _EV; p[8][11] = _EW

    elif style == "half_open":
        # Compressed open eye — lashes press down, 1 row of eye detail
        p[7][4] = _EK; p[7][5] = _EK; p[7][6] = _EK
        p[7][9] = _EK; p[7][10] = _EK; p[7][11] = _EK
        p[8][4] = _EW; p[8][5] = _EV; p[8][6] = _EP
        p[8][9] = _EP; p[8][10] = _EV; p[8][11] = _EW

    elif style == "squint":
        # Lashes
        p[6][4] = _EK; p[6][5] = _EK; p[6][6] = _EK
        p[6][9] = _EK; p[6][10] = _EK; p[6][11] = _EK
        # Squinted - just iris line
        p[7][4] = _EV; p[7][5] = _EV; p[7][6] = _EV
        p[7][9] = _EV; p[7][10] = _EV; p[7][11] = _EV

    elif style == "happy":
        #  ##        ##
        # #  #      #  #
        # Eyes shift outward by 1 from normal position
        # Left eye (shifted left)
        p[7][4] = _EK; p[7][5] = _EK
        p[8][3] = _EK; p[8][4] = (200, 170, 240); p[8][5] = _EV; p[8][6] = _EK
        # Right eye (shifted right)
        p[7][10] = _EK; p[7][11] = _EK
        p[8][9] = _EK; p[8][10] = _EV; p[8][11] = (200, 170, 240); p[8][12] = _EK

    elif style == "closed":
        p[8][4] = _EK; p[8][5] = _EK; p[8][6] = _EK
        p[8][9] = _EK; p[8][10] = _EK; p[8][11] = _EK

    elif style == "half":
        # Half-closed (sleepy) — 3px iris visible
        p[7][4] = _EK; p[7][5] = _EK; p[7][6] = _EK
        p[7][9] = _EK; p[7][10] = _EK; p[7][11] = _EK
        p[8][4] = _EV; p[8][5] = _EV; p[8][6] = _EV
        p[8][9] = _EV; p[8][10] = _EV; p[8][11] = _EV

    elif style == "wide":
        # Shocked wide eyes
        p[6][4] = _EK; p[6][5] = _EK; p[6][6] = _EK
        p[6][9] = _EK; p[6][10] = _EK; p[6][11] = _EK
        p[7][4] = _EW; p[7][5] = _EW; p[7][6] = _EP
        p[8][4] = _EW; p[8][5] = _EV; p[8][6] = _EV
        p[9][4] = _EW; p[9][5] = _EV; p[9][6] = _EV
        p[7][9] = _EP; p[7][10] = _EW; p[7][11] = _EW
        p[8][9] = _EV; p[8][10] = _EV; p[8][11] = _EW
        p[9][9] = _EV; p[9][10] = _EV; p[9][11] = _EW

    elif style == "hearts":
        h = (255, 80, 130)
        p[6][4] = h; p[6][6] = h
        p[7][4] = h; p[7][5] = h; p[7][6] = h
        p[8][5] = h
        p[6][9] = h; p[6][11] = h
        p[7][9] = h; p[7][10] = h; p[7][11] = h
        p[8][10] = h

    elif style == "one_closed":
        # Left open
        p[6][4] = _EK; p[6][5] = _EK; p[6][6] = _EK
        p[7][4] = _EW; p[7][5] = _EV; p[7][6] = _EP
        p[8][4] = _EW; p[8][5] = _EV; p[8][6] = _EV
        # Right closed (wink)
        p[8][9] = _EK; p[8][10] = _EK; p[8][11] = _EK

    elif style == "one_half_open":
        # Left open, right half-open (wink transition)
        p[6][4] = _EK; p[6][5] = _EK; p[6][6] = _EK
        p[7][4] = _EW; p[7][5] = _EV; p[7][6] = _EP
        p[8][4] = _EW; p[8][5] = _EV; p[8][6] = _EV
        # Right half-open
        p[7][9] = _EK; p[7][10] = _EK; p[7][11] = _EK
        p[8][9] = _EP; p[8][10] = _EV; p[8][11] = _EW

    elif style == "dizzy":
        p[7][4] = _EK; p[7][6] = _EK; p[8][5] = _EK
        p[7][9] = _EK; p[7][11] = _EK; p[8][10] = _EK

    elif style == "lookup":
        # Looking up (thinking) — open eyes shifted up by 1 row
        # Lashes
        p[5][4] = _EK; p[5][5] = _EK; p[5][6] = _EK
        p[5][9] = _EK; p[5][10] = _EK; p[5][11] = _EK
        # Left eye
        p[6][4] = _EW; p[6][5] = _EV; p[6][6] = _EP
        p[7][4] = _EW; p[7][5] = _EV; p[7][6] = _EV
        # Right eye
        p[6][9] = _EP; p[6][10] = _EV; p[6][11] = _EW
        p[7][9] = _EV; p[7][10] = _EV; p[7][11] = _EW

    elif style == "focused":
        # Determined narrow eyes
        p[6][4] = _EK; p[6][5] = _EK; p[6][6] = _EK
        p[6][9] = _EK; p[6][10] = _EK; p[6][11] = _EK
        p[7][4] = _EK; p[7][5] = _EV; p[7][6] = _EK
        p[7][9] = _EK; p[7][10] = _EV; p[7][11] = _EK

    elif style == "cross":
        # X eyes (error)
        r = (255, 80, 80)
        p[7][4] = r; p[7][6] = r; p[8][5] = r; p[6][4] = r; p[6][6] = r
        p[7][9] = r; p[7][11] = r; p[8][10] = r; p[6][9] = r; p[6][11] = r


def _draw_brows(p, style):
    """Draw Luna's eyebrows."""
    _EK = (30, 20, 40)
    if style == "angry":
        # V brows — outer high, inner low (pressed down)
        p[5][3] = _EK; p[5][4] = _EK
        p[6][5] = _EK; p[6][6] = _EK
        p[5][12] = _EK; p[5][11] = _EK
        p[6][10] = _EK; p[6][9] = _EK


# --- Mouth ---

def _draw_mouth(p, style):
    """Draw Luna's mouth at y=11.

    Styles: shy, smile, sad, open, flat, wavy, grin, kiss, determined
    """
    if style == "shy":
        p[11][7] = _LP; p[11][8] = _LP

    elif style == "smile_up":
        # Slight upturn: corners up one row, middle flat
        p[10][6] = _LP; p[10][9] = _LP
        p[11][7] = _LP; p[11][8] = _LP

    elif style == "smile":
        p[11][6] = _LP; p[11][7] = _LP; p[11][8] = _LP; p[11][9] = _LP

    elif style == "grin":
        p[11][6] = _LP; p[11][7] = _EW; p[11][8] = _EW; p[11][9] = _LP
        p[12][7] = _LP; p[12][8] = _LP

    elif style == "sad":
        p[11][6] = _LP; p[11][7] = _LP; p[11][8] = _LP; p[11][9] = _LP

    elif style == "open":
        p[11][7] = _EK; p[11][8] = _EK

    elif style == "flat":
        p[11][6] = _LP; p[11][7] = _LP; p[11][8] = _LP; p[11][9] = _LP

    elif style == "wavy":
        # _--_ shape: middle level, sides droop
        p[11][7] = _LP; p[11][8] = _LP
        p[12][6] = _LP; p[12][9] = _LP

    elif style == "kiss":
        p[11][7] = _LP; p[11][8] = _LP
        p[12][7] = _LP; p[12][8] = _LP

    elif style == "determined":
        p[11][6] = _LP; p[11][7] = _LP; p[11][8] = _LP; p[11][9] = _LP

    elif style == "thinking":
        # Small square mouth, shifted up
        p[10][7] = _LP; p[10][8] = _LP
        p[11][7] = _LP; p[11][8] = _LP


# --- Face Details ---

def _draw_blush(p):
    p[9][4] = _PK; p[9][5] = _PK; p[9][10] = _PK; p[9][11] = _PK


def _draw_nose(p):
    p[10][8] = _Sd


# --- Extras ---

def _draw_tear(p, side="both", heavy=False):
    lb = (80, 150, 255)
    lw = (150, 200, 255)
    if side in ("left", "both"):
        p[8][4] = lb; p[9][4] = lb; p[10][4] = lb
        if heavy:
            p[11][4] = lb
            p[9][3] = lw; p[10][3] = lw
            p[9][5] = lw
    if side in ("right", "both"):
        p[8][11] = lb; p[9][11] = lb; p[10][11] = lb
        if heavy:
            p[11][11] = lb
            p[9][12] = lw; p[10][12] = lw
            p[9][10] = lw


def _draw_sweat(p, side="left"):
    if side == "left":
        p[4][2] = _BLUE; p[5][2] = _BLUE
    elif side == "both":
        p[4][2] = _BLUE; p[5][2] = _BLUE
        p[4][13] = _BLUE; p[5][13] = _BLUE


def _draw_sparkles(p, density=1):
    spots_1 = [(0, 2), (0, 13), (3, 1), (3, 14), (8, 1), (8, 14)]
    spots_2 = spots_1 + [(13, 1), (13, 14), (15, 6), (15, 9), (1, 5), (1, 10)]
    colors = [_SP, _MG, _ST, _SP, _MG, _ST, _SP, _MG, _ST, _SP, _MG, _ST]
    spots = spots_1 if density == 1 else spots_2
    for i, (y, x) in enumerate(spots):
        p[y][x] = colors[i % len(colors)]


def _draw_zzz(p):
    z = _WHITE
    p[1][11] = z; p[1][12] = z; p[1][13] = z
    p[2][13] = z
    p[3][12] = z
    p[4][11] = z
    p[5][11] = z; p[5][12] = z; p[5][13] = z


def _draw_exclaim(p):
    p[2][15] = _RED; p[3][15] = _RED; p[4][15] = _RED; p[6][15] = _RED


def _draw_dots(p, count=3):
    """Draw thinking dots above head."""
    d = _WHITE
    positions = [(0, 6), (0, 8), (0, 10)]
    for i in range(min(count, 3)):
        y, x = positions[i]
        p[y][x] = d


def _draw_confetti(p, density=1):
    colors = [_RED, _BLUE, _GREEN, _ST, (255, 220, 50), _MG]
    spots_1 = [(0, 3), (0, 12), (2, 0), (2, 15), (14, 0), (14, 15)]
    spots_2 = spots_1 + [(0, 7), (0, 8), (15, 6), (15, 9), (1, 1), (1, 14)]
    spots = spots_1 if density == 1 else spots_2
    for i, (y, x) in enumerate(spots):
        p[y][x] = colors[i % len(colors)]


def _tint_red(p):
    """Red angry tint on skin areas."""
    for y in range(16):
        for x in range(16):
            if p[y][x] == _SK:
                p[y][x] = (255, 210, 190)
            elif p[y][x] == _Sd:
                p[y][x] = (240, 185, 165)


def _tint_green(p):
    """Green sick tint on skin areas."""
    for y in range(16):
        for x in range(16):
            if p[y][x] == _SK:
                p[y][x] = (220, 235, 200)
            elif p[y][x] == _Sd:
                p[y][x] = (200, 215, 180)


def _draw_sunglasses(p, shine=False):
    g = _EK
    for x in range(4, 12): p[6][x] = g
    for dy in (0, 1):
        for dx in range(3): p[7 + dy][4 + dx] = g; p[7 + dy][9 + dx] = g
    if shine:
        p[7][4] = _WHITE; p[7][5] = _WHITE
        p[7][9] = _WHITE; p[7][10] = _WHITE


# --- Helper to build a frame ---

def _frame(eyes="open", mouth="shy", blush=True, nose=True, skin=None,
           tear=None, heavy_tear=False, sweat=None, sparkles=0, zzz=False, exclaim=False,
           confetti=0, tint=None, sunglasses=False, sg_shine=False, brows=None, dots=0):
    """Build one Luna frame from components."""
    f = _luna_base(skin)
    if tint == "red":
        _tint_red(f)
    elif tint == "green":
        _tint_green(f)
    if sunglasses:
        _draw_sunglasses(f, sg_shine)
    else:
        _draw_eyes(f, eyes)
    if brows:
        _draw_brows(f, brows)
    if nose:
        _draw_nose(f)
    if blush and eyes != "wide":
        _draw_blush(f)
    _draw_mouth(f, mouth)
    if tear:
        _draw_tear(f, tear, heavy=heavy_tear)
    if sweat:
        _draw_sweat(f, sweat)
    if sparkles:
        _draw_sparkles(f, sparkles)
    if zzz:
        _draw_zzz(f)
    if exclaim:
        _draw_exclaim(f)
    if confetti:
        _draw_confetti(f, confetti)
    if dots:
        _draw_dots(f, dots)
    return f


# --- Emotion Animations ---

def happy():
    """Happy Luna."""
    return [
        _frame(eyes="open", mouth="shy"),
        _frame(eyes="open", mouth="smile"),
        _frame(eyes="half_open", mouth="grin"),
    ], [500, 500, 500]


def sad():
    """Sad Luna."""
    return [
        _frame(eyes="open", mouth="sad"),
        _frame(eyes="closed", mouth="sad"),
        _frame(eyes="closed", mouth="sad", tear="both"),
    ], [600, 600, 600]


def angry():
    """Angry Luna."""
    return [
        _frame(eyes="open", mouth="flat", brows="angry"),
        _frame(eyes="open", mouth="flat", brows="angry", tint="red"),
        _frame(eyes="squint", mouth="flat", brows="angry", tint="red"),
    ], [500, 500, 500]


def love():
    """Love-struck Luna."""
    return [
        _frame(eyes="hearts", mouth="shy"),
        _frame(eyes="hearts", mouth="smile", sparkles=1),
        _frame(eyes="hearts", mouth="shy", sparkles=2),
    ], [400, 400, 400]


def cool():
    """Cool Luna."""
    return [
        _frame(sunglasses=True, mouth="shy"),
        _frame(sunglasses=True, sg_shine=True, mouth="smile"),
    ], [600, 600]


def cry():
    """Crying Luna."""
    return [
        _frame(eyes="closed", mouth="sad", tear="both"),
        _frame(eyes="closed", mouth="sad", tear="both", heavy_tear=True),
        _frame(eyes="open", mouth="sad", tear="both"),
    ], [500, 500, 500]


def laugh():
    """Laughing Luna."""
    return [
        _frame(eyes="open", mouth="grin"),
        _frame(eyes="closed", mouth="grin"),
        _frame(eyes="happy", mouth="grin"),
    ], [400, 400, 400]


def sleepy():
    """Sleepy Luna."""
    return [
        _frame(eyes="half_open", mouth="flat"),
        _frame(eyes="closed", mouth="flat"),
        _frame(eyes="closed", mouth="flat", zzz=True),
    ], [700, 500, 700]


def shock():
    """Shocked Luna."""
    return [
        _frame(eyes="open", mouth="shy", blush=True),
        _frame(eyes="wide", mouth="smile", blush=False, exclaim=True),
        _frame(eyes="wide", mouth="smile", blush=False, exclaim=True, sparkles=1),
    ], [400, 400, 400]


def wink():
    """Winking Luna."""
    return [
        _frame(eyes="open", mouth="shy"),
        _frame(eyes="one_half_open", mouth="shy"),
        _frame(eyes="one_closed", mouth="smile_up", sparkles=1),
    ], [1000, 300, 500]


def sick():
    """Sick Luna."""
    return [
        _frame(eyes="half_open", mouth="flat", blush=False),
        _frame(eyes="half_open", mouth="flat", blush=False, sweat="left"),
        _frame(eyes="half_open", mouth="flat", blush=False, sweat="both"),
        _frame(eyes="half_open", mouth="flat", blush=False, sweat="both", tint="green"),
    ], [600, 600, 600, 600]


def party():
    """Party Luna."""
    return [
        _frame(eyes="open", mouth="grin"),
        _frame(eyes="half_open", mouth="grin", confetti=1),
        _frame(eyes="open", mouth="grin", confetti=2),
    ], [400, 400, 400]


def _draw_flying_heart(p, x, y):
    """Draw a small heart at position."""
    h = (255, 80, 130)
    if 0 <= y < 16 and 0 <= x < 15:
        p[y][x] = h; p[y][x + 1] = h
    if 0 <= y + 1 < 16 and 0 <= x - 1 < 16 and x + 2 < 16:
        p[y + 1][x - 1] = h; p[y + 1][x] = h; p[y + 1][x + 1] = h; p[y + 1][x + 2] = h
    if 0 <= y + 2 < 16 and 0 <= x < 15:
        p[y + 2][x] = h; p[y + 2][x + 1] = h
    if 0 <= y + 3 < 16:
        p[y + 3][x] = h


def kiss():
    """Flying kiss Luna."""
    return [
        _frame(eyes="one_closed", mouth="kiss"),
        _frame(eyes="one_closed", mouth="kiss", sparkles=1),
        _frame(eyes="one_closed", mouth="kiss"),
    ], [400, 400, 400]


def kiss_with_heart():
    """Flying kiss Luna with heart."""
    f1 = _frame(eyes="open", mouth="shy")
    f2 = _frame(eyes="one_half_open", mouth="kiss")
    _draw_flying_heart(f2, 12, 5)
    f3 = _frame(eyes="one_closed", mouth="kiss")
    _draw_flying_heart(f3, 13, 2)
    return [f1, f2, f3], [400, 400, 400]


def standby():
    """Standby Luna — blink, subtle mouth change, tiara breathing."""
    # Standing - tiara normal
    f1 = _frame(eyes="open", mouth="shy")
    f1[1][7] = _TJ; f1[1][8] = _TJ

    # Blink - tiara dim
    f2 = _frame(eyes="half_open", mouth="shy")
    f2[1][7] = _MG; f2[1][8] = _MG

    f3 = _frame(eyes="closed", mouth="shy")
    f3[1][7] = _MG; f3[1][8] = _MG

    # Eyes open - tiara bright
    f4 = _frame(eyes="open", mouth="shy")
    f4[1][7] = _SP; f4[1][8] = _SP

    # Smile - tiara normal
    f5 = _frame(eyes="open", mouth="smile")
    f5[1][7] = _TJ; f5[1][8] = _TJ

    # Back to shy - tiara dim
    f6 = _frame(eyes="open", mouth="shy")
    f6[1][7] = _MG; f6[1][8] = _MG

    return [f1, f2, f3, f4, f5, f6], [2000, 200, 200, 1500, 500, 300]


def thinking():
    """Thinking Luna — eyes look up, dots appear."""
    return [
        _frame(eyes="open", mouth="shy"),
        _frame(eyes="lookup", mouth="thinking"),
        _frame(eyes="lookup", mouth="thinking", dots=1),
        _frame(eyes="lookup", mouth="thinking", dots=2),
        _frame(eyes="lookup", mouth="thinking", dots=3),
    ], [600, 400, 400, 400, 400]


# --- Workflow Helpers ---


def _shift_frame(frame, xo=0, yo=0):
    """Shift all pixels in a frame by offset."""
    shifted = _blank()
    for r in range(16):
        for c in range(16):
            nr, nc = r + yo, c + xo
            if 0 <= nr < 16 and 0 <= nc < 16:
                shifted[nr][nc] = frame[r][c]
    return shifted


def _dim_frame(frame, factor=0.7):
    """Dim all non-background pixels."""
    dimmed = _blank()
    for r in range(16):
        for c in range(16):
            if frame[r][c] != _BG:
                cr, cg, cb = frame[r][c]
                dimmed[r][c] = (int(cr * factor), int(cg * factor), int(cb * factor))
    return dimmed


def _mini_luna(p, cx, cy):
    """Draw mini Luna head: purple hair dome + skin face + violet eyes."""
    ix, iy = int(cx), int(cy)
    def px(r, c, color):
        if 0 <= r < 16 and 0 <= c < 16:
            p[r][c] = color
    # Hair dome
    for dx in (-1, 0, 1):
        px(iy - 2, ix + dx, _H)
    for dx in (-2, -1, 0, 1, 2):
        px(iy - 1, ix + dx, _H)
    # Face with hair sides
    px(iy, ix - 2, _H); px(iy, ix + 2, _H)
    px(iy, ix, _SK)
    # Chin
    px(iy + 1, ix - 1, _SK); px(iy + 1, ix, _SK); px(iy + 1, ix + 1, _SK)
    # Violet eyes
    px(iy, ix - 1, _EV); px(iy, ix + 1, _EV)


def _draw_cat(p, cx, cy, color="white"):
    """Draw a cute mini cat inspired by preset cat.
    color: 'white' or 'orange'"""
    ix, iy = int(cx), int(cy)
    # Colors based on preset cat
    if color == "white":
        fur = _SK
        fur_dark = _Sd
        fur_light = (255, 240, 230)
    else:  # orange
        fur = (255, 165, 50)
        fur_dark = (200, 120, 30)
        fur_light = (255, 180, 70)
    def px(r, c, col):
        if 0 <= r < 16 and 0 <= c < 16:
            p[r][c] = col

    # Ears (pointy like preset cat)
    px(iy - 3, ix - 1, fur)
    px(iy - 2, ix - 2, fur); px(iy - 2, ix - 1, fur)

    px(iy - 3, ix + 1, fur)
    px(iy - 2, ix + 1, fur); px(iy - 2, ix + 2, fur)

    # Head top
    px(iy - 1, ix - 3, fur_dark); px(iy - 1, ix - 2, fur)
    px(iy - 1, ix - 1, fur); px(iy - 1, ix, fur)
    px(iy - 1, ix + 1, fur); px(iy - 1, ix + 2, fur); px(iy - 1, ix + 3, fur_dark)

    # Face with eyes (green eyes like preset)
    px(iy, ix - 3, fur_dark); px(iy, ix - 2, fur)
    px(iy, ix - 1, fur); px(iy, ix, fur)
    px(iy, ix + 1, fur); px(iy, ix + 2, fur); px(iy, ix + 3, fur_dark)

    # Eyes: black (single dot)
    px(iy, ix - 1, (40, 40, 40))
    px(iy, ix + 1, (40, 40, 40))

    # Face middle with nose
    px(iy + 1, ix - 3, fur_dark); px(iy + 1, ix - 2, fur)
    px(iy + 1, ix - 1, fur); px(iy + 1, ix, fur_dark)  # nose
    px(iy + 1, ix + 1, fur); px(iy + 1, ix + 2, fur); px(iy + 1, ix + 3, fur_dark)

    # Pink cheeks like preset
    px(iy + 1, ix - 1, (255, 140, 160))
    px(iy + 1, ix + 1, (255, 140, 160))

    # Face bottom
    px(iy + 2, ix - 2, fur_dark); px(iy + 2, ix - 1, fur)
    px(iy + 2, ix, fur); px(iy + 2, ix + 1, fur); px(iy + 2, ix + 2, fur_dark)

    # Chin
    px(iy + 3, ix - 1, fur_dark); px(iy + 3, ix, fur); px(iy + 3, ix + 1, fur_dark)


def _draw_magic_star(p, phase=0):
    """Draw rotating magic star at top-right corner."""
    colors = [_SP, _MG, _ST, _TJ]
    c = colors[phase % 4]
    c2 = colors[(phase + 1) % 4]
    p[1][14] = c
    if phase % 2 == 0:
        p[0][14] = c2; p[2][14] = c2; p[1][13] = c2; p[1][15] = c2
    else:
        p[0][13] = c2; p[0][15] = c2; p[2][13] = c2; p[2][15] = c2


def _draw_magic_star_at(p, cx, cy, phase=0):
    """Draw rotating magic star at position (cx, cy)."""
    colors = [_SP, _MG, _ST, _TJ]
    c = colors[phase % 4]
    c2 = colors[(phase + 1) % 4]

    def px(y, x, color):
        if 0 <= y < 16 and 0 <= x < 16:
            p[y][x] = color

    px(cy, cx, c)
    if phase % 2 == 0:
        px(cy - 1, cx, c2); px(cy + 1, cx, c2); px(cy, cx - 1, c2); px(cy, cx + 1, c2)
    else:
        px(cy - 1, cx - 1, c2); px(cy - 1, cx + 1, c2); px(cy + 1, cx - 1, c2); px(cy + 1, cx + 1, c2)


def _draw_checkbox_luna(p, y, x, checked=False):
    """3x3 checkbox with sparkle outline."""
    w = _SP
    green = (50, 205, 50)
    p[y][x] = w; p[y][x+1] = w; p[y][x+2] = w
    p[y+1][x] = w; p[y+1][x+1] = _BG; p[y+1][x+2] = w
    p[y+2][x] = w; p[y+2][x+1] = w; p[y+2][x+2] = w
    if checked:
        p[y+1][x+1] = green


def _draw_question_mark_luna(p, y, x):
    """Question mark in sparkle color, 3 wide 6 tall."""
    c = _SP
    p[y][x] = c; p[y][x+1] = c; p[y][x+2] = c
    p[y+1][x+2] = c
    p[y+2][x+1] = c
    p[y+3][x+1] = c
    p[y+5][x+1] = c


# --- Workflow Emotions ---


def working():
    """Working Luna — focused with wide eyes, breathing tiara, progressive sparkles."""
    # Frame 1: no sparkles
    f1 = _frame(eyes="open", mouth="shy", sparkles=0)
    f1[1][7] = _TJ; f1[1][8] = _TJ

    # Frame 2: few sparkles, tiara dim
    f2 = _frame(eyes="wide", mouth="shy", sparkles=1)
    f2[0][0] = _SP
    f2[1][7] = _MG; f2[1][8] = _MG

    # Frame 3: lots of sparkles, tiara bright
    f3 = _frame(eyes="wide", mouth="shy", sparkles=2)
    f3[0][0] = _SP; f3[0][15] = _MG
    f3[15][0] = _ST; f3[15][15] = _SP
    f3[7][0] = _MG; f3[7][15] = _ST
    f3[1][7] = _SP; f3[1][8] = _SP

    # Frame 4: few sparkles, tiara dim
    f4 = _frame(eyes="wide", mouth="shy", sparkles=1)
    f4[0][15] = _SP
    f4[1][7] = _MG; f4[1][8] = _MG

    return [f1, f2, f3, f4], [500, 600, 600, 600]


def subagent():
    """Subagent — Luna dims and splits into white and orange cat helpers."""
    f1 = _frame(eyes="open", mouth="smile")

    f2 = _shift_frame(_dim_frame(_frame(eyes="open", mouth="shy"), 0.8), xo=-1)
    _draw_cat(f2, 12, 5, color="white")

    f3 = _shift_frame(_dim_frame(_frame(eyes="open", mouth="shy"), 0.6), xo=-3)
    _draw_cat(f3, 11, 4, color="white")
    _draw_cat(f3, 12, 11, color="orange")

    f4 = _shift_frame(_dim_frame(_frame(eyes="open", mouth="shy"), 0.4), xo=-5)
    _draw_cat(f4, 10, 3, color="white")
    _draw_cat(f4, 11, 12, color="orange")

    f5 = _shift_frame(_dim_frame(_frame(eyes="open", mouth="shy"), 0.3), xo=-7)
    _draw_cat(f5, 9, 2, color="white")
    _draw_cat(f5, 10, 13, color="orange")

    return [f1, f2, f3, f4, f5], [500, 300, 300, 300, 300]


def done():
    """Done — excited Luna with sparkle burst and green checkmark."""
    f1 = _frame(eyes="open", mouth="smile")
    f2 = _frame(eyes="happy", mouth="grin")
    f3 = _frame(eyes="happy", mouth="grin", sparkles=1)
    f4 = _frame(eyes="happy", mouth="grin", sparkles=2, confetti=2)

    # Green checkmark animation (same style as default emotion)
    G = (50, 205, 50)
    # Frame 5: checkmark at (y=2, x=10) - 6x4 small check
    f5 = _frame(eyes="happy", mouth="grin", sparkles=2, confetti=2)
    f5[2][15] = G
    f5[3][14] = G
    f5[4][10] = G; f5[4][13] = G
    f5[5][11] = G; f5[5][12] = G

    # Frame 6: same checkmark, stays
    f6 = _frame(eyes="happy", mouth="grin", sparkles=2, confetti=2)
    f6[2][15] = G
    f6[3][14] = G
    f6[4][10] = G; f6[4][13] = G
    f6[5][11] = G; f6[5][12] = G

    return [f1, f2, f3, f4, f5, f6], [400, 300, 400, 400, 300, 600]


def notify():
    """Notify — gold bell sways at top-right."""
    f1 = _frame(eyes="open", mouth="shy")

    f2 = _frame(eyes="open", mouth="shy")
    _draw_bell_luna(f2, 11, tilt=0)

    f3 = _frame(eyes="lookup", mouth="smile")
    _draw_bell_luna(f3, 11, tilt=-1)

    f4 = _frame(eyes="open", mouth="smile")
    _draw_bell_luna(f4, 11, tilt=1)

    return [f1, f2, f3, f4], [400, 300, 400, 400]


def _draw_bell_luna(p, cx, tilt=0):
    """Draw gold bell — narrow rounded shape."""
    g = (255, 210, 60)  # gold
    d = (200, 165, 40)  # dark gold edge
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


def tooluse():
    """Tooluse — multiple magic stars rotate around Luna, tiara breathing."""
    f1 = _frame(eyes="open", mouth="shy")
    _draw_magic_star(f1, phase=0)
    _draw_magic_star_at(f1, 1, 1, phase=0)
    f1[1][7] = _TJ; f1[1][8] = _TJ

    f2 = _frame(eyes="open", mouth="shy")
    _draw_magic_star(f2, phase=1)
    _draw_magic_star_at(f2, 1, 1, phase=1)
    _draw_magic_star_at(f2, 14, 6, phase=0)
    f2[1][7] = _MG; f2[1][8] = _MG

    f3 = _frame(eyes="squint", mouth="shy")
    _draw_magic_star(f3, phase=2)
    _draw_magic_star_at(f3, 1, 1, phase=2)
    _draw_magic_star_at(f3, 14, 6, phase=1)
    _draw_magic_star_at(f3, 7, 14, phase=0)
    f3[1][7] = _SP; f3[1][8] = _SP

    f4 = _frame(eyes="open", mouth="shy")
    _draw_magic_star(f4, phase=3)
    _draw_magic_star_at(f4, 1, 1, phase=3)
    _draw_magic_star_at(f4, 14, 6, phase=2)
    _draw_magic_star_at(f4, 7, 14, phase=1)
    f4[1][7] = _MG; f4[1][8] = _MG

    return [f1, f2, f3, f4], [300, 300, 300, 300]


def oops():
    """Oops — wide eyes, exclaim, face shakes."""
    f1 = _frame(eyes="open", mouth="shy")
    f2 = _frame(eyes="wide", mouth="open", exclaim=True)

    f3 = _shift_frame(_frame(eyes="wide", mouth="open"), xo=-1)
    f3[2][15] = _RED; f3[3][15] = _RED; f3[4][15] = _RED; f3[6][15] = _RED

    f4 = _shift_frame(_frame(eyes="wide", mouth="open"), xo=1)
    f4[2][15] = _RED; f4[3][15] = _RED; f4[4][15] = _RED; f4[6][15] = _RED

    f5 = _frame(eyes="wide", mouth="open", exclaim=True)
    return [f1, f2, f3, f4, f5], [500, 400, 200, 200, 400]


def tasklist():
    """Tasklist — Luna shifts left, checkboxes appear."""
    xo = -3
    f1 = _frame(eyes="open", mouth="shy")

    f2 = _shift_frame(_frame(eyes="lookup", mouth="shy"), xo=xo)
    _draw_checkbox_luna(f2, 3, 13)

    f3 = _shift_frame(_frame(eyes="lookup", mouth="shy"), xo=xo)
    _draw_checkbox_luna(f3, 3, 13)
    _draw_checkbox_luna(f3, 7, 13)

    f4 = _shift_frame(_frame(eyes="lookup", mouth="shy"), xo=xo)
    _draw_checkbox_luna(f4, 3, 13)
    _draw_checkbox_luna(f4, 7, 13)
    _draw_checkbox_luna(f4, 11, 13)

    return [f1, f2, f3, f4], [500, 400, 400, 400]


def taskdone():
    """Taskdone — checkboxes check off + confetti."""
    xo = -3

    f1 = _shift_frame(_frame(eyes="open", mouth="smile"), xo=xo)
    _draw_checkbox_luna(f1, 3, 13, checked=True)
    _draw_checkbox_luna(f1, 7, 13)
    _draw_checkbox_luna(f1, 11, 13)

    f2 = _shift_frame(_frame(eyes="squint", mouth="smile"), xo=xo)
    _draw_checkbox_luna(f2, 3, 13, checked=True)
    _draw_checkbox_luna(f2, 7, 13, checked=True)
    _draw_checkbox_luna(f2, 11, 13)

    f3 = _shift_frame(_frame(eyes="happy", mouth="grin"), xo=xo)
    _draw_checkbox_luna(f3, 3, 13, checked=True)
    _draw_checkbox_luna(f3, 7, 13, checked=True)
    _draw_checkbox_luna(f3, 11, 13)
    _draw_confetti(f3, density=2)

    return [f1, f2, f3], [400, 400, 500]


def question():
    """Question — dots appear, then question mark sways."""
    f1 = _frame(eyes="open", mouth="shy")

    f2 = _frame(eyes="lookup", mouth="shy", dots=1)

    f3 = _frame(eyes="lookup", mouth="shy", dots=2)

    f4 = _frame(eyes="lookup", mouth="shy", dots=3)

    f5 = _frame(eyes="open", mouth="shy")
    _draw_question_mark_luna(f5, 0, 13)

    f6 = _frame(eyes="open", mouth="shy")
    _draw_question_mark_luna(f6, 0, 12)

    f7 = _frame(eyes="open", mouth="shy")
    _draw_question_mark_luna(f7, 0, 13)

    return [f1, f2, f3, f4, f5, f6, f7], [500, 350, 350, 400, 400, 400, 400]


def magic():
    """Magic — rotating stars multiply, screen fades to white."""
    w = (200, 170, 130)  # wand shaft

    f1 = _frame(eyes="open", mouth="determined")

    # Frame 2: 1 star at wand tip
    f2 = _frame(eyes="wide", mouth="shy")
    f2[3][14] = w; f2[4][14] = w; f2[5][14] = w; f2[6][14] = w; f2[7][14] = w
    _draw_magic_star_at(f2, 14, 2, phase=0)

    # Frame 3: 1 star, brighter
    f3 = _frame(eyes="wide", mouth="shy")
    f3[3][14] = w; f3[4][14] = w; f3[5][14] = w; f3[6][14] = w; f3[7][14] = w
    _draw_magic_star_at(f3, 14, 2, phase=1)

    # Frame 4: 2 stars (add top-left corner)
    f4 = _frame(eyes="one_half_open", mouth="smile")
    f4[3][14] = w; f4[4][14] = w; f4[5][14] = w; f4[6][14] = w; f4[7][14] = w
    _draw_magic_star_at(f4, 14, 2, phase=2)
    _draw_magic_star_at(f4, 1, 1, phase=0)

    # Frame 5: 3 stars (add top-right corner)
    f5 = _frame(eyes="one_closed", mouth="smile")
    f5[3][14] = w; f5[4][14] = w; f5[5][14] = w; f5[6][14] = w; f5[7][14] = w
    _draw_magic_star_at(f5, 14, 2, phase=3)
    _draw_magic_star_at(f5, 1, 1, phase=1)
    _draw_magic_star_at(f5, 1, 14, phase=2)

    # Frame 6: 4 stars (add bottom-center under face)
    f6 = _frame(eyes="happy", mouth="grin")
    f6[3][14] = w; f6[4][14] = w; f6[5][14] = w; f6[6][14] = w; f6[7][14] = w
    _draw_magic_star_at(f6, 14, 2, phase=0)
    _draw_magic_star_at(f6, 1, 1, phase=2)
    _draw_magic_star_at(f6, 1, 14, phase=3)
    _draw_magic_star_at(f6, 7, 14, phase=1)

    # Frame 7: 4 stars, start white overlay (lightest)
    f7 = _frame(eyes="happy", mouth="grin")
    f7[3][14] = w; f7[4][14] = w; f7[5][14] = w; f7[6][14] = w; f7[7][14] = w
    _draw_magic_star_at(f7, 14, 2, phase=1)
    _draw_magic_star_at(f7, 1, 1, phase=3)
    _draw_magic_star_at(f7, 1, 14, phase=0)
    _draw_magic_star_at(f7, 7, 14, phase=2)
    # Light white overlay on entire screen (25% white mixed)
    for y in range(16):
        for x in range(16):
            if f7[y][x] != _BG:
                r, g, b = f7[y][x]
                f7[y][x] = (min(255, r + 64), min(255, g + 64), min(255, b + 64))
            else:
                f7[y][x] = (64, 64, 64)

    # Frame 8: Medium white overlay (50% white mixed)
    f8 = _frame(eyes="happy", mouth="grin")
    f8[3][14] = w; f8[4][14] = w; f8[5][14] = w; f8[6][14] = w; f8[7][14] = w
    _draw_magic_star_at(f8, 14, 2, phase=2)
    _draw_magic_star_at(f8, 1, 1, phase=0)
    _draw_magic_star_at(f8, 1, 14, phase=1)
    _draw_magic_star_at(f8, 7, 14, phase=3)
    for y in range(16):
        for x in range(16):
            if f8[y][x] != _BG:
                r, g, b = f8[y][x]
                f8[y][x] = (min(255, r + 128), min(255, g + 128), min(255, b + 128))
            else:
                f8[y][x] = (128, 128, 128)

    # Frame 9: Heavy white overlay (75% white mixed)
    f9 = _frame(eyes="happy", mouth="grin")
    f9[3][14] = w; f9[4][14] = w; f9[5][14] = w; f9[6][14] = w; f9[7][14] = w
    _draw_magic_star_at(f9, 14, 2, phase=3)
    _draw_magic_star_at(f9, 1, 1, phase=1)
    _draw_magic_star_at(f9, 1, 14, phase=2)
    _draw_magic_star_at(f9, 7, 14, phase=0)
    for y in range(16):
        for x in range(16):
            if f9[y][x] != _BG:
                r, g, b = f9[y][x]
                f9[y][x] = (min(255, r + 192), min(255, g + 192), min(255, b + 192))
            else:
                f9[y][x] = (192, 192, 192)

    # Frame 10: Full white screen
    f10 = _blank()
    for y in range(16):
        for x in range(16):
            f10[y][x] = _WHITE

    return [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10], [400, 500, 500, 300, 500, 350, 300, 300, 300, 3000]


# --- Registry ---
# EMOTIONS is used by --load to override default emotion presets

EMOTIONS = {
    "happy": ("Happy Luna", happy),
    "sad": ("Sad Luna", sad),
    "angry": ("Angry Luna", angry),
    "love": ("Love Luna", love),
    "cool": ("Cool Luna", cool),
    "cry": ("Crying Luna", cry),
    "laugh": ("Laughing Luna", laugh),
    "sleepy": ("Sleepy Luna", sleepy),
    "shock": ("Shocked Luna", shock),
    "wink": ("Winking Luna", wink),
    "sick": ("Sick Luna", sick),
    "party": ("Party Luna", party),
    "kiss": ("Flying kiss Luna", kiss_with_heart),
    "standby": ("Standby Luna", standby),
    "thinking": ("Thinking Luna", thinking),
    "working": ("Working Luna", working),
    "subagent": ("Subagent Luna", subagent),
    "done": ("Done Luna", done),
    "notify": ("Notify Luna", notify),
    "tooluse": ("Tooluse Luna", tooluse),
    "oops": ("Oops Luna", oops),
    "tasklist": ("Tasklist Luna", tasklist),
    "taskdone": ("Taskdone Luna", taskdone),
    "question": ("Question Luna", question),
    "magic": ("Magic Luna", magic),
}

HIDDEN_EMOTIONS = {"magic"}
