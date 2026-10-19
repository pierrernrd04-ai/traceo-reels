#!/usr/bin/env python3
"""Render the given scene indices: soundtrack, then 4K video with the audio muxed in."""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audio10  # noqa: E402
from engine import render  # noqa: E402
from scenes10 import SCENES  # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

for idx in map(int, sys.argv[1:]):
    t0 = time.time()
    sc = SCENES[idx]()
    wav = os.path.join(OUT, f"{sc.name}.wav")
    audio10.SONGS[sc.song](sc.duration, wav, sc.end_t + 0.45)
    mp4 = os.path.join(OUT, f"traceo-{sc.name}.mp4")
    rc = render(sc, mp4, wav)
    print(f"{sc.name}: rc={rc} {time.time() - t0:.0f}s", flush=True)
