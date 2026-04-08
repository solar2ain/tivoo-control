"""
Tivoo Preset Library

All presets return (frames, delays) tuple for unified animation support.
"""

import copy

# --- Utilities ---

def _circle(cx, cy, r, pixels, color):
    """Draw a filled circle on the pixel array."""
    for y in range(16):
        for x in range(16):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                pixels[y][x] = color


def _empty():
    """Create a blank 16x16 canvas."""
    return [[(0, 0, 0)] * 16 for _ in range(16)]


def _static(pixels, duration=2000):
    """Wrap a single-frame pixel array as (frames, delays)."""
    return [pixels], [duration]


def _copy(pixels):
    """Deep copy a frame."""
    return [row[:] for row in pixels]


# --- Emoji ---

def heart():
    """Beating heart — pulse big/small."""
    _ = (0, 0, 0)
    R = (255, 20, 60)
    D = (200, 10, 40)
    W = (255, 255, 255)
    # Frame 1: normal
    f1 = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,R,R,_,_,_,_,_,R,R,_,_,_,_],
        [_,_,R,R,R,R,_,_,_,R,R,R,R,_,_,_],
        [_,R,R,W,R,R,R,_,R,R,R,R,R,R,_,_],
        [_,R,W,W,R,R,R,R,R,R,R,R,R,R,_,_],
        [_,R,R,R,R,R,R,R,R,R,R,R,R,R,_,_],
        [_,R,R,R,R,R,R,R,R,R,R,R,R,R,_,_],
        [_,_,R,R,R,R,R,R,R,R,R,R,R,_,_,_],
        [_,_,_,R,R,R,R,R,R,R,R,R,_,_,_,_],
        [_,_,_,_,R,R,R,R,R,R,R,_,_,_,_,_],
        [_,_,_,_,_,R,R,R,R,R,_,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,R,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    # Frame 2: big (expanded)
    f2 = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,R,R,_,_,_,_,_,R,R,_,_,_,_],
        [_,_,R,R,R,R,_,_,_,R,R,R,R,_,_,_],
        [_,R,R,W,R,R,R,_,R,R,R,R,R,R,_,_],
        [R,R,W,W,R,R,R,R,R,R,R,R,R,R,R,_],
        [R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,_],
        [R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,_],
        [_,R,R,R,R,R,R,R,R,R,R,R,R,R,_,_],
        [_,R,R,R,R,R,R,R,R,R,R,R,R,R,_,_],
        [_,_,R,R,R,R,R,R,R,R,R,R,R,_,_,_],
        [_,_,_,R,R,R,R,R,R,R,R,R,_,_,_,_],
        [_,_,_,_,R,R,R,R,R,R,R,_,_,_,_,_],
        [_,_,_,_,_,R,R,R,R,R,_,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,R,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    # Frame 3: small (contracted)
    f3 = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,D,_,_,_,_,_,D,_,_,_,_,_],
        [_,_,_,D,D,D,_,_,_,D,D,D,_,_,_,_],
        [_,_,D,D,D,D,D,_,D,D,D,D,D,_,_,_],
        [_,_,D,D,D,D,D,D,D,D,D,D,D,_,_,_],
        [_,_,D,D,D,D,D,D,D,D,D,D,D,_,_,_],
        [_,_,_,D,D,D,D,D,D,D,D,D,_,_,_,_],
        [_,_,_,_,D,D,D,D,D,D,D,_,_,_,_,_],
        [_,_,_,_,_,D,D,D,D,D,_,_,_,_,_,_],
        [_,_,_,_,_,_,D,D,D,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,D,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    return [f1, f2, f1, f3], [400, 300, 400, 300]


def smiley():
    """Winking smiley face."""
    _ = (0, 0, 0)
    Y = (255, 220, 50)
    E = (60, 40, 20)
    M = (200, 80, 60)
    def _face(wink=False):
        p = _empty()
        _circle(7.5, 7.5, 6.5, p, Y)
        # Left eye always open
        for dy in (0, 1):
            for dx in (0, 1):
                p[5 + dy][4 + dx] = E
        # Right eye: open or wink
        if wink:
            p[6][10] = E; p[6][11] = E
        else:
            for dy in (0, 1):
                for dx in (0, 1):
                    p[5 + dy][10 + dx] = E
        for x in range(5, 12):
            p[10][x] = M
        p[9][4] = M; p[9][11] = M
        return p
    return [_face(), _face(), _face(True), _face()], [600, 600, 400, 600]


def star():
    """Twinkling star — brightness pulses."""
    _ = (0, 0, 0)
    G = (255, 200, 0)
    W = (255, 240, 150)
    D = (180, 140, 0)
    base = [
        [_,_,_,_,_,_,_,G,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,G,G,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,G,G,G,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,G,W,G,G,_,_,_,_,_,_],
        [G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,_],
        [_,G,G,G,G,G,G,G,G,G,G,G,G,G,_,_],
        [_,_,G,G,G,G,G,G,G,G,G,G,G,_,_,_],
        [_,_,_,G,G,G,G,G,G,G,G,G,_,_,_,_],
        [_,_,_,G,G,G,G,G,G,G,G,G,_,_,_,_],
        [_,_,_,G,G,G,G,G,G,G,G,G,_,_,_,_],
        [_,_,G,G,G,G,_,_,_,G,G,G,G,_,_,_],
        [_,_,G,G,G,_,_,_,_,_,G,G,G,_,_,_],
        [_,G,G,G,_,_,_,_,_,_,_,G,G,G,_,_],
        [_,G,G,_,_,_,_,_,_,_,_,_,G,G,_,_],
        [G,G,_,_,_,_,_,_,_,_,_,_,_,G,G,_],
        [G,_,_,_,_,_,_,_,_,_,_,_,_,_,G,_],
    ]
    # Frame 2: sparkle spots
    f2 = _copy(base)
    for y, x in [(0, 3), (0, 12), (1, 0), (2, 14)]:
        f2[y][x] = W
    # Frame 3: dim
    f3 = [[(D if c == G else (G if c == W else c)) for c in row] for row in base]
    return [base, f2, base, f3], [500, 300, 500, 300]


def thumbs_up():
    """Bouncing thumbs up."""
    _ = (0, 0, 0)
    S = (255, 200, 140)
    N = (220, 170, 110)
    W = (255, 255, 200)
    base = [
        [_,_,_,_,_,_,_,S,S,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,S,S,S,S,_,_,_,_,_,_],
        [_,_,_,_,_,_,S,S,S,S,_,_,_,_,_,_],
        [_,_,_,_,_,_,S,S,S,S,_,_,_,_,_,_],
        [_,_,_,_,_,_,S,S,S,S,_,_,_,_,_,_],
        [_,_,_,_,_,_,S,S,S,S,S,S,S,_,_,_],
        [_,_,_,S,S,S,S,S,N,S,S,S,S,_,_,_],
        [_,_,S,S,S,S,S,S,N,S,S,S,S,_,_,_],
        [_,_,S,S,S,S,S,S,N,S,S,S,S,_,_,_],
        [_,_,_,S,S,S,S,S,N,S,S,S,S,_,_,_],
        [_,_,_,S,S,S,S,S,N,S,S,S,S,_,_,_],
        [_,_,_,_,S,S,S,S,S,S,S,S,_,_,_,_],
        [_,_,_,_,_,S,S,S,S,S,S,_,_,_,_,_],
    ]
    def _place(yoff, sparkle=False):
        f = _empty()
        for y, row in enumerate(base):
            for x, c in enumerate(row):
                ny = y + yoff
                if c != _ and 0 <= ny < 16:
                    f[ny][x] = c
        if sparkle:
            f[yoff][4] = W; f[yoff + 1][12] = W; f[yoff + 2][3] = W
        return f
    return [_place(2), _place(1), _place(2), _place(3)], [300, 250, 300, 250]


# --- Weather ---

def sun():
    """Spinning sun — rays rotate."""
    _ = (0, 0, 0)
    Y = (255, 200, 0)
    O = (255, 150, 0)
    W = (255, 240, 100)
    def _make(rot):
        p = _empty()
        # Core
        _circle(7.5, 7.5, 4, p, Y)
        _circle(7.5, 7.5, 2.5, p, W)
        if rot == 0:
            # Cross rays
            for i in range(16):
                p[7][i] = Y; p[8][i] = Y; p[i][7] = Y; p[i][8] = Y
        else:
            # Diagonal rays
            for i in range(16):
                p[i][i] = O; p[i][15 - i] = O
        _circle(7.5, 7.5, 4, p, Y)
        _circle(7.5, 7.5, 2.5, p, W)
        return p
    return [_make(0), _make(1)], [400, 400]


def moon():
    """Moon with twinkling stars."""
    _ = (0, 0, 0)
    Y = (255, 240, 180)
    D = (200, 190, 140)
    W = (255, 255, 255)
    S = (180, 200, 255)
    p = _empty()
    _circle(7, 7, 6, p, Y)
    _circle(9, 5, 5, p, _)
    p[8][5] = D; p[6][4] = D; p[10][6] = D
    f1 = _copy(p)
    f1[2][13] = W; f1[4][11] = S; f1[1][10] = S
    f2 = _copy(p)
    f2[3][12] = W; f2[1][14] = S; f2[5][10] = W
    f3 = _copy(p)
    f3[2][13] = S; f3[4][11] = W; f3[0][11] = W
    return [f1, f2, f3], [600, 600, 600]


def cloud():
    """Drifting cloud."""
    _ = (0, 0, 0)
    W = (240, 245, 255)
    G = (200, 210, 220)
    body = [
        [0,0,0,0,0,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,2,2,1,1,1,1,1,1,1,1,2,0],
        [0,0,0,2,2,2,2,2,2,2,0,0,0],
    ]
    cmap = {0: _, 1: W, 2: G}
    def _place(xoff):
        f = _empty()
        for y, row in enumerate(body):
            for x, v in enumerate(row):
                nx = x + xoff
                if 0 <= nx < 16 and cmap[v] != _:
                    f[y + 4][nx] = cmap[v]
        return f
    return [_place(1), _place(3), _place(5), _place(3)], [500, 500, 500, 500]


def rain():
    """Animated rain — drops falling."""
    _ = (0, 0, 0)
    W = (200, 210, 225)
    G = (160, 170, 185)
    B = (80, 150, 255)
    cloud_rows = [
        [_,_,_,_,_,W,W,W,_,_,_,_,_,_,_,_],
        [_,_,_,_,W,W,W,W,W,_,_,_,_,_,_,_],
        [_,_,W,W,W,W,W,W,W,W,W,_,_,_,_,_],
        [_,W,W,W,W,W,W,W,W,W,W,W,W,_,_,_],
        [_,W,W,W,W,W,W,W,W,W,W,W,W,W,_,_],
        [W,G,G,W,W,W,W,W,W,W,W,W,W,G,G,_],
        [_,_,_,G,G,G,G,G,G,G,G,G,_,_,_,_],
    ]
    drop_cols = [2, 5, 8, 11]
    frames = []
    for phase in range(3):
        f = _empty()
        for y, row in enumerate(cloud_rows):
            f[y] = row[:]
        for i, cx in enumerate(drop_cols):
            start = 8 + ((phase + i) % 3) * 2
            for dy in range(2):
                ry = start + dy
                if 7 <= ry < 16:
                    f[ry][cx] = B
        frames.append(f)
    return frames, [200, 200, 200]


def snow():
    """Animated snowflakes falling."""
    _ = (0, 0, 0)
    W = (220, 230, 255)
    B = (180, 200, 240)
    flake_xs = [2, 6, 10, 14, 4, 8, 12]
    frames = []
    for phase in range(4):
        f = _empty()
        for i, cx in enumerate(flake_xs):
            y = (phase * 2 + i * 3) % 16
            c = W if i % 2 == 0 else B
            if 0 <= cx < 16:
                f[y][cx] = c
                if y + 1 < 16: f[y + 1][cx] = c
                if cx > 0: f[y][cx - 1] = c
                if cx < 15: f[y][cx + 1] = c
        frames.append(f)
    return frames, [300, 300, 300, 300]


# --- Animals ---

def cat():
    """Blinking cat face."""
    _ = (0, 0, 0)
    O = (255, 165, 50)
    D = (200, 120, 30)
    W = (255, 255, 255)
    P = (255, 140, 160)
    E = (40, 40, 40)
    G = (100, 200, 80)
    base = [
        [_,_,O,_,_,_,_,_,_,_,_,_,_,O,_,_],
        [_,_,O,O,_,_,_,_,_,_,_,_,O,O,_,_],
        [_,_,O,D,O,_,_,_,_,_,_,O,D,O,_,_],
        [_,_,O,O,O,O,O,O,O,O,O,O,O,O,_,_],
        [_,O,O,O,O,O,O,O,O,O,O,O,O,O,O,_],
        [_,O,O,O,O,O,O,O,O,O,O,O,O,O,O,_],
        [_,O,O,E,E,O,O,O,O,O,O,E,E,O,O,_],
        [_,O,O,G,E,O,O,O,O,O,O,G,E,O,O,_],
        [_,O,O,O,O,O,O,P,P,O,O,O,O,O,O,_],
        [_,O,O,O,O,O,O,P,O,O,O,O,O,O,O,_],
        [_,O,O,O,O,O,O,O,O,O,O,O,O,O,O,_],
        [_,O,W,_,_,W,O,O,O,O,W,_,_,W,O,_],
        [_,_,O,O,O,O,O,O,O,O,O,O,O,O,_,_],
        [_,_,_,O,O,O,O,O,O,O,O,O,O,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    f1 = [row[:] for row in base]
    # Blink: closed eyes
    f2 = [row[:] for row in base]
    f2[6][3] = O; f2[6][4] = E; f2[6][5] = O; f2[6][11] = O; f2[6][12] = E; f2[6][13] = O
    f2[7][3] = O; f2[7][4] = O; f2[7][5] = O; f2[7][11] = O; f2[7][12] = O; f2[7][13] = O
    return [f1, f1, f2, f1], [700, 700, 200, 700]


def dog():
    """Tongue-wagging dog face."""
    _ = (0, 0, 0)
    B = (160, 110, 60)
    D = (120, 80, 40)
    W = (255, 255, 255)
    P = (60, 40, 30)
    E = (30, 30, 30)
    T = (200, 80, 80)
    base = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,D,D,D,_,_,_,_,_,_,D,D,D,_,_],
        [_,D,D,D,D,D,_,_,_,_,D,D,D,D,D,_],
        [_,D,D,D,D,B,B,B,B,B,B,D,D,D,D,_],
        [_,D,D,D,B,B,B,B,B,B,B,B,D,D,D,_],
        [_,_,D,B,B,B,B,B,B,B,B,B,B,D,_,_],
        [_,_,_,B,B,E,E,B,B,E,E,B,B,_,_,_],
        [_,_,_,B,B,E,E,B,B,E,E,B,B,_,_,_],
        [_,_,_,B,B,B,B,P,P,B,B,B,B,_,_,_],
        [_,_,_,B,B,B,P,P,P,P,B,B,B,_,_,_],
        [_,_,_,B,B,B,B,B,B,B,B,B,B,_,_,_],
    ]
    def _frame(tongue_out=False, tongue_side=0):
        f = _empty()
        for y, row in enumerate(base):
            for x, c in enumerate(row):
                f[y][x] = c
        if tongue_out:
            # Tongue sticking out
            tx = 7 + tongue_side
            f[11][tx] = T; f[11][tx + 1] = T
            f[12][tx] = T; f[12][tx + 1] = T
            f[13][tx] = T; f[13][tx + 1] = T
            # Mouth open
            f[10][6] = B; f[10][7] = B; f[10][8] = B; f[10][9] = B
        else:
            f[11][5] = B; f[11][6] = B; f[11][7] = B; f[11][8] = B; f[11][9] = B; f[11][10] = B
            f[12][6] = B; f[12][7] = B; f[12][8] = B; f[12][9] = B
            f[13][7] = B; f[13][8] = B
        return f
    return [_frame(False), _frame(True, 0), _frame(True, -1), _frame(False)], [500, 400, 400, 500]


def fish():
    """Swimming tropical fish with bubbles."""
    _ = (0, 0, 0)
    B = (0, 120, 255)
    C = (0, 200, 255)
    Y = (255, 200, 0)
    W = (255, 255, 255)
    E = (20, 20, 20)
    O = (255, 100, 0)
    BU = (180, 220, 255)  # bubble
    body = [
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,1,1,2,2,1,1,0,0,0],
        [1,1,0,1,1,3,3,4,5,3,2,1,0],
        [1,1,1,1,3,3,3,3,3,3,1,1,1],
        [1,1,1,1,6,6,6,6,6,3,1,1,1],
        [1,1,0,1,1,6,6,2,2,1,1,0,0],
        [0,0,0,0,1,1,2,2,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
    ]
    cmap = {0: _, 1: B, 2: C, 3: Y, 4: W, 5: E, 6: O}
    def _place(xoff, bubble_y=None):
        f = _empty()
        for y, row in enumerate(body):
            for x, v in enumerate(row):
                nx = x + xoff
                if 0 <= nx < 16 and cmap[v] != _:
                    f[y + 4][nx] = cmap[v]
        if bubble_y is not None:
            bx1 = xoff + 11
            bx2 = xoff + 12
            if 0 <= bx1 < 16:
                f[bubble_y][bx1] = BU
            if bubble_y > 2 and 0 <= bx2 < 16:
                f[bubble_y - 2][bx2] = BU
        return f
    return [_place(1), _place(2, 5), _place(3, 3), _place(2, 2)], [400, 400, 400, 400]


# --- Plants ---

def flower():
    """Blooming flower — bud to full bloom."""
    _ = (0, 0, 0)
    R = (255, 60, 80)
    P = (255, 120, 160)
    Y = (255, 220, 50)
    G = (60, 180, 60)
    D = (40, 130, 40)
    stem = [(11, 7), (11, 8), (12, 7), (12, 8), (13, 7), (13, 8), (14, 7), (14, 8)]
    leaf = [(12, 5), (12, 6), (13, 6), (13, 9), (13, 10), (14, 9)]
    # Frame 1: bud
    f1 = _empty()
    for y, x in stem: f1[y][x] = G
    for y, x in leaf: f1[y][x] = D
    for x in range(6, 10): f1[7][x] = P
    for x in range(6, 10): f1[8][x] = P
    for x in range(7, 9): f1[6][x] = P; f1[9][x] = P
    # Frame 2: opening
    f2 = _empty()
    for y, x in stem: f2[y][x] = G
    for y, x in leaf: f2[y][x] = D
    for x in range(5, 11): f2[6][x] = R
    for x in range(5, 11): f2[9][x] = R
    for y in range(5, 10):
        f2[y][4] = R; f2[y][11] = R
    for x in range(6, 10):
        for y in range(6, 9): f2[y][x] = P
    f2[7][7] = Y; f2[7][8] = Y; f2[8][7] = Y; f2[8][8] = Y
    # Frame 3: full bloom
    f3 = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,R,R,_,_,R,R,_,_,_,_,_],
        [_,_,_,_,R,R,R,R,R,R,R,R,_,_,_,_],
        [_,_,_,R,R,R,P,P,P,P,R,R,R,_,_,_],
        [_,_,R,R,R,P,Y,Y,Y,Y,P,R,R,R,_,_],
        [_,_,R,R,P,Y,Y,Y,Y,Y,Y,P,R,R,_,_],
        [_,_,R,R,P,Y,Y,Y,Y,Y,Y,P,R,R,_,_],
        [_,_,R,R,R,P,Y,Y,Y,Y,P,R,R,R,_,_],
        [_,_,_,R,R,R,P,P,P,P,R,R,R,_,_,_],
        [_,_,_,_,R,R,R,G,G,R,R,R,_,_,_,_],
        [_,_,_,_,_,R,R,G,G,R,R,_,_,_,_,_],
        [_,_,_,_,_,_,_,G,G,_,_,_,_,_,_,_],
        [_,_,_,_,_,G,G,G,G,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,D,G,G,G,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,G,G,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    return [f1, f2, f3], [600, 500, 700]


def tree():
    """Christmas tree with twinkling lights."""
    _ = (0, 0, 0)
    G = (30, 160, 40)
    Y = (255, 220, 0)
    R = (255, 50, 50)
    B = (100, 60, 30)
    BL = (80, 150, 255)
    W = (255, 255, 255)
    base = [
        [_,_,_,_,_,_,_,Y,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,Y,Y,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,G,G,G,_,_,_,_,_,_,_],
        [_,_,_,_,_,G,G,G,G,G,_,_,_,_,_,_],
        [_,_,_,_,G,G,G,G,G,G,G,_,_,_,_,_],
        [_,_,_,_,_,G,G,G,G,G,_,_,_,_,_,_],
        [_,_,_,_,G,G,G,G,G,G,G,_,_,_,_,_],
        [_,_,_,G,G,G,G,G,G,G,G,G,_,_,_,_],
        [_,_,G,G,G,G,G,G,G,G,G,G,G,_,_,_],
        [_,_,_,_,G,G,G,G,G,G,G,_,_,_,_,_],
        [_,_,_,G,G,G,G,G,G,G,G,G,_,_,_,_],
        [_,_,G,G,G,G,G,G,G,G,G,G,G,_,_,_],
        [_,G,G,G,G,G,G,G,G,G,G,G,G,G,_,_],
        [_,_,_,_,_,_,B,B,B,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,B,B,B,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    # Two sets of light positions that alternate
    lights_a = [(4, 6), (7, 5), (8, 9), (10, 6), (12, 3), (12, 11)]
    lights_b = [(3, 8), (6, 8), (7, 10), (9, 8), (11, 5), (11, 10)]
    colors_a = [R, BL, Y, R, Y, BL]
    colors_b = [Y, R, BL, Y, BL, R]
    f1 = [row[:] for row in base]
    for (y, x), c in zip(lights_a, colors_a):
        f1[y][x] = c
    f2 = [row[:] for row in base]
    for (y, x), c in zip(lights_b, colors_b):
        f2[y][x] = c
    f3 = [row[:] for row in base]
    for (y, x), c in zip(lights_a, colors_a):
        f3[y][x] = c
    for (y, x), c in zip(lights_b, colors_b):
        f3[y][x] = W  # all white flash
    return [f1, f2, f3], [500, 500, 400]


# --- Symbols ---

def check():
    """Green checkmark drawing stroke."""
    _ = (0, 0, 0)
    G = (50, 205, 50)
    D = (30, 150, 30)
    W = (255, 255, 200)
    full = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,G,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,G,G,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,G,G,G,_,_],
        [_,_,_,_,_,_,_,_,_,_,G,G,G,_,_,_],
        [_,_,_,_,_,_,_,_,_,G,G,G,_,_,_,_],
        [_,_,_,_,_,_,_,_,G,G,G,_,_,_,_,_],
        [_,_,G,_,_,_,_,G,G,G,_,_,_,_,_,_],
        [_,_,G,G,_,_,G,G,G,_,_,_,_,_,_,_],
        [_,_,G,G,G,G,G,G,_,_,_,_,_,_,_,_],
        [_,_,_,G,G,G,G,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,G,G,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    # Frame 1: just the bottom part of the stroke
    f1 = _empty()
    for y in range(8, 13):
        for x in range(16):
            f1[y][x] = full[y][x]
    # Frame 2: full check
    f2 = [row[:] for row in full]
    # Frame 3: full check + sparkle
    f3 = [row[:] for row in full]
    f3[1][12] = W; f3[3][15] = W; f3[6][1] = W; f3[13][3] = W
    return [f1, f2, f3], [300, 300, 500]


def cross():
    """Red cross mark — flash pulse."""
    _ = (0, 0, 0)
    R = (255, 50, 50)
    D = (180, 30, 30)
    W = (255, 100, 100)
    f1 = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,R,R,_,_,_,_,_,_,_,_,R,R,_,_],
        [_,_,R,R,R,_,_,_,_,_,_,R,R,R,_,_],
        [_,_,_,R,R,R,_,_,_,_,R,R,R,_,_,_],
        [_,_,_,_,R,R,R,_,_,R,R,R,_,_,_,_],
        [_,_,_,_,_,R,R,R,R,R,R,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,R,_,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,R,_,_,_,_,_,_],
        [_,_,_,_,_,R,R,R,R,R,R,_,_,_,_,_],
        [_,_,_,_,R,R,R,_,_,R,R,R,_,_,_,_],
        [_,_,_,R,R,R,_,_,_,_,R,R,R,_,_,_],
        [_,_,R,R,R,_,_,_,_,_,_,R,R,R,_,_],
        [_,_,R,R,_,_,_,_,_,_,_,_,R,R,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    # Bright flash
    f2 = [[(W if c == R else c) for c in row] for row in f1]
    # Dim
    f3 = [[(D if c == R else c) for c in row] for row in f1]
    return [f1, f2, f1, f3], [300, 150, 300, 250]


def music():
    """Bouncing music note."""
    _ = (0, 0, 0)
    W = (255, 255, 255)
    P = (180, 100, 255)
    note_base = [
        [_,_,_,_,_,_,W,W,W,W,W,W,W,_,_,_],
        [_,_,_,_,_,_,W,P,P,P,P,P,W,_,_,_],
        [_,_,_,_,_,_,W,_,_,_,_,_,W,_,_,_],
        [_,_,_,_,_,_,W,_,_,_,_,_,W,_,_,_],
        [_,_,_,_,_,_,W,_,_,_,_,_,W,_,_,_],
        [_,_,_,_,_,_,W,_,_,_,_,_,W,_,_,_],
        [_,_,_,_,_,_,W,_,_,_,_,_,W,_,_,_],
        [_,_,_,_,_,_,W,_,_,_,_,_,W,_,_,_],
        [_,_,_,_,_,_,W,_,_,_,_,_,W,_,_,_],
        [_,_,_,P,P,P,W,_,_,P,P,P,W,_,_,_],
        [_,_,P,P,P,P,P,_,P,P,P,P,P,_,_,_],
        [_,_,P,P,P,P,P,_,P,P,P,P,P,_,_,_],
        [_,_,_,P,P,P,_,_,_,P,P,P,_,_,_,_],
    ]
    # Frame 1: normal position
    f1 = _empty()
    for y, row in enumerate(note_base):
        for x, c in enumerate(row):
            if c != _: f1[y + 1][x] = c
    # Frame 2: bounced up
    f2 = _empty()
    for y, row in enumerate(note_base):
        for x, c in enumerate(row):
            if c != _: f2[y][x] = c
    # Frame 3: bounced down
    f3 = _empty()
    for y, row in enumerate(note_base):
        for x, c in enumerate(row):
            if c != _ and y + 2 < 16: f3[y + 2][x] = c
    return [f1, f2, f1, f3], [300, 200, 300, 200]


def lightning():
    """Flashing lightning bolt."""
    _ = (0, 0, 0)
    Y = (255, 230, 0)
    W = (255, 255, 200)
    D = (120, 110, 0)
    f1 = [
        [_,_,_,_,_,_,_,_,Y,Y,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,Y,Y,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,Y,Y,Y,_,_,_,_,_,_,_],
        [_,_,_,_,_,Y,Y,Y,_,_,_,_,_,_,_,_],
        [_,_,_,_,Y,Y,Y,_,_,_,_,_,_,_,_,_],
        [_,_,_,Y,Y,Y,_,_,_,_,_,_,_,_,_,_],
        [_,_,Y,Y,Y,Y,Y,Y,Y,Y,_,_,_,_,_,_],
        [_,_,_,_,_,_,W,Y,Y,_,_,_,_,_,_,_],
        [_,_,_,_,_,W,Y,Y,_,_,_,_,_,_,_,_],
        [_,_,_,_,Y,Y,Y,_,_,_,_,_,_,_,_,_],
        [_,_,_,Y,Y,Y,_,_,_,_,_,_,_,_,_,_],
        [_,_,Y,Y,Y,_,_,_,_,_,_,_,_,_,_,_],
        [_,Y,Y,Y,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,Y,Y,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,Y,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    # Flash bright
    f2 = [[(W if c == Y else (Y if c == W else c)) for c in row] for row in f1]
    # Flash dark
    f3 = _empty()
    return [f1, f2, f3, f1], [200, 100, 150, 300]


def fire():
    """Flickering fire."""
    _ = (0, 0, 0)
    R = (255, 30, 0)
    O = (255, 130, 0)
    Y = (255, 220, 50)
    W = (255, 255, 200)
    f1 = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,R,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,_,_,_,_,_,_,_],
        [_,_,_,_,_,R,R,O,R,_,_,R,_,_,_,_],
        [_,_,_,R,_,R,O,O,R,R,R,R,_,_,_,_],
        [_,_,_,R,R,R,O,O,O,R,R,R,_,_,_,_],
        [_,_,R,R,O,O,O,Y,O,O,R,R,R,_,_,_],
        [_,_,R,O,O,O,Y,Y,Y,O,O,R,R,_,_,_],
        [_,R,R,O,O,Y,Y,W,Y,Y,O,O,R,_,_,_],
        [_,R,O,O,Y,Y,W,W,W,Y,Y,O,R,R,_,_],
        [_,R,O,O,Y,Y,W,W,W,Y,Y,O,R,R,_,_],
        [_,R,R,O,O,Y,Y,Y,Y,Y,O,O,R,R,_,_],
        [_,_,R,R,O,O,O,Y,O,O,O,R,R,_,_,_],
        [_,_,_,R,R,O,O,O,O,O,R,R,_,_,_,_],
        [_,_,_,_,R,R,R,R,R,R,R,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,_,_,_,_,_,_,_],
    ]
    f2 = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,R,_,_,R,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,R,R,_,_,_,_,_],
        [_,_,_,_,R,R,R,O,O,R,R,R,_,_,_,_],
        [_,_,_,R,R,R,O,O,O,O,R,R,_,_,_,_],
        [_,_,R,R,O,O,Y,Y,O,O,O,R,R,_,_,_],
        [_,_,R,O,O,Y,Y,W,Y,O,O,R,R,_,_,_],
        [_,R,R,O,Y,Y,W,W,W,Y,O,O,R,_,_,_],
        [_,R,O,O,Y,Y,W,W,W,Y,Y,O,R,R,_,_],
        [_,R,O,O,Y,Y,Y,W,Y,Y,O,O,R,R,_,_],
        [_,R,R,O,O,Y,Y,Y,Y,O,O,R,R,_,_,_],
        [_,_,R,R,O,O,O,O,O,O,R,R,_,_,_,_],
        [_,_,_,R,R,R,O,O,O,R,R,_,_,_,_,_],
        [_,_,_,_,_,R,R,R,R,R,_,_,_,_,_,_],
        [_,_,_,_,_,_,R,R,R,_,_,_,_,_,_,_],
    ]
    return [f1, f2], [300, 300]


def ghost():
    """Floating ghost — bobs up and down."""
    _ = (0, 0, 0)
    W = (240, 245, 255)
    G = (200, 210, 225)
    E = (30, 30, 60)
    M = (60, 60, 100)
    body = [
        [_,_,_,_,_,W,W,W,W,W,W,_,_,_,_,_],
        [_,_,_,_,W,W,W,W,W,W,W,W,_,_,_,_],
        [_,_,_,W,W,W,W,W,W,W,W,W,W,_,_,_],
        [_,_,W,W,W,W,W,W,W,W,W,W,W,W,_,_],
        [_,_,W,W,E,E,W,W,W,W,E,E,W,W,_,_],
        [_,_,W,W,E,E,W,W,W,W,E,E,W,W,_,_],
        [_,_,W,W,W,W,W,W,W,W,W,W,W,W,_,_],
        [_,_,W,W,W,W,W,M,M,W,W,W,W,W,_,_],
        [_,_,W,W,W,W,M,M,M,M,W,W,W,W,_,_],
        [_,_,W,W,W,W,W,W,W,W,W,W,W,W,_,_],
        [_,_,W,W,W,W,W,W,W,W,W,W,W,W,_,_],
        [_,_,W,W,W,W,W,W,W,W,W,W,W,W,_,_],
        [_,_,W,W,_,_,W,W,W,W,_,_,W,W,_,_],
        [_,_,W,_,_,_,_,W,W,_,_,_,_,W,_,_],
    ]
    # Frame 1: top position (y offset 0)
    f1 = _empty()
    for y, row in enumerate(body):
        for x, c in enumerate(row):
            if c != _ and y + 0 < 16: f1[y][x] = c
    # Frame 2: middle (y offset 1)
    f2 = _empty()
    for y, row in enumerate(body):
        for x, c in enumerate(row):
            if c != _ and y + 1 < 16: f2[y + 1][x] = c
    # Frame 3: bottom (y offset 2)
    f3 = _empty()
    for y, row in enumerate(body):
        for x, c in enumerate(row):
            if c != _ and y + 2 < 16: f3[y + 2][x] = c
    return [f1, f2, f3, f2], [400, 400, 400, 400]


def skull():
    """Skull with glowing eyes."""
    _ = (0, 0, 0)
    W = (255, 255, 255)
    G = (180, 190, 200)
    E = (30, 30, 30)
    R = (255, 50, 50)
    D = (150, 30, 30)
    base = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,W,W,W,W,W,W,_,_,_,_,_],
        [_,_,_,_,W,W,W,W,W,W,W,W,_,_,_,_],
        [_,_,_,W,W,W,W,W,W,W,W,W,W,_,_,_],
        [_,_,W,W,W,W,W,W,W,W,W,W,W,W,_,_],
        [_,_,W,W,E,E,E,W,W,E,E,E,W,W,_,_],
        [_,_,W,W,E,E,E,W,W,E,E,E,W,W,_,_],
        [_,_,W,W,E,E,E,W,W,E,E,E,W,W,_,_],
        [_,_,W,W,W,W,W,G,G,W,W,W,W,W,_,_],
        [_,_,_,W,W,W,W,E,W,W,W,W,W,_,_,_],
        [_,_,_,_,W,W,W,W,W,W,W,W,_,_,_,_],
        [_,_,_,_,W,E,W,E,W,E,W,E,_,_,_,_],
        [_,_,_,_,_,E,_,E,_,E,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    f1 = [row[:] for row in base]
    # Eyes glow red
    f2 = [row[:] for row in base]
    for y in range(5, 8):
        for x in [4, 5, 6, 9, 10, 11]:
            f2[y][x] = R
    # Eyes glow dim red
    f3 = [row[:] for row in base]
    for y in range(5, 8):
        for x in [4, 5, 6, 9, 10, 11]:
            f3[y][x] = D
    return [f1, f2, f3, f2], [500, 300, 400, 300]


# --- Test Patterns ---

def gradient():
    """Color gradient cycling through hues."""
    import math
    frames = []
    for phase in range(4):
        pixels = []
        offset = phase * 60
        for y in range(16):
            row = []
            for x in range(16):
                # Hue shifts with phase
                h = ((x * 24 + y * 12 + offset) % 360) / 360.0
                # HSV to RGB (s=1, v=1)
                i = int(h * 6)
                f = h * 6 - i
                q = 1 - f
                t = f
                if i == 0:   r, g, b = 1, t, 0
                elif i == 1: r, g, b = q, 1, 0
                elif i == 2: r, g, b = 0, 1, t
                elif i == 3: r, g, b = 0, q, 1
                elif i == 4: r, g, b = t, 0, 1
                else:        r, g, b = 1, 0, q
                row.append((int(r * 255), int(g * 255), int(b * 255)))
            pixels.append(row)
        frames.append(pixels)
    return frames, [300, 300, 300, 300]


def rainbow():
    """Rainbow arc appearing then sparkling."""
    import math
    _ = (0, 0, 0)
    W = (255, 255, 255)
    bands = [
        (255, 0, 0), (255, 80, 0), (255, 200, 0),
        (0, 200, 0), (0, 100, 255), (75, 0, 130), (148, 0, 211),
    ]
    cx, cy = 7.5, 14  # arc center at bottom
    def _arc(n_bands, sparkle=False):
        f = _empty()
        for b in range(n_bands):
            r_outer = 13 - b
            r_inner = r_outer - 1
            for y in range(16):
                for x in range(16):
                    d2 = (x - cx) ** 2 + (y - cy) ** 2
                    if r_inner * r_inner <= d2 <= r_outer * r_outer and y <= cy:
                        f[y][x] = bands[b]
        if sparkle:
            for sy, sx in [(1, 3), (0, 7), (1, 12), (3, 1), (3, 14), (5, 0)]:
                f[sy][sx] = W
        return f
    f1 = _arc(3)
    f2 = _arc(5)
    f3 = _arc(7)
    f4 = _arc(7, sparkle=True)
    return [f1, f2, f3, f4], [300, 300, 400, 500]


# --- Workflow ---

_ = (0, 0, 0)  # shorthand for black

def working():
    """Hammer striking — sparks fly."""
    BG = _
    M = (180, 180, 200)  # metal
    W = (140, 100, 60)   # wood handle
    S = (255, 220, 80)   # spark
    # Frame 1: hammer raised
    f1 = _empty()
    for x in range(5, 11): f1[3][x] = M; f1[4][x] = M
    f1[5][7] = W; f1[6][7] = W; f1[7][7] = W; f1[8][7] = W
    f1[5][8] = W; f1[6][8] = W; f1[7][8] = W; f1[8][8] = W
    f1[9][7] = W; f1[9][8] = W; f1[10][7] = W; f1[10][8] = W
    # Anvil base
    for x in range(3, 13): f1[13][x] = M; f1[14][x] = M
    for x in range(5, 11): f1[12][x] = M
    # Frame 2: hammer down + sparks
    f2 = _empty()
    for x in range(5, 11): f2[8][x] = M; f2[9][x] = M
    f2[5][7] = W; f2[6][7] = W; f2[7][7] = W
    f2[5][8] = W; f2[6][8] = W; f2[7][8] = W
    for x in range(3, 13): f2[13][x] = M; f2[14][x] = M
    for x in range(5, 11): f2[12][x] = M; f2[10][x] = M
    # Sparks
    f2[7][4] = S; f2[7][11] = S; f2[8][3] = S; f2[8][12] = S
    f2[6][5] = S; f2[6][10] = S; f2[9][2] = S; f2[9][13] = S
    # Frame 3: hammer raised again, fading sparks
    f3 = _copy(f1)
    f3[9][4] = S; f3[10][3] = S; f3[9][11] = S; f3[10][12] = S
    return [f1, f2, f3], [400, 200, 400]


def thinking():
    """Lightbulb — dims then lights up."""
    BG = _
    G = (100, 100, 110)   # glass off
    Y = (255, 240, 100)   # glass on
    B = (255, 255, 200)   # bright center
    M = (180, 180, 180)   # metal base
    D = (80, 80, 90)      # dark glass
    def _bulb(on=False):
        f = _empty()
        gc = Y if on else G
        bc = B if on else D
        # Bulb top
        for x in range(5, 11): f[2][x] = gc
        for x in range(4, 12): f[3][x] = gc; f[4][x] = gc
        for x in range(4, 12): f[5][x] = gc; f[6][x] = gc
        for x in range(5, 11): f[7][x] = gc
        # Center glow
        for x in range(6, 10):
            f[4][x] = bc; f[5][x] = bc
        # Filament
        f[6][6] = M; f[6][9] = M; f[7][7] = M; f[7][8] = M
        # Base
        for x in range(6, 10): f[8][x] = M; f[9][x] = M; f[10][x] = M
        f[11][7] = M; f[11][8] = M
        if on:
            # Rays
            f[0][7] = Y; f[0][8] = Y
            f[3][2] = Y; f[3][13] = Y
            f[6][1] = Y; f[6][14] = Y
            f[1][4] = Y; f[1][11] = Y
        return f
    return [_bulb(False), _bulb(False), _bulb(True), _bulb(True)], [500, 300, 400, 500]


def error():
    """Warning triangle flashing red."""
    BG = _
    Y = (255, 200, 0)
    R = (255, 50, 50)
    W = (255, 255, 255)
    K = (40, 30, 20)
    def _tri(color, flash=False):
        f = _empty()
        c = R if flash else color
        # Triangle outline
        f[2][7] = c; f[2][8] = c
        for x in range(6, 10): f[3][x] = c
        for x in range(5, 11): f[4][x] = c
        for x in range(4, 12): f[5][x] = c; f[6][x] = c
        for x in range(3, 13): f[7][x] = c; f[8][x] = c
        for x in range(2, 14): f[9][x] = c; f[10][x] = c
        for x in range(1, 15): f[11][x] = c; f[12][x] = c
        # Fill inside with yellow
        if not flash:
            for y in range(4, 12):
                for x in range(16):
                    if f[y][x] == c:
                        f[y][x] = Y
            # Re-draw border
            for y in range(3, 13):
                for x in range(16):
                    if f[y][x] == Y:
                        # check if edge
                        pass
        # Exclamation mark
        f[5][7] = K; f[5][8] = K; f[6][7] = K; f[6][8] = K
        f[7][7] = K; f[7][8] = K; f[8][7] = K; f[8][8] = K
        f[10][7] = K; f[10][8] = K
        return f
    # Simpler approach: hand-draw
    f1 = _empty()
    # Yellow triangle
    f1[2][7] = Y; f1[2][8] = Y
    for x in range(6, 10): f1[3][x] = Y
    for x in range(5, 11): f1[4][x] = Y
    for x in range(4, 12): f1[5][x] = Y; f1[6][x] = Y
    for x in range(3, 13): f1[7][x] = Y; f1[8][x] = Y
    for x in range(2, 14): f1[9][x] = Y; f1[10][x] = Y
    for x in range(1, 15): f1[11][x] = Y; f1[12][x] = Y
    # Exclamation
    f1[5][7] = K; f1[5][8] = K; f1[6][7] = K; f1[6][8] = K
    f1[7][7] = K; f1[7][8] = K; f1[8][7] = K; f1[8][8] = K
    f1[10][7] = K; f1[10][8] = K
    # Frame 2: red flash
    f2 = _empty()
    f2[2][7] = R; f2[2][8] = R
    for x in range(6, 10): f2[3][x] = R
    for x in range(5, 11): f2[4][x] = R
    for x in range(4, 12): f2[5][x] = R; f2[6][x] = R
    for x in range(3, 13): f2[7][x] = R; f2[8][x] = R
    for x in range(2, 14): f2[9][x] = R; f2[10][x] = R
    for x in range(1, 15): f2[11][x] = R; f2[12][x] = R
    f2[5][7] = W; f2[5][8] = W; f2[6][7] = W; f2[6][8] = W
    f2[7][7] = W; f2[7][8] = W; f2[8][7] = W; f2[8][8] = W
    f2[10][7] = W; f2[10][8] = W
    return [f1, f2, f1, f2], [300, 200, 300, 200]


def success():
    """Checkmark drawn then stars sparkle."""
    BG = _
    G = (50, 220, 50)
    W = (255, 255, 255)
    Y = (255, 220, 50)
    # Frame 1: partial check
    f1 = _empty()
    f1[9][4] = G; f1[10][5] = G; f1[11][6] = G
    # Frame 2: full check
    f2 = _empty()
    f2[9][4] = G; f2[10][5] = G; f2[11][6] = G; f2[10][7] = G
    f2[9][8] = G; f2[8][9] = G; f2[7][10] = G; f2[6][11] = G; f2[5][12] = G
    # Frame 3: check + stars
    f3 = _copy(f2)
    for y, x in [(2, 3), (1, 10), (3, 14), (12, 2), (13, 12), (4, 1)]:
        f3[y][x] = Y
    for y, x in [(1, 5), (3, 12), (14, 8)]:
        f3[y][x] = W
    return [f1, f2, f3], [300, 300, 500]


def coding():
    """Terminal screen with blinking cursor."""
    BG = _
    F = (30, 40, 50)    # frame
    S = (20, 25, 35)     # screen bg
    G = (50, 220, 50)    # green text
    C = (0, 200, 255)    # cyan
    W = (255, 255, 255)  # cursor
    def _screen(cursor_on=True, lines=2):
        f = _empty()
        # Frame border
        for x in range(1, 15): f[1][x] = F; f[13][x] = F
        for y in range(1, 14): f[y][0] = F; f[y][15] = F
        # Screen fill
        for y in range(2, 13):
            for x in range(1, 15): f[y][x] = S
        # Prompt line 1: $ _
        f[3][2] = G; f[3][3] = G; f[3][4] = G; f[3][5] = G; f[3][6] = G
        if lines >= 2:
            f[5][2] = C; f[5][3] = C; f[5][4] = C; f[5][5] = C
            f[5][7] = G; f[5][8] = G; f[5][9] = G
        if lines >= 3:
            f[7][2] = G; f[7][3] = G; f[7][4] = G; f[7][5] = G; f[7][6] = G; f[7][7] = G
        # Cursor
        cy = 3 + lines * 2
        if cy < 13 and cursor_on:
            f[cy][2] = W; f[cy][3] = W
        # Title dots
        f[1][2] = (255, 80, 80); f[1][4] = (255, 200, 0); f[1][6] = (50, 200, 50)
        return f
    return [_screen(True, 1), _screen(False, 1), _screen(True, 2), _screen(True, 3)], [400, 300, 400, 500]


def loading():
    """Spinning ring of dots."""
    BG = _
    W = (255, 255, 255)
    D = (60, 60, 80)
    # 8 dots in a circle
    positions = [(3, 7), (3, 11), (7, 13), (11, 11), (12, 7), (11, 3), (7, 2), (3, 3)]
    frames = []
    for phase in range(8):
        f = _empty()
        for i, (y, x) in enumerate(positions):
            dist = (i - phase) % 8
            if dist == 0:
                f[y][x] = W; f[y][x + 1] = W
            elif dist == 1:
                c = (200, 200, 220)
                f[y][x] = c; f[y][x + 1] = c
            elif dist == 2:
                c = (140, 140, 160)
                f[y][x] = c; f[y][x + 1] = c
            else:
                f[y][x] = D; f[y][x + 1] = D
        frames.append(f)
    return frames, [120] * 8


def building():
    """Blocks stacking up."""
    BG = _
    colors = [(255, 80, 80), (255, 180, 50), (50, 200, 50), (80, 150, 255), (180, 100, 255)]
    # Ground
    GR = (100, 80, 60)
    frames = []
    for n in range(len(colors)):
        f = _empty()
        for x in range(16): f[15][x] = GR
        for i in range(n + 1):
            c = colors[i]
            y = 14 - i * 2
            for dy in range(2):
                for dx in range(6):
                    if 0 <= y - dy < 16:
                        f[y - dy][5 + dx] = c
        frames.append(f)
    return frames, [400] * len(colors)


def deploying():
    """Rocket launching upward."""
    BG = _
    W = (240, 240, 255)
    R = (255, 50, 50)
    O = (255, 150, 0)
    Y = (255, 220, 50)
    G = (100, 100, 120)
    def _rocket(yoff, flame=True):
        f = _empty()
        # Nose cone
        y = 2 + yoff
        if 0 <= y < 16: f[y][7] = R; f[y][8] = R
        y = 3 + yoff
        if 0 <= y < 16:
            for x in range(6, 10): f[y][x] = W
        # Body
        for dy in range(4):
            y = 4 + dy + yoff
            if 0 <= y < 16:
                for x in range(6, 10): f[y][x] = W
                f[y][7] = G; f[y][8] = G
        # Fins
        y = 7 + yoff
        if 0 <= y < 16: f[y][5] = R; f[y][10] = R
        y = 8 + yoff
        if 0 <= y < 16: f[y][5] = R; f[y][10] = R
        # Flame
        if flame:
            y = 9 + yoff
            if 0 <= y < 16: f[y][7] = Y; f[y][8] = Y
            y = 10 + yoff
            if 0 <= y < 16: f[y][7] = O; f[y][8] = O
            y = 11 + yoff
            if 0 <= y < 16: f[y][7] = R
        return f
    return [_rocket(4), _rocket(2), _rocket(0), _rocket(-2)], [300, 250, 200, 200]


def testing():
    """Test tube with bubbling liquid."""
    BG = _
    G = (200, 210, 220)  # glass
    L = (80, 200, 120)   # liquid
    B = (150, 255, 180)  # bubble
    D = (50, 150, 80)    # dark liquid
    def _tube(bubbles):
        f = _empty()
        # Tube outline
        for y in range(2, 12):
            f[y][6] = G; f[y][10] = G
        for x in range(6, 11): f[12][x] = G
        f[2][7] = G; f[2][9] = G  # rim
        # Liquid fill
        for y in range(7, 12):
            for x in range(7, 10): f[y][x] = L
        f[12][7] = D; f[12][8] = D; f[12][9] = D
        # Bubbles
        for by, bx in bubbles:
            if 3 <= by < 12 and 7 <= bx <= 9:
                f[by][bx] = B
        return f
    f1 = _tube([(9, 8)])
    f2 = _tube([(7, 7), (9, 9)])
    f3 = _tube([(5, 8), (8, 7), (10, 9)])
    f4 = _tube([(3, 8), (6, 9), (9, 8)])
    return [f1, f2, f3, f4], [300, 300, 300, 300]


def searching():
    """Magnifying glass scanning."""
    BG = _
    G = (180, 200, 220)  # glass rim
    L = (200, 220, 255)  # lens
    H = (140, 100, 60)   # handle
    def _mag(cx):
        f = _empty()
        # Lens circle (radius ~3)
        for y in range(16):
            for x in range(16):
                if (x - cx) ** 2 + (y - 6) ** 2 <= 9:
                    f[y][x] = L
                elif (x - cx) ** 2 + (y - 6) ** 2 <= 16:
                    f[y][x] = G
        # Handle
        f[9][cx + 2] = H; f[10][cx + 3] = H; f[11][cx + 4] = H
        if cx + 5 < 16: f[12][cx + 5] = H
        return f
    return [_mag(5), _mag(7), _mag(9), _mag(7)], [350, 350, 350, 350]


def downloading():
    """Arrow moving down + progress bar."""
    BG = _
    C = (0, 200, 255)
    G = (50, 180, 50)
    D = (40, 40, 50)
    def _dl(phase):
        f = _empty()
        # Arrow body
        ay = 2 + phase
        for dy in range(4):
            y = ay + dy
            if 0 <= y < 11: f[y][7] = C; f[y][8] = C
        # Arrow head
        hy = ay + 4
        if 0 <= hy < 12:
            f[hy][5] = C; f[hy][6] = C; f[hy][7] = C; f[hy][8] = C; f[hy][9] = C; f[hy][10] = C
        if 0 <= hy + 1 < 12:
            f[hy + 1][6] = C; f[hy + 1][7] = C; f[hy + 1][8] = C; f[hy + 1][9] = C
        if 0 <= hy + 2 < 12:
            f[hy + 2][7] = C; f[hy + 2][8] = C
        # Progress bar
        for x in range(3, 13): f[13][x] = D; f[14][x] = D
        fill = 3 + int((phase + 1) / 3 * 10)
        for x in range(3, min(fill, 13)): f[13][x] = G; f[14][x] = G
        return f
    return [_dl(0), _dl(1), _dl(2)], [350, 350, 350]


def uploading():
    """Arrow moving up + progress bar."""
    BG = _
    C = (0, 200, 255)
    G = (50, 180, 50)
    D = (40, 40, 50)
    def _ul(phase):
        f = _empty()
        ay = 8 - phase
        # Arrow head
        hy = ay - 2
        if 0 <= hy < 16: f[hy][7] = C; f[hy][8] = C
        if 0 <= hy + 1 < 16:
            f[hy + 1][6] = C; f[hy + 1][7] = C; f[hy + 1][8] = C; f[hy + 1][9] = C
        if 0 <= hy + 2 < 16:
            f[hy + 2][5] = C; f[hy + 2][6] = C; f[hy + 2][7] = C; f[hy + 2][8] = C; f[hy + 2][9] = C; f[hy + 2][10] = C
        # Arrow body
        for dy in range(4):
            y = ay + 1 + dy
            if 0 <= y < 12: f[y][7] = C; f[y][8] = C
        # Progress bar
        for x in range(3, 13): f[13][x] = D; f[14][x] = D
        fill = 3 + int((phase + 1) / 3 * 10)
        for x in range(3, min(fill, 13)): f[13][x] = G; f[14][x] = G
        return f
    return [_ul(0), _ul(1), _ul(2)], [350, 350, 350]


def debugging():
    """Bug with magnifying glass."""
    BG = _
    BU = (80, 60, 40)   # bug body
    L = (50, 40, 30)     # legs
    R = (255, 50, 50)    # bug eyes
    G = (180, 200, 220)  # glass
    H = (140, 100, 60)   # handle
    def _bug_frame(bx, mx):
        f = _empty()
        # Bug
        f[9][bx] = BU; f[9][bx + 1] = BU; f[10][bx] = BU; f[10][bx + 1] = BU
        f[8][bx] = R; f[8][bx + 1] = R
        if bx > 0: f[9][bx - 1] = L; f[10][bx - 1] = L
        if bx + 2 < 16: f[9][bx + 2] = L; f[10][bx + 2] = L
        f[11][bx] = L; f[11][bx + 1] = L
        # Magnifying glass
        for y in range(16):
            for x in range(16):
                if (x - mx) ** 2 + (y - 7) ** 2 <= 9:
                    if f[y][x] == BG: f[y][x] = (200, 220, 255)
                elif (x - mx) ** 2 + (y - 7) ** 2 <= 16:
                    f[y][x] = G
        f[10][mx + 2] = H; f[11][mx + 3] = H; f[12][mx + 4] = H
        return f
    return [_bug_frame(4, 8), _bug_frame(6, 9), _bug_frame(8, 10), _bug_frame(6, 8)], [400, 350, 350, 400]


def saving():
    """Floppy disk with write flash."""
    BG = _
    B = (60, 100, 200)   # disk body
    M = (180, 180, 200)  # metal
    L = (120, 160, 220)  # label
    W = (255, 255, 255)
    def _disk(flash=False):
        f = _empty()
        # Disk body
        for y in range(3, 14):
            for x in range(3, 13): f[y][x] = B
        # Metal shutter
        for x in range(5, 11): f[3][x] = M; f[4][x] = M; f[5][x] = M
        f[3][7] = B; f[4][7] = B; f[5][7] = B
        # Label
        for x in range(5, 11): f[9][x] = L; f[10][x] = L; f[11][x] = L; f[12][x] = L
        if flash:
            # Write indicator
            f[1][12] = W; f[2][12] = W
            f[1][13] = (50, 220, 50)
        return f
    return [_disk(False), _disk(True), _disk(False), _disk(True)], [400, 200, 400, 200]


def syncing():
    """Two circular arrows rotating."""
    BG = _
    C = (0, 200, 255)
    G = (50, 200, 50)
    # Simple two arrows in a circle
    def _sync(phase):
        f = _empty()
        # Top arrow (right-pointing)
        if phase == 0:
            for x in range(4, 12): f[4][x] = C
            f[3][10] = C; f[3][11] = C; f[5][10] = C; f[5][11] = C
            for x in range(4, 12): f[11][x] = G
            f[10][4] = G; f[10][5] = G; f[12][4] = G; f[12][5] = G
        else:
            for x in range(4, 12): f[4][x] = G
            f[3][4] = G; f[3][5] = G; f[5][4] = G; f[5][5] = G
            for x in range(4, 12): f[11][x] = C
            f[10][10] = C; f[10][11] = C; f[12][10] = C; f[12][11] = C
        return f
    return [_sync(0), _sync(1)], [500, 500]


def done():
    """Fireworks burst."""
    BG = _
    colors = [(255, 80, 80), (255, 220, 50), (50, 220, 50), (80, 150, 255), (255, 100, 255), (0, 220, 255)]
    # Frame 1: center dot
    f1 = _empty()
    f1[7][7] = (255, 255, 255); f1[7][8] = (255, 255, 255)
    f1[8][7] = (255, 255, 255); f1[8][8] = (255, 255, 255)
    # Frame 2: small burst
    f2 = _copy(f1)
    for i, (dy, dx) in enumerate([(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]):
        y, x = 7 + dy, 7 + dx
        if 0 <= y < 16 and 0 <= x < 16:
            f2[y][x] = colors[i % len(colors)]
    # Frame 3: big burst
    f3 = _empty()
    for i, (dy, dx) in enumerate([(-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (-3, 3), (3, -3), (3, 3),
                                   (-5, -1), (-1, -5), (5, 1), (1, 5), (-2, 4), (4, 2), (-4, -2), (2, -4)]):
        y, x = 7 + dy, 7 + dx
        if 0 <= y < 16 and 0 <= x < 16:
            f3[y][x] = colors[i % len(colors)]
    # Frame 4: fading
    f4 = _empty()
    for i, (dy, dx) in enumerate([(-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (-4, 4), (4, -4), (4, 4)]):
        y, x = 7 + dy, 7 + dx
        if 0 <= y < 16 and 0 <= x < 16:
            r, g, b = colors[i % len(colors)]
            f4[y][x] = (r // 3, g // 3, b // 3)
    return [f1, f2, f3, f4], [200, 200, 300, 400]


# =============================================
#  Registry
# =============================================

PRESETS = {
    # Emoji
    "heart": ("Beating heart", heart),
    "smiley": ("Winking smiley", smiley),
    "star": ("Twinkling star", star),
    "thumbs-up": ("Bouncing thumbs up", thumbs_up),
    # Weather
    "sun": ("Spinning sun", sun),
    "moon": ("Moon & stars", moon),
    "cloud": ("Drifting cloud", cloud),
    "rain": ("Rain", rain),
    "snow": ("Snowfall", snow),
    "lightning": ("Lightning flash", lightning),
    # Animals
    "cat": ("Blinking cat", cat),
    "dog": ("Tongue-wagging dog", dog),
    "fish": ("Swimming fish", fish),
    # Plants / Nature
    "flower": ("Blooming flower", flower),
    "tree": ("Christmas tree", tree),
    "fire": ("Flickering fire", fire),
    # Symbols
    "check": ("Checkmark stroke", check),
    "cross": ("Cross pulse", cross),
    "music": ("Bouncing note", music),
    "ghost": ("Floating ghost", ghost),
    "skull": ("Glowing skull", skull),
    # Test
    "gradient": ("Color cycle", gradient),
    "rainbow": ("Rainbow arc", rainbow),
    # Workflow
    "working": ("Hammer strike", working),
    "thinking": ("Lightbulb", thinking),
    "error": ("Warning flash", error),
    "success": ("Checkmark + stars", success),
    "coding": ("Terminal", coding),
    "loading": ("Spinning ring", loading),
    "building": ("Block stack", building),
    "deploying": ("Rocket launch", deploying),
    "testing": ("Test tube", testing),
    "searching": ("Magnifying glass", searching),
    "downloading": ("Download arrow", downloading),
    "uploading": ("Upload arrow", uploading),
    "debugging": ("Bug hunt", debugging),
    "saving": ("Floppy disk", saving),
    "syncing": ("Sync arrows", syncing),
    "done": ("Fireworks", done),
}
