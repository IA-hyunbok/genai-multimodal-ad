#!/bin/bash
# 사용: shoot.sh v4            -> s01~s10 동시 생성 (프롬프트 build/v4/sNN.prompt.txt, scripts/prompts.py로 생성)
#       shoot.sh v4 s03 v2     -> 한 클립 리테이크 (프롬프트 build/v4/s03_v2.prompt.txt 있으면 그걸, 없으면 s03 원본)
ROOT=/Users/hyunbok/Desktop/genai-multimodal-ad
ver=$1; mkdir -p "$ROOT/assets/$ver"
dur() { [ -f "$ROOT/build/$ver/$1.dur" ] && { cat "$ROOT/build/$ver/$1.dur"; return; }  # cuts.py가 만든 컷 길이
  case $1 in s03|s05|s07|s09) echo 4;; s10) echo 6;; *) echo 8;; esac; }
run() { # id suffix
  local id=$1 name=$1${2:+_$2}; local pf=$ROOT/build/$ver/$name.prompt.txt
  [ -f "$pf" ] || pf=$ROOT/build/$ver/$id.prompt.txt
  "$ROOT/.venv/bin/python" "$ROOT/scripts/copa.py" video veo-3.1 "$ROOT/assets/$ver/$name.mp4" "$(cat "$pf")" "$(dur "$id")" 720p 16:9 \
    > "$ROOT/build/$ver/$name.log" 2>&1
  echo "exit=$?" >> "$ROOT/build/$ver/$name.log"
}
if [ -n "$2" ]; then run "$2" "$3"; exit; fi
for i in 01 02 03 04 05 06 07 08 09 10; do run s$i "" & done
wait
