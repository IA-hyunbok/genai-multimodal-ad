#!/usr/bin/env python
"""씬별 키 비주얼 생성 (Pollinations Text-to-Image). 재실행 가능: 이미 있는 파일은 건너뜀(--force로 덮어쓰기).
사용: .venv/bin/python scripts/gen_images.py [--force] [job_file ...]
실제 응답(JPEG 1024x576, EXIF manufacturer=sana)을 ffmpeg로 PNG 변환해 저장한다.
기록: assets/images/generation_log.json (verdict/summary는 육안 검수 후 scripts/log_verdict.py 가 채움)
"""
import json, subprocess, sys, time, urllib.parse, pathlib
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/images"
LOG = IMG / "generation_log.json"
SB = json.loads((ROOT / "storyboard/storyboard.json").read_text())
SEED = SB["style_lock"]["seed"]
W, H = 1280, 720
SUFFIX = SB["style_lock"]["style_suffix"]
BEFORE = SB["prompt_revision_target"]["before_prompt"]

# (파일명, 프롬프트, seed, model 파라미터, attempt)
JOBS = [("scene01_img_v1.png", BEFORE, SEED, "flux", 1)]  # 수정 전: 의도적으로 부실한 프롬프트
for s in SB["scenes"]:
    n = s["no"]
    JOBS.append((f"scene{n:02d}_img_v{2 if n == 1 else 1}.png", s["image_prompt"], SEED, "flux", 2 if n == 1 else 1))

# 보너스: 모델 파라미터를 바꿔 비교 (turbo). 로그에 모델 파라미터 무시 여부를 기록.
for n in ():  # turbo 대조는 model 파라미터가 무시됨이 확인되어 폐기(바이트 동일, md5 일치). 대체: gen_images_alt.py
    p = next(s for s in SB["scenes"] if s["no"] == n)["image_prompt"]
    JOBS.append((f"scene{n:02d}_img_alt.png", p, SEED, "turbo", 1))

# 2차 수정(v2/v3): v1 육안 검수에서 실사풍·피사체 누락 발생 -> 긴 style_suffix는 모델이 무시하므로
# "flat vector illustration"을 맨 앞으로, 프롬프트를 짧게, 피사체를 명시. seed는 42 유지(프롬프트 효과만 분리).
REV = {
 (1, 3): "flat vector illustration, minimal geometric shapes, faceless silhouette seen from behind wearing an amber scarf, standing at a fork of many glowing paths in a foggy deep navy night, deep navy and electric blue with amber accent, no text",
 (2, 2): "flat vector illustration, minimal geometric shapes, two hands resting on a laptop keyboard, an hourglass and stacked coins on the desk, dark navy room, cold blue window light, deep navy and electric blue with amber accent, no text",
 (3, 2): "flat vector illustration, minimal geometric shapes, faceless silhouette with an amber scarf walking toward a glowing amber doorway at the end of a dark path, two small silhouettes waving from the light, navy to electric blue sky, no text",
 (4, 2): "flat vector illustration, minimal geometric shapes, four faceless silhouettes around a round table pointing at a glowing screen of floating geometric blocks, bright off-white and blue studio, amber accent, no text",
 (5, 2): "flat vector illustration, minimal geometric shapes, faceless silhouette with an amber scarf seen from behind at the start of two diverging roads, floating amber stars, bright blue sky, distant city skyline, no text",
 (4, 3): "flat vector illustration, four people silhouettes sitting around a round table in a bright office, a glowing screen above the table, blue and white colors with amber accent, no text",
 (6, 2): "flat vector illustration, minimal end card background, a small amber star orbiting a thin circle on a smooth electric blue to deep navy gradient, empty center, no text",
}
for (n, v), p in REV.items():
    JOBS.append((f"scene{n:02d}_img_v{v}.png", p, SEED, "flux", v))


def gen(fn, prompt, seed, model):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width={W}&height={H}&seed={seed}&model={model}&nologo=true")
    for i in range(8):
        try:
            r = requests.get(url, timeout=180)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
                tmp = IMG / (fn + ".tmp")
                tmp.write_bytes(r.content)
                subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-loglevel", "error", "-f", "image2", "-i", str(tmp),
                                str(IMG / fn)], check=True)
                tmp.unlink()
                return True, f"HTTP 200 {len(r.content)}B (시도 {i+1})"
            err = f"HTTP {r.status_code}"
        except Exception as e:
            err = repr(e)
        print(fn, "실패:", err)
        time.sleep(25)
    return False, err


def main():
    force = "--force" in sys.argv
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    for fn, prompt, seed, model, attempt in JOBS:
        if (IMG / fn).exists() and not force:
            continue
        ok, note = gen(fn, prompt, seed, model)
        e = log.get(fn, {})
        e.update(file=fn, model_param=model, model_actual="sana (응답 EXIF 기준; model 파라미터 무시됨)", seed=seed,
                 prompt=prompt, size=f"requested {W}x{H}, received 1024x576",
                 attempt=attempt, http=note, ok=ok)
        log[fn] = e
        LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1))
        print(fn, ok, note)


if __name__ == "__main__":
    main()
