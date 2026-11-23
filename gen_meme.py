#!/usr/bin/env python3
"""GTA V WANTED poster meme generator — deterministic, no network, no clock.

Renders meme.png (1080x1080) and meme-480.png (480x480) from fixed data.
Run: python3 gen_meme.py

Concept: a Leonida Police Department WANTED poster. The make.fun ghost IS
the mugshot (big, centre, against a police height chart) — the most
GTA-native visual (the 5-star wanted level), a genre no top-50 entry uses.
The punchline lands in one line: the reward for catching GTA V is one copy
of GTA VI — already claimed by my AI agent on make.fun.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1080
PAPER = (244, 234, 211)
INK = (26, 35, 50)
NAVY = (22, 35, 58)
MAGENTA = (214, 0, 109)
RED = (192, 57, 43)
GOLD = (216, 178, 60)
GREY = (110, 110, 105)
CHART_BG = (217, 222, 226)
CHART_LINE = (168, 174, 180)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def draw_star(d, cx, cy, r_out, fill, outline=None, width=1):
    pts = star_points(cx, cy, r_out, r_out * 0.42)
    d.polygon(pts, fill=fill, outline=outline)
    if outline is not None and width > 1:
        d.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def draw_ghost(d, x0, y0, x1, y1, eye_r=13, coin_r=21):
    """make.fun ghost: white body, thick black outline, sparkle eyes,
    round hand holding a magenta coin with a white star. Box (x0,y0,x1,y1)."""
    gw = x1 - x0
    gh = y1 - y0

    def shape(inset, fill):
        a, b, c, e = x0 + inset, y0 + inset, x1 - inset, y1 - inset
        d.ellipse([a, b, c, b + (e - b) * 0.55], fill=fill)
        d.rectangle([a, b + (e - b) * 0.28, c, e - 14], fill=fill)
        n, bw = 3, (c - a) / 3
        depth = max(18, int(bw * 0.35))  # deep bumps: a wide ghost
        for i in range(n):                # must not read as a flat cloud
            cx = a + bw * (i + 0.5)
            d.ellipse([cx - bw / 2, e - 14 - depth, cx + bw / 2,
                       e - 14 + depth], fill=fill)

    shape(0, (0, 0, 0))
    shape(7, (255, 255, 255))

    def sparkle(cx, cy, r):
        pts = [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
               (cx + r * 0.28, cy + r * 0.28), (cx, cy + r),
               (cx - r * 0.28, cy + r * 0.28), (cx - r, cy),
               (cx - r * 0.28, cy - r * 0.28)]
        d.polygon(pts, fill=(0, 0, 0))

    sparkle(x0 + gw * 0.35, y0 + gh * 0.38, eye_r)
    sparkle(x0 + gw * 0.65, y0 + gh * 0.38, eye_r)
    # round little hand holding the coin ON the white body
    hx, hy = x1 - 18, y0 + gh * 0.78
    d.ellipse([hx - 15, hy - 15, hx + 15, hy + 15],
              fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    ccx, ccy = x1 - 46, y0 + gh * 0.76
    d.ellipse([ccx - coin_r, ccy - coin_r, ccx + coin_r, ccy + coin_r],
              fill=MAGENTA, outline=(0, 0, 0), width=4)
    d.polygon(star_points(ccx, ccy, coin_r * 0.72, coin_r * 0.30),
              fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    def text(x, y, s, f, fill=INK, anchor="la"):
        d.text((x, y), s, font=f, fill=fill, anchor=anchor)

    # --- paper inset ---
    d.rectangle([20, 20, W - 20, H - 20], fill=PAPER)

    # --- header ---
    text(W // 2, 44, "LEONIDA POLICE DEPARTMENT",
         font("DejaVuSans-Bold.ttf", 25), anchor="ma")
    text(W // 2, 76, "VICE CITY  \u00b7  EST. 2013",
         font("DejaVuSans.ttf", 18), fill=GREY, anchor="ma")

    # --- WANTED ---
    text(W // 2, 104, "WANTED", font("DejaVuSerif-Bold.ttf", 148),
         anchor="ma")
    # 5 gold stars
    for i in range(5):
        cx = W // 2 + (i - 2) * 86
        draw_star(d, cx, 292, 30, GOLD, outline=(0, 0, 0), width=3)

    # --- mugshot box with police height chart ---
    bx0, by0, bx1, by1 = 150, 330, 930, 640
    d.rectangle([bx0, by0, bx1, by1], fill=CHART_BG, outline=(0, 0, 0),
                width=5)
    labels = [("7 FT", 372), ("6 FT", 432), ("5 FT", 492), ("4 FT", 552),
              ("3 FT", 612)]
    lab_f = font("DejaVuSans-Bold.ttf", 18)
    for lab, ly in labels:
        d.line([(bx0 + 5, ly), (bx1 - 5, ly)], fill=CHART_LINE, width=2)
        d.text((bx0 + 14, ly - 22), lab, font=lab_f, fill=(120, 126, 132))
    # ghost mugshot: 280px wide = ~26% of frame (top-1 benchmark ~25%),
    # nearly square so the bumps read as a ghost, not a flat cloud
    draw_ghost(d, 400, 340, 680, 632, eye_r=16, coin_r=26)

    # --- name plate ---
    text(W // 2, 656, "GRAND THEFT AUTO V",
         font("DejaVuSerif-Bold.ttf", 46), anchor="ma")
    text(W // 2, 712, "ALIAS: \u201cTHE GAME THAT NEVER LEFT\u201d",
         font("DejaVuSans.ttf", 22), fill=GREY, anchor="ma")
    d.line([(90, 748), (W - 90, 748)], fill=INK, width=2)

    # --- charges ---
    ch_f = font("DejaVuSans.ttf", 25)
    cy = 764
    for ln in ("CRIME: 4,811 DAYS OF LOITERING IN LOS SANTOS",
               "ARMED WITH HYPE \u2014 CONSIDERED EXTREMELY DANGEROUS",
               "ACCOMPLICES: JASON & LUCIA \u2014 AT LARGE IN VICE CITY"):
        text(W // 2, cy, ln, ch_f, anchor="ma")
        cy += 33

    # --- reward: the punchline ---
    text(W // 2, 872, "REWARD: ONE (1) COPY OF GRAND THEFT AUTO VI",
         font("DejaVuSans-Bold.ttf", 27), anchor="ma")
    text(W // 2, 906, "ALREADY CLAIMED BY MY AI AGENT ON MAKE.FUN",
         font("DejaVuSans-Bold.ttf", 27), fill=RED, anchor="ma")

    # --- magenta banner (winning template) ---
    d.rectangle([20, 948, W - 20, 1040], fill=MAGENTA)
    draw_ghost(d, 52, 958, 148, 1030, eye_r=8, coin_r=12)
    text(168, 962, "CAUGHT BY MY AI AGENT",
         font("DejaVuSans-Bold.ttf", 33), fill=(255, 255, 255))
    text(168, 1002, "it wins real money in make.fun bounties.",
         font("DejaVuSans.ttf", 21), fill=(255, 255, 255))
    d.rounded_rectangle([836, 966, 1036, 1022], radius=18,
                        fill=(255, 255, 255))
    text(936, 974, "make.fun", font("DejaVuSans-Bold.ttf", 26),
         fill=MAGENTA, anchor="ma")
    # --- footer ---
    text(W // 2, 1046, "FORM W-13 \u00b7 LEONIDA POLICE DEPT. \u00b7 PAGE 1 OF 1",
         font("DejaVuSans.ttf", 14), fill=GREY, anchor="ma")

    img.save("meme.png")
    img.resize((480, 480), Image.LANCZOS).save("meme-480.png")
    print("wrote meme.png + meme-480.png")


if __name__ == "__main__":
    main()
