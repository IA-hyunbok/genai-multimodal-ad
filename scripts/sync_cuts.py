#!/usr/bin/env python3
"""컷 클립 -> 실제 말소리 기준 타임라인(edit_cut.py 입력).
사용: .venv/bin/python scripts/sync_cuts.py v3 [c05=c05_v2 ...] [c10@crop=968:544:156:88 ...]
      c05=c05_v2: 리테이크 클립 지정 / c10@crop=...: 그 컷에 ffmpeg 필터(박힌 글자·레터박스 자르기)
- 각 클립을 faster-whisper로 받아써 첫 단어 -0.15s ~ 마지막 단어 +0.2s만 남긴다(마지막 컷은 끝까지).
- 자막 글자는 대본 그대로, 시간은 받아쓴 단어 시간. 대사가 둘이면 글자 수 비율로 단어를 나눈다.
- 대본과 받아쓰기 일치율을 출력한다(낮으면 리테이크 후보).
결과: storyboard/<ver>/timeline_<ver>c.json, 받아쓰기 캐시 build/<ver>c/asr.json
"""
import difflib, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ver = sys.argv[1]
swaps = dict(a.split("=", 1) for a in sys.argv[2:] if "@" not in a)
vfs = dict(a.split("@", 1) for a in sys.argv[2:] if "@" in a)
T = json.loads((ROOT / f"storyboard/{ver}/cuts_{ver}.json").read_text())
B, A = ROOT / f"build/{ver}c", ROOT / f"assets/{ver}c"
cache_f = B / "asr.json"
cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
norm = lambda s: re.sub(r"[^가-힣a-zA-Z0-9]", "", s)

cuts = [(sc, c) for sc in T["scenes"] for c in sc["cuts"]]
ids, n = [], 0
for sc, c in cuts:  # cuts.py와 같은 번호 규칙(id 있는 컷은 번호를 밀지 않음)
    n += "id" not in c
    ids.append(c.get("id", f"c{n:02d}"))
names = [swaps.get(k, k) for k in ids]
todo = [n for n in names if n not in cache]
if todo:
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", compute_type="int8")
    for n in todo:
        segs, _ = m.transcribe(str(A / f"{n}.mp4"), language="ko", word_timestamps=True, vad_filter=True,
                                 vad_parameters=dict(min_silence_duration_ms=200))  # VAD 없으면 첫 단어가 0초에 붙는다
        cache[n] = [[w.start, w.end, w.word.strip()] for s in segs for w in s.words]
    cache_f.write_text(json.dumps(cache, ensure_ascii=False))

segs, supers, report = [], [], []
for i, ((sc, c), n) in enumerate(zip(cuts, names)):
    src = A / f"{n}.mp4"
    length = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                                  capture_output=True, text=True).stdout)
    words = [w for w in cache[n] if norm(w[2])] if c["lines"] else []  # 대사 없는 컷은 받아쓰기 무시
    script = [l for _, _, l in c["lines"]]
    tail = norm("".join(script))[-2:]
    ends = [k for k, w in enumerate(words) if norm(w[2]).endswith(tail)]
    if ends:  # 대본 마지막 두 글자로 끝나는 단어 뒤의 군말은 버린다
        words = words[:ends[-1] + 1]
    head = norm("".join(script))[:2]
    starts = [k for k, w in enumerate(words) if norm(w[2]).startswith(head)]
    if starts:  # 대본 첫 두 글자로 시작하는 단어 앞의 군말도 버린다
        words = words[starts[0]:]
    heard = " ".join(w[2] for w in words)
    ratio = difflib.SequenceMatcher(None, norm("".join(script)), norm(heard)).ratio()
    report.append(f"{n:8s} {ratio:4.0%}  대본: {' / '.join(script)}  |  들림: {heard}")
    if not words:
        ss, dur, subs = 0, length, []
    else:
        ss = max(0, words[0][0] - 0.15)
        end = length + 1.0 if c.get("end") else min(length, words[-1][1] + 0.2)  # 마지막 컷은 끝 프레임 1초 정지(엔드카드·페이드용)
        dur = round(end - ss, 2)
        # 대사별로 단어 나누기: 글자 수 누적 비율
        sizes = [len(norm(l)) for l in script]
        tot, acc, k, groups = sum(sizes), 0, 0, [[] for _ in script]
        heard_tot = sum(len(norm(w[2])) for w in words)
        for w in words:
            groups[min(k, len(script) - 1)].append(w)
            acc += len(norm(w[2]))
            if k < len(script) - 1 and acc >= heard_tot * sum(sizes[:k + 1]) / tot:
                k += 1
        subs = []
        for l, g in zip(script, groups):
            if g:
                subs.append([round(max(0, g[0][0] - 0.1 - ss), 2), round(min(dur, g[-1][1] + 0.25 - ss), 2), l])
        for a in range(len(subs) - 1):  # 겹치지 않게
            subs[a][1] = min(subs[a][1], subs[a + 1][0] - 0.02)
    seg = {"src": str(src.relative_to(ROOT)), "ss": round(ss, 2), "dur": dur, "subs": subs}
    vf = vfs.get(ids[i])
    seg["vf"] = (vf + "," if vf else "") + "scale=1920:1080:flags=lanczos"
    if c.get("end"):
        seg["vf"] += ",tpad=stop_mode=clone:stop_duration=2"
    segs.append(seg)
    if c.get("super") and subs:
        supers.append([i, subs[-1][0], max(1.0, subs[-1][1] - subs[-1][0]), c["super"]])

out = {"out": f"output/{ver}/Codyssey_{ver}_cuts_16x9.mp4", "segs": segs, "supers": supers}
(ROOT / f"storyboard/{ver}/timeline_{ver}c.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print("\n".join(report))
print(f"total {sum(s['dur'] for s in segs):.2f}s")
