"""4K vertical motion-design engine (numpy + OpenCV for shapes, Pillow for type)."""
import math
import subprocess
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 2160, 3840, 30
X0, X1 = 150, 1700            # text column, clear of the right action rail
Y0, Y1 = 520, 2860            # clear of the top bar and the caption area
CX = (X0 + X1) // 2

F = {
    "inter_black": ("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 0),
    "inter_thin": ("/usr/share/fonts/opentype/inter/InterDisplay-Thin.otf", 0),
    "inter_light": ("/usr/share/fonts/opentype/inter/InterDisplay-Light.otf", 0),
    "inter_xbold": ("/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf", 0),
    "inter_med": ("/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf", 0),
    "heros_b": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bold.otf", 0),
    "heros_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-regular.otf", 0),
    "heroscn_bi": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheroscn-bolditalic.otf", 0),
    "heroscn_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheroscn-regular.otf", 0),
    "adv_b": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreadventor-bold.otf", 0),
    "adv_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreadventor-regular.otf", 0),
    "pop_sb": ("/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf", 0),
    "pop_b": ("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 0),
    "pop_l": ("/usr/share/fonts/truetype/google-fonts/Poppins-Light.ttf", 0),
    "mono_b": ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 0),
    "mono_r": ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 0),
    "lora": ("/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf", 0),
    "lora_i": ("/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf", 0),
    "pag_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-regular.otf", 0),
    "pag_i": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-italic.otf", 0),
    "pag_b": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-bold.otf", 0),
    "carl_b": ("/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf", 0),
    "carl_r": ("/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf", 0),
    "serif_l": ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Light.ttc", 0),
    "serif_sb": ("/usr/share/fonts/opentype/noto/NotoSerifCJK-SemiBold.ttc", 0),
    "serif_bl": ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc", 0),
    "src_r": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 0),
    "src_b": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 0),
    "src_bl": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", 0),
    "pixel": ("/usr/share/fonts/opentype/unifont/unifont.otf", 0),
    "quot_b": ("/usr/share/texmf/fonts/opentype/public/lm/lmsansquot8-bold.otf", 0),
    "quot_r": ("/usr/share/texmf/fonts/opentype/public/lm/lmsansquot8-regular.otf", 0),
    "schola_b": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-bold.otf", 0),
    "schola_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-regular.otf", 0),
    "schola_i": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-italic.otf", 0),
    "loma_b": ("/usr/share/fonts/opentype/tlwg/Loma-Bold.otf", 0),
    "loma_r": ("/usr/share/fonts/opentype/tlwg/Loma.otf", 0),
    "bonum_b": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrebonum-bold.otf", 0),
    "bonum_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrebonum-regular.otf", 0),
    "lmmono_c": ("/usr/share/texmf/fonts/opentype/public/lm/lmmonoltcond10-regular.otf", 0),
    "lmmono_b": ("/usr/share/texmf/fonts/opentype/public/lm/lmmonolt10-bold.otf", 0),
    "termes_b": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-bold.otf", 0),
    "termes_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-regular.otf", 0),
    "termes_i": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-italic.otf", 0),
    "cala_b": ("/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf", 0),
    "cala_r": ("/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf", 0),
    "cursor_b": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrecursor-bold.otf", 0),
    "cursor_r": ("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrecursor-regular.otf", 0),
}


@lru_cache(maxsize=512)
def font(key, size):
    path, idx = F[key]
    return ImageFont.truetype(path, size, index=idx)


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1, c2, a):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * a) for i in range(3))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eout(x, p=3):
    x = clamp(x)
    return 1 - (1 - x) ** p


def ein(x, p=3):
    x = clamp(x)
    return x ** p


def eback(x, s=1.4):
    x = clamp(x) - 1
    return x * x * ((s + 1) * x + s) + 1


def eexpo(x):
    x = clamp(x)
    return 1.0 if x >= 1 else 1 - 2 ** (-10 * x)


# ------------------------------------------------------------------ layers
class Layer:
    """Premultiplied RGBA as float32 (h, w, 3) colour + (h, w, 1) alpha."""
    __slots__ = ("rgb", "a", "w", "h")

    def __init__(self, rgba):
        arr = rgba.astype(np.float32) / 255.0
        self.a = arr[..., 3:4]
        self.rgb = arr[..., :3] * self.a * 255.0
        self.h, self.w = arr.shape[:2]

    def scaled(self, s):
        if abs(s - 1) < 1e-3:
            return self
        nw, nh = max(1, int(self.w * s)), max(1, int(self.h * s))
        L = Layer.__new__(Layer)
        interp = cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR
        L.rgb = cv2.resize(self.rgb, (nw, nh), interpolation=interp)
        L.a = cv2.resize(self.a, (nw, nh), interpolation=interp)[..., None]
        L.w, L.h = nw, nh
        return L


def from_pil(im):
    return Layer(np.asarray(im.convert("RGBA")))


def blit(frame, L, x, y, alpha=1.0, anchor="lt", scale=1.0):
    if alpha <= 0.003 or L is None:
        return
    if scale != 1.0:
        L = L.scaled(scale)
    if anchor == "mm":
        x, y = x - L.w / 2, y - L.h / 2
    elif anchor == "mt":
        x = x - L.w / 2
    elif anchor == "lm":
        y = y - L.h / 2
    elif anchor == "rt":
        x = x - L.w
    x, y = int(round(x)), int(round(y))
    fx0, fy0 = max(0, x), max(0, y)
    fx1, fy1 = min(W, x + L.w), min(H, y + L.h)
    if fx0 >= fx1 or fy0 >= fy1:
        return
    lx0, ly0 = fx0 - x, fy0 - y
    lx1, ly1 = lx0 + (fx1 - fx0), ly0 + (fy1 - fy0)
    reg = frame[fy0:fy1, fx0:fx1].astype(np.float32)
    a = L.a[ly0:ly1, lx0:lx1] * alpha
    reg = reg * (1 - a) + L.rgb[ly0:ly1, lx0:lx1] * alpha
    frame[fy0:fy1, fx0:fx1] = reg.astype(np.uint8)


@lru_cache(maxsize=2048)
def text(s, fk, size, color, maxw=X1 - X0, align="left", lh=1.08, track=0, accent=None):
    """Wrapped text layer. Words wrapped in *stars* take the accent colour."""
    fnt = font(fk, size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    sp = d0.textlength(" ", font=fnt)
    if track:
        sp += 2 * track

    def wl(w):
        w = w.strip("*")
        if not track:
            return d0.textlength(w, font=fnt)
        return sum(d0.textlength(c, font=fnt) + track for c in w) - track

    lines, cur, curw = [], [], 0
    for para in s.split("\n"):
        for w in para.split():
            ww = wl(w)
            if cur and curw + sp + ww > maxw:
                lines.append((cur, curw))
                cur, curw = [], 0
            curw = ww if not cur else curw + sp + ww
            cur.append(w)
        lines.append((cur, curw))
        cur, curw = [], 0
    asc, desc = fnt.getmetrics()
    lhpx = int(size * lh)
    pad = 8
    bw = int(max(l[1] for l in lines)) + 2 * pad
    bh = lhpx * (len(lines) - 1) + asc + desc + 2 * pad
    im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ws, lw_) in enumerate(lines):
        x = pad + (0 if align == "left" else (bw - 2 * pad - lw_) / (2 if align == "center" else 1))
        y = pad + i * lhpx
        for w in ws:
            col = accent if (w.startswith("*") and accent) else color
            w2 = w.strip("*")
            if track:
                for c in w2:
                    d.text((x, y), c, font=fnt, fill=col)
                    x += d0.textlength(c, font=fnt) + track
                x -= track
            else:
                d.text((x, y), w2, font=fnt, fill=col)
                x += d0.textlength(w2, font=fnt)
            x += sp
    return from_pil(im)


# ------------------------------------------------------------------ shapes
def flat(color):
    f = np.empty((H, W, 3), np.uint8)
    f[:] = color
    return f


def vgrad(c1, c2, curve=1.0):
    k = (np.linspace(0, 1, H) ** curve)[:, None, None]
    col = np.array(c1, np.float32) * (1 - k) + np.array(c2, np.float32) * k
    return np.repeat(col, W, axis=1).astype(np.uint8)


def radial(base, glow_col, cx, cy, r, strength=0.6):
    yy, xx = np.ogrid[:H, :W]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    k = np.clip(1 - d, 0, 1)[..., None] ** 2 * strength
    out = base.astype(np.float32) * (1 - k) + np.array(glow_col, np.float32) * k
    return out.astype(np.uint8)


def _p(pts):
    return (np.asarray(pts, np.float64) * 16).round().astype(np.int32)


def poly(frame, pts, color, th, closed=False):
    if len(pts) < 2:
        return
    cv2.polylines(frame, [_p(pts)], closed, color, int(th), cv2.LINE_AA, shift=4)


def line(frame, a, b, color, th):
    cv2.line(frame, tuple(_p([a])[0]), tuple(_p([b])[0]), color, int(th), cv2.LINE_AA, shift=4)


def circle(frame, c, r, color, th=-1):
    cv2.circle(frame, tuple(_p([c])[0]), int(r * 16), color, int(th), cv2.LINE_AA, shift=4)


def rrect(frame, x0, y0, x1, y1, r, color, th=-1):
    x0, y0, x1, y1, r = int(x0), int(y0), int(x1), int(y1), int(r)
    if th < 0:
        cv2.rectangle(frame, (x0 + r, y0), (x1 - r, y1), color, -1)
        cv2.rectangle(frame, (x0, y0 + r), (x1, y1 - r), color, -1)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)):
            cv2.circle(frame, (cx, cy), r, color, -1, cv2.LINE_AA)
    else:
        for (a, b) in (((x0 + r, y0), (x1 - r, y0)), ((x0 + r, y1), (x1 - r, y1)),
                       ((x0, y0 + r), (x0, y1 - r)), ((x1, y0 + r), (x1, y1 - r))):
            cv2.line(frame, a, b, color, th, cv2.LINE_AA)
        for (cx, cy, a0) in ((x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0),
                             (x0 + r, y1 - r, 90)):
            cv2.ellipse(frame, (cx, cy), (r, r), 0, a0, a0 + 90, color, th, cv2.LINE_AA)


def rrect_alpha(frame, x0, y0, x1, y1, r, color, alpha):
    """Translucent rounded rectangle (blended)."""
    x0, y0, x1, y1 = int(max(0, x0)), int(max(0, y0)), int(min(W, x1)), int(min(H, y1))
    if x1 <= x0 or y1 <= y0:
        return
    sub = frame[y0:y1, x0:x1].copy()
    rrect(sub, 0, 0, x1 - x0 - 1, y1 - y0 - 1, r, color)
    frame[y0:y1, x0:x1] = cv2.addWeighted(sub, alpha, frame[y0:y1, x0:x1], 1 - alpha, 0)


class Path:
    def __init__(self, pts, closed=False):
        pts = [tuple(map(float, p)) for p in pts]
        if closed:
            pts = pts + [pts[0]]
        self.pts = np.array(pts)
        seg = np.sqrt(((self.pts[1:] - self.pts[:-1]) ** 2).sum(1))
        self.cum = np.concatenate([[0], np.cumsum(seg)])
        self.L = self.cum[-1]

    def at(self, s):
        s = clamp(s, 0, self.L)
        i = int(np.searchsorted(self.cum, s, "right") - 1)
        i = min(i, len(self.pts) - 2)
        seg = self.cum[i + 1] - self.cum[i]
        k = 0 if seg == 0 else (s - self.cum[i]) / seg
        return tuple(self.pts[i] + (self.pts[i + 1] - self.pts[i]) * k)

    def part(self, a, b=None):
        """Points between fractions a..b of the length (b None: 0..a)."""
        if b is None:
            a, b = 0.0, a
        sa, sb = self.L * clamp(a), self.L * clamp(b)
        if sb <= sa:
            p = self.at(sa)
            return [p, p]
        inner = [tuple(p) for p, c in zip(self.pts, self.cum) if sa < c < sb]
        return [self.at(sa)] + inner + [self.at(sb)]

    def resample(self, n):
        return [self.at(self.L * i / (n - 1)) for i in range(n)]


def smooth(pts, iters=2, closed=True):
    """Chaikin corner cutting."""
    p = np.array(pts, float)
    for _ in range(iters):
        q = []
        rng = range(len(p)) if closed else range(len(p) - 1)
        for i in rng:
            a, b = p[i], p[(i + 1) % len(p)]
            q += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        if not closed:
            q = [p[0]] + q + [p[-1]]
        p = np.array(q)
    return [tuple(x) for x in p]


def grad_poly(frame, pts, c1, c2, th, n_seg=None):
    """Polyline with a colour gradient along its length."""
    if len(pts) < 2:
        return
    P = Path(pts)
    n = n_seg or max(2, min(160, int(P.L / 18)))
    sp = P.resample(n + 1)
    for i in range(n):
        col = mix(c1, c2, i / max(1, n - 1))
        line(frame, sp[i], sp[i + 1], col, th)


def glow_path(frame, pts, color, th, sigma=40, strength=0.9, closed=False):
    """Soft bloom under a path, drawn at quarter resolution."""
    if len(pts) < 2:
        return
    q = 4
    small = np.zeros((H // q, W // q, 3), np.uint8)
    cv2.polylines(small, [_p(np.array(pts) / q)], closed, color, max(1, int(th / q)), cv2.LINE_AA,
                  shift=4)
    small = cv2.GaussianBlur(small, (0, 0), sigma / q)
    big = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)
    cv2.addWeighted(frame, 1.0, big, strength, 0, dst=frame)


def glow_dot(frame, c, r, color, strength=0.8):
    q = 4
    small = np.zeros((H // q, W // q, 3), np.uint8)
    cv2.circle(small, (int(c[0] / q), int(c[1] / q)), max(1, int(r / q)), color, -1, cv2.LINE_AA)
    small = cv2.GaussianBlur(small, (0, 0), r / q)
    big = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)
    cv2.addWeighted(frame, 1.0, big, strength, 0, dst=frame)


# ------------------------------------------------------------------ city generator
def city(seed, cols=7, rows=11, x0=-80, y0=380, cw=340, ch=320, jitter=55):
    """Jittered street grid: nodes, edges, and helpers to build loops."""
    rnd = np.random.default_rng(seed)
    nodes = {}
    for i in range(cols + 1):
        for j in range(rows + 1):
            nodes[(i, j)] = (x0 + i * cw + rnd.uniform(-jitter, jitter),
                             y0 + j * ch + rnd.uniform(-jitter, jitter))
    edges = []
    for i in range(cols + 1):
        for j in range(rows + 1):
            if i < cols and rnd.random() > 0.06:
                edges.append(((i, j), (i + 1, j)))
            if j < rows and rnd.random() > 0.06:
                edges.append(((i, j), (i, j + 1)))
    return nodes, edges


def loop_from_cells(nodes, cells):
    """Boundary of a set of grid cells, as an ordered list of node points."""
    cnt = {}
    for (i, j) in cells:
        for e in (((i, j), (i + 1, j)), ((i + 1, j), (i + 1, j + 1)),
                  ((i + 1, j + 1), (i, j + 1)), ((i, j + 1), (i, j))):
            k = tuple(sorted(e))
            cnt[k] = cnt.get(k, 0) + 1
    bnd = [e for e, c in cnt.items() if c == 1]
    adj = {}
    for a, b in bnd:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    start = min(adj)
    order, prev, cur = [start], None, start
    while True:
        nxt = [n for n in adj[cur] if n != prev]
        if not nxt:
            break
        n = nxt[0]
        if n == start:
            break
        order.append(n)
        prev, cur = cur, n
        if len(order) > 400:
            break
    return [nodes[k] for k in order], bnd


# ------------------------------------------------------------------ Traceo logo
TEAL = hexc("#3CC79A")
BLUE = hexc("#4AA6D8")
DOTW = hexc("#EEF4F2")


def spiral_pts(cx, cy, s, n=220):
    """Traceo mark: a lead-in from the dot, sweeping clockwise into an inner curl."""
    pts = []
    for i in range(n):
        u = i / (n - 1)
        th = math.radians(152 + u * 378)
        r = (60 + 103 * math.exp(-(math.degrees(th) - 152) / 68)) * s
        r *= 1 + 0.06 * math.sin(u * math.pi)
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    return pts


def draw_mark(frame, cx, cy, s, frac=1.0, dot_k=1.0, glow=True, bright=1.0, dot=None):
    """Draw the spiral mark centred at (cx, cy); s=1 is ~330 px wide."""
    pts = spiral_pts(cx, cy, s)
    P = Path(pts)
    part = P.part(frac)
    th = 38 * s
    if glow and len(part) > 1:
        glow_path(frame, part, mix((0, 0, 0), TEAL, 0.8 * bright), th * 1.8, 34 * s, 0.55)
    if len(part) > 1:
        n = max(2, int(len(part)))
        P2 = Path(part)
        sp = P2.resample(min(140, n * 2))
        tot = len(sp) - 1
        for i in range(tot):
            u = (P2.L * i / tot) / P.L
            col = mix(TEAL, BLUE, math.sin(min(1, u * 1.25) * math.pi * 0.95) ** 1.2)
            line(frame, sp[i], sp[i + 1], col, th)
        circle(frame, sp[-1], th / 2, mix(TEAL, BLUE, 0.3))
    if dot_k > 0:
        d0 = pts[0]
        circle(frame, d0, 42 * s * dot_k, dot or DOTW)


@lru_cache(maxsize=32)
def wordmark(height, color=(240, 245, 244)):
    """'traceo' wordmark, last o in brand teal."""
    size = int(height * 1.38)
    fnt = font("inter_black", size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w1 = d0.textlength("trace", font=fnt)
    w2 = d0.textlength("o", font=fnt)
    im = Image.new("RGBA", (int(w1 + w2 + 20), int(size * 1.3)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((0, 0), "trace", font=fnt, fill=color + (255,))
    d.text((w1 - size * 0.02, 0), "o", font=fnt, fill=TEAL + (255,))
    bbox = im.getbbox()
    return from_pil(im.crop(bbox))


def watermark(frame, alpha=0.9, color=(240, 245, 244)):
    blit(frame, wordmark(64, color), X0, 470, alpha)


def endcard(frame, t, bg, tagline_layer, cta_layer, ink=(240, 245, 244), glow=True):
    """Brand end card: the mark draws itself, the dot lands, wordmark + tagline + CTA."""
    if isinstance(bg, np.ndarray):
        frame[:] = bg
    else:
        frame[:] = bg
    cy = 1500
    draw_mark(frame, CX + 20, cy, 1.9, eout(t / 0.9, 3), eback((t - 0.75) / 0.35), glow=glow,
              dot=None if glow else ink)
    wm = wordmark(150, ink)
    blit(frame, wm, CX, 1980 + 40 * (1 - eout((t - 0.9) / 0.5)), clamp((t - 0.9) / 0.4), "mt")
    blit(frame, tagline_layer, CX, 2280, clamp((t - 1.3) / 0.4), "mt")
    if cta_layer is not None:
        blit(frame, cta_layer, CX, 2560, clamp((t - 1.6) / 0.4), "mt")


def pill(label_layer, fill, pad_x=56, pad_y=30, r=None):
    w, h = label_layer.w + 2 * pad_x, label_layer.h + 2 * pad_y
    r = r or h // 2
    arr = np.zeros((h, w, 4), np.uint8)
    rrect(arr, 0, 0, w - 1, h - 1, r, fill + (255,))
    L = Layer(arr)
    sub = np.zeros((h, w, 3), np.uint8)
    # composite label onto the pill
    canvas = (L.rgb).copy()
    a = L.a.copy()
    lx, ly = pad_x, pad_y
    ra = label_layer.a
    canvas[ly:ly + label_layer.h, lx:lx + label_layer.w] = (
        canvas[ly:ly + label_layer.h, lx:lx + label_layer.w] * (1 - ra) + label_layer.rgb)
    out = Layer.__new__(Layer)
    out.rgb, out.a, out.w, out.h = canvas, a, w, h
    return out


# ------------------------------------------------------------------ render
def render(scene, out_path, audio_path, crf=17, preset="veryfast"):
    n = int(round(scene.duration * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", audio_path,
           "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-level:v", "5.1", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
           out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(scene.frame(i / FPS).tobytes())
    p.stdin.close()
    return p.wait()
