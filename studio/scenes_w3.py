"""Wave 3: Traceo Reels made from the daily menu (stock videos, method 1)."""
import numpy as np

from engine import (CX, circle, H, W, X0, X1, Path, blit, clamp, eback, endcard, eout, glow_dot, glow_path,
                    grad_poly, hexc, mix, pill, poly, rrect, text)
from scenes10 import loop, make_map, show

TEAL, BLUE = (60, 199, 154), (74, 166, 216)


# =====================================================================
# W3-01 — « Les niveaux du coureur » · FreeSans + Charter italique · sable et terracotta · UK garage
# =====================================================================
class Niveaux:
    name, duration, end_t, song = "w3-01-niveaux", 16.4, 14.0, "garage"
    BG, INK, TERRA = hexc("#EFE6D8"), hexc("#1B1B1B"), hexc("#D9603B")
    STREET, MUTED = hexc("#DCCFBC"), hexc("#8C8276")
    LV = [(0.0, 3.0), (3.0, 6.0), (6.0, 9.0), (9.0, 12.0)]

    def __init__(self):
        bg = np.empty((H, W, 3), np.uint8)
        bg[:] = self.BG
        self.bg = bg
        self.map, nodes, _ = make_map(11, bg, self.STREET, 9, x0=150, y0=1180, cw=260, ch=230,
                                      cols=6, rows=4, fade=False, jitter=30)
        self.small = Path(loop(nodes, {(1, 1), (2, 1), (1, 2), (2, 2)}), True)
        wander = [(1, 2), (2, 2), (2, 3), (3, 3), (3, 2), (4, 2), (4, 1), (3, 1), (3, 0), (4, 0), (5, 0),
                  (5, 1), (5, 2)]
        self.wander = Path([nodes[k] for k in wander])
        cells = {(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2), (4, 3)}
        self.big = Path(loop(nodes, cells), True)
        self.home = self.big.at(0)
        lab = ["NIVEAU 1", "NIVEAU 2", "NIVEAU 3", "NIVEAU MAX"]
        self.labels = [text(s, "free_b", 128, self.TERRA if i < 3 else hexc("#1F9E78"), track=6) for i, s in enumerate(lab)]
        lines = ["Tu cours *le* *même* *tour.*",
                 "Tu le cours *dans* *l'autre* *sens.*",
                 "Tu tournes au hasard et tu *cherches* *le* *retour.*",
                 "Une *boucle* *neuve* en 10 s, qui te ramène chez toi."]
        self.lines = [text(s, "free_b", 120, self.INK, maxw=1550, align="center", lh=1.15,
                           accent=self.TERRA if i < 3 else hexc("#1F9E78")) for i, s in enumerate(lines)]
        self.chip10 = pill(text("≈ 10 secondes", "free_b", 64, (255, 255, 255)), hexc("#1F9E78"), 48, 24)
        self.qmark = text("?", "charter_bi", 260, self.TERRA)
        self.q1 = text("T'es à quel", "charter_bi", 200, self.INK, align="center")
        self.q2 = text("niveau ?", "charter_bi", 200, self.TERRA, align="center")
        self.opts = text("1  ·  2  ·  3  ·  MAX", "free_b", 96, self.MUTED, track=4)
        self.cta = pill(text("Lien en bio", "free_b", 76, (255, 255, 255)), hexc("#1F9E78"), 64, 30)
        self.tag = text("Une boucle neuve à chaque sortie.", "free_r", 72, self.INK)
        self.sfx = [(3.0, "ding"), (6.0, "ding"), (9.0, "ding"), (10.6, "pop"), (12.0, "swoosh"),
                    (13.0, "pop")]

    # ------------------------------------------------------------ pieces
    def bar(self, f, t):
        n = 4
        gap, y0, y1 = 30, 600, 640
        w = (X1 - X0 - gap * (n - 1)) / n
        for i in range(n):
            x0 = int(X0 + i * (w + gap))
            x1 = int(x0 + w)
            rrect(f, x0, y0, x1, y1, 20, self.STREET)
            st = self.LV[i][0]
            k = 1.0 if (i == 0) else eout((t - st) / 0.45)
            if t >= st or i == 0:
                xf = int(x0 + (x1 - x0) * clamp(k))
                if xf > x0 + 40:
                    rrect(f, x0, y0, xf, y1, 20, self.TERRA if i < 3 else TEAL)

    def map_layer(self, f, t, a):
        if a >= 1:
            f[:] = self.map
        else:
            f[:] = (self.bg * (1 - a) + self.map * a).astype(np.uint8)

    def runner(self, f, path, s, col):
        p = path.at(path.L * (s % 1.0))
        glow_dot(f, p, 40, col, 0.7)
        circle(f, p, 22, col)
        circle(f, p, 10, (255, 255, 255))

    # ------------------------------------------------------------ frame
    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.BG, self.tag, self.cta, ink=self.INK, glow=False)
            return f
        f = self.bg.copy()
        if t < 12.0:
            self.map_layer(f, t, 1.0 if t < 11.7 else clamp((12.0 - t) / 0.3))
            self.bar(f, t)
            lv = 0 if t < 3 else 1 if t < 6 else 2 if t < 9 else 3
            st, en = self.LV[lv]
            # level art
            if lv in (0, 1):
                poly(f, self.small.pts, self.TERRA, 14, closed=True)
                s = (t - st) * 0.9
                self.runner(f, self.small, s if lv == 0 else -s, self.TERRA)
            elif lv == 2:
                poly(f, self.small.pts, mix(self.STREET, self.TERRA, 0.35), 10, closed=True)
                k = eout((t - st) / 1.9, 2)
                pts = self.wander.part(k)
                poly(f, pts, self.TERRA, 14)
                glow_dot(f, pts[-1], 34, self.TERRA, 0.6)
                if t > 7.9:
                    end = self.wander.at(self.wander.L)
                    blit(f, self.qmark, end[0] + 40, end[1] - 300, clamp((t - 7.9) / 0.3), "lt",
                         0.6 + 0.4 * eback((t - 7.9) / 0.35))
            else:
                k = eout((t - 9.25) / 1.3, 2)
                pts = self.big.part(max(k, 0.002))
                glow_path(f, pts, TEAL, 22, 30, 0.7)
                grad_poly(f, pts, TEAL, BLUE, 20)
                glow_dot(f, self.home, 30, (255, 255, 255), 0.9)
                if t > 10.6:
                    blit(f, self.chip10, CX, 820, clamp((t - 10.6) / 0.3), "mt",
                         0.8 + 0.2 * eback((t - 10.6) / 0.35))
            hold = -1 if lv == 0 else st
            show(f, self.labels[lv], CX, 690, t, hold, en if lv < 3 else 11.85, dy=40, anchor="mt")
            show(f, self.lines[lv], CX, 2230, t, hold if lv == 0 else st + 0.15, en if lv < 3 else 11.85,
                 dy=50, anchor="mt")
        else:
            show(f, self.q1, CX, 1250, t, 12.05, None, dy=60, anchor="mt")
            show(f, self.q2, CX, 1500, t, 12.25, None, dy=60, anchor="mt")
            show(f, self.opts, CX, 1880, t, 12.5, None, dy=40, anchor="mt")
            show(f, self.cta, CX, 2250, t, 13.0, None, dy=40, anchor="mt")
        return f


SCENES_W3 = [Niveaux]
