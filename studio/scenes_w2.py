"""Wave 2: ten Traceo Reels built for reach (participation, series, humour, satisfying loops)."""
import math

import cv2
import numpy as np

from engine import (CX, H, W, X0, X1, Path, blit, circle, city, clamp, draw_mark, eback, ease,
                    endcard, eout, flat, glow_dot, glow_path, grad_poly, hexc, line, loop_from_cells,
                    mix, pill, poly, rrect, rrect_alpha, smooth, text, watermark)
from scenes10 import WHITE, loop, make_map, rot, show

TEAL, BLUE = (60, 199, 154), (74, 166, 216)


def end(self, t, bg, ink=WHITE, glow=True):
    f = np.empty((H, W, 3), np.uint8)
    endcard(f, t - self.end_t, bg, self.tag, self.cta, ink=ink, glow=glow)
    return f


# =====================================================================
# W1 — « On doit parler » · Source Sans · chat sombre · chill pop
# =====================================================================
class OnDoitParler:
    name, duration, end_t, song = "w01-on-doit-parler", 15.4, 12.8, "chill_pop"
    IN, OUT, GREY = (38, 38, 42), hexc("#179C78"), (142, 142, 147)
    MSGS = [(0.0, "in", "On doit parler."), (1.6, "out", "?"),
            (2.8, "in", "Ça fait 3 ans. Toujours moi."), (4.0, "in", "Mêmes rues. Mêmes virages."),
            (5.4, "in", "Et là, je te vois regarder d'autres rues…"),
            (7.0, "out", "C'est Traceo. Une boucle neuve à chaque sortie."),
            (9.4, "in", "Tu me quittes pour des rues que tu ne connais même pas ?"),
            (11.0, "out", "Exactement.")]

    def __init__(self):
        self.bg = flat((0, 0, 0))
        self.b = [pill(text(s, "src_r", 96, WHITE, maxw=1200), self.IN if who == "in" else self.OUT,
                       48, 26, 56) for _, who, s in self.MSGS]
        self.name_l = text("Ton tour habituel", "src_b", 70, WHITE)
        self.status = text("en ligne", "src_r", 50, self.GREY)
        self.vu = text("Vu", "src_r", 46, self.GREY)
        self.typing = pill(text("     ", "src_r", 96, WHITE), self.IN, 48, 26, 56)
        self.tag = text("Une boucle neuve à chaque sortie.", "src_r", 86, (220, 225, 224))
        self.cta = pill(text("Lien en bio", "src_b", 72, (0, 0, 0)), TEAL)
        self.sfx = [(t, "pop" if w == "in" else "send") for t, w, _ in self.MSGS[1:]]
        self.sfx += [(t - 0.9, "type") for t, w, _ in self.MSGS[2:] if w == "in"]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, (0, 0, 0))
        f = self.bg.copy()
        vis = [i for i, (st, _, _) in enumerate(self.MSGS) if t >= st]
        typing = None
        for i, (st, who, _) in enumerate(self.MSGS):
            if who == "in" and i > 1 and st - 0.9 <= t < st:
                typing = i
        heights, y = [], 840
        pos = []
        prev = None
        for i in vis:
            who = self.MSGS[i][1]
            y += 14 if prev == who else 34
            pos.append(y)
            k = 1.0 if i == 0 else eout((t - self.MSGS[i][0]) / 0.3)
            y += self.b[i].h * k
            prev = who
        if typing is not None:
            y += 34
            ty = y
            y += self.typing.h
        shift = max(0, y - 2650)
        for j, i in enumerate(vis):
            st, who, _ = self.MSGS[i]
            k = 1.0 if i == 0 else eback((t - st) / 0.35)
            a = 1.0 if i == 0 else clamp((t - st) / 0.15)
            L = self.b[i]
            yy = pos[j] - shift
            if who == "in":
                blit(f, L, X0, yy, a, "lt", 0.85 + 0.15 * k)
            else:
                blit(f, L, X1, yy, a, "rt", 0.85 + 0.15 * k)
        if typing is not None:
            yy = ty - shift
            blit(f, self.typing, X0, yy)
            for d in range(3):
                bob = 14 * max(0, math.sin(t * 9 - d * 0.8))
                circle(f, (X0 + 90 + d * 64, yy + self.typing.h / 2 - bob), 18, self.GREY)
        if t >= 11.6:
            last = len(vis) - 1
            blit(f, self.vu, X1, pos[last] - shift + self.b[vis[last]].h + 10, clamp((t - 11.6) / 0.3),
                 "rt")
        rrect(f, 0, 0, W, 760, 0, (18, 18, 20))
        line(f, (0, 760), (W, 760), (40, 40, 44), 3)
        line(f, (X0 + 10, 600), (X0 + 50, 560), (10, 132, 255), 10)
        line(f, (X0 + 10, 600), (X0 + 50, 640), (10, 132, 255), 10)
        circle(f, (X0 + 190, 600), 84, (30, 30, 34))
        cv2.ellipse(f, (X0 + 190, 600), (42, 42), 0, 40, 330, TEAL, 12, cv2.LINE_AA)
        blit(f, self.name_l, X0 + 310, 545)
        blit(f, self.status, X0 + 310, 625)
        watermark(f, 0.0)
        return f


# =====================================================================
# W2 — « Débloque ta ville » · Unifont (pixel) · jeu vidéo, brouillard · chiptune
# =====================================================================
class Debloque:
    name, duration, end_t, song = "w02-debloque-ta-ville", 16.0, 13.4, "chiptune"
    BG, YEL, GREEN = (12, 14, 30), hexc("#FFD447"), hexc("#7CF29A")

    def __init__(self):
        bg = flat(self.BG)
        self.dark, nodes, _ = make_map(5, bg, (34, 40, 70), 6, fade=False)
        self.lit, _, _ = make_map(5, bg, (90, 200, 140), 10, fade=False)
        cells = {(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (1, 3), (2, 3), (3, 3),
                 (4, 3), (5, 3), (3, 4), (4, 4), (5, 4)}
        self.route = Path(loop(nodes, cells), True)
        self.t0, self.t1 = 2.6, 12.0
        self.samples = self.route.resample(220)
        self.h = [text("ET SI TA VILLE", "pixel", 150, WHITE),
                  text("ÉTAIT UNE CARTE", "pixel", 150, WHITE),
                  text("À DÉBLOQUER ?", "pixel", 150, self.YEL)]
        self.start = text("▶ START", "pixel", 80, self.GREEN)
        self.lv1 = text("NIV. 1 · EXPLORATEUR", "pixel", 88, WHITE)
        self.lv2 = text("NIV. 2 · AVENTURIER", "pixel", 88, self.YEL)
        self.plus = text("+1 RUE", "pixel", 72, self.YEL)
        self.ach1 = text("★ SUCCÈS DÉBLOQUÉ", "pixel", 64, self.YEL)
        self.ach2 = text("LA RUE D'À CÔTÉ", "pixel", 88, WHITE)
        self.f1 = text("100 SORTIES = 1 DIAMANT", "pixel", 96, WHITE)
        self.f2 = text("= 31 JOURS DE PREMIUM", "pixel", 96, self.YEL)
        self.f3 = text("TRACEO TRACE LES RUES.", "pixel", 76, WHITE)
        self.f4 = text("TOI, TU JOUES.", "pixel", 76, self.GREEN)
        self.cnt = {n: text(f"RUES DÉCOUVERTES : {n}", "pixel", 72, (180, 190, 220)) for n in range(0, 25)}
        self.plus_times = [3.0 + 0.75 * i for i in range(12)]
        self.tag = text("Une boucle neuve à chaque sortie.", "pixel", 70, WHITE)
        self.cta = pill(text("LIEN EN BIO", "pixel", 70, self.BG), self.YEL)
        self.sfx = [(pt, "coin") for pt in self.plus_times] + [(8.0, "ding"), (9.2, "ding")]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG)
        if t < 2.6:
            f = self.dark.copy()
            f[:] = (f.astype(np.uint16) * 2 // 5).astype(np.uint8)
            for i, L in enumerate(self.h):
                blit(f, L, X0, 900 + i * 190)
            if int(t * 2.5) % 2 == 0:
                blit(f, self.start, X0, 1580)
            watermark(f, 0.85)
            return f
        p = clamp((t - self.t0) / (self.t1 - self.t0))
        n = max(1, int(220 * p))
        q = 4
        m = np.zeros((H // q, W // q), np.float32)
        for (x, y) in self.samples[:n]:
            cv2.circle(m, (int(x / q), int(y / q)), 55, 1.0, -1, cv2.LINE_AA)
        m = cv2.GaussianBlur(m, (0, 0), 10)
        y0, y1 = 1000, 2700
        mm = cv2.resize(m, (W // q * q, H // q * q), interpolation=cv2.INTER_LINEAR)[y0:y1, :, None]
        f = self.dark.copy()
        reg = self.dark[y0:y1].astype(np.float32) * (1 - mm) + self.lit[y0:y1].astype(np.float32) * mm
        f[y0:y1] = reg.astype(np.uint8)
        pos = self.samples[min(n, 219)]
        if t < 11.4:
            glow_dot(f, pos, 60, self.YEL, 0.9)
            circle(f, pos, 30, WHITE)
        lv = self.lv2 if t >= 8.0 else self.lv1
        blit(f, lv, X0, 640)
        rrect(f, X0, 770, X1, 812, 0, (40, 44, 70))
        xp = (p * 2) % 1 if t < 8.0 else (p - 0.5) * 2
        rrect(f, X0, 770, X0 + int((X1 - X0) * clamp(xp)), 812, 0, self.YEL)
        if 8.0 <= t < 8.4:
            f[:] = cv2.addWeighted(f, 0.7, np.full_like(f, 255), 0.3, 0)
        found = sum(1 for pt in self.plus_times if t >= pt)
        blit(f, self.cnt[found], X0, 850)
        for pt in self.plus_times:
            if pt <= t < pt + 0.9:
                k = (t - pt) / 0.9
                ppos = self.samples[min(219, int(220 * clamp((pt - self.t0) / (self.t1 - self.t0))))]
                blit(f, self.plus, ppos[0] + 40, ppos[1] - 120 - 140 * k, 1 - k * k)
        if 9.2 <= t < 11.4:
            a = clamp((t - 9.2) / 0.2) * clamp((11.4 - t) / 0.3)
            rrect_alpha(f, X0, 2720, X1, 3020, 24, (20, 22, 44), 0.95 * a)
            rrect(f, X0, 2720, X1, 3020, 24, self.YEL, 6) if a > 0.5 else None
            blit(f, self.ach1, X0 + 50, 2760, a)
            blit(f, self.ach2, X0 + 50, 2860, a)
        if t >= 11.4:
            f[:] = (f.astype(np.uint16) * 2 // 5).astype(np.uint8)
            show(f, self.f1, X0, 1200, t, 11.4, self.end_t, dy=30, dur=0.2)
            show(f, self.f2, X0, 1340, t, 11.6, self.end_t, dy=30, dur=0.2)
            show(f, self.f3, X0, 1700, t, 12.0, self.end_t, dy=30, dur=0.2)
            show(f, self.f4, X0, 1820, t, 12.2, self.end_t, dy=30, dur=0.2)
        watermark(f, 0.85)
        return f


# =====================================================================
# W3 — « Tier list des excuses » · Latin Modern Sans Quotation · trap
# =====================================================================
class TierList:
    name, duration, end_t, song = "w03-tier-list", 15.4, 12.8, "trap"
    BG = (18, 18, 18)
    TIERS = [("S", hexc("#FF5E5B")), ("A", hexc("#FF9F43")), ("B", hexc("#FFD166")),
             ("C", hexc("#8BD3A6")), ("D", hexc("#7FB7E6"))]
    ITEMS = [(2.6, 4, "Il pleut"), (3.4, 4, "Il fait froid"), (4.3, 3, "J'ai mal dormi"),
             (5.3, 2, "Pas le temps"), (6.3, 1, "Demain, promis"), (7.6, 0, "Je connais déjà le parcours")]

    def __init__(self):
        self.bg = flat(self.BG)
        self.y0, self.rh = 1000, 300
        for i, (lab, col) in enumerate(self.TIERS):
            y = self.y0 + i * (self.rh + 16)
            rrect(self.bg, X0, y, X0 + 250, y + self.rh, 18, col)
            blit(self.bg, text(lab, "quot_b", 190, (18, 18, 18)), X0 + 125, y + self.rh / 2, 1, "mm")
            rrect(self.bg, X0 + 270, y, X1, y + self.rh, 18, (32, 32, 34))
        self.h1 = text("TIER LIST", "quot_b", 160, WHITE)
        self.h2 = text("des excuses pour ne pas courir", "quot_r", 92, (190, 190, 190), maxw=1550)
        self.items = []
        for st, tier, s in self.ITEMS:
            fill = TEAL if tier == 0 else (240, 240, 240)
            self.items.append(pill(text(s, "quot_b", 84, (18, 18, 18), maxw=1150), fill, 40, 22, 30))
        self.e1 = text("La seule excuse", "quot_b", 130, WHITE)
        self.e2 = text("qui se règle en 10 secondes.", "quot_b", 100, TEAL, maxw=1550)
        self.tag = text("Une boucle neuve à chaque sortie.", "quot_r", 88, WHITE)
        self.cta = pill(text("Lien en bio", "quot_b", 72, self.BG), TEAL)
        self.sfx = [(st + 0.3, "thud") for st, _, _ in self.ITEMS]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG)
        f = self.bg.copy()
        slot = {}
        for (st, tier, s), L in zip(self.ITEMS, self.items):
            if t < st:
                continue
            x = X0 + 300 + slot.get(tier, 0)
            slot[tier] = slot.get(tier, 0) + L.w + 24
            ty = self.y0 + tier * (self.rh + 16) + self.rh / 2 - L.h / 2
            k = eback((t - st) / 0.35, 1.8)
            y = ty - (1 - k) * 700
            blit(f, L, x, y, clamp((t - st) / 0.1))
            if tier == 0 and t > 8.0:
                pulse = 0.5 + 0.5 * math.sin((t - 8.0) * 6)
                rrect(f, x - 10, ty - 10, x + L.w + 10, ty + L.h + 10, 36, mix(self.BG, TEAL, pulse), 6)
        if t < 9.4:
            blit(f, self.h1, X0, 560)
            blit(f, self.h2, X0, 760)
        else:
            show(f, self.e1, X0, 540, t, 9.4, self.end_t)
            show(f, self.e2, X0, 720, t, 9.7, self.end_t)
        watermark(f, 0.8)
        return f


# =====================================================================
# W4 — « 1 an en 15 secondes » · TeX Gyre Schola · avant/après côte à côte · progressive
# =====================================================================
class UnAn:
    name, duration, end_t, song = "w04-un-an", 15.4, 12.8, "progressive"
    LBG, RBG, ORANGE = hexc("#170F0C"), hexc("#06171A"), hexc("#FF7A3D")

    def __init__(self):
        bg = np.empty((H, W, 3), np.uint8)
        bg[:, :W // 2] = self.LBG
        bg[:, W // 2:] = self.RBG
        rng = np.random.default_rng(4)
        self.nodesL, eL = city(31, 4, 6, -20, 1150, 280, 230, 30)
        self.nodesR, eR = city(32, 4, 6, W // 2 - 20, 1150, 280, 230, 30)
        for a, b in eL:
            line(bg, self.nodesL[a], self.nodesL[b], (44, 30, 26), 4)
        for a, b in eR:
            line(bg, self.nodesR[a], self.nodesR[b], (16, 46, 48), 4)
        line(bg, (W // 2, 860), (W // 2, 2560), (90, 90, 90), 3)
        self.bg = bg
        self.L = loop(self.nodesL, {(1, 2), (2, 2), (1, 3), (2, 3)})
        self.R = []
        for k in range(46):
            c = (int(rng.integers(0, 4)), int(rng.integers(0, 6)))
            cells = {c}
            for _ in range(int(rng.integers(1, 4))):
                cx, cy = list(cells)[int(rng.integers(0, len(cells)))]
                d = [(1, 0), (-1, 0), (0, 1), (0, -1)][int(rng.integers(0, 4))]
                nc = (cx + d[0], cy + d[1])
                if 0 <= nc[0] < 4 and 0 <= nc[1] < 6:
                    cells.add(nc)
            self.R.append(loop(self.nodesR, cells))
        self.h = text("1 an de footings,\nrésumé en 15 secondes.", "schola_b", 110, WHITE,
                      align="center", maxw=2000)
        self.l1 = text("Même tour", "schola_i", 84, self.ORANGE, align="center")
        self.l2 = text("Une boucle neuve\nà chaque sortie", "schola_i", 84, TEAL, align="center")
        self.runs = {n: text(f"Sortie {n}", "schola_b", 110, WHITE) for n in range(1, 157)}
        self.e1 = text("À gauche, un tour.", "schola_b", 110, self.ORANGE)
        self.e2 = text("À droite, une ville.", "schola_b", 110, TEAL)
        self.ill = text("Illustration", "schola_i", 52, (130, 130, 130))
        self.tag = text("Une boucle neuve à chaque sortie.", "schola_r", 86, WHITE)
        self.cta = pill(text("Lien en bio", "schola_b", 72, self.RBG), TEAL)
        self.sfx = [(7.0, "swoosh")]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.RBG)
        f = self.bg.copy()
        p = ease(clamp((t - 1.0) / 10.0)) if t < 7.0 else 0.4 + 0.6 * eout((t - 7.0) / 4.0)
        p = clamp(p)
        runs = 1 + int(155 * p)
        th = 10 + 26 * math.log1p(runs) / math.log(157)
        heat = mix((120, 60, 30), self.ORANGE, p)
        PL = Path(self.L, True)
        glow_path(f, PL.part(1.0), mix((0, 0, 0), self.ORANGE, 0.6 * p), th * 2, 40, 0.4 + 0.6 * p)
        poly(f, PL.part(1.0), heat, th)
        k = int(len(self.R) * p)
        for i, lp_ in enumerate(self.R[:k]):
            age = (k - i) / max(1, k)
            col = mix(TEAL, (20, 80, 70), clamp(age * 1.2))
            poly(f, Path(lp_, True).part(1.0), col, 9 if i < k - 1 else 14)
        if k:
            glow_path(f, Path(self.R[k - 1], True).part(1.0), (20, 110, 90), 20, 30, 0.8)
        blit(f, self.h, W // 2, 500, 1, "mt")
        blit(f, self.l1, W // 4, 880, 1, "mt")
        blit(f, self.l2, 3 * W // 4, 880, 1, "mt")
        if t < 11.0:
            blit(f, self.runs[runs], W // 2, 2620, 1, "mt")
        else:
            show(f, self.e1, W // 2 - 600, 2600, t, 11.0, self.end_t)
            show(f, self.e2, W // 2 - 600, 2740, t, 11.3, self.end_t)
        blit(f, self.ill, W // 2, 2900, 0.9, "mt")
        watermark(f, 0.8)
        return f


# =====================================================================
# W5 — « Le chrono » · Loma · jaune signal · tic-tac
# =====================================================================
class Chrono:
    name, duration, end_t, song = "w05-le-chrono", 15.0, 12.4, "ticking"
    BG, INK, RING = hexc("#FFE14D"), (17, 17, 17), hexc("#E6C631")
    C, R = (925, 1700), 600

    def __init__(self):
        bg = flat(self.BG)
        sub = flat(self.BG)
        nodes, edges = city(55, 6, 7, 300, 1050, 220, 200, 30)
        for a, b in edges:
            line(sub, nodes[a], nodes[b], hexc("#D7B92A"), 6)
        mask = np.zeros((H, W), np.uint8)
        cv2.circle(mask, self.C, self.R - 50, 255, -1, cv2.LINE_AA)
        m = (mask.astype(np.float32) / 255)[..., None]
        self.bg = (bg * (1 - m) + sub * m).astype(np.uint8)
        cv2.circle(self.bg, self.C, self.R, self.RING, 40, cv2.LINE_AA)
        self.route = Path(loop(nodes, {(2, 2), (3, 2), (3, 3), (4, 3), (4, 4), (3, 4), (2, 4)}), True)
        self.h1 = text("Je te trace une boucle", "loma_b", 118, self.INK)
        self.h2 = text("avant la fin du chrono.", "loma_b", 118, self.INK)
        self.digits = {}
        self.done1 = text("Boucle prête.", "loma_b", 150, self.INK)
        self.done2 = text("Environ 10 secondes : le temps qu'il faut à Traceo.", "loma_r", 76,
                          self.INK, maxw=1550)
        self.tag = text("Une boucle neuve à chaque sortie.", "loma_r", 86, self.INK)
        self.cta = pill(text("Lien en bio", "loma_b", 72, self.BG), self.INK)
        self.sfx = [(11.0, "ding")]

    def dig(self, s):
        if s not in self.digits:
            self.digits[s] = text(s, "loma_b", 280, self.INK, align="center")
        return self.digits[s]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG, ink=self.INK, glow=False)
        f = self.bg.copy()
        rem = clamp(10 - (t - 1.0), 0, 10)
        k = 1 - rem / 10
        if k > 0:
            cv2.ellipse(f, self.C, (self.R, self.R), -90, 0, 360 * k, self.INK, 40, cv2.LINE_AA)
            part = self.route.part(k)
            poly(f, part, self.INK, 22)
            circle(f, part[-1], 30, WHITE)
            circle(f, part[-1], 30, self.INK, 6)
        if t < 11.0:
            s = f"{rem:.1f}".replace(".", ",")
            blit(f, self.dig(s), self.C[0], 2400, 1, "mt")
            blit(f, self.h1, X0, 560)
            blit(f, self.h2, X0, 720)
        else:
            show(f, self.done1, X0, 560, t, 11.0, self.end_t, dur=0.25)
            show(f, self.done2, X0, 760, t, 11.2, self.end_t, dur=0.25)
            blit(f, self.dig("0,0"), self.C[0], 2400, 1, "mt")
        watermark(f, 0.9, self.INK)
        return f


# =====================================================================
# W6 — « Défi #UneRueParSortie » · TeX Gyre Bonum · cobalt + citron vert · disco
# =====================================================================
class Defi:
    name, duration, end_t, song = "w06-defi-30-jours", 16.0, 13.4, "disco"
    BG, LIME, DEEP = hexc("#1636FF"), hexc("#D7FF3A"), hexc("#0F28C8")

    def __init__(self):
        self.bg = flat(self.BG)
        rng = np.random.default_rng(30)
        self.cw, self.ch, self.gy = (X1 - X0) / 6, 220, 1250
        self.cells = []
        for i in range(30):
            c, r = i % 6, i // 6
            x0, y0 = X0 + c * self.cw, self.gy + r * self.ch
            cx, cy = x0 + self.cw / 2, y0 + self.ch / 2 + 14
            pts = [(cx + rng.uniform(-80, 80), cy + rng.uniform(-62, 62)) for _ in range(6)]
            ang = [math.atan2(p[1] - cy, p[0] - cx) for p in pts]
            pts = [p for _, p in sorted(zip(ang, pts))]
            self.cells.append((x0, y0, smooth(pts, 2)))
            rrect(self.bg, x0 + 8, y0 + 8, x0 + self.cw - 8, y0 + self.ch - 8, 22, (70, 96, 255), 3)
            blit(self.bg, text(str(i + 1), "bonum_r", 44, (170, 185, 255)), x0 + 26, y0 + 18)
        self.h1 = text("DÉFI 30 JOURS", "bonum_b", 150, self.LIME)
        self.h2 = text("Une rue nouvelle", "bonum_b", 120, WHITE)
        self.h3 = text("à chaque sortie.", "bonum_b", 120, WHITE)
        self.r = [text("1. Trace ta boucle sur Traceo.", "bonum_b", 82, WHITE, maxw=1550),
                  text("2. Cours-la.", "bonum_b", 82, WHITE),
                  text("3. Partage-la en story avec", "bonum_b", 82, WHITE, maxw=1550)]
        self.hashtag = text("#UneRueParSortie", "bonum_b", 140, self.LIME)
        self.tag = text("Une boucle neuve à chaque sortie.", "bonum_r", 84, WHITE)
        self.cta = pill(text("Lien en bio", "bonum_b", 72, self.BG), self.LIME)
        self.fill_t = [2.4 + i * 0.2 for i in range(30)]
        self.sfx = [(ft, "tick") for ft in self.fill_t[::2]] + [(8.6, "swoosh")]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG)
        f = self.bg.copy()
        for (x0, y0, pts), ft in zip(self.cells, self.fill_t):
            if t < ft:
                continue
            k = eout((t - ft) / 0.35)
            rrect(f, x0 + 8, y0 + 8, x0 + self.cw - 8, y0 + self.ch - 8, 22, self.DEEP)
            poly(f, Path(pts, True).part(k), self.LIME, 9)
        if t < 8.6:
            blit(f, self.h1, X0, 560)
            blit(f, self.h2, X0, 780)
            blit(f, self.h3, X0, 930)
        else:
            for i, L in enumerate(self.r):
                show(f, L, X0, 520 + i * 125, t, 8.6 + i * 0.4, self.end_t, dur=0.3)
            show(f, self.hashtag, X0, 2420, t, 9.8, self.end_t, dur=0.35)
        watermark(f, 0.85)
        return f


# =====================================================================
# W7 — « La montre » · Latin Modern Mono · noir + orange sport · glitch
# =====================================================================
class Montre:
    name, duration, end_t, song = "w07-la-montre", 15.4, 12.8, "glitch"
    BG, ORA, GREY = (5, 5, 5), hexc("#FF8A1F"), (120, 120, 120)
    C, R = (925, 1750), 560

    def __init__(self):
        bg = flat(self.BG)
        cx, cy = self.C
        rrect(bg, cx - 300, cy - self.R - 520, cx + 300, cy - self.R + 40, 120, (22, 22, 22))
        rrect(bg, cx - 300, cy + self.R - 40, cx + 300, cy + self.R + 520, 120, (22, 22, 22))
        circle(bg, self.C, self.R + 60, (40, 40, 40))
        circle(bg, self.C, self.R, (0, 0, 0))
        rrect(bg, cx + self.R + 40, cy - 90, cx + self.R + 110, cy + 90, 20, (60, 60, 60))
        self.bg = bg
        nodes, edges = city(77, 5, 5, cx - 470, cy - 420, 200, 190, 24)
        self.edges = [(nodes[a], nodes[b]) for a, b in edges]
        self.route = Path(loop(nodes, {(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (2, 3), (1, 3)}), True)
        self.time = text("18:30", "lmmono_b", 110, WHITE, align="center")
        self.sport = text("Footing", "lmmono_c", 70, self.ORA, align="center")
        self.n = [text(s, "lmmono_c", 92, WHITE, align="center", maxw=860) for s in
                  ("Parcours reconnu.", "Tu es déjà passé ici.", "… et ici aussi.")]
        self.imp = text("Boucle Traceo importée", "lmmono_c", 62, self.ORA, align="center")
        self.h1 = text("POV : ta montre connaît", "lmmono_c", 104, WHITE)
        self.h2 = text("ton parcours par cœur.", "lmmono_c", 104, self.ORA)
        self.m1 = text("Exporte ta boucle vers", "lmmono_c", 104, WHITE)
        self.m2 = text("Strava, Garmin ou en GPX.", "lmmono_c", 104, self.ORA)
        self.m3 = text("Ta montre aussi a envie", "lmmono_c", 104, WHITE)
        self.m4 = text("de voir du pays.", "lmmono_c", 104, self.ORA)
        self.tag = text("Une boucle neuve à chaque sortie.", "lmmono_c", 84, WHITE)
        self.cta = pill(text("Lien en bio", "lmmono_b", 70, self.BG), self.ORA)
        self.sfx = [(2.4, "pop"), (4.2, "pop"), (5.8, "pop"), (7.6, "ding")]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG)
        f = self.bg.copy()
        cx, cy = self.C
        if t < 7.6:
            blit(f, self.time, cx, cy - 330, 1, "mt")
            blit(f, self.sport, cx, cy - 190, 1, "mt")
            for i, st in enumerate((2.4, 4.2, 5.8)):
                if t >= st:
                    k = eback((t - st) / 0.35)
                    y = cy - 40 + i * 0 - (1 - k) * 120
                    if i == 2 or t < (4.2, 5.8, 99)[i]:
                        rrect_alpha(f, cx - 470, y - 30, cx + 470, y + 150, 40, (34, 34, 34), clamp(k))
                        blit(f, self.n[i], cx, y, clamp((t - st) / 0.15), "mt")
        else:
            for a, b in self.edges:
                line(f, a, b, (40, 40, 40), 5)
            part = self.route.part(eout((t - 7.8) / 1.6))
            glow_path(f, part, (120, 60, 10), 26, 30, 0.8)
            poly(f, part, self.ORA, 20)
            circle(f, part[-1], 22, WHITE)
            blit(f, self.imp, cx, cy + 300, clamp((t - 7.6) / 0.3), "mt")
            mask = np.zeros((H, W), np.uint8)
            cv2.circle(mask, self.C, self.R, 255, -1, cv2.LINE_AA)
            outside = mask == 0
            f[outside] = self.bg[outside]
        if t < 7.6:
            blit(f, self.h1, X0, 560)
            blit(f, self.h2, X0, 700)
        elif t < 11.0:
            show(f, self.m1, X0, 560, t, 7.6, 11.0)
            show(f, self.m2, X0, 700, t, 7.8, 11.0)
        else:
            show(f, self.m3, X0, 560, t, 11.0, self.end_t)
            show(f, self.m4, X0, 700, t, 11.2, self.end_t)
        watermark(f, 0.8)
        return f


# =====================================================================
# W8 — « Ce que ta boucle dit de toi » · TeX Gyre Termes · magazine crème · jazz swing
# =====================================================================
class Quiz:
    name, duration, end_t, song = "w08-ta-boucle-dit", 16.0, 13.4, "jazz_swing"
    BG, INK, RED = hexc("#F6F0E6"), (26, 26, 26), hexc("#D7263D")

    def __init__(self):
        self.bg = flat(self.BG)
        line(self.bg, (X0, 1000), (X1, 1000), self.INK, 4)
        cx, cy = 925, 1700
        sq = [(cx - 380, cy - 380), (cx + 380, cy - 380), (cx + 380, cy + 380), (cx - 380, cy + 380)]
        small = [(cx - 140, cy - 140), (cx + 140, cy - 140), (cx + 140, cy + 140), (cx - 140, cy + 140)]
        rng = np.random.default_rng(8)
        org = []
        for i in range(10):
            a = 2 * math.pi * i / 10
            r = 420 + rng.uniform(-170, 120)
            org.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.shapes = [("Le carré parfait", "Tu as tes habitudes.\nEt tes habitudes t'ont.", sq, True),
                       ("L'aller-retour", "Efficace. Zéro surprise.",
                        [(cx - 420, cy), (cx + 420, cy)], False),
                       ("Le tour du pâté de maisons", "Tu connais chaque fissure du trottoir.", small,
                        True),
                       ("La boucle jamais vue", "Tu es déjà sur Traceo.", smooth(org, 3), True)]
        self.t = [2.4, 5.0, 7.6, 10.2]
        self.names = [text(n, "termes_b", 110, self.RED if i < 3 else TEAL, maxw=1550)
                      for i, (n, _, _, _) in enumerate(self.shapes)]
        self.diag = [text(d, "termes_i", 86, self.INK, maxw=1550) for _, d, _, _ in self.shapes]
        self.num = {i: text(f"{i}/4", "termes_r", 64, (120, 120, 120)) for i in range(1, 5)}
        self.h1 = text("Ce que ta boucle", "termes_b", 150, self.INK)
        self.h2 = text("dit de toi.", "termes_i", 150, self.RED)
        self.cta2 = text("Identifie quelqu'un qui court en carré.", "termes_r", 70, self.INK, maxw=1550)
        self.tag = text("Une boucle neuve à chaque sortie.", "termes_i", 88, self.INK)
        self.cta = pill(text("Lien en bio", "termes_b", 72, self.BG), self.INK)
        self.sfx = [(st, "swoosh") for st in self.t]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG, ink=self.INK, glow=False)
        f = self.bg.copy()
        blit(f, self.h1, X0, 540)
        blit(f, self.h2, X0, 720)
        idx = -1
        for i, st in enumerate(self.t):
            if t >= st:
                idx = i
        if idx >= 0:
            st = self.t[idx]
            lt = t - st
            name, _, pts, closed = self.shapes[idx]
            col = TEAL if idx == 3 else self.INK
            if closed:
                P = Path(pts, True)
                part = P.part(eout(lt / 0.8))
                poly(f, part, col, 22)
                circle(f, part[-1], 26, self.RED if idx < 3 else TEAL)
            else:
                a, b = pts
                ph = (lt / 0.7) % 2
                x = a[0] + (b[0] - a[0]) * (ph if ph < 1 else 2 - ph)
                line(f, a, b, col, 22)
                circle(f, (x, a[1]), 34, self.RED)
            blit(f, self.num[idx + 1], X1, 1060, 1, "rt")
            show(f, self.names[idx], X0, 2260, t, st, None, dur=0.3)
            show(f, self.diag[idx], X0, 2400, t, st + 0.3, None, dur=0.3)
            if idx == 3:
                show(f, self.cta2, X0, 2720, t, 11.6, None)
        watermark(f, 0.9, self.INK)
        return f


# =====================================================================
# W9 — « Commente ta ville » · Caladea · bleu nuit + crème · dembow
# =====================================================================
class TaVille:
    name, duration, end_t, song = "w09-commente-ta-ville", 15.0, 12.4, "dembow"
    BG, CREAM, ACC = hexc("#0F1B3D"), hexc("#F4EFE6"), hexc("#FF7A59")

    def __init__(self):
        bg = flat(self.BG)
        ox, oy, s = 260, 1180, 1.0
        fr = [(2.37, 51.03), (2.9, 51.1), (3.6, 50.5), (4.2, 50.0), (4.83, 50.13), (5.4, 49.6),
              (6.1, 49.5), (7.0, 49.1), (8.2, 48.97), (7.8, 48.5), (7.55, 47.58), (6.9, 47.4),
              (6.1, 46.2), (6.85, 45.83), (7.0, 45.2), (6.65, 44.5), (7.5, 43.78), (7.0, 43.55),
              (6.4, 43.15), (5.9, 43.1), (5.35, 43.3), (4.6, 43.4), (3.9, 43.5), (3.2, 43.0),
              (3.15, 42.45), (2.1, 42.4), (0.7, 42.8), (-0.6, 42.85), (-1.78, 43.37), (-1.5, 43.6),
              (-1.25, 44.6), (-1.15, 45.5), (-1.2, 46.15), (-2.1, 46.8), (-2.2, 47.27), (-2.9, 47.5),
              (-4.4, 47.8), (-4.75, 48.0), (-4.8, 48.4), (-4.1, 48.7), (-3.5, 48.83), (-2.7, 48.55),
              (-2.0, 48.65), (-1.5, 48.63), (-1.6, 49.2), (-1.95, 49.7), (-1.25, 49.65), (-1.15, 49.35),
              (-0.2, 49.3), (0.1, 49.5), (1.08, 49.93), (1.6, 50.2), (1.6, 50.73), (1.85, 50.95)]
        co = [(9.35, 43.0), (9.55, 42.5), (9.4, 41.6), (9.2, 41.37), (8.8, 41.6), (8.6, 42.1),
              (8.75, 42.6)]
        sx = 1340 / ((9.6 + 4.9) * 0.688)
        proj = lambda lo, la: (ox - 60 + (lo + 4.9) * 0.688 * sx, oy - 60 + (51.2 - la) * sx)
        self.poly = smooth([proj(*p) for p in fr], 1)
        poly(bg, self.poly, self.CREAM, 6, True)
        self.cors = smooth([proj(*p) for p in co], 2)
        poly(bg, self.cors, self.CREAM, 6, True)
        self.om = [(X0 + 40 + i * 300, 2720) for i in range(4)]
        for x, y in self.om:
            rrect(bg, x, y, x + 200, y + 140, 30, self.CREAM, 4)
        blit(bg, text("Outre-mer", "cala_r", 54, (170, 175, 195)), X0, 2620)
        self.bg = bg
        rng = np.random.default_rng(9)
        cnt = np.array(self.poly, np.float32)
        self.dots = []
        while len(self.dots) < 46:
            x, y = rng.uniform(ox - 60, ox + 1300), rng.uniform(oy - 60, oy + 1300)
            if cv2.pointPolygonTest(cnt, (float(x), float(y)), True) > 50:
                self.dots.append((x, y, rng.uniform(3.0, 8.0)))
        self.dots.sort(key=lambda d: d[2])
        self.dots += [(sum(p[0] for p in self.cors) / len(self.cors), sum(p[1] for p in self.cors) / len(self.cors), 7.0)] + [(x + 100, y + 70, 7.3 + i * 0.1)
                                                     for i, (x, y) in enumerate(self.om)]
        self.h1 = text("Dis-moi ta ville.", "cala_b", 170, self.CREAM)
        self.h2 = text("Je te dis si Traceo y trace une boucle.", "cala_r", 88, (190, 196, 214),
                       maxw=1550)
        self.s1 = text("Spoiler : partout en France.", "cala_b", 118, self.CREAM, maxw=1550)
        self.s2 = text("Corse et outre-mer compris.", "cala_r", 92, self.ACC)
        self.c1 = text("Commente ta ville ↓", "cala_b", 150, self.CREAM)
        self.tag = text("Une boucle neuve à chaque sortie.", "cala_r", 88, self.CREAM)
        self.cta = pill(text("Lien en bio", "cala_b", 72, self.BG), self.ACC)
        self.sfx = [(8.0, "ding"), (10.4, "swoosh")]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG)
        f = self.bg.copy()
        for x, y, st in self.dots:
            if t >= st:
                k = eback((t - st) / 0.3)
                circle(f, (x, y), 20 * k, TEAL)
                if t - st < 0.5:
                    circle(f, (x, y), 20 + 60 * (t - st) / 0.5, mix(self.BG, TEAL, 1 - (t - st) / 0.5), 4)
        if t < 8.0:
            blit(f, self.h1, X0, 520)
            blit(f, self.h2, X0, 740)
        elif t < 10.4:
            show(f, self.s1, X0, 520, t, 8.0, 10.4)
            show(f, self.s2, X0, 680, t, 8.3, 10.4)
        else:
            bounce = 20 * abs(math.sin((t - 10.4) * 5))
            show(f, self.c1, X0, 560 + bounce, t, 10.4, self.end_t)
        watermark(f, 0.85)
        return f


# =====================================================================
# W10 — « Le ticket » · TeX Gyre Cursor · ticket de caisse · boom bap
# =====================================================================
class Ticket:
    name, duration, end_t, song = "w10-le-ticket", 15.4, 12.8, "boom_bap"
    BG, PAPER, INK, RED = (27, 27, 27), hexc("#F7F5F0"), (26, 26, 26), hexc("#D7263D")
    PX0, PX1, SLOT = 260, 1590, 900

    def __init__(self):
        self.bg = flat(self.BG)
        L = [("TRACEO", 120, True), ("-" * 29, 68, False), ("Boucle neuve ...... 0,00 €", 68, False),
             ("Rues inconnues .... offertes", 68, False), ("Compte ......... pas besoin", 68, False),
             ("Appli à installer .. aucune", 68, False), ("-" * 29, 68, False),
             ("TOTAL ............. 0,00 €", 76, True), ("", 40, False),
             ("Premium : 4,99 € / 31 jours", 64, False), ("sans abonnement", 64, False),
             ("", 40, False), ("MERCI, BONNE SORTIE", 70, True)]
        self.lines = [text(s, "cursor_b" if b else "cursor_r", sz, self.INK, align="center",
                           maxw=1300) if s else None for s, sz, b in L]
        self.lh = [(l.h if l is not None else 40) + 18 for l in self.lines]
        self.times = [1.4 + 0.6 * i for i in range(len(L))]
        self.h1 = text("Combien coûte", "cursor_b", 120, WHITE)
        self.h2 = text("une boucle neuve ?", "cursor_b", 120, WHITE)
        st = text("GRATUIT", "cursor_b", 150, self.RED)
        arr = np.zeros((st.h + 60, st.w + 80, 4), np.uint8)
        rrect(arr, 0, 0, arr.shape[1] - 1, arr.shape[0] - 1, 20, self.RED + (255,), 10)
        from engine import Layer
        S = Layer(arr)
        S.rgb[30:30 + st.h, 40:40 + st.w] = S.rgb[30:30 + st.h, 40:40 + st.w] * (1 - st.a) + st.rgb
        S.a[30:30 + st.h, 40:40 + st.w] = np.maximum(S.a[30:30 + st.h, 40:40 + st.w], st.a)
        self.stamp = S
        self.tag = text("Une boucle neuve à chaque sortie.", "cursor_r", 76, WHITE)
        self.cta = pill(text("Lien en bio", "cursor_b", 70, self.BG), TEAL)
        self.sfx = [(tt_, "print") for tt_ in self.times] + [(10.6, "thud")]

    def frame(self, t):
        if t >= self.end_t:
            return end(self, t, self.BG)
        f = self.bg.copy()
        shown = [i for i, st in enumerate(self.times) if t >= st]
        total = 260 + sum(self.lh[i] for i in shown)
        if shown:
            last = shown[-1]
            total -= self.lh[last] * (1 - eout((t - self.times[last]) / 0.4))
        paper_h = max(60, total)
        shift = max(0, self.SLOT + paper_h - 2800)
        top = self.SLOT - shift
        bot = self.SLOT + paper_h - shift
        rrect(f, self.PX0, max(self.SLOT, top), self.PX1, bot, 0, self.PAPER)
        zig = [(x, bot + (14 if (x // 30) % 2 else 0)) for x in range(self.PX0, self.PX1 + 1, 30)]
        cv2.fillPoly(f, [np.array([(self.PX0, bot)] + zig + [(self.PX1, bot)], np.int32)], self.PAPER)
        y = top + 80
        if bot > top + 230:
            draw_mark(f, (self.PX0 + self.PX1) / 2 + 10, top + 120, 0.32, 1.0, 1.0, glow=False,
                      dot=self.INK)
        y = top + 240
        for i in shown:
            L = self.lines[i]
            if L is not None and y + L.h > self.SLOT:
                blit(f, L, (self.PX0 + self.PX1) / 2, y, 1, "mt")
            y += self.lh[i]
        rrect(f, self.PX0 - 80, self.SLOT - 70, self.PX1 + 80, self.SLOT + 10, 24, (8, 8, 8))
        line(f, (self.PX0 - 40, self.SLOT - 4), (self.PX1 + 40, self.SLOT - 4), (60, 60, 60), 4)
        blit(f, self.h1, X0, 500)
        blit(f, self.h2, X0, 650)
        if t >= 10.6:
            k = eout((t - 10.6) / 0.22)
            blit(f, self.stamp.scaled(1.0), 925, 2000, clamp(k * 1.5), "mm", 2.2 - 1.2 * k)
        watermark(f, 0.85)
        return f


SCENES_W2 = [OnDoitParler, Debloque, TierList, UnAn, Chrono, Defi, Montre, Quiz, TaVille, Ticket]
