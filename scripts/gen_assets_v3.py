import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
R = "/Users/hyunbok/Desktop/genai-multimodal-ad"
PY = f"{R}/.venv/bin/python"; C = f"{R}/scripts/copa.py"
d = json.load(open(f"{R}/storyboard/v3/storyboard_v3.json"))
VOICE = {"MASTER": "onyx", "SORA": "nova", "DOHYUN": "echo", "MINSEOK": "fable"}
jobs = []
for s in d["scenes"]:
    n = s["no"]
    jobs.append([PY, C, "image", "gpt-image-2", f"{R}/assets/v3/stills/scene{n:02d}.png", s["still_prompt"], "1536x1024"])
    for i, l in enumerate(s["dialogue"]):
        t = l["line"].replace("...", "").strip()
        if l["speaker"] not in VOICE and "합창" not in l["speaker"] or t.startswith("("): continue
        v = VOICE.get(l["speaker"], "echo")
        jobs.append([PY, C, "tts", "gpt-4o-mini-tts", f"{R}/assets/v3/vo/scene{n:02d}_{i}.mp3", t, v, "1.0"])
def run(j):
    r = subprocess.run(j, capture_output=True, text=True); print(j[2], j[4], r.returncode, r.stderr[-200:], flush=True)
with ThreadPoolExecutor(5) as ex: list(ex.map(run, jobs))
