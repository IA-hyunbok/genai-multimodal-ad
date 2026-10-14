#!/usr/bin/env python3
"""v3 live 영상용 자막/키워드 슈퍼/엔드카드를 투명 PNG(1920x1080)로 렌더링하고 manifest를 만든다.
사용: python3 scripts/make_overlays_v3.py <클립 길이 10개...>   (edit_v3_live.sh 가 호출; 시스템 python3 + Pillow)
출력: build/v3edit/ov/*.png, build/v3edit/ov/manifest.txt  (줄: png 시작초 끝초)
대사 타이밍은 veo 오디오 음량 포락선(0.25s 단위) 기반 추정치다. 한국어 발화를 청취·ASR로 확인하지 못했다.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build/v3edit/ov")
os.makedirs(OUT, exist_ok=True)
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
BOLD = 6
W, H = 1920, 1080
DUR = [float(x) for x in sys.argv[1:11]]
assert len(DUR) == 10, "클립 길이 10개 필요"
ST = [sum(DUR[:i]) for i in range(10)]  # 클립 시작(타임라인 초)
END = sum(DUR)

# (샷 인덱스 1~10, 클립 내 시작, 클립 내 끝, 텍스트) — shot03은 ss=0.7 보정 후 값, shot10은 ss=1.0 보정 후 값
SUBS = [
    (1, 2.7, 3.9, "별이 말했다."),
    (1, 4.6, 6.0, "평범한 자에게도, 부름은 온다."),
    (2, 0.1, 2.6, "깨어나라, 그대여. 코디세이로 오라."),
    (2, 3.5, 5.2, "...저 국문과인데요?"),
    (2, 6.2, 7.5, "입구에 전공 칸 없다."),
    (3, 0.3, 1.3, "어? 문턱이 없네?"),
    (3, 1.8, 3.05, "경력도 안 본다."),
    (4, 0.1, 1.5, "그대 안의 코드도 깨어났다."),
    (4, 1.8, 3.0, "코디세이로 오라."),
    (4, 3.1, 5.0, "충성! ...통장이 비었습니다!"),
    (4, 5.4, 7.4, "장학금 받으며 배운다."),
    (5, 0.0, 1.0, "...받으며요?!"),
    (5, 1.75, 3.25, "배우는 데만 집중해."),
    (6, 0.0, 2.3, "지친 자여. 코디세이로 오라."),
    (6, 2.75, 4.25, "혼자 하면 맨날 포기하는데요..."),
    (6, 4.75, 5.5, "혼자 안 한다."),
    (6, 6.25, 7.9, "먼저 푼 사람이 가르친다."),
    (8, 0.0, 0.9, "...저분들도요?"),
    (8, 1.3, 2.75, "충성! 동료입니까!"),
    (8, 2.8, 3.95, "여기 교수는 없다. 동료가 있다."),
    (8, 4.0, 4.8, "나도 동료한테 배웠다."),
    (8, 5.0, 6.3, "같이 갑니다!"),
    (9, 0.1, 1.0, "노크는요?"),
    (9, 1.5, 2.5, "문이 없다."),
    (10, 2.5, 3.75, "코디세이로 오세요~"),
]
# 키워드 슈퍼: 받아침 직후 0.8초 (타임라인 절대 시각 = 해당 샷 시작 + 오프셋)
SUPERS = [
    ("전공·경력 무관", ST[2] + DUR[2] - 0.05, 0.8),
    ("장학금", ST[4] + DUR[4] - 0.4, 0.8),
    ("동료학습", ST[6], 0.8),
]


def f(size):
    return ImageFont.truetype(FONT, size, index=BOLD)


def canvas():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def center(d, y, text, font, fill=(255, 255, 255, 255), stroke=0, sfill=(0, 0, 0, 255), track=0):
    if track:
        ws = [d.textlength(c, font=font) for c in text]
        total = sum(ws) + track * (len(text) - 1)
        x = (W - total) / 2
        for c, w in zip(text, ws):
            d.text((x, y), c, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill)
            x += w + track
    else:
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill)


man = []


def save(im, name, a, b):
    p = os.path.join(OUT, name)
    im.save(p)
    man.append(f"{p} {a:.3f} {b:.3f}")


for k, (s, a, b, t) in enumerate(SUBS):
    im, d = canvas()
    center(d, 880, t, f(56), stroke=6)
    save(im, f"sub{k:02d}.png", ST[s - 1] + a, ST[s - 1] + b)

for k, (t, a, dur) in enumerate(SUPERS):
    im, d = canvas()
    center(d, 400, t, f(170), fill=(255, 226, 130, 255), stroke=12, sfill=(10, 14, 30, 255))
    save(im, f"super{k}.png", a, a + dur)

# 엔드카드 (마지막 샷, 5초): 상단 어둡게 그라데이션 + 순차 등장
e0 = ST[9]
grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grad)
for y in range(0, 520):
    gd.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * (1 - y / 520))))
save(grad, "end_grad.png", e0 + 0.2, END)
im, d = canvas(); center(d, 50, "문턱은 없고, 동료는 있다.", f(84), stroke=7); save(im, "end1.png", e0 + 0.5, END)
im, d = canvas(); center(d, 165, "전공 무관 · 장학금 · 동료학습", f(46), stroke=5); save(im, "end2.png", e0 + 1.2, END)
im, d = canvas()
center(d, 235, "CODYSSEY", f(86), fill=(255, 226, 130, 255), stroke=8, sfill=(10, 14, 30, 255), track=12)
center(d, 345, "codyssey.kr", f(44), stroke=4)
save(im, "end3.png", e0 + 1.9, END)
im, d = canvas(); center(d, 1020, "※ 연출된 가상 상황 · AI로 제작", f(28), fill=(255, 255, 255, 215), stroke=3); save(im, "end4.png", e0 + 0.2, END)

open(os.path.join(OUT, "manifest.txt"), "w").write("\n".join(man) + "\n")
print(len(man), "overlays, total", END)
