#!/usr/bin/env python3
"""자막/라벨/엔드카드를 투명 PNG로 렌더링한다 (ffmpeg에 drawtext/subtitles 필터가 없어 PIL로 대체).
출력: build/ov_{16x9|9x16}_sub{NN}.png (내레이션 자막), build/ov_{layout}_deco{NN}.png (씬5 라벨, 씬6 엔드카드)
실행: python3 scripts/make_overlays.py   (시스템 python3 + Pillow, .venv에는 PIL 없음)
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
BOLD, SEMI = 6, 4  # ttc index
OUT = os.path.join(ROOT, "build")
os.makedirs(OUT, exist_ok=True)
sb = json.load(open(os.path.join(ROOT, "storyboard/storyboard.json")))
cam = sb["campaign"]
LAYOUTS = {"16x9": (1920, 1080), "9x16": (1080, 1920)}


def font(size, idx=SEMI):
    return ImageFont.truetype(FONT, size, index=idx)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def centered(d, cx, y, text, f, fill, stroke=0):
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(5, 12, 35, 255))


def subtitle(W, H, text, path, ybottom):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fs = 50 if W > H else 46
    f = font(fs)
    lines = wrap(d, text, f, W * 0.84)
    lh = int(fs * 1.35)
    bh = lh * len(lines) + 30
    bw = max(d.textlength(l, font=f) for l in lines) + 70
    y0 = ybottom - bh
    d.rounded_rectangle((W / 2 - bw / 2, y0, W / 2 + bw / 2, ybottom), 18, fill=(8, 18, 50, 170))
    for i, l in enumerate(lines):
        centered(d, W / 2, y0 + 15 + i * lh, l, f, (245, 247, 251, 255))
    img.save(path)


def pill(d, cx, cy, text, f, fill, fg):
    w = d.textlength(text, font=f) + 70
    h = f.size + 34
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, fill=fill)
    centered(d, cx, cy - f.size * 0.62, text, f, fg)


def deco5(W, H, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(46 if W > H else 40, BOLD)
    if W > H:
        pill(d, W * 0.24, H * 0.60, "5개월 AI 네이티브", f, (47, 107, 255, 235), (245, 247, 251, 255))
        pill(d, W * 0.76, H * 0.60, "18개월 AI 올인원", f, (255, 180, 0, 240), (11, 27, 63, 255))
    else:
        pill(d, W / 2, H * 0.36, "5개월 AI 네이티브", f, (47, 107, 255, 235), (245, 247, 251, 255))
        pill(d, W / 2, H * 0.42, "18개월 AI 올인원", f, (255, 180, 0, 240), (11, 27, 63, 255))
    img.save(path)


def deco6(W, H, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    land = W > H
    pw, ph = (1300, 560) if land else (940, 620)
    cy = H * (0.46 if land else 0.42)
    d.rounded_rectangle((W / 2 - pw / 2, cy - ph / 2, W / 2 + pw / 2, cy + ph / 2), 36, fill=(8, 18, 50, 175))
    top = cy - ph / 2
    centered(d, W / 2, top + 50, "CODYSSEY", font(150 if land else 120, BOLD), (245, 247, 251, 255))
    sf = font(58 if land else 46, SEMI)
    sl = wrap(d, cam["slogan"], sf, pw - 100)
    y = top + (250 if land else 220)
    for l in sl:
        centered(d, W / 2, y, l, sf, (255, 180, 0, 255))
        y += int(sf.size * 1.4)
    pill(d, W / 2, cy + ph / 2 - 85, cam["cta"], font(44 if land else 38, BOLD), (47, 107, 255, 240), (245, 247, 251, 255))
    img.save(path)


for lay, (W, H) in LAYOUTS.items():
    yb = H - 70 if W > H else 1720
    for sc in sb["scenes"]:
        n = sc["no"]
        subtitle(W, H, sc["narration"], f"{OUT}/ov_{lay}_sub{n:02d}.png", yb)
    deco5(W, H, f"{OUT}/ov_{lay}_deco05.png")
    deco6(W, H, f"{OUT}/ov_{lay}_deco06.png")
print("overlays ok")
