#!/usr/bin/env python3
"""Render wave-3 scenes: soundtrack + sound effects, then 4K video."""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audio_w3  # noqa: E402
from engine import render  # noqa: E402
from scenes_w3 import SCENES_W3  # noqa: E402
from sfx import add_sfx  # noqa: E402

OUT = os.path.join(HERE, "out3")
os.makedirs(OUT, exist_ok=True)

for idx in map(int, sys.argv[1:]):
    t0 = time.time()
    sc = SCENES_W3[idx]()
    music = os.path.join(OUT, f"{sc.name}_music.wav")
    audio_w3.SONGS[sc.song](sc.duration, music, sc.end_t + 0.45)
    wav = os.path.join(OUT, f"{sc.name}.wav")
    add_sfx(music, getattr(sc, "sfx", []), wav)
    mp4 = os.path.join(OUT, f"traceo-{sc.name}.mp4")
    rc = render(sc, mp4, wav)
    print(f"{sc.name}: rc={rc} {time.time() - t0:.0f}s", flush=True)
