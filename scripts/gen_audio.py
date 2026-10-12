#!/usr/bin/env python3
"""씬별 내레이션(edge-tts) + BGM/효과음(HF Space) 생성. 재실행 가능. 결과는 assets/audio/audio_log.json.
사용: .venv/bin/python scripts/gen_audio.py [vo|bgm|sfx ...]  (인자 없으면 전부)
"""
import asyncio, json, shutil, subprocess, sys, time
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/audio"
SB = json.loads((ROOT / "storyboard/storyboard.json").read_text())
LOG_P = OUT / "audio_log.json"
LOG = json.loads(LOG_P.read_text()) if LOG_P.exists() else []
FF = "/opt/homebrew/bin/"


def dur(p):
    return float(subprocess.check_output([FF + "ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


def log(**kw):
    kw["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    LOG[:] = json.loads(LOG_P.read_text()) if LOG_P.exists() else LOG  # 병렬 실행 대비 재로드
    LOG.append(kw)
    LOG_P.write_text(json.dumps(LOG, ensure_ascii=False, indent=2))
    print(kw.get("file"), kw.get("status"), kw.get("duration"), kw.get("summary", "")[:100])


def vo_gtts(n, text, limit, f):
    """edge-tts 403 시 대체: gTTS(Google Translate TTS, 키 불필요, lang=ko). rate 대신 ffmpeg atempo로 길이 조정."""
    from gtts import gTTS
    raw = OUT / f"_raw_scene{n:02d}.mp3"
    gTTS(text, lang="ko").save(str(raw))
    for t in (1.0, 1.1, 1.2, 1.3):
        subprocess.check_call([FF + "ffmpeg", "-y", "-v", "error", "-i", str(raw), "-filter:a", f"atempo={t}",
                               "-ar", "44100", "-b:a", "128k", str(f)])
        d = dur(f)
        ok = d <= limit - 0.3
        log(file=f.name, tool="gTTS + ffmpeg atempo", voice="gTTS ko (Google Translate TTS)", text=text,
            params={"lang": "ko", "atempo": t}, duration=round(d, 2), scene_duration=limit,
            status="ok" if ok else "too_long_retry",
            summary=f"{d:.2f}s / 씬 {limit}s, atempo {t}" + ("" if ok else " -> 초과, 속도 상향"))
        if ok:
            raw.unlink()
            return True
    return False


# gTTS atempo 1.2 이내로 들어오지 않는 씬은 의미 유지한 채 문장 축약 (storyboard.json 씬5 narration에도 반영됨)
NARRATION_OVERRIDE = {5: "장학금으로 학비 부담은 덜고, 나에게 맞는 AI 과정을 고르세요."}


def vo():
    voice = SB["tts_voice"]["voice"]
    use_edge = True
    for s in SB["scenes"]:
        n, limit, text = s["no"], s["duration_sec"], NARRATION_OVERRIDE.get(s["no"], s["narration"])
        f = OUT / f"scene{n:02d}_vo.mp3"
        if use_edge:
            try:
                # 씬 길이 - 0.3초 여유 안에 들어올 때까지 rate를 +0% -> +10% -> ... 올림
                for pct in (0, 10, 15, 20, 25):
                    rate = f"{pct:+d}%"
                    asyncio.run(edge_tts.Communicate(text, voice, rate=rate).save(str(f)))
                    d = dur(f)
                    ok = d <= limit - 0.3
                    log(file=f.name, tool="edge-tts", voice=voice, text=text, params={"rate": rate},
                        duration=round(d, 2), scene_duration=limit, status="ok" if ok else "too_long_retry",
                        summary=f"{d:.2f}s / 씬 {limit}s, rate {rate}" + ("" if ok else " -> 초과, rate 상향 재생성"))
                    if ok:
                        break
                continue
            except Exception as e:
                use_edge = False
                log(file=f.name, tool="edge-tts", voice=voice, text=text, status="failed",
                    summary=f"edge-tts 실패: {type(e).__name__}: {str(e)[:120]} (speech.platform.bing.com WS 403, 재시도·버전 헤더 변경 모두 실패) -> gTTS 대체 (MeloTTS Space는 KR 화자가 선택지에 없어 실패)")
        if not vo_gtts(n, text, limit, f):
            log(file=f.name, status="failed", summary="atempo 1.3에도 씬 길이 초과, 문장 축약 필요")


def stream_musicgen(prompt, secs, seed, out):
    """이 Space는 HLS(m3u8) 스트림을 반환 -> raw API로 URL을 받아 ffmpeg로 wav 변환."""
    import requests
    B = "https://sanchit-gandhi-musicgen-streaming.hf.space"
    p = {"text_prompt": prompt, "audio_length_in_s": secs, "play_steps_in_s": 1.5, "seed": seed}
    eid = requests.post(B + "/gradio_api/call/generate_audio", json={"data": list(p.values())}).json()["event_id"]
    url = None
    with requests.get(B + f"/gradio_api/call/generate_audio/{eid}", stream=True) as r:
        for l in r.iter_lines(decode_unicode=True):
            if l and l.startswith("data:"):
                url = json.loads(l[5:])[0]["url"]
    subprocess.check_call([FF + "ffmpeg", "-y", "-v", "error", "-i", url, str(out)])
    return p


def space_call(space, prompt, secs, out):
    from gradio_client import Client
    c = Client(space)
    if "Stable-Audio" in space:
        p = {"prompt": prompt, "seconds_total": secs, "steps": 100, "cfg_scale": 7}
        r = c.predict(api_name="/predict", **p)
    elif space == "sanchit-gandhi/musicgen-streaming":
        return stream_musicgen(prompt, min(secs, 30), 5, out)
    elif space == "patgpt4/MusicGen":  # CPU Space(ZeroGPU 쿼터 무관), 출력이 mp4 -> wav 변환
        p = {"model": "small", "input_text": prompt, "melody_condition_optional": None, "duration": min(secs, 30),
             "topk": 250, "topp": 0, "temperature": 1, "classifier_free_guidance": 3}
        r = c.predict(*p.values(), fn_index=1)
        r = r[0] if isinstance(r, (list, tuple)) else r
        subprocess.check_call([FF + "ffmpeg", "-y", "-v", "error", "-i", r, "-vn", str(out)])
        return p
    elif space == "facebook/MusicGen":
        p = {"texts": prompt, "melodies": None}
        r = c.predict(api_name="/predict_batched", **p)
    else:
        raise ValueError(space)
    r = r[0] if isinstance(r, (list, tuple)) else r
    shutil.copy(r, out)
    return p


# 실제 존재/RUNNING 확인한 Space 순서 (HF API로 확인)
BGM_SPACES = ["artificialguybr/Stable-Audio-Open-Zero", "sanchit-gandhi/musicgen-streaming", "facebook/MusicGen", "patgpt4/MusicGen"]
if "--cpu-only" in sys.argv:  # ZeroGPU 쿼터 소진 시 앞 3개 건너뜀
    BGM_SPACES = BGM_SPACES[3:]


OK_SPACE = []


def music(name, prompt, secs, spaces=BGM_SPACES):
    out = OUT / name
    for sp in spaces:
        try:
            params = space_call(sp, prompt, secs, out)
            d = dur(out)
            note = "" if d >= 30 or name != "bgm_main.wav" else " (30초 미만: 루프/이어붙이기 필요)"
            OK_SPACE[:] = [sp]
            log(file=name, tool="HF Space gradio_client", space=sp, prompt=prompt, params=params, duration=round(d, 2),
                status="ok", summary=f"{sp} 성공, {d:.1f}s{note}")
            return True
        except Exception as e:
            log(file=name, tool="HF Space gradio_client", space=sp, prompt=prompt, status="failed",
                summary=f"{sp} 실패: {type(e).__name__}: {str(e)[:200]}")
    return False


def sfx():
    music("sfx_whoosh.wav", "short soft whoosh riser sweep, clean, no music", 3)
    music("sfx_chime.wav", "single bright glass chime, soft bell, short, gentle decay, no music", 3)


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")] or ["vo", "bgm", "sfx"]
    if "vo" in a:
        vo()
    if "bgm" in a:
        # 스트리밍 MusicGen은 최대 30초/회 -> 길이가 모자라면 seed를 바꿔 2번 생성 후 2초 크로스페이드로 이어붙임
        if music("bgm_part1.wav", SB["bgm_prompt"], 45, BGM_SPACES):
            d1 = dur(OUT / "bgm_part1.wav")
            if d1 >= 45:
                shutil.copy(OUT / "bgm_part1.wav", OUT / "bgm_main.wav")
            else:
                space_call(OK_SPACE[0], SB["bgm_prompt"] + ", variation", 30, OUT / "bgm_part2.wav")
                subprocess.check_call([FF + "ffmpeg", "-y", "-v", "error", "-i", str(OUT / "bgm_part1.wav"), "-i",
                                       str(OUT / "bgm_part2.wav"), "-filter_complex", "acrossfade=d=2", str(OUT / "bgm_main.wav")])
                log(file="bgm_main.wav", tool="ffmpeg acrossfade", params={"parts": ["bgm_part1.wav", "bgm_part2.wav"], "d": 2},
                    duration=round(dur(OUT / "bgm_main.wav"), 2), status="ok", summary="2개 클립 크로스페이드 이어붙임")
    if "sfx" in a:
        sfx()
