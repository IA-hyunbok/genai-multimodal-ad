#!/usr/bin/env python3
"""타임라인 JSON -> 완성 mp4 (컷, 자막, 키워드 슈퍼, 마지막 세그먼트 엔드카드, 음량 맞춤)
사용: python3 scripts/edit_cut.py storyboard/v4/timeline_v4.json   (homebrew python3 + Pillow, ffmpeg)
JSON: {"out": mp4, "segs": [{"src", "ss", "dur", "vf"?, "mute"?: [[a,b]], "subs": [[a,b,text]]}], "supers": [[seg, a, dur, text]]}
자막 a,b는 세그먼트 내 상대초이며 faster-whisper 단어 타임스탬프(scripts/words.py) 기준으로 적는다.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
T = json.load(open(sys.argv[1]))
OUT, SEGS, SUPERS = T["out"], T["segs"], T.get("supers", [])
B = "build/edit_" + os.path.splitext(os.path.basename(OUT))[0]
os.makedirs(f"{B}/seg", exist_ok=True)
os.makedirs(f"{B}/ov", exist_ok=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
W, H, FPS = 1920, 1080, 30


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *map(str, a)], check=True)


def font(size):
    return ImageFont.truetype(FONT, size, index=6)


def text_c(d, y, t, f, fill=(255, 255, 255, 255), stroke=0, sfill=(0, 0, 0, 255), track=0):
    ws = [d.textlength(c, font=f) for c in t]
    x = (W - sum(ws) - track * (len(t) - 1)) / 2
    for c, w in zip(t, ws):
        d.text((x, y), c, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
        x += w + track


# 1) 세그먼트
starts, t = [], 0.0
for i, s in enumerate(SEGS):
    starts.append(t)
    t += s["dur"]
    v, a = f"{B}/seg/v{i:02d}.mp4", f"{B}/seg/v{i:02d}.wav"
    vf = s.get("vf") or "scale=1920:1080:flags=lanczos"
    ff("-ss", s["ss"], "-i", s["src"], "-t", s["dur"], "-an", "-vf", f"{vf},fps={FPS},setsar=1,format=yuv420p", "-c:v", "libx264", "-crf", 12, v)
    af = "".join(f"volume=0:enable='between(t,{x},{y})'," for x, y in s.get("mute", []))
    ff("-ss", s["ss"], "-i", s["src"], "-vn", "-af", f"{af}aresample=48000,apad=whole_dur={s['dur']}", "-t", s["dur"], "-ac", 2, a)
TOTAL = t

# 2) 오디오: 세그먼트별 -20 LUFS 맞춤(±6dB) → 짧은 크로스페이드로 연결 → loudnorm
ins, fc = [], ""
for i in range(len(SEGS)):
    a = f"{B}/seg/v{i:02d}.wav"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    lufs = float([l.split()[1] for l in r.stderr.splitlines() if l.strip().startswith("I:")][-1])
    g = 0 if lufs <= -70 else max(-6, min(6, -20 - lufs))
    ins += ["-i", a]
    fc += f"[{i}:a]volume={g:.1f}dB,afade=t=in:d=0.02,afade=t=out:st={SEGS[i]['dur']-0.03:.3f}:d=0.03[g{i}];"
fc += "".join(f"[g{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=0:a=1,afade=t=out:st={TOTAL-0.4:.2f}:d=0.4,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
ff(*ins, "-filter_complex", fc, "-map", "[a]", "-ac", 2, f"{B}/audio.wav")

# 3) 영상 연결
with open(f"{B}/list.txt", "w") as fp:
    fp.writelines(f"file 'seg/v{i:02d}.mp4'\n" for i in range(len(SEGS)))
ff("-f", "concat", "-safe", 0, "-i", f"{B}/list.txt", "-c", "copy", f"{B}/clean.mp4")

# 4) 오버레이
ov = []


def add(im, name, a, b):
    p = f"{B}/ov/{name}.png"
    im.save(p)
    ov.append((p, a, b))


def canvas():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


for i, s in enumerate(SEGS):
    for k, (a, b, txt) in enumerate(s.get("subs", [])):
        im, d = canvas()
        text_c(d, 900, txt, font(56), stroke=6)
        add(im, f"sub{i:02d}_{k}", starts[i] + a, starts[i] + b)
for k, (i, a, dur, txt) in enumerate(SUPERS):
    im, d = canvas()
    text_c(d, 380, txt, font(150), fill=(255, 226, 130, 255), stroke=12, sfill=(10, 14, 30, 255))
    add(im, f"super{k}", starts[i] + a, starts[i] + a + dur)

e0 = starts[-1]  # 엔드카드 = 마지막 세그먼트
grad, gd = canvas()
for y in range(520):
    gd.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * (1 - y / 520))))
add(grad, "end_grad", e0, TOTAL)
im, d = canvas(); text_c(d, 50, "문턱은 없고, 동료는 있다.", font(84), stroke=7); add(im, "end1", e0 + 0.3, TOTAL)
im, d = canvas(); text_c(d, 165, "전공 무관 · 장학금 · 동료학습", font(46), stroke=5); add(im, "end2", e0 + 0.8, TOTAL)
im, d = canvas()
text_c(d, 235, "CODYSSEY", font(86), fill=(255, 226, 130, 255), stroke=8, sfill=(10, 14, 30, 255), track=12)
text_c(d, 345, "codyssey.kr", font(44), stroke=4)
add(im, "end3", e0 + 1.2, TOTAL)
im, d = canvas(); text_c(d, 1030, "※ 연출된 가상 상황 · AI로 제작", font(28), fill=(255, 255, 255, 215), stroke=3); add(im, "end4", e0, TOTAL)

# 5) 합성
args, fc, prev = ["-i", f"{B}/clean.mp4"], "", "[0:v]"
for k, (p, a, b) in enumerate(ov, 1):
    args += ["-loop", 1, "-framerate", FPS, "-t", f"{TOTAL:.3f}", "-i", p]
    fc += f"{prev}[{k}:v]overlay=enable='between(t,{a:.3f},{b:.3f})':format=auto[o{k}];"
    prev = f"[o{k}]"
fc += f"{prev}fade=t=in:d=0.3,fade=t=out:st={TOTAL-0.4:.3f}:d=0.4,format=yuv420p[v]"
ff(*args, "-i", f"{B}/audio.wav", "-filter_complex", fc, "-map", "[v]", "-map", f"{len(ov)+1}:a",
   "-c:v", "libx264", "-crf", 16, "-r", FPS, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{TOTAL:.3f}", OUT)
print("done", OUT, f"{TOTAL:.2f}s", len(ov), "overlays")
