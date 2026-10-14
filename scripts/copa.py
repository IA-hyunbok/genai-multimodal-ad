"""코디세이 COPA 게이트웨이 미디어 API 클라이언트.

설정: 프로젝트 루트 .env 의 COPA_BASE_URL, COPA_API_KEY
사용:
  python scripts/copa.py image <model> <out.png> "<prompt>" [size]
  python scripts/copa.py tts   <model> <out.mp3> "<text>" [voice] [speed]
  python scripts/copa.py video <model> <out.mp4> "<prompt>" [seconds] [resolution] [aspect]
모든 호출은 assets/copa_log.jsonl 에 한 줄씩 남는다.
"""
import base64
import json
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "assets" / "copa_log.jsonl"


def load_env():
    env = {}
    for line in (ROOT / ".env").read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    if not env.get("COPA_API_KEY"):
        sys.exit(".env 의 COPA_API_KEY 가 비어 있습니다")
    return env["COPA_BASE_URL"].rstrip("/"), env["COPA_API_KEY"]


BASE, KEY = load_env()
HEADERS = {"Authorization": f"Bearer {KEY}"}


def log(**entry):
    entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with LOG.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def post(path, body):
    r = requests.post(BASE + path, json=body, headers=HEADERS, timeout=300)
    if r.status_code >= 400:
        log(path=path, body=body, status=r.status_code, error=r.text[:500])
        sys.exit(f"{r.status_code} {r.text[:500]}")
    return r.json()["result"]


def image(model, out, prompt, size="1536x1024"):
    body = {"model": model, "prompt": prompt, "size": size, "n": 1, "response_format": "b64_json"}
    res = post("/api/v1/images", body)
    Path(out).write_bytes(base64.b64decode(res["images"][0]["b64_json"]))
    log(kind="image", model=model, size=size, prompt=prompt, file=str(out), request_id=res.get("requestId"))
    print(out)


def tts(model, out, text, voice="alloy", speed="1.0"):
    body = {"model": model, "input": text, "voice": voice, "speed": float(speed),
            "format": "mp3", "response_format": "b64_json"}
    res = post("/api/v1/audio/tts", body)
    Path(out).write_bytes(base64.b64decode(res["b64_json"]))
    log(kind="tts", model=model, voice=voice, speed=float(speed), text=text, file=str(out),
        request_id=res.get("requestId"))
    print(out)


def video(model, out, prompt, seconds="8", resolution="720p", aspect="16:9"):
    body = {"model": model, "prompt": prompt, "durationSeconds": int(seconds),
            "resolution": resolution, "aspectRatio": aspect}
    job = post("/api/v1/videos", body)
    job_id = job["jobId"]
    print("job", job_id, flush=True)
    while True:
        time.sleep(10)
        r = requests.get(f"{BASE}/api/v1/videos/{job_id}", headers=HEADERS, timeout=60)
        st = r.json()["result"]
        print(st["status"], st.get("progress"), flush=True)
        if st["status"] in ("completed", "failed"):
            break
    if st["status"] == "failed":
        log(kind="video", model=model, prompt=prompt, job_id=job_id, status="failed", error=st.get("error"))
        sys.exit(f"failed: {st.get('error')}")
    r = requests.get(f"{BASE}/api/v1/videos/{job_id}/download", headers=HEADERS, timeout=300)
    r.raise_for_status()
    Path(out).write_bytes(r.content)
    log(kind="video", model=model, seconds=int(seconds), resolution=resolution, aspect=aspect, prompt=prompt,
        job_id=job_id, status="completed", file=str(out))
    print(out)


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"image": image, "tts": tts, "video": video}[cmd](*args)
