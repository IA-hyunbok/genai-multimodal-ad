#!/usr/bin/env bash
# 통합 편집(컷·자막·색보정·오디오 레벨) 전용. 재실행 가능: bash scripts/assemble.sh
# 입력: assets/images 채택본, assets/video/sceneNN_motion.mp4(있으면 우선 사용), assets/audio/sceneNN_vo_gpt.mp3, bgm_veo.m4a(있으면)
# 출력: output/Codyssey_GenAI_Ad_16x9.mp4, output/Codyssey_GenAI_Ad_9x16.mp4
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FF=/opt/homebrew/bin/ffmpeg; FP=/opt/homebrew/bin/ffprobe
B=build; mkdir -p "$B" output

# 씬 정의 (storyboard.json duration_sec 와 동일). 최종 이미지 = generation_log.json verdict=채택 (gpt-image, 1536x1024, 워터마크 없음)
DUR=(7 7 8 8 9 5)
IMG=(scene01_img_gpt scene02_img_gpt_v2 scene03_img_gpt scene04_img_gpt scene05_img_gpt scene06_img_gpt_v2)
# 모션: in=줌인, out=줌아웃, pan=좌→우 패닝 (COPA 영상 503 전 씬 실패 -> motion.mp4 없으면 zoompan)
MOT=(in pan in out in in)
FPS=30; N=6
TOTAL=0; START=()
for d in "${DUR[@]}"; do START+=("$TOTAL"); TOTAL=$((TOTAL+d)); done

# 1) 씬별 클립: 영상 있으면 정규화, 없으면 16:9 중앙 크롭(1536x864) -> 업스케일 -> zoompan
for i in $(seq 0 $((N-1))); do
  n=$(printf %02d $((i+1))); f=$((DUR[i]*FPS)); out="$B/clip$n.mp4"
  V=$(python3 -c "import json;print(json.load(open('assets/video/video_log.json'))['final'].get('$((i+1))',''))")
  # 씬1 클립만 가벼운 보정(시안 길/밝은 회청 구름이 이웃 네이비 씬보다 떠서 채도·밝기만 낮춤)
  VEQ=null; [ "$n" = 01 ] && VEQ="eq=brightness=-0.03:saturation=0.9"
  if [ -n "$V" ] && [ -f "$V" ]; then
    # AI 영상 클립: 무음, 씬 길이로 트림(짧으면 마지막 프레임 유지), 1920x1080 30fps
    "$FF" -y -v error -i "$V" -vf "scale=1920:1080:flags=lanczos,$VEQ,fps=$FPS,tpad=stop_mode=clone:stop_duration=${DUR[i]},format=yuv420p" -t "${DUR[i]}" -an -c:v libx264 -crf 14 "$out"
    continue
  fi
  case "${MOT[i]}" in
    in)  Z="z='1+0.12*on/$f':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'";;
    out) Z="z='1.12-0.12*on/$f':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'";;
    pan) Z="z=1.15:x='(iw-iw/zoom)*on/$f':y='ih/2-ih/zoom/2'";;
  esac
  "$FF" -y -v error -i "assets/images/${IMG[i]}.png" -vf "crop=1536:864:0:80,scale=5760:3240:flags=lanczos,zoompan=${Z}:d=$f:s=1920x1080:fps=$FPS,format=yuv420p" -frames:v "$f" -c:v libx264 -crf 14 "$out"
done

# 2) 컷 연결 + 전체 동일 색보정 + 페이드 인/아웃 (자막 없는 clean 영상)
: > "$B/list.txt"; for i in $(seq 1 $N); do echo "file 'clip$(printf %02d $i).mp4'" >> "$B/list.txt"; done
"$FF" -y -v error -f concat -safe 0 -i "$B/list.txt" \
  -vf "eq=contrast=1.05:saturation=1.08:gamma=0.98,colorbalance=rs=0.01:bs=0.03:bm=0.02,fade=t=in:d=0.5,fade=t=out:st=$((TOTAL-1)):d=1,fps=$FPS,format=yuv420p" \
  -c:v libx264 -crf 14 -preset medium "$B/clean.mp4"

# 3) 오디오: 내레이션을 씬 시작+0.3초에 배치, BGM 있으면 -19dB + 내레이션 덕킹 + 끝 페이드, loudnorm -16 LUFS
IN=(); FC=""; MIX=""
for i in $(seq 0 $((N-1))); do
  n=$(printf %02d $((i+1))); IN+=(-i "assets/audio/scene${n}_vo_gpt.mp3")
  ms=$(( (START[i]*10+3)*100 ))
  FC+="[$i:a]aresample=48000,adelay=${ms}|${ms}[v$i];"; MIX+="[v$i]"
done
FC+="${MIX}amix=inputs=$N:normalize=0:duration=longest,apad=whole_dur=$TOTAL[vo];"
BGMF=${BGM:-$(ls assets/audio/bgm_veo.* 2>/dev/null | head -1 || true)}
if [ -n "$BGMF" ]; then
  # 8초 BGM을 1초 크로스페이드로 7회 이어붙여 TOTAL초 이상 확보
  XF="[0:a]aresample=48000[l0];"; P=l0
  for k in 1 2 3 4 5 6; do XF+="[0:a]aresample=48000[c$k];[$P][c$k]acrossfade=d=1[l$k];"; P=l$k; done
  "$FF" -y -v error -i "$BGMF" -filter_complex "${XF%;}" -map "[$P]" -ar 48000 "$B/bgm_loop.wav"
  IN+=(-i "$B/bgm_loop.wav")
  FC+="[vo]asplit=2[vo1][sc];[$N:a]aresample=48000,atrim=0:$TOTAL,volume=-19dB[bg];"
  FC+="[bg][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[duck];"
  FC+="[duck]afade=t=in:d=2,afade=t=out:st=$((TOTAL-3)):d=3[bgf];[vo1][bgf]amix=inputs=2:normalize=0:duration=first[m];"
else
  echo "[info] BGM 없음(bgm_veo.m4a 미생성) -> 내레이션만 믹스" >&2
  FC+="[vo]anull[m];"
fi
FC+="[m]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
"$FF" -y -v error "${IN[@]}" -filter_complex "$FC" -map "[a]" -t "$TOTAL" -ar 48000 -c:a pcm_s16le "$B/audio.wav"

# 4) 자막/라벨/엔드카드 PNG 오버레이 + 인코딩
python3 scripts/make_overlays.py
render() { # $1=layout(16x9|9x16) $2=output
  local lay=$1 out=$2 args=() fc="" k=1 prev="base"
  if [ "$lay" = 16x9 ]; then fc="[0:v]null[base];"
  else fc="[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.08[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"; fi
  args=(-i "$B/clean.mp4")
  add() { # png start end
    args+=(-i "$1"); fc+="[$prev][$k:v]overlay=enable='between(t,$2,$3)'[o$k];"; prev="o$k"; k=$((k+1)); }
  for i in $(seq 0 $((N-1))); do
    n=$(printf %02d $((i+1))); s=${START[i]}; e=$((s+DUR[i]))
    L=$("$FP" -v error -show_entries format=duration -of csv=p=0 "assets/audio/scene${n}_vo_gpt.mp3")
    add "$B/ov_${lay}_sub${n}.png" "$(echo "$s+0.2" | bc)" "$(echo "$s+0.4+$L" | bc)"
    [ -f "$B/ov_${lay}_deco${n}.png" ] && add "$B/ov_${lay}_deco${n}.png" "$(echo "$s+0.3" | bc)" "$e"
  done
  "$FF" -y -v error "${args[@]}" -i "$B/audio.wav" -filter_complex "${fc%;}" -map "[$prev]" -map "$((k)):a" \
    -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -r $FPS -c:a aac -b:a 192k -t "$TOTAL" -movflags +faststart "$out"
}
render 16x9 output/Codyssey_GenAI_Ad_16x9.mp4
render 9x16 output/Codyssey_GenAI_Ad_9x16.mp4

# 5) 검증 출력
for f in output/Codyssey_GenAI_Ad_*.mp4; do
  echo "== $f"; "$FP" -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration -of default=nw=1 "$f"
done
