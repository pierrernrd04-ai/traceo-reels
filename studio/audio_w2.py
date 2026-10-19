#!/usr/bin/env python3
"""Wave 2 soundtracks: ten new genres, built on the audio10 instruments."""
import numpy as np

from audio10 import (Mix, SR, adsr, apply_delay, apply_reverb, bass808, bell, clap, conga, crackle,
                     duck_env, finish, fm, grid, hat, hp, hz, impact, kick, lead, lp, marimba,
                     noise, ns, piano, pluck, rhodes, rim, riser, saw, shaker, sine, snare, sonic_logo,
                     sq, sub, supersaw, tom, tt, whoosh)


def pulse(m, dur, pw=0.25, vol=0.5):
    n = ns(dur + 0.02)
    s = sq(hz(m), n, 0, pw)
    return s * adsr(n, 0.002, 0.05, 0.8, 0.02, dur) * vol


def tri(m, dur):
    n = ns(dur + 0.02)
    ph = (hz(m) * tt(n)) % 1
    return (4 * np.abs(ph - 0.5) - 1) * adsr(n, 0.002, 0.05, 0.9, 0.02, dur)


def nz_drum(dur=0.08, cut=6000):
    n = ns(dur)
    t = tt(n)
    q = np.repeat(noise(n // 8 + 1), 8)[:n]
    return lp(q, cut) * np.exp(-t * (40 / dur * 0.08))


def swish():
    n = ns(0.25)
    t = tt(n)
    return hp(noise(n), 3000) * np.sin(np.pi * t / 0.25) ** 2 * 0.3


def ride():
    n = ns(0.9)
    t = tt(n)
    m = sum(sq(f, n) for f in (420, 589, 711, 978)) / 4
    return hp(m + 0.4 * noise(n), 5000) * np.exp(-t * 5) * 0.25


def tick():
    n = ns(0.03)
    t = tt(n)
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 300)


def bitcrush(x, steps=24):
    return np.round(x * steps) / steps


# ---------------------------------------------------------------- songs
def chill_pop(dur, path, logo_t):
    """W1 chat: soft pop, marimba plucks, finger snaps, warm bass."""
    mx = Mix(dur)
    b, nb = grid(104, dur)
    prog = [(48, [64, 67, 71]), (45, [64, 67, 72]), (41, [65, 69, 72]), (43, [62, 67, 71])]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = prog[bar % 4]
        for k in range(4):
            mx.add(kick("soft"), t0 + k * b, 0.55 if k % 2 == 0 else 0.0, 0, "drums")
        for sb in (1, 3):
            mx.add(clap(), t0 + sb * b, 0.25, 0.2, "drums")
        for e in range(8):
            mx.add(shaker(), t0 + e * b / 2 + 0.03 * (e % 2), 0.12, -0.3, "drums")
        for i, m in enumerate([ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12]):
            mx.add(marimba(m, 0.3), t0 + [0, 0.75, 1.5, 2, 2.75, 3.5][i] * b, 0.25,
                   0.3 if i % 2 else -0.3, "keys")
        mx.add(sub(root - 12, 1.8 * b), t0, 0.45, 0, "bass")
        mx.add(sub(root - 12, 1.4 * b), t0 + 2.5 * b, 0.4, 0, "bass")
        mx.add(supersaw(ch, 4 * b, 1500, 0.6, 0.8), t0, 0.18, 0, "pad")
    sonic_logo(mx, logo_t, 72)
    finish(mx, path, {"keys": 0.3, "pad": 0.3, "fx": 0.5})


def chiptune(dur, path, logo_t):
    """W2 game: 8-bit, pulse lead, triangle bass, noise drums."""
    mx = Mix(dur)
    b, nb = grid(144, dur)
    prog = [57, 53, 48, 55]
    mel = [69, 72, 76, 79, 76, 72, 74, 76, 77, 76, 74, 72, 71, 72, 74, 71]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root = prog[bar % 4]
        for e in range(8):
            mx.add(tri(root - 12 + (12 if e % 2 else 0), b / 2 * 0.9), t0 + e * b / 2, 0.45, 0, "bass")
            mx.add(nz_drum(0.05, 9000), t0 + e * b / 2, 0.12, 0.2, "drums")
        for k in (0, 2):
            mx.add(kick("soft"), t0 + k * b, 0.5, 0, "drums")
        for k in (1, 3):
            mx.add(nz_drum(0.18, 5000), t0 + k * b, 0.4, 0, "drums")
        for s in range(16):
            arp = [root + 12, root + 16, root + 19, root + 24][s % 4]
            mx.add(pulse(arp, b / 4 * 0.5, 0.125, 0.12), t0 + s * b / 4, 1.0, 0.35, "arp")
        if bar % 2 == 1 or bar >= 2:
            for i in range(8):
                mx.add(pulse(mel[(bar * 8 + i) % 16], b / 2 * 0.8, 0.25, 0.3), t0 + i * b / 2, 1.0,
                       -0.15, "lead")
    for i, m in enumerate([72, 76, 79, 84]):
        mx.add(pulse(m, 0.09, 0.5, 0.35), 2.6 + i * 0.07, 1.0, 0, "fx")
    sonic_logo(mx, logo_t, 76)
    for k in ("arp", "lead"):
        mx.buses[k] = bitcrush(mx.buses[k], 16)
    finish(mx, path, {"lead": 0.15, "arp": 0.1, "fx": 0.4})


def trap(dur, path, logo_t):
    """W3 tier list: trap, 808 glides, hat rolls, half-time snare."""
    mx = Mix(dur)
    b, nb = grid(140, dur)
    roots = [45, 45, 41, 43]
    bells = [76, 72, 69, 72, 76, 79, 76, 72]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        r = roots[bar % 4]
        mx.add(kick("808"), t0, 0.7, 0, "drums")
        mx.add(bass808(r - 24, 1.4 * b), t0, 0.6, 0, "bass")
        mx.add(kick("808"), t0 + 2.5 * b, 0.6, 0, "drums")
        mx.add(bass808(r - 24 + 3, 1.0 * b, r - 24), t0 + 2.5 * b, 0.55, 0, "bass")
        mx.add(clap(), t0 + 2 * b, 0.45, 0, "drums")
        mx.add(snare("tight"), t0 + 2 * b, 0.3, 0, "drums")
        for e in range(8):
            t = t0 + e * b / 2
            if e in (3, 7):
                for r32 in range(4):
                    mx.add(hat(False, 1.3), t + r32 * b / 8, 0.12, 0.3, "drums")
            else:
                mx.add(hat(False, 1.3), t, 0.18, 0.3, "drums")
        for i, m in enumerate(bells):
            mx.add(bell(m, 0.4), t0 + i * b / 2, 0.08, -0.3 if i % 2 else 0.3, "keys")
    sonic_logo(mx, logo_t, 69)
    finish(mx, path, {"keys": 0.4, "fx": 0.5, "drums": 0.04})


def progressive(dur, path, logo_t, drop_t=7.0):
    """W4 before/after: filtered build, riser, drop on the reveal."""
    mx = Mix(dur)
    b, nb = grid(124, dur)
    prog = [(50, [62, 65, 69, 72]), (46, [62, 65, 70, 74]), (48, [64, 67, 72, 76]),
            (45, [64, 69, 72, 76])]
    kicks = []
    for k in range(nb):
        t = k * b
        bar = k // 4
        root, ch = prog[bar % 4]
        post = t >= drop_t
        if post or k % 2 == 0:
            kicks.append(t)
            mx.add(kick("house"), t, 0.85 if post else 0.5, 0, "drums")
        if post:
            mx.add(hat(True), t + b / 2, 0.2, 0.3, "drums")
            if k % 2:
                mx.add(clap(), t, 0.35, 0, "drums")
            mx.add(sub(root - 24, 0.4 * b), t + b / 2, 0.5, 0, "bass")
        for s in range(4):
            m = ch[(k * 4 + s) % 4] + 12
            cut = 600 + 2600 * min(1, t / drop_t) if not post else 4200
            mx.add(pluck(m, b / 4 * 0.8, cut), t + s * b / 4, 0.16, 0.3 * (1 if s % 2 else -1), "arp")
        if k % 4 == 0:
            mx.add(supersaw(ch, 4 * b, 900 if not post else 3000, 0.5, 0.8, 7, 0.012), t, 0.3, 0,
                   "pad")
    mx.add(riser(2.6), drop_t - 2.6, 0.7, 0, "fx")
    mx.add(impact(), drop_t, 0.6, 0, "fx")
    sonic_logo(mx, logo_t, 74)
    e = duck_env(mx.n, kicks, 0.6, 0.14)
    mx.buses["pad"] *= e
    mx.buses["arp"] = apply_delay(mx.buses["arp"] * e, b * 0.75, 0.35, 0.4)
    finish(mx, path, {"pad": 0.3, "arp": 0.2, "fx": 0.5})


def ticking(dur, path, logo_t, stop_t=11.0):
    """W5 stopwatch: clock ticks, pulsing low synth, stop hit."""
    mx = Mix(dur)
    b, nb = grid(120, dur)
    for k in range(nb):
        t = k * b
        if t >= stop_t:
            break
        mx.add(tick(), t, 0.5, 0.2, "fx")
        mx.add(tick(), t + b / 2, 0.25, -0.2, "fx")
        mx.add(kick("techno"), t, 0.55 + 0.3 * (t / stop_t), 0, "drums")
        for s in range(4):
            mx.add(saw(hz(38), ns(b / 4 * 0.6)) * adsr(ns(b / 4 * 0.6), 0.002, 0.05, 0.6, 0.02) * 0.3,
                   t + s * b / 4, 1.0, 0, "bass")
    mx.buses["bass"] = np.stack([lp(mx.buses["bass"][c], 700) for c in range(2)])
    mx.add(supersaw([50, 57, 62, 65], stop_t, 1200, 2.0, 0.3, 5, 0.008), 0, 0.3, 0, "pad")
    mx.add(riser(3.0), stop_t - 3.0, 0.5, 0, "fx")
    mx.add(impact(), stop_t, 0.7, 0, "fx")
    for i, m in enumerate([74, 78, 81, 86]):
        mx.add(bell(m, 1.0), stop_t + 0.05 + i * 0.08, 0.15, 0.2 * (i - 1.5), "fx")
    mx.add(supersaw([50, 57, 62, 66, 69], dur - stop_t, 3000, 0.05, 1.5, 7, 0.01), stop_t, 0.35, 0,
           "pad")
    sonic_logo(mx, logo_t, 74)
    finish(mx, path, {"pad": 0.35, "fx": 0.4})


def disco(dur, path, logo_t):
    """W6 challenge: disco house, octave bass, string stabs, claps."""
    mx = Mix(dur)
    b, nb = grid(118, dur)
    prog = [(52, [64, 68, 71, 76]), (49, [64, 68, 73, 76]), (45, [64, 69, 73, 76]),
            (47, [63, 66, 71, 75])]
    kicks = []
    for k in range(nb):
        t = k * b
        root, ch = prog[(k // 4) % 4]
        kicks.append(t)
        mx.add(kick("house"), t, 0.8, 0, "drums")
        mx.add(hat(True), t + b / 2, 0.22, 0.3, "drums")
        mx.add(hat(False), t + b / 4, 0.08, -0.3, "drums")
        mx.add(hat(False), t + 3 * b / 4, 0.08, -0.3, "drums")
        if k % 2:
            mx.add(clap(), t, 0.4, 0, "drums")
        mx.add(pluck(root - 12, b / 2 * 0.7, 900), t, 0.5, 0, "bass")
        mx.add(pluck(root, b / 2 * 0.6, 1400), t + b / 2, 0.4, 0, "bass")
        if k % 4 in (1, 3):
            for m in ch:
                mx.add(supersaw([m], b * 0.3, 4500, 0.005, 0.1, 5, 0.01), t + b / 2, 0.22, 0.2, "keys")
        if k % 8 == 0:
            mx.add(rhodes(ch[3] + 12, 2 * b), t, 0.12, -0.2, "keys")
    sonic_logo(mx, logo_t, 76)
    e = duck_env(mx.n, kicks, 0.5, 0.12)
    mx.buses["keys"] *= e
    finish(mx, path, {"keys": 0.3, "fx": 0.5, "drums": 0.05})


def glitch(dur, path, logo_t):
    """W7 watch: glitchy IDM, stutters, crushed plucks, sub pulses."""
    mx = Mix(dur)
    b, nb = grid(96, dur)
    rng = np.random.default_rng(42)
    notes = [62, 65, 69, 72, 74, 77]
    for k in range(nb):
        t = k * b
        mx.add(kick("soft"), t, 0.6 if k % 2 == 0 else 0.3, 0, "drums")
        if k % 2 == 1:
            mx.add(snare("tight"), t, 0.35, 0, "drums")
        for s in range(8):
            if rng.random() < 0.6:
                mx.add(rim(), t + s * b / 8, 0.08 + 0.08 * rng.random(), rng.uniform(-0.6, 0.6), "drums")
            if rng.random() < 0.5:
                m = notes[rng.integers(0, len(notes))] + 12 * rng.integers(0, 2)
                mx.add(pluck(m, b / 8 * 0.5, 5000), t + s * b / 8, 0.18, rng.uniform(-0.5, 0.5), "keys")
        if k % 4 == 3:
            st = t + b * 0.5
            for r in range(6):
                mx.add(hat(False, 1.5), st + r * b / 12, 0.12, 0, "drums")
        if k % 4 == 0:
            mx.add(supersaw([50, 57, 62], 4 * b, 1000, 1.0, 1.0, 5, 0.006), t, 0.3, 0, "pad")
            mx.add(sub(38, 3.5 * b), t, 0.45, 0, "bass")
    mx.buses["keys"] = bitcrush(mx.buses["keys"], 12)
    sonic_logo(mx, logo_t, 74)
    finish(mx, path, {"keys": 0.25, "pad": 0.4, "fx": 0.5})


def jazz_swing(dur, path, logo_t):
    """W8 quiz: swing jazz, walking bass, ride, brushes, Rhodes comping."""
    mx = Mix(dur)
    b, nb = grid(150, dur)
    sw = b * 0.66
    prog = [(50, [65, 69, 72, 76]), (55, [65, 69, 71, 76]), (48, [64, 67, 71, 74]),
            (57, [61, 67, 70, 76])]
    walk = {50: [38, 41, 45, 46], 55: [43, 47, 50, 49], 48: [36, 40, 43, 44], 57: [45, 49, 52, 51]}
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = prog[bar % 4]
        for k, m in enumerate(walk[root]):
            mx.add(pluck(m, b * 0.9, 700), t0 + k * b, 0.55, 0, "bass")
        for k in range(4):
            mx.add(ride(), t0 + k * b, 0.2, 0.35, "drums")
            if k % 2 == 1:
                mx.add(ride(), t0 + k * b + sw, 0.12, 0.35, "drums")
                mx.add(swish(), t0 + k * b, 0.35, -0.2, "drums")
        for st in (1.66, 3.0):
            for m in ch:
                mx.add(rhodes(m, b * 0.5), t0 + st * b, 0.07, 0.15, "keys")
        if bar % 2 == 0:
            mx.add(kick("soft"), t0, 0.3, 0, "drums")
    sonic_logo(mx, logo_t, 74)
    finish(mx, path, {"keys": 0.35, "drums": 0.15, "fx": 0.5})


def dembow(dur, path, logo_t):
    """W9 your city: dembow groove, plucked synth, bouncy sub."""
    mx = Mix(dur)
    b, nb = grid(96, dur)
    prog = [(45, [69, 72, 76]), (41, [69, 72, 77]), (48, [67, 72, 76]), (43, [67, 71, 74])]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = prog[bar % 4]
        for k in range(4):
            t = t0 + k * b
            mx.add(kick("house"), t, 0.75, 0, "drums")
            mx.add(snare("tight"), t + 0.75 * b, 0.4, 0.05, "drums")
            mx.add(snare("tight"), t + 1.5 * b if k % 2 == 0 else t + 0.75 * b + 0.001, 0.0, 0,
                   "drums")
            mx.add(rim(), t + 0.5 * b, 0.15, -0.3, "drums")
            mx.add(hat(False), t + 0.25 * b, 0.1, 0.3, "drums")
            mx.add(hat(False), t + 0.75 * b, 0.1, 0.3, "drums")
        for i, st in enumerate((0, 0.75, 1.5, 2.25, 3.0, 3.5)):
            mx.add(pluck(ch[i % 3] + 12, b * 0.25, 3000), t0 + st * b, 0.25, 0.25 * (i % 2 * 2 - 1),
                   "keys")
        mx.add(bass808(root - 24, 1.4 * b), t0, 0.5, 0, "bass")
        mx.add(bass808(root - 24 + 7, 0.8 * b), t0 + 2.5 * b, 0.45, 0, "bass")
    sonic_logo(mx, logo_t, 76)
    finish(mx, path, {"keys": 0.25, "fx": 0.5, "drums": 0.05})


def boom_bap(dur, path, logo_t):
    """W10 receipt: dusty boom bap, piano chops, vinyl."""
    mx = Mix(dur)
    b, nb = grid(90, dur)
    prog = [(45, [57, 60, 64, 67]), (50, [57, 62, 65, 69]), (43, [55, 59, 62, 65]),
            (48, [55, 60, 64, 67])]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = prog[bar % 4]
        for kb in (0, 0.75, 2.5):
            mx.add(kick("soft"), t0 + kb * b, 0.75, 0, "drums")
        for sb in (1, 3):
            mx.add(snare("lofi"), t0 + sb * b, 0.6, 0, "drums")
        for e in range(8):
            mx.add(hat(False, 0.7), t0 + e * b / 2 + (0.05 if e % 2 else 0), 0.12, 0.3, "drums")
        for i, st in enumerate((0, 1.5, 2.0, 3.25)):
            for m in ch:
                mx.add(piano(m + 12, b * 0.4, 0.5), t0 + st * b, 0.08, 0.15, "keys")
        mx.add(sub(root - 12, 1.9 * b), t0, 0.45, 0, "bass")
        mx.add(sub(root - 12 + 5, 1.4 * b), t0 + 2.5 * b, 0.4, 0, "bass")
    mx.add(crackle(dur + 1), 0, 0.45, 0, "fx")
    sonic_logo(mx, logo_t, 69)
    finish(mx, path, {"keys": 0.25, "drums": 0.06, "fx": 0.35}, master_lp=9000)


SONGS = {
    "chill_pop": chill_pop, "chiptune": chiptune, "trap": trap, "progressive": progressive,
    "ticking": ticking, "disco": disco, "glitch": glitch, "jazz_swing": jazz_swing,
    "dembow": dembow, "boom_bap": boom_bap,
}
