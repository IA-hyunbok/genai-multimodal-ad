#!/bin/bash
# 사용: shoot_v3_live.sh            -> 10샷 전부 백그라운드 동시 생성
#       shoot_v3_live.sh shot04 v2  -> 리테이크(프롬프트는 build/v3live/shot04_v2.prompt.txt)
ROOT=/Users/hyunbok/Desktop/genai-multimodal-ad
PY=$ROOT/.venv/bin/python
mkdir -p "$ROOT/assets/v3/live" "$ROOT/build/v3live"

run() { # id suffix
  local id=$1 suf=$2 name=$1${2:+_$2}
  local pf=$ROOT/build/v3live/$name.prompt.txt
  if [ -z "$suf" ]; then
    $PY - "$id" > "$pf" <<'EOF'
import json,sys
d=json.load(open('/Users/hyunbok/Desktop/genai-multimodal-ad/storyboard/v3/live_shotlist.json'))
print(next(s for s in d['shots'] if s['id']==sys.argv[1])['prompt'],end='')
EOF
  fi
  local meta
  meta=$($PY -c "
import json,sys
d=json.load(open('$ROOT/storyboard/v3/live_shotlist.json'))
s=next(s for s in d['shots'] if s['id']=='$id');print(s['model'],s['seconds'])")
  set -- $meta
  $PY "$ROOT/scripts/copa.py" video "$1" "$ROOT/assets/v3/live/$name.mp4" "$(cat "$pf")" "$2" 720p 16:9 \
    > "$ROOT/build/v3live/$name.log" 2>&1
  echo "exit=$?" >> "$ROOT/build/v3live/$name.log"
}

if [ -n "$1" ]; then run "$1" "$2"; exit; fi
for i in 01 02 03 04 05 06 07 08 09 10; do run shot$i "" & done
wait
