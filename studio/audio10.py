#!/usr/bin/env python3
"""Ten original soundtracks for the Traceo Reels, synthesised in numpy and mastered with ffmpeg.

Every sound is generated here, so the music is royalty-free by construction.
"""
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
RNG = np.random.default_rng(7)


# ------------------------------------------------------------------ basics
def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(n):
    return np.arange(n) / SR


def ns(d):
    return max(1, int(d * SR))


def _sos(kind, f, order=2):
    if kind == "band":
        lo, hi = f
        return butter(order, [lo / (SR / 2), min(hi / (SR / 2), 0.99)], "band", output="sos")
    return butter(order, min(f / (SR / 2), 0.99), kind, output="sos")


def lp(x, f, order=2):
    return sosfilt(_sos("low", f, order), x)


def hp(x, f, order=2):
    return sosfilt(_sos("high", f, order), x)


def bp(x, lo, hi, order=2):
    return sosfilt(_sos("band", (lo, hi), order), x)


def adsr(n, a=0.005, d=0.1, s=0.7, r=0.15, gate=None):
    t = tt(n)
    g = gate if gate is not None else max(n / SR - r, a)
    e = np.where(t < a, t / max(a, 1e-5), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4) * 3))
    e = np.where(t > g, e * np.exp(-(t - g) / max(r, 1e-4) * 4), e)
    return e


def saw(f, n, ph=0.0):
    return 2 * ((f * tt(n) + ph) % 1.0) - 1


def sq(f, n, ph=0.0, pw=0.5):
    return np.where(((f * tt(n) + ph) % 1.0) < pw, 1.0, -1.0)


def sine(f, n, ph=0.0):
    return np.sin(2 * np.pi * (f * tt(n) + ph))


def noise(n):
    return RNG.standard_normal(n)


# ------------------------------------------------------------------ drums
def kick(style="house"):
    p = {"house": (150, 48, 26, 5.5, 0.45), "dnb": (190, 52, 40, 9, 0.30),
         "808": (110, 41, 18, 1.6, 1.1), "soft": (120, 50, 22, 7, 0.4),
         "techno": (170, 46, 30, 4.5, 0.5), "cine": (90, 38, 12, 3.2, 0.9)}[style]
    f0, f1, sweep, dec, dur = p
    n = ns(dur)
    t = tt(n)
    f = f1 + (f0 - f1) * np.exp(-t * sweep)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * dec)
    click = hp(noise(n), 2500) * np.exp(-t * 600) * 0.35
    out = np.tanh((body + click) * (2.2 if style in ("techno", "808") else 1.4))
    return out


def snare(style="tight"):
    n = ns(0.45)
    t = tt(n)
    tone = 185 if style != "lofi" else 160
    body = (np.sin(2 * np.pi * tone * t) + 0.5 * np.sin(2 * np.pi * tone * 1.6 * t)) * np.exp(-t * 28)
    nz = bp(noise(n), 1500, 9000) * np.exp(-t * (14 if style != "gated" else 6))
    s = 0.55 * body + 0.7 * nz
    if style == "gated":
        s *= np.where(t < 0.22, 1.0, np.exp(-(t - 0.22) * 60))
    if style == "lofi":
        s = lp(s, 4500)
    return s


def clap():
    n = ns(0.4)
    t = tt(n)
    env = sum(np.where(t >= o, np.exp(-(t - o) * 120), 0) for o in (0, 0.009, 0.018, 0.027))
    env += np.where(t >= 0.027, np.exp(-(t - 0.027) * 16), 0) * 0.7
    return bp(noise(n), 900, 6000) * env * 0.8


_METAL = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)


def hat(open_=False, bright=1.0):
    n = ns(0.5 if open_ else 0.09)
    t = tt(n)
    m = sum(sq(f * 2.6 * bright, n) for f in _METAL) / 6
    s = hp(m + 0.6 * noise(n), 7000, 3)
    return s * np.exp(-t * (9 if open_ else 70)) * 0.45


def shaker():
    n = ns(0.12)
    t = tt(n)
    env = np.minimum(t / 0.02, 1) * np.exp(-t * 35)
    return hp(noise(n), 5000, 2) * env * 0.35


def rim():
    n = ns(0.08)
    t = tt(n)
    return (np.sin(2 * np.pi * 1700 * t) * 0.6 + bp(noise(n), 2000, 6000) * 0.5) * np.exp(-t * 90)


def conga(m=62):
    n = ns(0.35)
    t = tt(n)
    f = hz(m) * (1 + 0.18 * np.exp(-t * 40))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)
            + bp(noise(n), 800, 3000) * np.exp(-t * 80) * 0.3)


def tom(m=40, dec=4.0):
    n = ns(1.4)
    t = tt(n)
    f = hz(m) * (1 + 0.35 * np.exp(-t * 18))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * dec)
    return np.tanh(1.6 * (s + lp(noise(n), 900) * np.exp(-t * 25) * 0.5))


# ------------------------------------------------------------------ tonal
def fm(m, dur, ratio=1.0, index=2.0, idec=4.0, adec=2.0, att=0.003):
    n = ns(dur + 1.2)
    t = tt(n)
    f = hz(m)
    I = index * np.exp(-t * idec) + 0.15
    s = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * ratio * t))
    env = np.minimum(t / att, 1) * np.exp(-t * adec)
    env *= np.where(t > dur, np.exp(-(t - dur) * 8), 1)
    return s * env


def rhodes(m, dur):
    t = tt(ns(dur + 1.2))
    trem = 1 + 0.1 * np.sin(2 * np.pi * 4.8 * t)
    return fm(m, dur, 1.0, 2.2, 5, 1.4) * trem + 0.25 * fm(m + 12, dur, 1.0, 0.8, 8, 3)


def marimba(m, dur=0.35):
    return fm(m, dur, 4.0, 1.6, 30, 7) * 0.9 + 0.3 * fm(m, dur, 1.0, 0.2, 5, 6)


def bell(m, dur=1.6):
    return fm(m, dur, 3.5, 3.0, 2.5, 1.6)


def piano(m, dur, vel=0.8):
    n = ns(dur + 2.5)
    t = tt(n)
    f = hz(m)
    s = np.zeros(n)
    for k in range(1, 9):
        fk = k * f * np.sqrt(1 + 0.0004 * k * k)
        if fk > SR / 2.2:
            break
        s += np.sin(2 * np.pi * fk * t) * (1 / k ** 1.4) * np.exp(-t * (0.9 + 0.7 * k))
    ham = lp(noise(n), 1800) * np.exp(-t * 60) * 0.15
    env = np.where(t > dur, np.exp(-(t - dur) * 5), 1)
    return lp((s + ham) * env * vel, 3200)


def supersaw(ms, dur, cut=2200, att=0.6, rel=1.0, voices=5, det=0.011):
    n = ns(dur + rel)
    s = np.zeros(n)
    for m in ms:
        for v in range(voices):
            d = (v - (voices - 1) / 2) / ((voices - 1) / 2) * det
            s += saw(hz(m) * (1 + d), n, RNG.random())
    s = lp(lp(s, cut), cut) / (voices * len(ms))
    return s * adsr(n, att, 0.6, 0.85, rel, dur)


def sub(m, dur, glide_from=None):
    n = ns(dur + 0.05)
    t = tt(n)
    f = np.full(n, hz(m))
    if glide_from is not None:
        f = hz(m) + (hz(glide_from) - hz(m)) * np.exp(-t * 25)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return s * adsr(n, 0.004, 0.2, 0.9, 0.04, dur)


def bass808(m, dur, glide_from=None):
    return np.tanh(2.5 * sub(m, dur, glide_from)) * 0.8


def reese(m, dur, cut=900):
    n = ns(dur + 0.05)
    s = saw(hz(m) * 0.995, n) + saw(hz(m) * 1.005, n) + 0.6 * sine(hz(m) / 2, n)
    return lp(s, cut, 4) * adsr(n, 0.01, 0.2, 0.85, 0.05, dur) * 0.5


def acid(m, dur, cut=1200):
    n = ns(dur + 0.05)
    s = saw(hz(m), n)
    return lp(s, cut, 4) * adsr(n, 0.002, 0.12, 0.25, 0.04, dur)


def pluck(m, dur=0.25, cut=3500):
    n = ns(dur + 0.4)
    t = tt(n)
    s = saw(hz(m), n) * 0.6 + sq(hz(m) * 1.003, n) * 0.4
    return lp(s, cut, 2) * np.exp(-t * 9)


def lead(m, dur, cut=3000):
    n = ns(dur + 0.2)
    t = tt(n)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(t * 3, 1)
    ph = np.cumsum(hz(m) * vib) / SR
    s = 2 * (ph % 1) - 1 + 0.5 * np.where((ph % 1) < 0.5, 1, -1)
    return lp(s, cut) * adsr(n, 0.01, 0.2, 0.7, 0.15, dur) * 0.5


def riser(dur=2.0):
    n = ns(dur)
    t = tt(n)
    x = noise(n)
    out = np.zeros(n)
    seg = n // 16
    for i in range(16):
        f = 400 * (12 ** (i / 15))
        a, b = i * seg, n if i == 15 else (i + 1) * seg
        out[a:b] = bp(x, f, min(f * 3, 20000))[a:b]
    return out * (t / dur) ** 2 * 0.6


def impact():
    n = ns(2.5)
    t = tt(n)
    boom = np.sin(2 * np.pi * (35 + 60 * np.exp(-t * 8)) * t) * np.exp(-t * 2)
    hit = lp(noise(n), 3000) * np.exp(-t * 6) * 0.4
    return np.tanh(1.5 * (boom + hit))


def whoosh(dur=0.7):
    n = ns(dur)
    t = tt(n)
    env = np.sin(np.pi * t / dur) ** 2
    return bp(noise(n), 600, 5000) * env * 0.5


def crackle(dur):
    n = ns(dur)
    c = np.zeros(n)
    idx = RNG.integers(0, n, int(dur * 25))
    c[idx] = RNG.uniform(-1, 1, len(idx))
    return lp(c, 6000) * 0.6 + lp(noise(n), 3000) * 0.012


# ------------------------------------------------------------------ mixing
class Mix:
    def __init__(self, dur):
        self.n = ns(dur + 3)
        self.dur = dur
        self.buses = {}

    def bus(self, name):
        if name not in self.buses:
            self.buses[name] = np.zeros((2, self.n))
        return self.buses[name]

    def add(self, sig, t, gain=1.0, pan=0.0, bus="main"):
        i = int(t * SR)
        if i >= self.n or t < 0:
            return
        sig = sig[: self.n - i] * gain
        b = self.bus(bus)
        b[0, i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
        b[1, i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def duck_env(n, times, depth=0.65, rel=0.16):
    e = np.ones(n)
    t = tt(n)
    for k in times:
        i = int(k * SR)
        if i < n:
            seg = t[i:] - k
            e[i:] = np.minimum(e[i:], 1 - depth * np.exp(-seg / rel))
    return e


def reverb_ir(secs=2.0, bright=6000):
    n = ns(secs)
    t = tt(n)
    irs = []
    for _ in range(2):
        ir = noise(n) * np.exp(-t * 6.9 / secs)
        irs.append(lp(ir, bright))
    return irs


def apply_reverb(st, secs=2.0, mix=0.25, bright=6000):
    irs = reverb_ir(secs, bright)
    wet = np.stack([fftconvolve(st[c], irs[c])[: st.shape[1]] for c in range(2)])
    wet *= (np.abs(st).max() + 1e-9) / (np.abs(wet).max() + 1e-9)
    return st + wet * mix


def apply_delay(st, time, fb=0.35, mix=0.25):
    d = int(time * SR)
    out = st.copy()
    tap = st.copy()
    for k in range(1, 6):
        shifted = np.zeros_like(st)
        shifted[:, d * k:] = tap[:, : -d * k] if d * k < st.shape[1] else 0
        # ping-pong: alternate channels
        if k % 2:
            shifted = shifted[::-1]
        out += shifted * (fb ** k) * mix / fb
    return out


def sonic_logo(mx, t0, key_m=72):
    """Traceo audio signature: whoosh into a two-note bell as the logo dot appears."""
    mx.add(whoosh(0.7), t0 - 0.35, 0.5, 0.0, "fx")
    mx.add(bell(key_m, 1.4), t0 + 0.35, 0.32, -0.15, "fx")
    mx.add(bell(key_m + 7, 1.6), t0 + 0.55, 0.26, 0.15, "fx")


def finish(mx, path, sends=None, master_lp=None):
    """Sum the buses with reverb sends, write a wav, then master it with ffmpeg."""
    sends = sends or {}
    total = np.zeros((2, mx.n))
    rev_in = np.zeros((2, mx.n))
    for name, b in mx.buses.items():
        total += b
        rev_in += b * sends.get(name, 0.0)
    if np.abs(rev_in).max() > 0:
        wet = apply_reverb(rev_in, 2.4, 1.0) - rev_in
        total += wet * 0.6
    if master_lp:
        total = np.stack([lp(total[c], master_lp) for c in range(2)])
    n = ns(mx.dur)
    total = total[:, :n]
    fo = ns(1.0)
    total[:, -fo:] *= np.linspace(1, 0, fo) ** 1.5
    total[:, :ns(0.005)] *= np.linspace(0, 1, ns(0.005))
    total = total / (np.abs(total).max() + 1e-9) * 0.7
    raw = path.replace(".wav", "_raw.wav")
    pcm = (total.T * 32767).astype(np.int16)
    with wave.open(raw, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    af = ("acompressor=threshold=0.18:ratio=2.5:attack=12:release=180:makeup=1.6,"
          "loudnorm=I=-14:TP=-1.2:LRA=9,alimiter=limit=0.89:level=false")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", str(SR),
                    path], check=True)
    os.remove(raw)


def grid(bpm, dur):
    b = 60 / bpm
    return b, int(dur / b) + 2


# ------------------------------------------------------------------ songs
def deep_house(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(122, dur)
    prog = [(57, [69, 72, 76, 79, 83]), (53, [69, 72, 76, 79]), (48, [67, 71, 76, 79]),
            (55, [67, 71, 74, 76])]
    kicks = []
    for k in range(nb):
        t = k * b
        bar = k // 4
        root, ch = prog[bar % 4]
        kicks.append(t)
        mx.add(kick("house"), t, 0.85, 0, "drums")
        if k % 2 == 1:
            mx.add(clap(), t, 0.4, 0.05, "drums")
        mx.add(hat(True), t + b / 2, 0.22, 0.25, "drums")
        for s in range(4):
            mx.add(shaker(), t + s * b / 4, 0.18 if s % 2 else 0.1, -0.35, "drums")
        mx.add(sub(root - 24, b * 0.42), t + b / 2, 0.55, 0, "bass")
        if k % 4 in (1, 3) or (k % 8 == 6):
            st = t + (b * 0.75 if k % 2 else b * 0.5)
            for m in ch:
                mx.add(rhodes(m - 12, b * 0.35), st, 0.07, 0.2, "keys")
        if k % 4 == 0:
            mx.add(supersaw(ch[:3], 4 * b, 1600, 0.4, 0.8), t, 0.35, 0, "pad")
    sonic_logo(mx, logo_t, 72)
    n = mx.n
    e = duck_env(n, kicks, 0.7, 0.14)
    for name in ("pad", "keys", "bass"):
        mx.buses[name] *= e
    finish(mx, path, {"keys": 0.35, "pad": 0.3, "drums": 0.06, "fx": 0.5})


def liquid_dnb(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(174, dur)
    chords = [(53, [64, 69, 72, 76]), (52, [62, 67, 71, 74]), (50, [60, 65, 69, 72]),
              (48, [59, 64, 67, 71])]
    kicks = []
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = chords[bar % 4]
        for kb in (0, 2.5):
            kicks.append(t0 + kb * b)
            mx.add(kick("dnb"), t0 + kb * b, 0.9, 0, "drums")
        for sb in (1, 3):
            mx.add(snare("tight"), t0 + sb * b, 0.55, 0.03, "drums")
        for e8 in range(8):
            mx.add(hat(False, 1.2), t0 + e8 * b / 2 + (0.02 if e8 % 2 else 0), 0.16 if e8 % 2 else 0.24,
                   0.3, "drums")
        mx.add(shaker(), t0 + 3.75 * b, 0.25, -0.3, "drums")
        mx.add(reese(root - 24, 2.5 * b, 700), t0, 0.5, 0, "bass")
        mx.add(reese(root - 24 + 3, 1.4 * b, 700), t0 + 2.5 * b, 0.45, 0, "bass")
        mx.add(supersaw(ch, 4 * b, 2600, 0.15, 0.6, 5, 0.008), t0, 0.32, 0, "pad")
        for i, m in enumerate([ch[3] + 12, ch[2] + 12, ch[1] + 12, ch[2] + 12]):
            mx.add(piano(m, b * 0.9, 0.6), t0 + i * b, 0.16, 0.25 if i % 2 else -0.25, "keys")
    sonic_logo(mx, logo_t, 76)
    e = duck_env(mx.n, kicks, 0.5, 0.1)
    mx.buses["pad"] *= e
    finish(mx, path, {"keys": 0.45, "pad": 0.3, "drums": 0.05, "fx": 0.5})


def cine_pulse(dur, path, logo_t, hit_t=8.0):
    mx = Mix(dur)
    b, nb = grid(70, dur)
    for k in range(nb):
        t = k * b
        mx.add(kick("cine"), t, 0.7, 0, "drums")
        mx.add(kick("soft"), t + b * 0.28, 0.35, 0, "drums")
        for s in range(4):
            mx.add(rim(), t + s * b / 4, 0.06 if s else 0.1, 0.4, "drums")
    mx.add(supersaw([38, 45, 50], hit_t + 0.2, 900, 1.5, 0.5, 5, 0.006), 0, 0.5, 0, "pad")
    mx.add(riser(2.4), hit_t - 2.4, 0.7, 0, "fx")
    mx.add(impact(), hit_t, 0.9, 0, "fx")
    mx.add(supersaw([50, 57, 62, 65, 69], dur - hit_t, 2400, 0.3, 1.5, 7, 0.01), hit_t, 0.45, 0,
           "pad")
    for i, m in enumerate([74, 77, 81, 79, 77, 74, 72, 74]):
        t = hit_t + 0.4 + i * b / 2
        if t < dur - 2.5:
            mx.add(piano(m, b, 0.7), t, 0.2, 0.2 if i % 2 else -0.2, "keys")
    sonic_logo(mx, logo_t, 74)
    finish(mx, path, {"pad": 0.4, "keys": 0.55, "fx": 0.6, "drums": 0.15})


def uk_garage(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(132, dur)
    sw = 0.17 * b
    chords = [(51, [67, 70, 74, 77]), (48, [67, 70, 72, 75]), (53, [69, 72, 75, 77]),
              (46, [65, 69, 72, 74])]
    kicks = []
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = chords[bar % 4]
        for kb in (0, 1.75, 2.5):
            kicks.append(t0 + kb * b)
            mx.add(kick("house"), t0 + kb * b, 0.75 if kb else 0.85, 0, "drums")
        for sb in (1, 3):
            mx.add(snare("tight"), t0 + sb * b, 0.45, 0.04, "drums")
            mx.add(clap(), t0 + sb * b, 0.25, -0.05, "drums")
        for e8 in range(8):
            t = t0 + e8 * b / 2 + (sw if e8 % 2 else 0)
            mx.add(hat(False, 1.1), t, 0.2 if e8 % 2 else 0.12, 0.3, "drums")
        mx.add(hat(True), t0 + 3.5 * b + sw, 0.15, 0.3, "drums")
        for st in (0.5, 1.5 + 0.17, 3.0):
            for m in ch:
                mx.add(fm(m, b * 0.22, 2.0, 1.5, 12, 6), t0 + st * b, 0.06, 0.15, "keys")
        mx.add(sub(root - 24, 1.4 * b, root - 12), t0, 0.6, 0, "bass")
        mx.add(sub(root - 24 + 7, 0.8 * b), t0 + 2.5 * b, 0.5, 0, "bass")
        mx.add(supersaw(ch[:3], 4 * b, 1500, 0.5, 0.6), t0, 0.22, 0, "pad")
    sonic_logo(mx, logo_t, 74)
    e = duck_env(mx.n, kicks, 0.55, 0.12)
    mx.buses["pad"] *= e
    mx.buses["keys"] *= e
    finish(mx, path, {"keys": 0.35, "pad": 0.25, "drums": 0.05, "fx": 0.5})


def minimal_techno(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(126, dur)
    seq = [45, 45, 57, 45, 48, 45, 55, 52, 45, 45, 57, 45, 50, 45, 52, 55]
    kicks = []
    for k in range(nb):
        t = k * b
        kicks.append(t)
        mx.add(kick("techno"), t, 0.9, 0, "drums")
        mx.add(lp(kick("techno"), 180) * 0.6, t + b / 2, 0.35, 0, "rumble")
        mx.add(hat(True, 0.9), t + b / 2, 0.18, 0.3, "drums")
        mx.add(hat(False), t + 3 * b / 4, 0.1, -0.3, "drums")
        if k % 2 == 1:
            mx.add(clap(), t, 0.25, 0.1, "drums")
        if k % 4 == 3:
            mx.add(rim(), t + b * 0.25, 0.12, 0.5, "drums")
        for s in range(4):
            i = (k * 4 + s) % 16
            cut = 500 + 1800 * (0.5 + 0.5 * np.sin(2 * np.pi * (k * 4 + s) / 64))
            mx.add(acid(seq[i], b / 4 * 0.7, cut), t + s * b / 4, 0.3, 0.1 * (1 if s % 2 else -1),
                   "synth")
    sonic_logo(mx, logo_t, 69)
    e = duck_env(mx.n, kicks, 0.6, 0.12)
    mx.buses["synth"] *= e
    mx.buses["rumble"] = apply_reverb(mx.buses["rumble"], 1.2, 0.8, 300)
    finish(mx, path, {"synth": 0.25, "drums": 0.05, "fx": 0.5})


def synthwave(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(100, dur)
    chords = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]
    mel = [76, 74, 72, 74, 76, 79, 76, 74]
    kicks = []
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = chords[bar % 4]
        for k in range(4):
            kicks.append(t0 + k * b)
            mx.add(kick("soft"), t0 + k * b, 0.8, 0, "drums")
            mx.add(hat(False), t0 + k * b + b / 2, 0.14, 0.3, "drums")
        for sb in (1, 3):
            mx.add(snare("gated"), t0 + sb * b, 0.5, 0, "snare")
        for e8 in range(8):
            mx.add(acid(root - 12, b / 2 * 0.8, 900), t0 + e8 * b / 2, 0.42, 0, "bass")
        mx.add(supersaw(ch, 4 * b, 3000, 0.3, 0.8, 7, 0.012), t0, 0.35, 0, "pad")
        if bar % 2 == 1:
            for i, m in enumerate(mel):
                mx.add(lead(m, b * 0.45, 2600), t0 + i * b / 2, 0.16, 0.1, "lead")
    sonic_logo(mx, logo_t, 76)
    mx.buses["snare"] = apply_reverb(mx.buses["snare"], 1.8, 0.6)
    mx.buses["lead"] = apply_delay(mx.buses["lead"], b * 0.75, 0.4, 0.5)
    e = duck_env(mx.n, kicks, 0.45, 0.15)
    mx.buses["pad"] *= e
    finish(mx, path, {"pad": 0.3, "lead": 0.3, "fx": 0.5})


def lofi(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(84, dur)
    sw = 0.2 * b
    chords = [(50, [65, 69, 72, 76]), (55, [65, 69, 71, 76]), (48, [64, 67, 71, 74]),
              (57, [64, 67, 70, 73])]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = chords[bar % 4]
        for kb in (0, 1.75 + 0.2, 2.5):
            mx.add(kick("soft"), t0 + kb * b, 0.7, 0, "drums")
        for sb in (1, 3):
            mx.add(snare("lofi"), t0 + sb * b + 0.012, 0.45, 0.05, "drums")
        for e8 in range(8):
            mx.add(hat(False, 0.8), t0 + e8 * b / 2 + (sw if e8 % 2 else 0), 0.12 if e8 % 2 else 0.08,
                   0.3, "drums")
        for i, m in enumerate(ch):
            mx.add(rhodes(m, 3.2 * b), t0 + i * 0.025, 0.12, 0.2 * (i - 1.5), "keys")
        mx.add(sub(root - 24, 1.8 * b), t0, 0.5, 0, "bass")
        mx.add(sub(root - 24 + 7, 1.5 * b), t0 + 2.5 * b, 0.4, 0, "bass")
    mx.add(crackle(dur + 1), 0, 0.5, 0, "fx")
    sonic_logo(mx, logo_t, 69)
    finish(mx, path, {"keys": 0.3, "drums": 0.08, "fx": 0.3}, master_lp=7500)


def ambient_piano(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(72, dur)
    chords = [(49, [61, 65, 68, 72]), (46, [58, 61, 65, 68]), (42, [61, 65, 66, 70]),
              (44, [60, 63, 65, 68])]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        root, ch = chords[bar % 4]
        mx.add(piano(root - 12, 4 * b, 0.6), t0, 0.35, -0.1, "keys")
        arp = [ch[0], ch[2], ch[3] + 12, ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[1] + 12, ch[2]]
        for i, m in enumerate(arp):
            mx.add(piano(m, b, 0.45 + 0.1 * (i == 2)), t0 + i * b / 2, 0.22, 0.3 * np.sin(i), "keys")
        mx.add(supersaw([root, root + 7, root + 12], 4 * b, 1100, 1.2, 1.5, 5, 0.006), t0, 0.28, 0,
               "pad")
    sonic_logo(mx, logo_t, 73)
    finish(mx, path, {"keys": 0.55, "pad": 0.5, "fx": 0.6})


def afro_house(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(120, dur)
    riff = [67, 70, 72, 74, 72, 70, 67, 65]
    kicks = []
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        for k in range(4):
            kicks.append(t0 + k * b)
            mx.add(kick("house"), t0 + k * b, 0.8, 0, "drums")
            mx.add(shaker(), t0 + k * b + b / 4, 0.2, -0.3, "drums")
            mx.add(shaker(), t0 + k * b + 3 * b / 4, 0.2, -0.3, "drums")
        for sb in (1, 3):
            mx.add(clap(), t0 + sb * b, 0.32, 0.1, "drums")
        for pos, m, pan in ((0.75, 62, 0.4), (1.5, 67, -0.4), (2.25, 62, 0.4), (2.75, 64, 0.4),
                            (3.5, 67, -0.4)):
            mx.add(conga(m), t0 + pos * b, 0.35, pan, "perc")
        for i, m in enumerate(riff):
            if i % 3 != 2:
                mx.add(marimba(m, 0.3), t0 + i * b / 2 + (b / 4 if i % 2 else 0), 0.3, 0.2, "keys")
        for pos, m in ((0.5, 43), (1.75, 43), (2.5, 46), (3.25, 41)):
            mx.add(sub(m - 12, 0.4 * b), t0 + pos * b, 0.55, 0, "bass")
        mx.add(supersaw([55, 58, 62], 4 * b, 1300, 0.5, 0.6), t0, 0.22, 0, "pad")
    sonic_logo(mx, logo_t, 74)
    e = duck_env(mx.n, kicks, 0.55, 0.13)
    mx.buses["pad"] *= e
    mx.buses["bass"] *= e
    finish(mx, path, {"keys": 0.3, "perc": 0.15, "pad": 0.3, "drums": 0.05, "fx": 0.5})


def cine_hybrid(dur, path, logo_t):
    mx = Mix(dur)
    b, nb = grid(80, dur)
    chords = [(45, [57, 60, 64, 69]), (41, [57, 60, 65, 69]), (48, [55, 60, 64, 67]),
              (43, [55, 59, 62, 67])]
    build = logo_t
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        if t0 > dur:
            break
        root, ch = chords[bar % 4]
        mx.add(supersaw(ch, 4 * b, 1400 + 400 * bar, 0.8, 1.2, 7, 0.009), t0, 0.35, 0, "pad")
        mx.add(piano(root, 4 * b, 0.6), t0, 0.25, -0.1, "keys")
        for i, m in enumerate([ch[3] + 12, ch[2] + 12, ch[1] + 12, ch[3] + 12]):
            mx.add(piano(m, b, 0.55), t0 + i * b, 0.18, 0.25 * (i % 2 * 2 - 1), "keys")
        if t0 >= 4 * b:
            for k in range(4):
                if t0 + k * b < build:
                    mx.add(tom(36, 3.5), t0 + k * b, 0.5, 0, "drums")
                    if bar >= 2:
                        mx.add(tom(43, 6), t0 + k * b + b / 2, 0.3, 0.2, "drums")
    mx.add(riser(2.5), build - 2.5, 0.6, 0, "fx")
    mx.add(impact(), build - 0.3, 1.0, 0, "fx")
    mx.add(supersaw([45, 52, 57, 60, 64], dur - build + 1, 2600, 0.05, 2.0, 7, 0.01), build - 0.3,
           0.5, 0, "pad")
    sonic_logo(mx, logo_t + 0.4, 69)
    finish(mx, path, {"pad": 0.4, "keys": 0.5, "drums": 0.2, "fx": 0.6})


SONGS = {
    "deep_house": deep_house, "liquid_dnb": liquid_dnb, "cine_pulse": cine_pulse,
    "uk_garage": uk_garage, "minimal_techno": minimal_techno, "synthwave": synthwave,
    "lofi": lofi, "ambient_piano": ambient_piano, "afro_house": afro_house,
    "cine_hybrid": cine_hybrid,
}

if __name__ == "__main__":
    name, dur, logo_t, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    SONGS[name](dur, out, logo_t)
