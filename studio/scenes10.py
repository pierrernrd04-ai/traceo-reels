"""Ten Traceo Reels, 4K vertical. Each scene: name, duration, end_t, song, frame(t) -> uint8 frame."""
import math

import cv2
import numpy as np

from engine import (CX, H, W, X0, X1, Path, blit, circle, city, clamp, draw_mark, eback, ease,
                    ein, endcard, eout, flat, glow_dot, glow_path, grad_poly, hexc, line,
                    loop_from_cells, mix, pill, poly, radial, rrect, rrect_alpha, smooth, text,
                    vgrad, watermark, wordmark)

WHITE = (240, 245, 244)


def show(frame, L, x, y, t, t0, t1=None, dy=60, dur=0.4, anchor="lt", out=0.3, scale=1.0):
    """Fade + slide a layer in at t0 and out before t1."""
    if t < t0 or (t1 is not None and t >= t1):
        return
    a = 1.0 if t0 < 0 else eout((t - t0) / dur)
    if t1 is not None:
        a *= clamp((t1 - t) / out)
    blit(frame, L, x, y + dy * (1 - (1.0 if t0 < 0 else eout((t - t0) / dur))), a, anchor, scale)


def make_map(seed, bg, street, th, x0=-40, y0=1150, cw=270, ch=235, cols=8, rows=6, fade=True,
             jitter=38):
    nodes, edges = city(seed, cols, rows, x0, y0, cw, ch, jitter)
    layer = bg.copy()
    for a, b in edges:
        line(layer, nodes[a], nodes[b], street, th)
    if fade:
        yy = np.arange(H)[:, None, None].astype(np.float32)
        top, bot = y0 + 40, y0 + rows * ch - 40
        m = np.clip((yy - (top - 260)) / 260, 0, 1) * np.clip(((bot + 260) - yy) / 260, 0, 1)
        layer = (bg.astype(np.float32) * (1 - m) + layer.astype(np.float32) * m).astype(np.uint8)
    return layer, nodes, edges


def loop(nodes, cells, iters=0):
    pts, _ = loop_from_cells(nodes, cells)
    return smooth(pts, iters) if iters else pts


def rot(pts, k):
    k = k % len(pts)
    return pts[k:] + pts[:k]


# =====================================================================
# V1 — « Même endroit »  · Inter Display · midnight + brand gradient · deep house
# =====================================================================
class MemeEndroit:
    name, duration, end_t, song = "v01-meme-endroit", 16.0, 13.4, "deep_house"

    def __init__(self):
        self.bg0 = radial(flat(hexc("#07131A")), hexc("#0E2A2F"), CX, 900, 1600, 0.7)
        self.map, nodes, _ = make_map(3, self.bg0, (22, 44, 52), 5)
        self.worn = loop(nodes, {(3, 2), (4, 2), (3, 3), (4, 3)})
        self.cands = [loop(nodes, {(1, 1), (2, 1), (2, 2)}),
                      loop(nodes, {(5, 3), (6, 3), (6, 4), (5, 4), (5, 5)}),
                      loop(nodes, {(0, 3), (1, 3), (1, 4)})]
        self.new = rot(loop(nodes, {(1, 3), (2, 3), (2, 4), (3, 4), (4, 4), (4, 5), (3, 5)}), 3)
        self.h = [text("Marre de", "inter_thin", 200, WHITE),
                  text("toujours courir", "inter_black", 200, WHITE),
                  text("au même", "inter_black", 200, WHITE),
                  text("endroit ?", "inter_black", 200, (60, 199, 154))]
        self.same = [text(s, "inter_black", 150, WHITE) for s in
                     ("Même rue.", "Même virage.", "Même ennui.")]
        self.c1 = text("Traceo compare plusieurs itinéraires", "inter_med", 104, WHITE)
        self.c2 = text("et garde celui qui a le plus de *rues* *nouvelles.*", "inter_med", 104,
                       WHITE, accent=(60, 199, 154))
        self.f1 = text("En 10 secondes.", "inter_black", 190, WHITE)
        self.f2 = text("Depuis chez toi.", "inter_thin", 150, WHITE)
        self.tag = text("Une boucle neuve à chaque sortie.", "inter_light", 92, (200, 214, 212))
        self.cta = pill(text("Lien en bio", "inter_xbold", 72, (7, 19, 26)), (60, 199, 154))

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.bg0, self.tag, self.cta)
            return f
        k_map = clamp((t - 1.0) / 1.2)
        f = cv2.addWeighted(self.bg0, 1 - k_map, self.map, k_map, 0) if k_map < 1 else self.map.copy()
        P = Path(self.worn, True)
        if 1.2 <= t < 6.6:
            laps = (t - 1.2) / 1.35
            done = int(laps)
            th = 14 + 6 * done
            if done:
                poly(f, P.part(1.0), (230, 236, 235), th)
            poly(f, P.part(laps - done), (245, 250, 249), th + 6)
            circle(f, P.at(P.L * (laps - done)), 30, (255, 255, 255))
        elif t >= 6.6:
            poly(f, P.part(1.0), (40, 62, 70), 30)
            for i, c in enumerate(self.cands):
                st = 6.7 + i * 0.4
                if st <= t < 8.4:
                    a = clamp((t - st) / 0.3) * clamp((8.4 - t) / 0.3)
                    poly(f, Path(c, True).part(eout((t - st) / 0.5)), mix((40, 62, 70), WHITE, a * 0.7),
                         8)
            if t >= 8.2:
                NP = Path(self.new, True)
                part = NP.part(eout((t - 8.2) / 1.6, 2))
                glow_path(f, part, (30, 120, 95), 40, 60, 0.9)
                grad_poly(f, part, (60, 199, 154), (74, 166, 216), 30)
                circle(f, part[-1], 34, (255, 255, 255))
                if t > 9.8:
                    pulse = 0.5 + 0.5 * math.sin((t - 9.8) * 5)
                    glow_dot(f, part[-1], 60 + 30 * pulse, (60, 199, 154), 0.8)
        y = 700
        if t < 2.6:
            s = 1 + 0.02 * t / 2.6
            for i, L in enumerate(self.h):
                show(f, L, X0, y + i * 215, t, -1, 2.6, scale=s)
        elif t < 6.6:
            i = min(2, int((t - 2.6) / 1.33))
            show(f, self.same[i], X0, 2420, t, 2.6 + i * 1.33, 2.6 + (i + 1) * 1.33, dy=40, dur=0.25,
                 out=0.15)
        elif t < 11.0:
            show(f, self.c1, X0, 700, t, 6.6, 11.0)
            show(f, self.c2, X0, 970, t, 8.0, 11.0)
        else:
            show(f, self.f1, X0, 700, t, 11.0, self.end_t)
            show(f, self.f2, X0, 920, t, 11.25, self.end_t)
        watermark(f, 0.85)
        return f


# =====================================================================
# V2 — « 156 »  · TeX Gyre Heros (Helvetica) · bone + ink, Swiss grid · liquid drum & bass
# =====================================================================
class Cent56:
    name, duration, end_t, song = "v02-156", 15.0, 12.4, "liquid_dnb"
    INK, BONE, ACC = (17, 17, 17), hexc("#EFECE6"), hexc("#0FA37F")

    def __init__(self):
        self.bg = flat(self.BONE)
        for x in (X0, CX, X1):
            line(self.bg, (x, 420), (x, 3300), (222, 218, 210), 3)
        self.big = text("156", "heros_b", 900, self.INK)
        self.sub = text("fois le même tour.", "heros_r", 150, self.INK)
        self.kick = text("Par an, si tu cours toujours au même endroit.", "heros_r", 76,
                         (90, 90, 90), maxw=1300)
        self.eq = [(text("3", "heros_b", 190, self.INK), text("sorties par semaine", "heros_r", 88,
                                                               self.INK)),
                   (text("× 52", "heros_b", 190, self.INK), text("semaines", "heros_r", 88, self.INK)),
                   (text("= 156", "heros_b", 190, self.ACC), text("fois le même tour", "heros_r", 88,
                                                                   self.INK))]
        self.q = text("Et si chacune traçait une rue nouvelle ?", "heros_b", 130, self.INK, maxw=1500)
        self.t1 = text("Traceo.", "heros_b", 300, self.INK)
        self.t2 = text("Une boucle neuve à chaque sortie.", "heros_r", 110, self.INK, maxw=1500)
        self.tag = text("Une boucle neuve à chaque sortie.", "heros_r", 92, self.INK)
        self.cta = pill(text("Lien en bio", "heros_b", 72, self.BONE), self.INK)
        rnd = np.random.default_rng(156)
        self.cells = []
        cw, chh = 129, 120
        for j in range(13):
            for i in range(12):
                cx, cy = X0 + i * cw + cw / 2, 1330 + j * chh + chh / 2
                pts = [(cx + rnd.uniform(-44, 44), cy + rnd.uniform(-42, 42)) for _ in range(5)]
                ang = [math.atan2(p[1] - cy, p[0] - cx) for p in pts]
                pts = [p for _, p in sorted(zip(ang, pts))]
                self.cells.append((cx, cy, smooth(pts, 2)))

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.BONE, self.tag, self.cta, ink=self.INK, glow=False)
            return f
        f = self.bg.copy()
        if t < 2.7:
            s = 1.0 + 0.015 * t
            show(f, self.big, X0 - 30, 470, t, -1, 2.7, scale=s)
            show(f, self.sub, X0, 1440, t, -1, 2.7)
            show(f, self.kick, X0, 1660, t, 0.6, 2.7)
        elif t < 6.4:
            for i, (n, lab) in enumerate(self.eq):
                st = 2.7 + i * 0.45
                show(f, n, X0, 540 + i * 220, t, st, 6.4, dy=80, dur=0.3)
                show(f, lab, X0 + 620, 540 + i * 220 + 90, t, st + 0.1, 6.4, dy=80, dur=0.3)
            if t > 3.1:
                line(f, (X0, 1250), (X0 + int(1550 * eout((t - 3.1) / 0.6)), 1250), self.INK,
                     6)
        if 4.2 <= t < self.end_t:
            for idx, (cx, cy, pts) in enumerate(self.cells):
                i, j = idx % 12, idx // 12
                appear = 4.2 + (i + j) * 0.035
                if t < appear:
                    continue
                k = eback((t - appear) / 0.25)
                r = 34 * k
                turn = 6.6 + (i + j) * 0.06
                if t < turn:
                    cv2.rectangle(f, (int(cx - r), int(cy - r)), (int(cx + r), int(cy + r)), self.INK, 5,
                                  cv2.LINE_AA)
                else:
                    kk = eout((t - turn) / 0.4)
                    poly(f, Path(pts, True).part(kk), self.ACC, 7)
        if 6.4 <= t < 9.8:
            rrect(f, X0 - 20, 520, X1, 1270, 0, self.BONE)
            show(f, self.q, X0, 640, t, 6.5, 9.8)
        elif t >= 9.8:
            rrect(f, X0 - 20, 520, X1, 1270, 0, self.BONE)
            show(f, self.t1, X0, 560, t, 9.8, self.end_t)
            show(f, self.t2, X0, 900, t, 10.1, self.end_t)
        watermark(f, 0.9, self.INK)
        return f


# =====================================================================
# V3 — « Les yeux fermés »  · TeX Gyre Adventor · black + white line + teal · cinematic pulse
# =====================================================================
class YeuxFermes:
    name, duration, end_t, song = "v03-yeux-fermes", 15.0, 12.4, "cine_pulse"

    def __init__(self):
        self.bg = flat((4, 6, 8))
        rnd = np.random.default_rng(31)
        cx, cy = CX, 1850
        pts = []
        for i in range(9):
            a = 2 * math.pi * i / 9
            r = 430 + rnd.uniform(-120, 120)
            pts.append((cx + r * math.cos(a), cy + 0.82 * r * math.sin(a)))
        self.loop1 = smooth(pts, 4)
        pts2 = []
        for i in range(11):
            a = 2 * math.pi * i / 11 + 0.3
            r = 560 + rnd.uniform(-220, 160)
            pts2.append((cx + 60 + r * math.cos(a), cy - 40 + 0.9 * r * math.sin(a)))
        self.loop2 = smooth(pts2, 3)
        nodes, edges = city(9, 9, 11, -120, 900, 270, 240, 70)
        self.web = []
        for a, b in edges:
            pa, pb = nodes[a], nodes[b]
            d = math.dist(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2), (cx, cy))
            self.web.append((d, pa, pb))
        self.web.sort()
        self.h1 = text("Ferme les yeux.", "adv_b", 170, WHITE, align="center")
        self.h2 = text("Tu peux dessiner\nton parcours ?", "adv_r", 104, (170, 176, 178),
                       align="center")
        self.l1 = text("Sans hésiter ?", "adv_b", 130, WHITE, align="center")
        self.l2 = text("Alors tu le connais par cœur.", "adv_r", 104, (170, 176, 178), align="center")
        self.l3 = text("Traceo te trace une boucle", "adv_b", 110, WHITE, align="center")
        self.l4 = text("que tu ne connais pas encore.", "adv_r", 104, (60, 199, 154), align="center")
        self.l5 = text("Réponds en commentaire :\noui ou non ?", "adv_b", 110, WHITE, align="center")
        self.tag = text("Une boucle neuve à chaque sortie.", "adv_r", 88, (200, 205, 206))
        self.cta = pill(text("Lien en bio", "adv_b", 70, (4, 6, 8)), WHITE)

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, (4, 6, 8), self.tag, self.cta)
            return f
        f = self.bg.copy()
        if t < 8.0:
            if t >= 2.4:
                P = Path(self.loop1, True)
                part = P.part(eout((t - 2.4) / 2.2, 2))
                glow_path(f, part, (90, 90, 90), 16, 40, 0.8)
                poly(f, part, (245, 245, 245), 12)
                if t < 4.6:
                    circle(f, part[-1], 18, (255, 255, 255))
                if t > 5.8:
                    breathe = 0.5 + 0.5 * math.sin((t - 5.8) * 6)
                    glow_path(f, P.part(1.0), (60, 60, 60), 16, 60, 0.6 * breathe)
        else:
            lt = t - 8.0
            fade = clamp(1 - lt / 0.6)
            if fade > 0:
                poly(f, Path(self.loop1, True).part(1.0), mix((4, 6, 8), WHITE, fade), 12)
            n = int(len(self.web) * eout(lt / 1.6))
            for d, a, b in self.web[:n]:
                line(f, a, b, (46, 52, 56), 5)
            if t >= 8.8:
                P2 = Path(self.loop2, True)
                part = P2.part(eout((t - 8.8) / 1.8, 2))
                glow_path(f, part, (25, 110, 85), 36, 55, 0.9)
                grad_poly(f, part, (60, 199, 154), (74, 166, 216), 24)
                circle(f, part[-1], 26, (255, 255, 255))
        if t < 2.6:
            show(f, self.h1, CX, 820, t, -1, 2.6, anchor="mt")
            show(f, self.h2, CX, 1060, t, -1, 2.6, anchor="mt")
        elif t < 5.8:
            show(f, self.l1, CX, 820, t, 3.6, 5.8, anchor="mt")
        elif t < 8.0:
            show(f, self.l2, CX, 820, t, 5.8, 8.0, anchor="mt")
        elif t < 11.0:
            show(f, self.l3, CX, 760, t, 9.0, 11.0, anchor="mt")
            show(f, self.l4, CX, 900, t, 9.3, 11.0, anchor="mt")
        else:
            show(f, self.l5, CX, 760, t, 11.0, self.end_t, anchor="mt")
        watermark(f, 0.8)
        return f


# =====================================================================
# V4 — « Trois gestes »  · Poppins · navy + mint, app-card UI · UK garage
# =====================================================================
class TroisGestes:
    name, duration, end_t, song = "v04-trois-gestes", 17.0, 14.4, "uk_garage"
    NAVY, MINT, CARD = hexc("#0B1E2D"), hexc("#5EEAD4"), hexc("#0F2A3D")
    CX0, CY0, CX1, CY1 = 200, 1300, 1660, 2720

    def __init__(self):
        self.bg = vgrad(hexc("#0B1E2D"), hexc("#081521"))
        card = self.bg.copy()
        rrect(card, self.CX0, self.CY0, self.CX1, self.CY1, 70, self.CARD)
        rrect(card, self.CX0, self.CY0, self.CX1, self.CY1, 70, hexc("#1C4058"), 4)
        self.card = card
        mp = card.copy()
        sub = mp[self.CY0 + 40:self.CY1 - 40, self.CX0 + 40:self.CX1 - 40]
        nodes, edges = city(12, 6, 6, -40, -40, 250, 240, 36)
        for a, b in edges:
            line(sub, nodes[a], nodes[b], hexc("#1D3A4F"), 6)
        self.mapcard = mp
        off = (self.CX0 + 40, self.CY0 + 40)
        raw = loop(nodes, {(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (2, 4), (1, 4)})
        self.route = [(x + off[0], y + off[1]) for x, y in raw]
        self.h1 = text("Trois gestes,", "pop_b", 190, WHITE)
        self.h2 = text("et tu cours.", "pop_l", 190, self.MINT)
        self.steps = [text("1 · Choisis ta distance", "pop_sb", 110, WHITE),
                      text("2 · Traceo trace ta boucle", "pop_sb", 110, WHITE),
                      text("3 · Tu cours, guidé à la voix", "pop_sb", 110, WHITE)]
        self.cap1 = text("De 2 à 42 km, ou de 10 min à 4 h.", "pop_l", 76, (170, 196, 210))
        self.cap2 = text("Il garde l'itinéraire avec le plus de rues nouvelles.", "pop_l", 76,
                         (170, 196, 210), maxw=1450)
        self.chip = pill(text("≈ 10 s", "pop_b", 60, self.NAVY), self.MINT, 40, 18)
        self.voice = text("« Dans 100 mètres, tourne à droite. »", "pop_sb", 70, WHITE, maxw=1100)
        self.km = {k: text(f"{k} km", "pop_b", 300, WHITE) for k in range(2, 11)}
        self.tag = text("Tracer sa boucle est gratuit.", "pop_l", 92, (200, 220, 228))
        self.cta = pill(text("Lien en bio", "pop_b", 72, self.NAVY), self.MINT)

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.NAVY, self.tag, self.cta)
            return f
        if t < 2.6:
            f = self.bg.copy()
            show(f, self.h1, X0, 820, t, -1, 2.6)
            show(f, self.h2, X0, 1050, t, -1, 2.6)
            for i in range(3):
                cx = X0 + 90 + i * 230
                circle(f, (cx, 1620), 80, self.MINT if t > 0.6 + i * 0.5 else hexc("#1C4058"), 6)
                blit(f, text(str(i + 1), "pop_b", 96, WHITE), cx, 1620, 1, "mm")
            watermark(f, 0.85)
            return f
        if t < 6.2:
            f = self.card.copy()
            show(f, self.steps[0], X0, 760, t, 2.6, 6.2)
            k = eout((t - 3.0) / 2.0)
            val = int(round(2 + 8 * k))
            blit(f, self.km[val], CX, 1620, 1, "mt")
            y = 2160
            line(f, (self.CX0 + 140, y), (self.CX1 - 140, y), hexc("#1C4058"), 18)
            xk = self.CX0 + 140 + (self.CX1 - self.CX0 - 280) * (0.05 + 0.2 * k)
            line(f, (self.CX0 + 140, y), (xk, y), self.MINT, 18)
            circle(f, (xk, y), 46, WHITE)
            show(f, self.cap1, self.CX0 + 140, 2330, t, 3.4, 6.2)
        elif t < 10.4:
            f = self.mapcard.copy()
            show(f, self.steps[1], X0, 760, t, 6.2, 10.4)
            P = Path(self.route, True)
            part = P.part(eout((t - 6.6) / 1.8, 2))
            if len(part) > 1:
                glow_path(f, part, (30, 120, 110), 36, 50, 0.8)
                poly(f, part, self.MINT, 24)
                circle(f, part[-1], 26, WHITE)
            blit(f, self.chip, self.CX1 - 60, self.CY0 + 60, clamp((t - 6.4) / 0.3), "rt")
            show(f, self.cap2, X0, 2800, t, 8.0, 10.4, dy=30)
        else:
            f = self.mapcard.copy()
            show(f, self.steps[2], X0, 760, t, 10.4, self.end_t)
            P = Path(self.route, True)
            poly(f, P.part(1.0), self.MINT, 20)
            pos = P.at(P.L * ((t - 10.4) / 4.0 % 1))
            glow_dot(f, pos, 50, self.MINT, 0.9)
            circle(f, pos, 32, WHITE)
            a = clamp((t - 10.8) / 0.3)
            rrect_alpha(f, self.CX0 + 70, self.CY1 - 300, self.CX1 - 70, self.CY1 - 80, 60,
                        hexc("#06121C"), 0.92 * a)
            if a > 0:
                for i in range(7):
                    hgt = 24 + 70 * abs(math.sin(t * 9 + i * 1.3))
                    x = self.CX0 + 140 + i * 34
                    line(f, (x, self.CY1 - 190 - hgt / 2), (x, self.CY1 - 190 + hgt / 2), self.MINT, 16)
                blit(f, self.voice, self.CX0 + 420, self.CY1 - 190, a, "lm")
        watermark(f, 0.85)
        return f


# =====================================================================
# V5 — « Comment il choisit »  · DejaVu Sans Mono · graphite + data green · minimal techno
# =====================================================================
class LeChoix:
    name, duration, end_t, song = "v05-le-choix", 16.0, 13.4, "minimal_techno"
    BG, GREEN, KNOWN = hexc("#111418"), hexc("#3DDC97"), hexc("#4B5A66")

    def __init__(self):
        self.bg0 = flat(self.BG)
        self.map, nodes, edges = make_map(21, self.bg0, (36, 41, 47), 5)
        rnd = np.random.default_rng(5)
        self.known = [(nodes[a], nodes[b]) for a, b in edges if rnd.random() < 0.22]
        self.cands = {"A": loop(nodes, {(1, 1), (2, 1), (2, 2), (1, 2)}),
                      "B": loop(nodes, {(5, 2), (6, 2), (6, 3), (5, 3)}),
                      "C": rot(loop(nodes, {(2, 3), (3, 3), (4, 3), (4, 4), (3, 4), (3, 5), (2, 5)}),
                               2)}
        self.D = loop(nodes, {(5, 0), (6, 0), (6, 1), (5, 1), (4, 1)})
        self.home = nodes[(3, 3)]
        self.h1 = text("> comment traceo", "mono_b", 118, WHITE)
        self.h2 = text("  choisit ta boucle ?", "mono_b", 118, self.GREEN)
        self.leg = text("━ rues déjà courues", "mono_r", 56, self.KNOWN)
        self.s1 = text("plusieurs itinéraires comparés", "mono_b", 80, WHITE)
        self.s2 = text("il garde celui qui a le plus", "mono_b", 80, WHITE)
        self.s3 = text("de rues nouvelles", "mono_b", 80, self.GREEN)
        self.s4 = text("et il se souvient de celles", "mono_b", 80, WHITE)
        self.s5 = text("qu'il t'a déjà proposées", "mono_b", 80, self.GREEN)
        self.bl = {k: text(k, "mono_b", 70, WHITE) for k in "ABC"}
        self.tag = text("Une boucle neuve à chaque sortie.", "mono_r", 76, (200, 210, 205))
        self.cta = pill(text("lien en bio", "mono_b", 66, self.BG), self.GREEN)

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.BG, self.tag, self.cta)
            return f
        k = clamp((t - 2.4) / 0.8)
        f = cv2.addWeighted(self.bg0, 1 - k, self.map, k, 0) if k < 1 else self.map.copy()
        if t >= 2.8:
            kk = clamp((t - 2.8) / 0.8)
            for a, b in self.known[: int(len(self.known) * kk)]:
                line(f, a, b, self.KNOWN, 12)
            circle(f, self.home, 30, WHITE)
            show(f, self.leg, X0, 2700, t, 2.9, self.end_t, dy=20)
        if t < 2.6:
            show(f, self.h1, X0, 760, t, -1, 2.6)
            show(f, self.h2, X0, 900, t, -1, 2.6)
            if int(t * 3) % 2 == 0:
                rrect(f, X0 + 1330, 925, X0 + 1395, 1035, 0, self.GREEN)
        if 5.0 <= t < 9.6:
            show(f, self.s1, X0, 760, t, 5.0, 8.4)
            for i, key in enumerate("ABC"):
                st = 5.2 + i * 0.9
                if t < st:
                    continue
                P = Path(self.cands[key], True)
                win = key == "C" and t >= 8.2
                if not win:
                    a = 1.0 if t < 8.2 else clamp(1 - (t - 8.2) / 0.5)
                    if a > 0:
                        poly(f, P.part(eout((t - st) / 0.7)), mix(self.BG, WHITE, 0.85 * a), 8)
                bx, by = X0 + i * 520, 2400
                blit(f, self.bl[key], bx, by - 10, 1, "lt")
                full = {"A": 0.45, "B": 0.3, "C": 0.95}[key]
                wbar = 360 * full * eout((t - st - 0.3) / 0.6)
                rrect(f, bx + 70, by + 20, bx + 70 + 360, by + 60, 0, (36, 41, 47))
                if wbar > 2:
                    rrect(f, bx + 70, by + 20, bx + 70 + wbar, by + 60, 0,
                          self.GREEN if win else (200, 205, 206))
            if t >= 8.2:
                P = Path(self.cands["C"], True)
                glow_path(f, P.part(1.0), (20, 110, 70), 30, 50, 0.9)
                poly(f, P.part(1.0), self.GREEN, 22)
                show(f, self.s2, X0, 760, t, 8.4, 9.6)
                show(f, self.s3, X0, 870, t, 8.6, 9.6)
        elif t >= 9.6:
            P = Path(self.cands["C"], True)
            fade = clamp((t - 9.8) / 0.8)
            poly(f, P.part(1.0), mix(self.GREEN, self.KNOWN, fade), 22 - 10 * fade)
            if t >= 10.6:
                D = Path(self.D, True)
                part = D.part(eout((t - 10.6) / 1.4))
                glow_path(f, part, (20, 110, 70), 30, 50, 0.9)
                poly(f, part, self.GREEN, 22)
            show(f, self.s4, X0, 760, t, 9.8, self.end_t)
            show(f, self.s5, X0, 870, t, 10.0, self.end_t)
        watermark(f, 0.8)
        return f


# =====================================================================
# V6 — « Mode nuit »  · TeX Gyre Heros Condensed Bold Italic · black + neon · synthwave
# =====================================================================
class ModeNuit:
    name, duration, end_t, song = "v06-mode-nuit", 15.0, 12.4, "synthwave"
    BG, CYAN, MAG = hexc("#05060A"), hexc("#19E3FF"), hexc("#FF2E88")

    def __init__(self):
        self.bg0 = flat(self.BG)
        m, nodes, _ = make_map(44, self.bg0, (24, 28, 40), 5)
        line(m, (-50, nodes[(0, 4)][1]), (W + 50, nodes[(8, 4)][1]), (40, 46, 66), 34)
        line(m, (nodes[(5, 0)][0], 900), (nodes[(5, 6)][0], 2800), (40, 46, 66), 34)
        self.map = m
        self.route = loop(nodes, {(1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (2, 3)})
        self.h = [text("19 H.", "heroscn_bi", 340, WHITE), text("IL FAIT NUIT.", "heroscn_bi", 210, WHITE),
                  text("TU COURS OÙ ?", "heroscn_bi", 210, self.CYAN)]
        self.l = [text("CARTE CONTRASTÉE. MODE NUIT.", "heroscn_bi", 130, WHITE),
                  text("PETITES RUES, LOIN DES GRANDS AXES.", "heroscn_bi", 130, WHITE, maxw=1500),
                  text("TA BOUCLE EN IMAGE NÉON,", "heroscn_bi", 130, WHITE),
                  text("PRÊTE POUR TA STORY.", "heroscn_bi", 130, self.MAG),
                  text("COURS. PARTAGE.", "heroscn_bi", 170, WHITE),
                  text("RECOMMENCE AILLEURS.", "heroscn_bi", 150, self.CYAN)]
        self.prem = pill(text("PREMIUM", "heroscn_r", 54, self.BG), self.MAG, 40, 14)
        self.tag = text("UNE BOUCLE NEUVE À CHAQUE SORTIE.", "heroscn_r", 90, (210, 220, 230))
        self.cta = pill(text("LIEN EN BIO", "heroscn_bi", 74, self.BG), self.CYAN)

    def neon(self, f, pts, frac, th=26, closed=True):
        P = Path(pts, closed)
        part = P.part(frac)
        if len(part) < 2:
            return part
        glow_path(f, part, (10, 120, 160), th * 2.4, 70, 1.0)
        glow_path(f, part, (150, 20, 80), th * 1.4, 30, 0.6)
        grad_poly(f, part, self.CYAN, self.MAG, th)
        return part

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.BG, self.tag, self.cta)
            return f
        if t < 2.6:
            f = self.bg0.copy()
            flick = 0.55 if (0.35 < t < 0.42 or 0.5 < t < 0.55) else 1.0
            for i, L in enumerate(self.h):
                show(f, L, X0, [700, 1060, 1290][i], t, -1, 2.6)
            if flick < 1:
                f[:] = (f.astype(np.float32) * flick).astype(np.uint8)
            watermark(f, 0.8)
            return f
        k = clamp((t - 2.6) / 0.6)
        f = cv2.addWeighted(self.bg0, 1 - k, self.map, k, 0) if k < 1 else self.map.copy()
        if t < 7.0:
            part = self.neon(f, self.route, eout((t - 2.9) / 2.0, 2))
            if len(part) > 1:
                circle(f, part[-1], 24, WHITE)
            show(f, self.l[0], X0, 700, t, 3.0, 5.0)
            show(f, self.l[1], X0, 700, t, 5.0, 7.0)
            if t >= 5.2:
                blit(f, self.prem, X0, 1000, clamp((t - 5.2) / 0.3) * clamp((7.0 - t) / 0.3))
        elif t < 10.2:
            f = (f.astype(np.float32) * 0.35).astype(np.uint8)
            k = eback((t - 7.0) / 0.5)
            x0, y0, x1, y1 = 520, 1180, 1340, 2640
            yo = int((1 - k) * 600)
            rrect(f, x0, y0 + yo, x1, y1 + yo, 50, (10, 12, 20))
            rrect(f, x0, y0 + yo, x1, y1 + yo, 50, (60, 66, 90), 4)
            pts = [((x - 0) * 0.42 + 470, (y - 1150) * 0.42 + 1500 + yo) for x, y in self.route]
            self.neon(f, pts, 1.0, 16)
            blit(f, wordmark(70), (x0 + x1) / 2, y1 - 200 + yo, 1, "mt")
            show(f, self.l[2], X0, 640, t, 7.2, 10.2)
            show(f, self.l[3], X0, 790, t, 7.4, 10.2)
        else:
            self.neon(f, self.route, 1.0)
            show(f, self.l[4], X0, 700, t, 10.2, self.end_t)
            show(f, self.l[5], X0, 900, t, 10.4, self.end_t)
        watermark(f, 0.8)
        return f


# =====================================================================
# V7 — « Marcheurs »  · Lora · sand + forest + terracotta · lo-fi
# =====================================================================
class Marcheurs:
    name, duration, end_t, song = "v07-marcheurs", 15.0, 12.4, "lofi"
    SAND, FOREST, TERRA = hexc("#EDE6DA"), hexc("#24493B"), hexc("#C8643B")

    def __init__(self):
        self.bg = flat(self.SAND)
        self.map, nodes, _ = make_map(77, self.bg, (216, 205, 186), 6)
        self.route = loop(nodes, {(2, 2), (3, 2), (4, 2), (4, 3), (3, 3), (3, 4), (2, 4)})
        self.home = self.route[0]
        self.h1 = text("Tu marches", "lora", 200, self.FOREST)
        self.h2 = text("tous les jours ?", "lora", 200, self.FOREST)
        self.h3 = text("Pas forcément au même endroit.", "lora_i", 112, self.TERRA, maxw=1500)
        self.d1 = text("Choisis une durée,", "lora_i", 116, self.FOREST)
        self.d2 = text("pas une distance.", "lora_i", 116, self.FOREST)
        self.vals = {v: text(v, "lora", 230, self.FOREST, align="center")
                     for v in ("10 min", "30 min", "1 h", "2 h", "4 h")}
        self.m1 = text("Une boucle qui part de ta porte", "lora", 116, self.FOREST, maxw=1500)
        self.m2 = text("et t'y ramène.", "lora_i", 116, self.TERRA)
        self.e1 = text("Chaque fois,", "lora", 190, self.FOREST)
        self.e2 = text("d'autres rues.", "lora_i", 190, self.TERRA)
        self.tag = text("Une boucle neuve à chaque sortie.", "lora_i", 92, self.FOREST)
        self.cta = pill(text("Lien en bio", "lora", 74, self.SAND), self.FOREST)

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.SAND, self.tag, self.cta, ink=self.FOREST, glow=False)
            return f
        if t < 6.4:
            f = self.bg.copy()
            if t < 2.6:
                show(f, self.h1, X0, 760, t, -1, 2.6)
                show(f, self.h2, X0, 990, t, -1, 2.6)
                show(f, self.h3, X0, 1300, t, -1, 2.6)
            else:
                show(f, self.d1, X0, 720, t, 2.6, 6.4)
                show(f, self.d2, X0, 870, t, 2.8, 6.4)
                c, r = (CX, 1900), 520
                cv2.ellipse(f, c, (r, r), 0, 0, 360, (216, 205, 186), 14, cv2.LINE_AA)
                k = eout((t - 3.0) / 3.0, 2)
                cv2.ellipse(f, c, (r, r), -90, 0, 20 + 340 * k, self.TERRA, 36, cv2.LINE_AA)
                keys = ["10 min", "30 min", "1 h", "2 h", "4 h"]
                v = keys[min(4, int(k * 5))]
                blit(f, self.vals[v], CX, 1900, 1, "mm")
        else:
            k = clamp((t - 6.4) / 0.6)
            f = cv2.addWeighted(self.bg, 1 - k, self.map, k, 0) if k < 1 else self.map.copy()
            if t < 10.6:
                P = Path(self.route, True)
                part = P.part(eout((t - 6.8) / 2.8, 2))
                if len(part) > 1:
                    poly(f, part, self.FOREST, 22)
                    circle(f, part[-1], 28, self.TERRA)
                hx, hy = self.home
                pts = np.array([(hx - 60, hy - 10), (hx, hy - 70), (hx + 60, hy - 10), (hx + 60, hy + 60),
                                (hx - 60, hy + 60)], np.int32)
                cv2.fillPoly(f, [pts], self.TERRA, cv2.LINE_AA)
                show(f, self.m1, X0, 720, t, 6.6, 10.6)
                show(f, self.m2, X0, 1000, t, 8.4, 10.6)
            else:
                poly(f, Path(self.route, True).part(1.0), self.FOREST, 22)
                show(f, self.e1, X0, 700, t, 10.6, self.end_t)
                show(f, self.e2, X0, 920, t, 10.8, self.end_t)
        watermark(f, 0.9, self.FOREST)
        return f


# =====================================================================
# V8 — « Randonnée »  · TeX Gyre Pagella · forest + cream topo lines · ambient piano
# =====================================================================
class Rando:
    name, duration, end_t, song = "v08-randonnee", 16.0, 13.4, "ambient_piano"
    BG, CREAM, MOSS, LINE = hexc("#0E2621"), hexc("#EFE7D6"), hexc("#8FB996"), (34, 66, 57)

    def __init__(self):
        self.bg = flat(self.BG)
        rnd = np.random.default_rng(8)
        self.blobs = [(rnd.uniform(0, 270), rnd.uniform(0, 480), rnd.uniform(40, 120),
                       rnd.uniform(-1, 1), rnd.uniform(0, 6.28)) for _ in range(9)]
        yy, xx = np.mgrid[0:480, 0:270].astype(np.float32)
        self.xx, self.yy = xx, yy
        pts = [(260, 2350), (520, 2100), (700, 2180), (900, 1900), (1180, 1820), (1420, 1600),
               (1560, 1700), (1500, 2050), (1250, 2300), (980, 2480), (640, 2560), (380, 2520)]
        self.trail = smooth(pts, 3)
        self.h = text("Le plus beau chemin\nest peut-être à\n20 minutes de chez toi.", "pag_i", 150,
                      self.CREAM, lh=1.15)
        self.l1 = text("Petites rues. Chemins.", "pag_r", 140, self.CREAM)
        self.l2 = text("Loin des grands axes.", "pag_i", 140, self.MOSS)
        self.l3 = text("Une boucle qui part de chez toi", "pag_r", 120, self.CREAM, maxw=1500)
        self.l4 = text("et t'y ramène.", "pag_i", 120, self.MOSS)
        self.l5 = text("Explore ce qui\nest déjà là.", "pag_i", 190, self.CREAM, lh=1.1)
        self.tag = text("Une boucle neuve à chaque sortie.", "pag_i", 96, self.CREAM)
        self.cta = pill(text("Lien en bio", "pag_b", 74, self.BG), self.CREAM)

    def field(self, t):
        z = np.zeros_like(self.xx)
        for (bx, by, r, s, ph) in self.blobs:
            cx = bx + 12 * math.sin(t * 0.25 + ph)
            cy = by + 12 * math.cos(t * 0.2 + ph)
            z += s * np.exp(-((self.xx - cx) ** 2 + (self.yy - cy) ** 2) / (2 * r * r))
        return z

    def topo(self, f, t):
        z = self.field(t)
        for lv in np.linspace(z.min() + 0.08, z.max() - 0.05, 11):
            mask = (z > lv).astype(np.uint8)
            cs, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for c in cs:
                if len(c) < 6:
                    continue
                pts = c.reshape(-1, 2).astype(np.float64) * 8
                poly(f, pts, self.LINE, 4, True)

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.BG, self.tag, self.cta, ink=self.CREAM)
            return f
        f = self.bg.copy()
        self.topo(f, t)
        if t < 3.0:
            show(f, self.h, X0, 760, t, -1, 3.0)
        if t >= 3.0:
            P = Path(self.trail, t >= 7.6)
            frac = eout((t - 3.2) / 4.4, 2) if t < 7.6 else 1.0
            sp = P.resample(160)
            n = int(160 * frac)
            for i in range(0, n, 3):
                circle(f, sp[i], 14, self.MOSS)
            if n > 0:
                circle(f, sp[min(n, 159)], 26, self.CREAM)
            circle(f, sp[0], 40, self.CREAM, 6)
            if 3.0 <= t < 7.6:
                show(f, self.l1, X0, 760, t, 3.4, 7.6)
                show(f, self.l2, X0, 920, t, 5.2, 7.6)
            elif t < 11.4:
                Pc = Path(self.trail + [self.trail[0]])
                grad = eout((t - 7.6) / 1.0)
                poly(f, Pc.part(1 - 0.08, 1 - 0.08 + 0.08 * grad), self.MOSS, 8)
                show(f, self.l3, X0, 760, t, 7.8, 11.4)
                show(f, self.l4, X0, 1040, t, 8.4, 11.4)
            else:
                show(f, self.l5, X0, 740, t, 11.4, self.end_t)
        watermark(f, 0.85)
        return f


# =====================================================================
# V9 — « Jamais seul »  · Carlito · charcoal + coral · afro house
# =====================================================================
class JamaisSeul:
    name, duration, end_t, song = "v09-jamais-seul", 15.0, 12.4, "afro_house"
    BG, CORAL, WARM, GREY = hexc("#15171C"), hexc("#FF6B57"), hexc("#F4EDE4"), hexc("#8B8F98")

    def __init__(self):
        self.bg = flat(self.BG)
        rnd = np.random.default_rng(99)
        self.c = (CX, 1950)
        self.R = 640
        self.dots = []
        while len(self.dots) < 16:
            a, r = rnd.uniform(0, 6.28), self.R * math.sqrt(rnd.uniform(0.08, 0.95))
            self.dots.append((self.c[0] + r * math.cos(a), self.c[1] + r * math.sin(a),
                              rnd.uniform(0, 6.28), rnd.uniform(3.0, 6.4)))
        self.h1 = text("Ne cours plus", "carl_b", 230, WHITE)
        self.h2 = text("jamais seul.", "carl_b", 230, self.CORAL)
        self.l1 = text("Un bouton : « Je pars courir ».", "carl_b", 110, WHITE, maxw=1500)
        self.l2 = text("Les coureurs à moins de 5 km sont prévenus.", "carl_r", 92, self.GREY,
                       maxw=1500)
        self.l3 = text("Positions arrondies.", "carl_b", 130, WHITE)
        self.l4 = text("Mode invisible.", "carl_b", 130, self.CORAL)
        self.l5 = text("Trouve tes partenaires de course,", "carl_b", 110, WHITE, maxw=1500)
        self.l6 = text("près de chez toi.", "carl_b", 110, self.CORAL)
        self.km = text("5 km", "carl_b", 64, self.GREY)
        self.n1 = text("Léa part courir", "carl_b", 78, WHITE)
        self.n2 = text("à 2 km · maintenant", "carl_r", 62, self.GREY)
        self.ex = text("exemple", "carl_r", 48, self.GREY)
        self.inv = text("Mode invisible", "carl_b", 74, WHITE)
        self.prem = pill(text("Premium", "carl_b", 56, self.BG), self.CORAL, 36, 12)
        self.tag = text("Une boucle neuve à chaque sortie.", "carl_r", 92, self.WARM)
        self.cta = pill(text("Lien en bio", "carl_b", 76, self.BG), self.CORAL)

    def radar(self, f, t, snap=0.0):
        cx, cy = self.c
        k = eout((t - 2.6) / 1.2)
        for rr in (0.33, 0.66, 1.0):
            cv2.circle(f, (cx, cy), int(self.R * rr * k), (40, 43, 52), 4, cv2.LINE_AA)
        blit(f, self.km, cx + self.R * k * 0.72, cy - self.R * k * 0.72, k, "lm")
        sweep = (t * 1.4) % 1
        cv2.circle(f, (cx, cy), int(self.R * sweep), mix(self.BG, self.CORAL, 0.35 * (1 - sweep)), 6,
                   cv2.LINE_AA)
        for i, (x, y, ph, sp) in enumerate(self.dots):
            st = 3.0 + i * 0.12
            if t < st:
                continue
            if snap > 0:
                gx, gy = round(x / 160) * 160, round(y / 160) * 160
                x, y = x + (gx - x) * snap, y + (gy - y) * snap
            a = eout((t - st) / 0.3)
            pr = 0.5 + 0.5 * math.sin(t * sp + ph)
            circle(f, (x, y), (18 + 8 * pr) * a, self.WARM)
        circle(f, (cx, cy), 44, self.CORAL)
        circle(f, (cx, cy), 22, WHITE)

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.BG, self.tag, self.cta)
            return f
        f = self.bg.copy()
        if t < 2.6:
            show(f, self.h1, X0, 800, t, -1, 2.6)
            show(f, self.h2, X0, 1060, t, -1, 2.6)
        else:
            snap = eout((t - 7.4) / 0.8) if 7.0 <= t < 10.2 else 0.0
            self.radar(f, t, snap)
        if 3.4 <= t < 7.0:
            k = eback((t - 3.4) / 0.45)
            y = 640 - (1 - k) * 300
            rrect(f, X0, y, X1, y + 260, 56, hexc("#23262E"))
            circle(f, (X0 + 130, y + 130), 76, self.CORAL)
            blit(f, text("L", "carl_b", 90, WHITE), X0 + 130, y + 130, 1, "mm")
            blit(f, self.n1, X0 + 250, y + 55)
            blit(f, self.n2, X0 + 250, y + 150)
            blit(f, self.ex, X1 - 40, y + 30, 0.8, "rt")
            show(f, self.l1, X0, 2700, t, 4.4, 7.0, dy=30)
            show(f, self.l2, X0, 2840 - 20, t, 5.4, 7.0, dy=30)
        elif 7.0 <= t < 10.2:
            show(f, self.l3, X0, 700, t, 7.2, 10.2)
            show(f, self.l4, X0, 860, t, 8.4, 10.2)
            if t >= 8.4:
                on = eout((t - 8.8) / 0.3)
                x0, y0 = X0, 2700
                rrect(f, x0, y0, x0 + 230, y0 + 120, 60, mix((60, 63, 72), self.CORAL, on))
                circle(f, (x0 + 60 + 110 * on, y0 + 60), 46, WHITE)
                blit(f, self.inv, x0 + 280, y0 + 60, 1, "lm")
        elif t >= 10.2:
            show(f, self.l5, X0, 700, t, 10.2, self.end_t)
            show(f, self.l6, X0, 980, t, 10.4, self.end_t)
            blit(f, self.prem, X0, 1150, clamp((t - 10.8) / 0.3))
        watermark(f, 0.85)
        return f


# =====================================================================
# V10 — « Manifeste »  · Source Serif (Noto Serif) · black to deep teal · cinematic hybrid
# =====================================================================
class Manifeste:
    name, duration, end_t, song = "v10-manifeste", 17.0, 13.6, "cine_hybrid"
    CREAM = hexc("#EDE7DC")

    def __init__(self):
        self.bg = radial(vgrad((3, 4, 6), hexc("#0A2A2C"), 1.6), hexc("#0F3A38"), CX, 3300, 1900, 0.6)
        lines = ["Courir, ce n'est pas\n*tourner* *en* *rond.*",
                 "C'est tourner à gauche,\nlà où tu tournes\ntoujours à droite.",
                 "C'est la boulangerie\nque tu ne connaissais pas.",
                 "La rue d'à côté.\nLe chemin derrière l'école.",
                 "Rentrer avec une ville\nun peu plus grande."]
        self.L = [text(s, "serif_l", 128, self.CREAM, align="center", lh=1.22, maxw=1600,
                       accent=hexc("#6FD6B4")) for s in lines]
        rnd = np.random.default_rng(10)
        pts = [(-80, 2600)]
        x = -80
        while x < W + 100:
            x += rnd.uniform(160, 260)
            pts.append((x, 2600 + rnd.uniform(-160, 160)))
        self.path = smooth(pts, 3, closed=False)
        self.tag = text("Une boucle neuve à chaque sortie.", "serif_l", 84, self.CREAM)
        self.cta = pill(text("Lien en bio", "serif_sb", 74, (3, 4, 6)), self.CREAM)

    def frame(self, t):
        if t >= self.end_t:
            f = np.empty((H, W, 3), np.uint8)
            endcard(f, t - self.end_t, self.bg, self.tag, self.cta, ink=self.CREAM)
            return f
        f = self.bg.copy()
        P = Path(self.path)
        part = P.part(t / self.end_t)
        if len(part) > 1:
            poly(f, part, (60, 80, 78), 6)
            glow_dot(f, part[-1], 26, (60, 199, 154), 0.8)
            circle(f, part[-1], 12, (200, 240, 230))
        seg = 2.72
        i = min(4, int(t / seg))
        t0 = i * seg
        lt = t - t0
        a = (1.0 if (i == 0 and lt < 0.5) else eout(lt / 0.6)) * clamp((seg - lt) / 0.45 if i < 4 else
                                                                         (self.end_t - t) / 0.4)
        s = 1.0 + 0.03 * (lt / seg)
        blit(f, self.L[i], CX, 1500, a, "mm", s)
        watermark(f, 0.7, self.CREAM)
        return f


SCENES = [MemeEndroit, Cent56, YeuxFermes, TroisGestes, LeChoix, ModeNuit, Marcheurs, Rando,
          JamaisSeul, Manifeste]
