#!/usr/bin/env python
"""보너스: 동일 씬(3, 5)을 다른 모델(HF Space black-forest-labs/FLUX.1-schnell)로 재생성 -> scene{NN}_img_alt.png
Pollinations의 model 파라미터(flux/turbo/sana)는 응답이 바이트 동일(md5 일치)해 비교 불가 -> HF Space로 대체.
프롬프트는 gen_images.py의 REV (n,2) 와 동일(순수 모델 차이만 비교). 로그는 generation_log.json 에 병합.
"""
import json, pathlib, shutil, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gradio_client import Client

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/images"
LOG = IMG / "generation_log.json"
import importlib.util
spec = importlib.util.spec_from_file_location("gi", ROOT / "scripts/gen_images.py"); gi = importlib.util.module_from_spec(spec); spec.loader.exec_module(gi)

c = Client("black-forest-labs/FLUX.1-schnell")
log = json.loads(LOG.read_text())
for n in (3, 5):
    fn = f"scene{n:02d}_img_alt.png"
    prompt = gi.REV[(n, 2)]
    try:
        res, seed = c.predict(prompt, 42, False, 1280, 720, 4, api_name="/infer")
        subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-loglevel", "error", "-i", res, str(IMG / fn)], check=True)
        log[fn] = dict(file=fn, model_param="HF Space black-forest-labs/FLUX.1-schnell (steps=4)", model_actual="FLUX.1-schnell",
                       seed=42, prompt=prompt, size="1280x720", attempt=1, http="gradio ok", ok=True)
    except Exception as e:
        print(fn, "실패", repr(e))
        log[fn] = dict(file=fn, model_param="HF Space FLUX.1-schnell", seed=42, prompt=prompt, attempt=1, ok=False, error=repr(e))
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1))
    print(fn, log[fn]["ok"])
