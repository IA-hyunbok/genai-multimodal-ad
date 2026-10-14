#!/usr/bin/env python3
"""v4 편집: 조정실 veo 클립 + v3 재사용 클립 + 프롬프트 입력창 -> output/v4/Codyssey_v4_booth_16x9.mp4
사용: python3 scripts/edit_v4.py   (homebrew python3 + Pillow, ffmpeg)
자막 시각은 전부 faster-whisper 단어 타임스탬프(scripts/words.py) 기준이다. 추정치 없음.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
B = "build/v4edit"
os.makedirs(f"{B}/seg", exist_ok=True)
os.makedirs(f"{B}/ov", exist_ok=True)
OUT = "output/v4/Codyssey_v4_booth_16x9.mp4"
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
W, H, FPS = 1920, 1080, 30
V3, V4 = "assets/v3/live", "assets/v4"

# v3 크롭 필터 (edit_v3_live.sh 와 동일)
VF_02 = "crop=985:554:147:66,scale=1920:1080:flags=lanczos"
VF_10 = "scale=1920:1080:flags=lanczos,split[a][b];[a]crop=1920:140:0:0,vflip[t];[b]crop=1920:940:0:0[m];[t][m]vstack"

# (소스, 시작초, 길이, 영상필터, 묵음구간[(a,b)], 자막[(a,b,text)], 배지)  — 자막 a,b는 세그먼트 내 상대초
SEGS = [
    (f"{V4}/B01.mp4", 0, 6.5, None, [], [(0.0, 2.2, "민준아, 홍보영상 어디 있어?"), (3.0, 4.1, "아… 그게…"), (4.2, 6.4, "지금 AI로 금방 만들게요!")], None),
    ("PROMPT", 0, 2.4, None, [], [], "코디세이 홍보영상 만들어줘. 웅장하게."),
    (f"{V3}/shot01.mp4", 0, 2.6, None, [], [(0.0, 1.9, "별이 말했다.")], "AI 결과물 ①"),
    (f"{V4}/B02_v2.mp4", 1.0, 4.3, None, [], [(0.8, 4.2, "교육 플랫폼이 왜 우주 전쟁을 해!")], None),
    ("PROMPT", 0, 2.4, None, [], [], "칼 빼고, 배우는 사람 얘기로."),
    (f"{V3}/shot02.mp4", 4.0, 3.7, VF_02, [], [(0.2, 1.6, "…저 국문과인데요?"), (2.0, 3.6, "입구에 전공 칸 없다.")], "AI 결과물 ②"),
    (f"{V3}/shot04.mp4", 5.1, 2.9, None, [], [(0.1, 1.4, "통장이 비었습니다!"), (1.5, 2.9, "장학금 받으며 배운다.")], "AI 결과물 ②"),
    (f"{V4}/B03.mp4", 0, 2.35, None, [], [(0.0, 2.35, "어? 괜찮은데?")], None),
    (f"{V3}/shot08_v2.mp4", 4.4, 2.9, None, [], [(0.1, 1.9, "(갑자기 이탈리아어)"), (1.9, 2.9, "Andiamo insieme!")], "AI 결과물 ②"),
    (f"{V4}/B04.mp4", 0, 4.0, None, [], [(0.0, 1.4, "이탈리아어는 왜 나와?!"), (1.7, 3.9, "혼자서는… 못 하겠어요.")], None),
    (f"{V4}/B05.mp4", 0, 4.5, None, [(1.05, 4.5)], [(0.0, 1.0, "같이 고치자.")], None),
    ("PROMPT", 0, 3.0, None, [], [], "전공 몰라도, 돈 걱정 없이, 동료랑 같이 배우는 곳."),
    (f"{V4}/F01_v2.mp4", 0, 7.2, None, [], [(0.0, 2.4, "같이 갑니다!"), (3.7, 5.8, "여기 교수는 없다."), (5.9, 7.1, "동료가 있다.")], "AI 결과물 ③"),
    (f"{V4}/B06_v2.mp4", 0, 2.6, None, [], [(0.0, 1.7, "…안디아모.")], None),
    (f"{V3}/shot10_v2.mp4", 1.0, 5.0, VF_10, [], [(1.8, 3.8, "코디세이로 오세요~")], None),
]
# 키워드 슈퍼: (세그먼트 인덱스, 상대 시작, 길이, 텍스트)
SUPERS = [(5, 2.3, 1.3, "전공·경력 무관"), (6, 1.5, 1.4, "장학금"), (12, 5.9, 1.3, "동료학습")]


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


def prompt_frames(text, dur, out):
    """프롬프트 입력창: 70% 동안 한 글자씩 타이핑, 이후 '생성 중…'"""
    fdir = out + "_f"
    os.makedirs(fdir, exist_ok=True)
    n, f, fs = int(dur * FPS), font(52), font(30)
    for i in range(n):
        im = Image.new("RGB", (W, H), (14, 16, 24))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((260, 430, 1660, 650), 28, fill=(30, 33, 46), outline=(90, 110, 200), width=3)
        d.text((310, 455), "AI 영상 생성", font=fs, fill=(140, 150, 190))
        k = min(len(text), int(len(text) * i / (n * 0.7)) + 1)
        d.text((310, 525), text[:k], font=f, fill=(240, 240, 250))
        if (i // 8) % 2 == 0:  # 커서 (폰트에 ▏ 글리프가 없어 사각형으로)
            x = 314 + d.textlength(text[:k], font=f)
            d.rectangle((x, 532, x + 4, 590), fill=(240, 240, 250))
        if i > n * 0.75:
            d.text((310, 690), "생성 중" + "." * (1 + (i // 6) % 3), font=fs, fill=(140, 150, 190))
        im.save(f"{fdir}/{i:04d}.png")
    ff("-framerate", FPS, "-i", f"{fdir}/%04d.png", "-c:v", "libx264", "-crf", 12, "-pix_fmt", "yuv420p", out)
    # 키보드 소리: 타이핑 구간만 0.09초 간격 짧은 노이즈
    ty = dur * 0.7
    ff("-f", "lavfi", "-i", f"aevalsrc='(random(0)*2-1)*0.35*lt(mod(t\\,0.09)\\,0.012)*lt(t\\,{ty})':s=48000:d={dur}",
       "-ac", 2, out.replace(".mp4", ".wav"))


# 1) 세그먼트 렌더링
starts, t = [], 0.0
for i, (src, ss, dur, vf, mute, _, badge) in enumerate(SEGS):
    starts.append(t)
    t += dur
    v, a = f"{B}/seg/v{i:02d}.mp4", f"{B}/seg/v{i:02d}.wav"
    if src == "PROMPT":
        prompt_frames(badge, dur, v)
        continue
    ff("-ss", ss, "-i", src, "-t", dur, "-an", "-vf", f"{vf or 'scale=1920:1080:flags=lanczos'},fps={FPS},setsar=1,format=yuv420p",
       "-c:v", "libx264", "-crf", 12, v)
    af = "".join(f"volume=0:enable='between(t,{x},{y})'," for x, y in mute)
    ff("-ss", ss, "-i", src, "-vn", "-af", f"{af}aresample=48000,apad=whole_dur={dur}", "-t", dur, "-ac", 2, a)
TOTAL = t

# 2) 오디오: 세그먼트별 -20 LUFS 맞춤(±6dB) 후 이어붙이고 전체 loudnorm
ins, fc = [], ""
for i in range(len(SEGS)):
    a = f"{B}/seg/v{i:02d}.wav"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    lufs = [l.split()[1] for l in r.stderr.splitlines() if l.strip().startswith("I:")][-1]
    g = 0 if SEGS[i][0] == "PROMPT" or lufs == "-70.0" else max(-6, min(6, -20 - float(lufs)))
    ins += ["-i", a]
    fc += f"[{i}:a]volume={g:.1f}dB[g{i}];"
fc += "".join(f"[g{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=0:a=1,afade=t=out:st={TOTAL-0.8:.2f}:d=0.8,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
ff(*ins, "-filter_complex", fc, "-map", "[a]", "-ac", 2, f"{B}/audio.wav")

# 3) 영상 이어붙이기
with open(f"{B}/list.txt", "w") as fp:
    fp.writelines(f"file 'seg/v{i:02d}.mp4'\n" for i in range(len(SEGS)))
ff("-f", "concat", "-safe", 0, "-i", f"{B}/list.txt", "-c", "copy", f"{B}/clean.mp4")

# 4) 오버레이 PNG (png, 시작, 끝)
ov = []


def add(im, name, a, b):
    p = f"{B}/ov/{name}.png"
    im.save(p)
    ov.append((p, a, b))


def canvas():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


for i, seg in enumerate(SEGS):
    for k, (a, b, txt) in enumerate(seg[5]):
        im, d = canvas()
        text_c(d, 900, txt, font(56), stroke=6)
        add(im, f"sub{i:02d}_{k}", starts[i] + a, starts[i] + b)
    if seg[0] != "PROMPT" and seg[6]:
        im, d = canvas()
        d.rounded_rectangle((40, 36, 380, 100), 14, fill=(0, 0, 0, 150))
        d.text((64, 46), "● " + seg[6], font=font(36), fill=(255, 90, 90, 255))
        add(im, f"badge{i:02d}", starts[i], starts[i] + seg[2])
for k, (i, a, dur, txt) in enumerate(SUPERS):
    im, d = canvas()
    text_c(d, 380, txt, font(150), fill=(255, 226, 130, 255), stroke=12, sfill=(10, 14, 30, 255))
    add(im, f"super{k}", starts[i] + a, starts[i] + a + dur)

e0 = starts[-1]  # 엔드카드 = 마지막 5초
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
fc += f"{prev}fade=t=in:d=0.3,fade=t=out:st={TOTAL-0.6:.3f}:d=0.6,format=yuv420p[v]"
ff(*args, "-i", f"{B}/audio.wav", "-filter_complex", fc, "-map", "[v]", "-map", f"{len(ov)+1}:a",
   "-c:v", "libx264", "-crf", 16, "-r", FPS, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{TOTAL:.3f}", OUT)
print("done", OUT, f"{TOTAL:.2f}s", len(ov), "overlays")
