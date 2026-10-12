#!/usr/bin/env bash
# COPA gpt-image-2 로 6개 씬 재생성. 사용: scripts/gen_images_copa.sh [씬번호|all] [gpt|gpt_v2]
# 호출은 assets/copa_log.jsonl 에 자동 기록된다.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
OUT="$ROOT/assets/images"
MODEL=gpt-image-2
SIZE=1536x1024

# style_lock: 모든 씬 동일 고정
STYLE="Strict flat 2D vector illustration, solid color shapes only, no painterly texture, no photorealism, no 3D render, no gradients except smooth sky/background. Palette limited to deep navy #0B1B3F, electric blue #2F6BFF, warm amber #FFB400, off-white #F5F7FB. Any human is a faceless solid-color silhouette with no facial features at all (no eyes, nose, mouth). The single protagonist always wears a bright amber #FFB400 scarf as the identifying marker. Wide cinematic 3:2 composition. Absolutely no text, no letters, no numbers, no logo, no watermark."

prompt() { case "$1" in
1) echo "A single faceless silhouette seen from behind, wearing an amber scarf, small figure in the lower-left third, standing at a fork of many glowing blue paths and arrow-like shards in a foggy deep navy night sky. Feeling lost and uncertain." ;;
2) echo "Medium close-up of two faceless hands resting still on a laptop keyboard on a desk, a stack of course cards, a few coins and an hourglass beside it, dim navy room with cold electric-blue window light, a sense of being stuck. No face visible. A small amber scarf end is visible hanging on the chair edge." ;;
3) echo "Wide shot: one faceless silhouette wearing an amber scarf, alone in the foreground, stepping along a dark path toward a large glowing amber doorway opening at the path's end. Sky shifts from deep navy to electric blue. Exactly one human figure in the whole image. Hopeful turning point." ;;
4) echo "Medium wide shot of four faceless solid-color silhouettes (blank smooth heads, no facial features, flat vector shapes) around a round table, all pointing together at a glowing screen of floating geometric code blocks. One of them wears an amber scarf. Bright off-white and blue collaborative studio, floating geometric blocks, warm friendly mood." ;;
5) echo "Wide shot: a faceless silhouette wearing an amber scarf seen from behind at the start of two diverging glowing roads, one short and one long, small amber stars and coins floating along the paths, clear bright blue sky with a distant campus and city skyline silhouette, confident hopeful mood." ;;
6) echo "Minimal end card background: smooth electric blue to deep navy gradient, one small amber star orbiting a faint thin circle placed in the far upper-right corner. The entire center and lower two-thirds are completely empty open space for text overlay. No people." ;;
esac; }

# 1차(gpt) 검수 후 일관성이 깨진 씬만 1회 재생성(gpt_v2)
prompt_v2() { case "$1" in
2) echo "Medium close-up framed tightly on the desk only: two faceless hands resting still on a laptop keyboard, the person's body cut off above the wrist so no head and no torso are visible. Beside the laptop a stack of course cards, a few coins and an hourglass. Dim navy room with a cold electric-blue window behind. A small amber scarf end hangs over the chair edge as the identifying marker." ;;
6) echo "Minimal end card background: smooth electric blue to deep navy gradient. In the upper-right corner a clearly visible amber star with a soft glow orbiting a thin off-white circle ring, the star about 4 percent of image width. The entire center and lower two-thirds are completely empty open space for text overlay. No people." ;;
esac; }

gen() { # $1=씬번호 $2=variant
  local n; n=$(printf %02d "$1")
  "$PY" "$ROOT/scripts/copa.py" image "$MODEL" "$OUT/scene${n}_img_$2.png" "$(if [ "$2" = gpt_v2 ]; then prompt_v2 "$1"; else prompt "$1"; fi) $STYLE" "$SIZE"
}

SCENES="${1:-all}"; VAR="${2:-gpt}"
if [ "$SCENES" = all ]; then for i in 1 2 3 4 5 6; do gen "$i" "$VAR"; done; else gen "$SCENES" "$VAR"; fi
