"""Sound effects layered over a mastered soundtrack (pops, ticks, coins, thuds, printer)."""
import subprocess
import wave

import numpy as np

from audio10 import SR, bell, hp, lp, noise, ns, tt


def _pop():
    n = ns(0.09)
    t = tt(n)
    f = 520 + 520 * (t / 0.09)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45) * 0.8


def _send():
    n = ns(0.18)
    t = tt(n)
    f = 900 - 500 * (t / 0.18)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + hp(noise(n), 3000) * 0.2) * np.exp(-t * 18)


def _type():
    out = np.zeros(ns(0.5))
    for k in range(5):
        i = ns(0.09 * k)
        n = ns(0.02)
        out[i:i + n] += hp(noise(n), 4000) * np.exp(-tt(n) * 300) * 0.25
    return out


def _coin():
    out = np.zeros(ns(0.25))
    for k, f in enumerate((988, 1319)):
        i = ns(0.06 * k)
        n = ns(0.16)
        sq = np.where(((f * tt(n)) % 1) < 0.5, 1.0, -1.0)
        out[i:i + n] += sq * np.exp(-tt(n) * 18) * 0.25
    return out


def _thud():
    n = ns(0.3)
    t = tt(n)
    return (np.sin(2 * np.pi * (70 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 14)
            + lp(noise(n), 1500) * np.exp(-t * 40) * 0.4)


def _tick():
    n = ns(0.03)
    t = tt(n)
    return np.sin(2 * np.pi * 3000 * t) * np.exp(-t * 280) * 0.7


def _ding():
    return bell(84, 0.8) * 0.4


def _swoosh():
    n = ns(0.35)
    t = tt(n)
    return hp(noise(n), 1800) * np.sin(np.pi * t / 0.35) ** 2 * 0.35


def _print():
    out = np.zeros(ns(0.45))
    for k in range(9):
        i = ns(0.05 * k)
        n = ns(0.035)
        out[i:i + n] += lp(hp(noise(n), 800), 5000) * 0.35
    return out


KINDS = {"pop": _pop, "send": _send, "type": _type, "coin": _coin, "thud": _thud, "tick": _tick,
         "ding": _ding, "swoosh": _swoosh, "print": _print}


def add_sfx(wav_in, events, wav_out, gain=0.55):
    """events: list of (time_s, kind). Mixed on top, then limited with ffmpeg."""
    with wave.open(wav_in) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32).reshape(-1, ch) / 32768
    for t, kind in events:
        s = KINDS[kind]() * gain
        i = int(t * sr)
        if i >= len(x):
            continue
        s = s[: len(x) - i]
        x[i:i + len(s), 0] += s
        x[i:i + len(s), 1] += s
    tmp = wav_out.replace(".wav", "_tmp.wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(x * 0.85, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af",
                    "loudnorm=I=-14:TP=-1.2:LRA=9,alimiter=limit=0.89:level=false", "-ar", str(sr),
                    wav_out], check=True)
    import os
    os.remove(tmp)
