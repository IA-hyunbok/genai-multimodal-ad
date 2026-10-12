#!/bin/bash
# COPA gpt-4o-mini-tts 내레이션 생성. 사용:
#   scripts/gen_audio_copa.sh compare        # 씬1 문장으로 voice 비교 (assets/audio/_voice_cmp/)
#   VOICE=nova scripts/gen_audio_copa.sh     # 전 씬 생성 (길이 초과 시 speed 1.05~1.2 재생성)
# 결과는 assets/audio/scene{NN}_vo_gpt.mp3 + audio_log.json 추가. 기존 gTTS 파일은 그대로 둔다.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
OUT="$ROOT/assets/audio"
MODEL=gpt-4o-mini-tts

text_of() { "$PY" -c "import json,sys;print(json.load(open('$ROOT/storyboard/storyboard.json'))['scenes'][int(sys.argv[1])-1][sys.argv[2]])" "$1" "$2"; }
dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
log() { # file voice speed text duration scene_dur status summary
  "$PY" - "$OUT/audio_log.json" "$@" <<'EOF'
import json, sys, time
p, f, voice, speed, text, d, sd, st, sm = sys.argv[1:]
L = json.load(open(p))
L.append({"file": f, "tool": "COPA gpt-4o-mini-tts", "voice": voice, "speed": float(speed), "text": text,
          "duration": round(float(d), 2), "scene_duration": float(sd), "status": st, "summary": sm,
          "time": time.strftime("%Y-%m-%d %H:%M:%S")})
json.dump(L, open(p, "w"), ensure_ascii=False, indent=2)
EOF
}

if [ "${1:-}" = compare ]; then
  mkdir -p "$OUT/_voice_cmp"; T="$(text_of 1 narration)"
  for v in nova shimmer alloy; do
    "$PY" "$ROOT/scripts/copa.py" tts $MODEL "$OUT/_voice_cmp/scene01_$v.mp3" "$T" $v 1.0
    echo "$v $(dur "$OUT/_voice_cmp/scene01_$v.mp3")"
  done
  exit 0
fi

VOICE="${VOICE:?VOICE 필요}"
for n in 1 2 3 4 5 6; do
  NN=$(printf %02d $n); F="$OUT/scene${NN}_vo_gpt.mp3"
  T="$(text_of $n narration)"; SD="$(text_of $n duration_sec)"
  for sp in 1.0 1.05 1.1 1.15 1.2; do
    "$PY" "$ROOT/scripts/copa.py" tts $MODEL "$F" "$T" $VOICE $sp >/dev/null || { log "$(basename "$F")" $VOICE $sp "$T" 0 "$SD" failed "COPA 호출 실패 speed=$sp"; continue; }
    D=$(dur "$F")
    if awk "BEGIN{exit !($D <= $SD - 0.4)}"; then
      log "$(basename "$F")" $VOICE $sp "$T" "$D" "$SD" ok "${D}s / 씬 ${SD}s, speed $sp"; break
    fi
    log "$(basename "$F")" $VOICE $sp "$T" "$D" "$SD" too_long_retry "${D}s / 씬 ${SD}s, speed $sp -> 초과"
  done
  echo "scene$NN $(dur "$F") / $SD"
done
