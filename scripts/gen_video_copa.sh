#!/bin/bash
# COPA veo-3.1-fast Text-to-Video (씬 1,3,5) + 보너스 sora-2 (씬 3). 영상 API는 이미지 입력이 없어 프롬프트로 화풍을 맞춘다.
#   scripts/gen_video_copa.sh 1|3|5|6|3sora [out_suffix]   # 예: 재생성은 두번째 인자 _r2
# 결과: assets/video/scene{NN}_motion{suffix}.mp4 (sora는 scene03_motion_sora.mp4). 호출 기록은 assets/copa_log.jsonl
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
V="$ROOT/assets/video"
STYLE="Minimal flat vector illustration look, clean geometric shapes, smooth soft gradients, deep navy (#0B1B3F) and electric blue (#2F6BFF) palette with a warm amber (#FFB400) accent and off-white (#F5F7FB) highlights. The protagonist is a faceless dark navy silhouette wearing a flowing amber scarf. No text, no letters, no logos, no watermark, no subtitles. No human speech, no dialogue, no voice-over."
case "$1" in
1) M=veo-3.1-fast; OUT=$V/scene01_motion${2:-}.mp4
   P="Wide shot, slow dolly-in. A faceless silhouette seen from behind in a dark navy coat with an amber scarf gently fluttering, standing at a fork of many glowing electric-blue winding paths with floating blue arrow shapes, in a foggy deep navy night with soft rounded cloud banks drifting slowly. Arrows pulse softly, the mood is lost and uncertain. $STYLE Audio: soft ambient piano and synth pad music, no speech, no voice." ;;
3) M=veo-3.1-fast; OUT=$V/scene03_motion${2:-}.mp4
   P="Wide shot, slow dolly-in toward the light. A faceless silhouette in a dark navy suit with an amber scarf blowing in the wind walks up a winding path on a dark navy rocky hilltop toward a tall glowing amber doorway at the summit, warm amber light spreading along the path, sky shifting from deep navy to bright electric blue, flat white clouds drifting. Hopeful turning point. $STYLE Audio: gentle wind only, no music, no speech." ;;
5) M=veo-3.1-fast; OUT=$V/scene05_motion${2:-}.mp4
   P="Medium wide shot from behind, slow dolly-in. A faceless silhouette with an amber scarf fluttering stands at the fork of two glowing off-white roads, a distant campus building on the left and a city skyline on the right, small amber stars and gold coins floating and twinkling upward along the paths in a clear bright electric blue sky. Confident and hopeful. $STYLE Audio: light airy ambience, no speech." ;;
6) M=veo-3.1-fast; OUT=$V/scene06_motion${2:-}.mp4
   P="Minimal end card background, static camera. Smooth electric blue to deep navy gradient. In the upper-right corner a glowing amber star slowly orbits a thin off-white circle ring. The center and lower two-thirds stay completely empty. No people. $STYLE Audio: soft airy synth pad, no speech." ;;
1v2) M=veo-3.1-fast; OUT=$V/scene01_motion_v2.mp4   # 프롬프트 수정판: 구름·화살표 색, 카메라 거리 명시
   P="Wide shot, very slow dolly-in, camera stays far back. A small faceless silhouette seen from behind in a dark navy coat with an amber scarf gently fluttering, standing in the lower-left third at a fork of many glowing electric-blue (#2F6BFF) winding paths with floating saturated electric-blue arrow shapes, in a foggy deep navy night. All clouds and hills are dark navy and slate-blue shapes with a faint blue rim light; no white, beige, peach or orange clouds. The amber scarf is the only warm color. Arrows pulse softly, the mood is lost and uncertain. $STYLE Audio: soft ambient piano and synth pad music, no speech, no voice." ;;
5v2) M=veo-3.1-fast; OUT=$V/scene05_motion_v2.mp4   # 프롬프트 수정판: 갈림길 구도 고정, 포크/식기 형상 금지
   P="Wide shot from behind, camera locked with only a very slow subtle push-in, never close to the character. A small faceless silhouette with an amber scarf fluttering stands at the bottom center where one road splits into two separate glowing off-white ribbon-like winding roads in a Y shape, no lane markings, no asphalt. The left road leads to a small distant campus building, the right road leads to a city skyline. Small amber stars and gold coins float and twinkle upward along both roads in a clear bright electric blue sky with deep navy hills. No forks, knives, spoons or cutlery shapes anywhere. Confident and hopeful. $STYLE Audio: light airy ambience, no speech." ;;
3q) M=veo-3.1; OUT=$V/scene03_motion_veo31.mp4   # 보너스: 비 fast 모델 비교 (프롬프트는 씬 3과 동일)
   P="Wide shot, slow dolly-in toward the light. A faceless silhouette in a dark navy suit with an amber scarf blowing in the wind walks up a winding path on a dark navy rocky hilltop toward a tall glowing amber doorway at the summit, warm amber light spreading along the path, sky shifting from deep navy to bright electric blue, flat white clouds drifting. Hopeful turning point. $STYLE Audio: gentle wind only, no music, no speech." ;;
3sora) M=sora-2; OUT=$V/scene03_motion_sora.mp4
   P="Wide shot, slow dolly-in toward the light. A faceless silhouette in a dark navy suit with an amber scarf blowing in the wind walks up a winding path on a dark navy rocky hilltop toward a tall glowing amber doorway at the summit, warm amber light spreading along the path, sky shifting from deep navy to bright electric blue, flat white clouds drifting. Hopeful turning point. $STYLE Audio: gentle wind only, no music, no speech." ;;
*) echo "usage: $0 1|3|5|6|3sora [suffix]"; exit 1 ;;
esac
RES=720p; [ "$M" = sora-2 ] && RES=1280x720  # sora-2는 1280x720 표기만 허용
"$PY" "$ROOT/scripts/copa.py" video "$M" "$OUT" "$P" 8 $RES
