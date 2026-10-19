#!/usr/bin/env python3
"""Render the Facebook post: two static JPGs and the animated MP4 with soundtrack."""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image  # noqa: E402

import audio10  # noqa: E402
import fb_post as P  # noqa: E402
from engine import render  # noqa: E402
from sfx import add_sfx  # noqa: E402

OUT = os.path.join(HERE, "outfb")
os.makedirs(OUT, exist_ok=True)
for v, name in (("A", "traceo-facebook-meme-tour"), ("B", "traceo-facebook-boucle-neuve")):
    im = Image.fromarray(P.Post(v, static=True).frame(0))
    im.save(os.path.join(OUT, f"{name}.jpg"), quality=95, subsampling=0)

t0 = time.time()
sc = P.Post("A")
K = sc.k
raw = os.path.join(OUT, "fb_raw.wav")
wav = os.path.join(OUT, "fb.wav")
audio10.SONGS["deep_house"](sc.duration, raw, K["cta"] - 0.2)
ev = [(K["count"] + K["count_d"] * (i / 14) ** 0.6, "tick") for i in range(15)]
ev += [(K["new"], "swoosh"), (K["lbl"], "pop")]
ev += [(K["st"] + 0.22 * i, "pop") for i in range(3)]
add_sfx(raw, ev, wav)
rc = render(sc, os.path.join(OUT, "traceo-facebook-anime.mp4"), wav)
print("video rc", rc, f"{time.time() - t0:.0f}s")
