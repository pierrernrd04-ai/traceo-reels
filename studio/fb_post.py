#!/usr/bin/env python3
"""Facebook group post for Traceo: 4:5 visual (2160x2700), static PNG variants + animated MP4."""
import math
import os
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cv2  # noqa: E402
import numpy as np  # noqa: E402

import engine as E  # noqa: E402

E.W, E.H = 2160, 2700
W, H = E.W, E.H
from engine import (BLUE, DOTW, TEAL, Layer, Path, blit, circle, city, clamp, eback, ein,  # noqa: E402
                    eout, glow_dot, glow_path, grad_poly, hexc, line, loop_from_cells, mix, poly,
                    rrect, smooth, text, wordmark)

ML, MR = 150, 2010
INK = (244, 247, 246)
GREY = (142, 158, 156)
DARK = (6, 16, 15)
CARD = (150, 1000, 2010, 1960)


# ------------------------------------------------------------------ helpers
def grad_layer(L, c1, c2):
    out = Layer.__new__(Layer)
    g = np.linspace(0, 1, L.w, dtype=np.float32)[None, :, None]
    col = np.array(c1, np.float32) * (1 - g) + np.array(c2, np.float32) * g
    out.rgb = (col * L.a).astype(np.float32)
    out.a, out.w, out.h = L.a, L.w, L.h
    return out


@lru_cache(maxsize=512)
def gtext(s, fk, size):
    return grad_layer(text(s, fk, size, (255, 255, 255), maxw=4000), TEAL, BLUE)


def over(canvas, L, x, y):
    """Premultiplied 'over' of layer L onto layer canvas at (x, y) (in place)."""
    x, y = int(x), int(y)
    h, w = L.h, L.w
    ra = L.a
    canvas.rgb[y:y + h, x:x + w] = canvas.rgb[y:y + h, x:x + w] * (1 - ra) + L.rgb
    canvas.a[y:y + h, x:x + w] = canvas.a[y:y + h, x:x + w] * (1 - ra) + ra


def box_layer(w, h, r, fill, fill_a=255, border=None, bth=3, grad=None):
    arr = np.zeros((h, w, 4), np.uint8)
    rrect(arr, 0, 0, w - 1, h - 1, r, tuple(fill) + (fill_a,))
    if border:
        rrect(arr, 1, 1, w - 2, h - 2, r, tuple(border) + (255,), th=bth)
    L = Layer(arr)
    if grad:
        g = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]
        col = np.array(grad[0], np.float32) * (1 - g) + np.array(grad[1], np.float32) * g
        L.rgb = (col * L.a).astype(np.float32)
    return L


def chip(items, pad_x=34, pad_y=22, gap=14, fill=(12, 24, 25), fill_a=235, border=(40, 60, 62),
         r=None, vertical=False):
    """A rounded label box holding text layers laid out in a row (or a column)."""
    if vertical:
        w = max(L.w for L in items) + 2 * pad_x
        h = sum(L.h for L in items) + gap * (len(items) - 1) + 2 * pad_y
    else:
        w = sum(L.w for L in items) + gap * (len(items) - 1) + 2 * pad_x
        h = max(L.h for L in items) + 2 * pad_y
    box = box_layer(w, h, r or min(h // 2, 40), fill, fill_a, border)
    x, y = pad_x, pad_y
    for L in items:
        if vertical:
            over(box, L, x, y)
            y += L.h + gap
        else:
            over(box, L, x, (h - L.h) // 2)
            x += L.w + gap
    return box


def dot_layer(r, col):
    s = 2 * r + 4
    arr = np.zeros((s, s, 4), np.uint8)
    cv2.circle(arr, (s // 2, s // 2), r, tuple(col) + (255,), -1, cv2.LINE_AA)
    return Layer(arr)


# ------------------------------------------------------------------ static assets
def make_bg():
    k = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    c1, c2 = np.array(hexc("#040B0A"), np.float32), np.array(hexc("#0A1518"), np.float32)
    bg = np.repeat(c1 * (1 - k) + c2 * k, W, axis=1)
    yy, xx = np.ogrid[:H, :W]
    for cx, cy, r, col, s in ((1600, 1450, 1350, TEAL, 0.15), (200, 2550, 1100, BLUE, 0.10),
                              (2050, 150, 900, BLUE, 0.08)):
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
        kk = (np.clip(1 - d, 0, 1) ** 2 * s)[..., None].astype(np.float32)
        bg = bg * (1 - kk) + np.array(col, np.float32) * kk
    rng = np.random.default_rng(3)
    bg += rng.normal(0, 2.0, (H, W, 1)).astype(np.float32)
    return np.clip(bg, 0, 255).astype(np.uint8)


NODES, EDGES = city(11, cols=7, rows=4, x0=60, y0=1040, cw=310, ch=270, jitter=34)
OLD_CELLS = [(1, 1)]
NEW_CELLS = [(2, 1), (3, 1), (4, 1), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (4, 2)]


def rotate_to(pts, start):
    i = int(np.argmin([(p[0] - start[0]) ** 2 + (p[1] - start[1]) ** 2 for p in pts]))
    return pts[i:] + pts[:i]


HOME = NODES[(2, 2)]
_old, OLD_BND = loop_from_cells(NODES, OLD_CELLS)
_new, NEW_BND = loop_from_cells(NODES, NEW_CELLS)
OLD = smooth(rotate_to(_old, HOME), 3)
NEW = smooth(rotate_to(_new, HOME), 2)
OLD = rotate_to(OLD, HOME) + [rotate_to(OLD, HOME)[0]]
NEW = rotate_to(NEW, HOME) + [rotate_to(NEW, HOME)[0]]
P_OLD, P_NEW = Path(OLD), Path(NEW)


def make_map_base(bg):
    """Card with the street map, composited into the background (static part)."""
    x0, y0, x1, y1 = CARD
    mask = np.zeros((H, W), np.uint8)
    rrect(mask, x0, y0, x1, y1, 56, 255)
    m = bg.copy()
    m[:] = (m.astype(np.float32) * 0.55 + np.array((10, 20, 21), np.float32) * 0.45).astype(np.uint8)
    rnd = np.random.default_rng(5)
    # park and water blocks
    for (i, j), col in (((6, 1), (16, 34, 28)), ((0, 2), (16, 34, 28)), ((6, 2), (14, 28, 36))):
        pts = [NODES[(i, j)], NODES[(i + 1, j)], NODES[(i + 1, j + 1)], NODES[(i, j + 1)]]
        cv2.fillPoly(m, [np.array(pts, np.int32)], col, cv2.LINE_AA)
    # lanes inside blocks
    for i in range(7):
        for j in range(4):
            if rnd.random() < 0.55:
                a = np.array(NODES[(i, j)]) * 0.5 + np.array(NODES[(i + 1, j)]) * 0.5
                b = np.array(NODES[(i, j + 1)]) * 0.5 + np.array(NODES[(i + 1, j + 1)]) * 0.5
                line(m, a, b, (21, 33, 35), 6)
            if rnd.random() < 0.35:
                a = np.array(NODES[(i, j)]) * 0.5 + np.array(NODES[(i, j + 1)]) * 0.5
                b = np.array(NODES[(i + 1, j)]) * 0.5 + np.array(NODES[(i + 1, j + 1)]) * 0.5
                line(m, a, b, (21, 33, 35), 6)
    for a, b in list(EDGES) + list(OLD_BND) + list(NEW_BND):
        line(m, NODES[a], NODES[b], (30, 45, 47), 14)
    # a diagonal avenue
    poly(m, [(60, 1900), (900, 1730), (1500, 1220), (2200, 1000)], (34, 50, 52), 22)
    out = bg.copy()
    sel = mask > 0
    out[sel] = m[sel]
    border = np.zeros_like(out)
    rrect(border, x0, y0, x1, y1, 56, (38, 58, 60), th=3)
    bsel = border.any(-1)
    out[bsel] = border[bsel]
    return out, sel


BG = make_bg()
BASE, MASK = make_map_base(BG)

WM = wordmark(70, INK)
TOPPILL = chip([dot_layer(11, TEAL), text("GRATUIT · SANS APPLI", "inter_med", 40, TEAL, maxw=4000,
                                          track=4)],
               pad_x=36, pad_y=20, fill=(8, 22, 20), fill_a=255, border=(36, 110, 90), gap=18)

OLD_LBL = text("TON TOUR HABITUEL", "inter_med", 32, GREY, maxw=4000, track=4)
HOME_CHIP = chip([dot_layer(10, DOTW), text("Départ : chez toi", "inter_med", 38, INK, maxw=4000)],
                 pad_x=28, pad_y=16, gap=14)
NEW_CHIP = chip([dot_layer(12, TEAL), text("Ta nouvelle boucle", "inter_xbold", 44, INK, maxw=4000),
                 text("7,5 km", "inter_med", 44, GREY, maxw=4000)], pad_x=36, pad_y=22, gap=18,
                fill=(9, 26, 24), fill_a=240, border=(40, 120, 96))

STATS = [
    ("10 s", "pour tracer ta boucle\ndepuis chez toi"),
    ("42 km", "dès 2 km, ou en durée\nde 10 min à 4 h"),
    ("0 €", "pour commencer,\nsans appli à installer"),
]
SY0, SY1 = 2015, 2330
SW = (MR - ML - 2 * 36) // 3
STAT_BOX = box_layer(SW, SY1 - SY0, 40, (11, 21, 23), 232, (32, 50, 52))
STAT_LBL = [text(s[1], "inter_med", 40, GREY, maxw=SW - 80, lh=1.22) for s in STATS]

BY0, BY1 = 2395, 2560
BTN = box_layer(MR - ML, BY1 - BY0, (BY1 - BY0) // 2, (255, 255, 255), 255, grad=(TEAL, BLUE))
BTN_TXT = text("Trace ta boucle gratuite", "inter_black", 70, DARK, maxw=4000)
BTN_ARROW = text("→", "inter_black", 84, DARK, maxw=4000)
URL = text("traceorun.pages.dev  ·  partout en France  ·  guidage vocal", "inter_med", 40, GREY,
           maxw=4000)
BTN_MASK = BTN.a[..., 0]


def draw_old(f, frac=1.0, wear=1.0):
    pts = P_OLD.part(frac)
    if len(pts) < 2:
        return
    poly(f, pts, mix((34, 46, 48), (62, 74, 76), wear), int(18 + 16 * wear))
    poly(f, pts, mix((96, 108, 110), (168, 176, 176), wear), 9)


def draw_new(f, frac=1.0, head=True):
    pts = P_NEW.part(frac)
    if len(pts) < 2:
        return
    glow_path(f, pts, mix((0, 0, 0), TEAL, 0.85), 34, 46, 0.75)
    n = max(8, int(160 * frac))
    sp = Path(pts).resample(n + 1)
    for i in range(n):
        u = (i / n) * frac
        line(f, sp[i], sp[i + 1], mix(TEAL, BLUE, math.sin(min(1, u) * math.pi * 0.98) ** 1.1), 20)
    if head and frac < 0.999:
        glow_dot(f, pts[-1], 40, (255, 255, 255), 0.6)
        circle(f, pts[-1], 15, (255, 255, 255))


def draw_home(f, t_pulse=None):
    if t_pulse is not None:
        ph = t_pulse % 1.6 / 1.6
        r = 26 + 70 * eout(ph, 2)
        a = 1 - ph
        circle(f, HOME, r, mix((10, 20, 21), DOTW, 0.55 * a), 4)
    glow_dot(f, HOME, 46, DOTW, 0.45)
    circle(f, HOME, 26, DOTW)
    circle(f, HOME, 11, (10, 20, 21))


def shimmer(f, pos):
    """Diagonal light band across the CTA button; pos in 0..1."""
    h, w = BY1 - BY0, MR - ML
    xx = np.arange(w, dtype=np.float32)[None, :]
    yy = np.arange(h, dtype=np.float32)[:, None]
    c = -300 + pos * (w + 600)
    band = np.exp(-(((xx + 0.45 * yy) - c) / 70) ** 2) * 0.55 * BTN_MASK
    reg = f[BY0:BY1, ML:MR].astype(np.float32)
    reg = reg + (255 - reg) * band[..., None]
    f[BY0:BY1, ML:MR] = reg.astype(np.uint8)


# ------------------------------------------------------------------ scene
HEADS = {
    "A": (["Tu cours encore", "le *même* *tour* ?"],
          "3 sorties par semaine, c'est *156* *fois*\nle même parcours par an."),
    "B": (["Donne une distance.", "Reçois une *boucle* *neuve.*"],
          "Une boucle depuis chez toi, par des\n*rues* *que* *tu* *n'as* *jamais* *courues.*"),
}


class Post:
    duration = 12.0
    name = "fb-post"

    def __init__(self, variant="A", static=False):
        self.v = variant
        self.static = static
        h, sub = HEADS[variant]
        size = 212
        while max(text(x, "inter_black", size, INK, maxw=9000, accent=TEAL).w for x in h) > 1880:
            size -= 4
        self.h1 = text(h[0], "inter_black", size, INK, maxw=9000, accent=TEAL)
        self.h2 = text(h[1], "inter_black", size, INK, maxw=9000, accent=TEAL)
        self.lh = int(size * 1.06)
        self.sub = text(sub, "inter_light", 62, GREY, maxw=1900, lh=1.22, accent=INK)
        self.show_old = variant == "A"
        if self.show_old:
            self.k = dict(old=0.7, count=1.3, count_d=1.6, sub=1.6, home=2.7, new=3.0, lbl=4.6,
                          st=4.75, cta=5.75)
        else:
            self.k = dict(old=99, count=99, count_d=1, sub=1.0, home=0.5, new=0.9, lbl=2.6,
                          st=2.8, cta=3.8)
        self.duration = 10.5

    def frame(self, t):
        K = self.k
        T = 99.0 if self.static else t
        f = BASE.copy()
        # top bar
        a = clamp(T / 0.4)
        blit(f, WM, ML, 150, a)
        blit(f, TOPPILL, MR - TOPPILL.w, 150 + WM.h / 2 - TOPPILL.h / 2, a)
        # headline
        y = max(300, 950 - (2 * self.lh + 50 + self.sub.h))
        for i, L in enumerate((self.h1, self.h2)):
            k = eout((T - 0.1 - 0.25 * i) / 0.55)
            blit(f, L, ML - 8, y + i * self.lh + 50 * (1 - k), k)
        ysub = y + self.lh * 2 + 50
        blit(f, self.sub, ML, ysub + 20 * (1 - eout((T - K["sub"]) / 0.6)),
             clamp((T - K["sub"]) / 0.6))

        def count_at(T):
            if T < K["count"]:
                return 1
            return 1 + int(round(155 * ein(clamp((T - K["count"]) / K["count_d"]), 2.0)))

        # map content (clipped to the card)
        m = f.copy()
        if self.show_old:
            c = count_at(T)
            draw_old(m, eout((T - K["old"]) / 0.6), wear=c / 156)
            if K["count"] <= T < K["count"] + K["count_d"] + 0.1:
                laps = 1 + 155 * ein(clamp((T - K["count"]) / K["count_d"]), 2.0)
                p = P_OLD.at((laps % 1) * P_OLD.L)
                circle(m, p, 14, (220, 226, 226))
        fr = 1.0 if self.static else eout((T - K["new"]) / 1.7, 2)
        if fr > 0:
            draw_new(m, fr)
        if not self.static and T > K["new"] + 1.9:
            u = ((T - K["new"] - 1.9) / 3.6) % 1.0
            trail = P_NEW.part(max(0, u - 0.07), u)
            if len(trail) > 1:
                poly(m, trail, (255, 255, 255), 10)
            p = P_NEW.at(u * P_NEW.L)
            glow_dot(m, p, 36, (255, 255, 255), 0.55)
            circle(m, p, 14, (255, 255, 255))
        draw_home(m, None if self.static else max(0.0, T - K["home"]))
        f[MASK] = m[MASK]

        # map labels
        if self.show_old and T >= K["old"]:
            num = text(f"×{count_at(T)}", "inter_black", 78, INK, maxw=4000)
            per = text("par an", "inter_med", 40, GREY, maxw=4000)
            row = chip([num, per], pad_x=0, pad_y=0, gap=16, fill=(0, 0, 0), fill_a=0, border=None)
            box = chip([OLD_LBL, row], pad_x=34, pad_y=24, gap=6, vertical=True)
            blit(f, box, 205, 1060, clamp((T - K["old"]) / 0.4))
        blit(f, HOME_CHIP, HOME[0], HOME[1] + 60, clamp((T - K["home"]) / 0.4), "mt")
        k = eback((T - K["lbl"]) / 0.45)
        if k > 0:
            blit(f, NEW_CHIP, 1440, 1446, clamp((T - K["lbl"]) / 0.25), "mm", scale=0.85 + 0.15 * k)

        # stats
        for i, (num, _) in enumerate(STATS):
            ti = T - K["st"] - 0.22 * i
            k = eout(ti / 0.5)
            if k <= 0:
                continue
            x = ML + i * (SW + 36)
            yy = SY0 + 70 * (1 - k)
            blit(f, STAT_BOX, x, yy, k)
            if num == "10 s":
                s = f"{int(round(10 * eout(clamp(ti / 0.9), 2)))} s"
            elif num == "42 km":
                s = f"{int(round(2 + 40 * eout(clamp(ti / 0.9), 2)))} km"
            else:
                s = num
            blit(f, gtext(s, "inter_black", 150), x + 40, yy + 26, k)
            blit(f, STAT_LBL[i], x + 44, yy + 205, k)

        # CTA
        t_cta = K["cta"]
        k = eback((T - t_cta) / 0.5, 1.8)
        if k > 0:
            a = clamp((T - t_cta) / 0.25)
            blit(f, BTN, (ML + MR) / 2, (BY0 + BY1) / 2, a, "mm", scale=0.9 + 0.1 * k)
            if k >= 0.999 or self.static:
                tw = BTN_TXT.w + 40 + BTN_ARROW.w
                bx = (ML + MR) / 2 - tw / 2
                nudge = 0 if self.static else 12 * math.sin(max(0, T - t_cta) * 4.0) ** 2
                blit(f, BTN_TXT, bx, (BY0 + BY1) / 2 - BTN_TXT.h / 2 + 2)
                blit(f, BTN_ARROW, bx + BTN_TXT.w + 40 + nudge, (BY0 + BY1) / 2 - BTN_ARROW.h / 2 - 4)
                for ts in (t_cta + 0.9, t_cta + 3.0):
                    if not self.static and ts <= T < ts + 0.9:
                        shimmer(f, (T - ts) / 0.9)
        blit(f, URL, (ML + MR) / 2, 2595, clamp((T - t_cta - 0.3) / 0.4), "mt")
        return f
