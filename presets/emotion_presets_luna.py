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
        p[8][3] = _EK; p[8][6] = _EK
        # Right eye (shifted right)
        p[7][10] = _EK; p[7][11] = _EK
        p[8][9] = _EK; p[8][12] = _EK

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
        # Looking up (thinking)
        p[6][4] = _EK; p[6][5] = _EK; p[6][6] = _EK
        p[6][9] = _EK; p[6][10] = _EK; p[6][11] = _EK
        p[7][5] = _EV; p[7][6] = _EV
        p[7][10] = _EV; p[7][11] = _EV

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


# --- Face Details ---

def _draw_blush(p):
    p[9][4] = _PK; p[9][5] = _PK; p[9][11] = _PK; p[9][12] = _PK


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
    d = _SP
    positions = [(0, 5), (0, 7), (0, 9)]
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
    if blush:
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
    """Standby Luna — blink and subtle mouth change."""
    # Standing
    f1 = _frame(eyes="open", mouth="shy")

    # Blink
    f2 = _frame(eyes="half_open", mouth="shy")
    f3 = _frame(eyes="closed", mouth="shy")
    f4 = _frame(eyes="open", mouth="shy")

    # Smile briefly
    f5 = _frame(eyes="open", mouth="smile")
    f6 = _frame(eyes="open", mouth="shy")

    return [f1, f2, f3, f4, f5, f6], [2000, 200, 200, 1500, 500, 300]


def thinking():
    """Thinking Luna — eyes look up, dots appear."""
    return [
        _frame(eyes="open", mouth="shy"),
        _frame(eyes="lookup", mouth="shy"),
        _frame(eyes="lookup", mouth="shy", dots=1),
        _frame(eyes="lookup", mouth="shy", dots=2),
        _frame(eyes="lookup", mouth="shy", dots=3),
    ], [600, 400, 400, 400, 400]


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
}
