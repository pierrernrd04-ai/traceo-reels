#!/usr/bin/env python3
"""Wave 3 soundtracks, built on the audio10 instruments."""
from audio10 import (Mix, adsr, clap, finish, grid, hat, kick, ns, rhodes, rim, shaker, sonic_logo,
                     sub, supersaw)


def garage(dur, path, logo_t, ups=(3.0, 6.0, 9.0)):
    """W3 levels: 2-step UK garage, skippy kick, rim shots, Rhodes stabs, sub; lifts on each level."""
    mx = Mix(dur)
    b, nb = grid(132, dur)
    prog = [(45, [57, 60, 64, 67]), (41, [57, 60, 65, 69]), (43, [59, 62, 67, 71]), (40, [55, 59, 64, 67])]
    for bar in range(nb // 4 + 1):
        t0 = bar * 4 * b
        if t0 > dur:
            break
        root, ch = prog[bar % 4]
        for k in (0, 2.5):
            mx.add(kick("soft"), t0 + k * b, 0.6, 0, "drums")
        for k in (1, 3):
            mx.add(clap(), t0 + k * b, 0.3, 0.1, "drums")
        for e in range(8):
            sw = 0.04 if e % 2 else 0.0
            mx.add(hat(e % 4 == 2, 0.8), t0 + e * b / 2 + sw, 0.14, 0.3, "drums")
        for s in (0.75, 1.75, 3.25):
            mx.add(rim(), t0 + s * b, 0.18, -0.3, "drums")
        mx.add(shaker(), t0 + 3.5 * b, 0.12, 0.4, "drums")
        for s in (0, 1.5, 2.75):
            for m in ch:
                mx.add(rhodes(m, 0.35 * b), t0 + s * b, 0.1, -0.1, "keys")
        mx.add(sub(root - 12, 1.2 * b), t0, 0.5, 0, "bass")
        mx.add(sub(root - 12, 0.6 * b), t0 + 2.5 * b, 0.45, 0, "bass")
    for i, t in enumerate(ups):
        mx.add(supersaw([69 + 2 * i, 73 + 2 * i, 76 + 2 * i], 0.9, 2600, 0.02, 0.6), t, 0.12, 0, "pad")
    sonic_logo(mx, logo_t, 69)
    finish(mx, path, {"keys": 0.35, "pad": 0.4, "fx": 0.5})


SONGS = {"garage": garage}
