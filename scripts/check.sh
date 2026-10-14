#!/bin/bash
# 클립 검수: 단어 타임스탬프(words.py) + 4프레임 콘택트시트(build/check/<ver>/<clip>.jpg)
# 사용: check.sh assets/v4/s01.mp4 [...]
ROOT=/Users/hyunbok/Desktop/genai-multimodal-ad
for f in "$@"; do
  v=$(basename "$(dirname "$f")"); n=$(basename "$f" .mp4); d=$ROOT/build/check/$v; mkdir -p "$d"
  len=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  args=(); k=0
  for p in 0.1 0.35 0.6 0.85; do
    ffmpeg -loglevel error -y -ss "$(awk -v l="$len" -v p="$p" 'BEGIN{print l*p}')" -i "$f" -frames:v 1 "$d/$n.$k.jpg"; args+=(-i "$d/$n.$k.jpg"); k=$((k+1))
  done
  ffmpeg -loglevel error -y "${args[@]}" -filter_complex "[0][1][2][3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,scale=1200:-1" "$d/$n.jpg"
done
"$ROOT/.venv/bin/python" "$ROOT/scripts/words.py" "$@" 2>&1 | grep -v Warn
