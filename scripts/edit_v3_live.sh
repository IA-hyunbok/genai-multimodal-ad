#!/usr/bin/env bash
# v3 live 편집: veo 실사 클립 10개 -> output/v3/Codyssey_v3_live_16x9.mp4 (1920x1080 30fps, H.264/AAC)
# 재실행 가능: bash scripts/edit_v3_live.sh   (자막 PNG는 시스템 python3 + Pillow)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
FF=/opt/homebrew/bin/ffmpeg
B=build/v3edit; mkdir -p "$B/seg" output
L=assets/v3/live
OUT=output/v3/Codyssey_v3_live_16x9.mp4

# 샷별 입력 / 시작(ss) / 길이 — live_shoot_log.json final 기준
SRC=(shot01 shot02 shot03 shot04 shot05 shot06 shot07_v2 shot08_v2 shot09_v2 shot10_v2)
SS=(0 0 0.7 0 0 0 0 0 0 1.0)
DUR=(6.0 8.0 3.15 8.0 3.7 8.0 3.2 8.0 3.0 5.0)
XF=0.06   # 오디오 크로스페이드 길이
N=10

# 샷별 영상 필터: 02(레터박스+검 하단 제거) 03(상하 12% 글자 띠 제거) 10(엔드카드 글자 자리 확보: 140px 아래로 밀고 윗부분은 하늘 미러)
VF_02="crop=985:554:147:66,scale=1920:1080:flags=lanczos"
VF_03="crop=972:546:154:87,scale=1920:1080:flags=lanczos"
VF_10="scale=1920:1080:flags=lanczos,split[a][b];[a]crop=1920:140:0:0,vflip[t];[b]crop=1920:940:0:0[m];[t][m]vstack"

for i in $(seq 0 $((N-1))); do
  n=$(printf %02d $((i+1))); d=${DUR[i]}; ss=${SS[i]}
  case $n in 02) vf=$VF_02;; 03) vf=$VF_03;; 10) vf=$VF_10;; *) vf="scale=1920:1080:flags=lanczos";; esac
  "$FF" -y -v error -ss "$ss" -i "$L/${SRC[i]}.mp4" -t "$d" -an \
    -vf "$vf,fps=30,setsar=1,format=yuv420p" -c:v libx264 -crf 12 -preset medium "$B/seg/v$n.mp4"
  # 오디오: 크로스페이드용으로 XF만큼 더 뽑고(부족하면 무음 패드) 48k 스테레오
  ext=$(awk -v d="$d" -v x="$XF" 'BEGIN{print d+x}')
  "$FF" -y -v error -ss "$ss" -i "$L/${SRC[i]}.mp4" -vn -af "aresample=48000,apad=whole_dur=$ext" -t "$ext" -ac 2 "$B/seg/a$n.wav"
done

# 클립 간 레벨 맞춤: 구간별 integrated LUFS -> -20 LUFS 로 (±6dB 제한)
FC=""; IN=()
for i in $(seq 0 $((N-1))); do
  n=$(printf %02d $((i+1)))
  lufs=$("$FF" -hide_banner -nostats -i "$B/seg/a$n.wav" -af ebur128 -f null - 2>&1 | awk '/^ +I:/{v=$2} END{print v}')
  g=$(awk -v l="$lufs" 'BEGIN{g=-20-l; if(g>6)g=6; if(g<-6)g=-6; printf "%.1f", g}')
  echo "shot$n LUFS=$lufs gain=${g}dB"
  IN+=(-i "$B/seg/a$n.wav")
  FC+="[$i:a]volume=${g}dB[g$i];"
done
P=g0
for i in $(seq 1 $((N-1))); do FC+="[$P][g$i]acrossfade=d=$XF:c1=tri:c2=tri[x$i];"; P=x$i; done
TOTAL=$(awk 'BEGIN{t=0} {for(i=1;i<=NF;i++)t+=$i} END{printf "%.3f", t}' <<<"${DUR[*]}")
FADEOUT=$(awk -v t="$TOTAL" 'BEGIN{printf "%.3f", t-0.8}')
FC+="[$P]afade=t=in:d=0.25,afade=t=out:st=$FADEOUT:d=0.8,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,atrim=0:$TOTAL[aout]"
"$FF" -y -v error "${IN[@]}" -filter_complex "$FC" -map "[aout]" -ar 48000 -ac 2 "$B/audio.wav"

# 컷 연결 + 전체 동일 가벼운 시네마틱 그레이드
: > "$B/list.txt"; for i in $(seq 1 $N); do echo "file 'seg/v$(printf %02d $i).mp4'" >> "$B/list.txt"; done
"$FF" -y -v error -f concat -safe 0 -i "$B/list.txt" \
  -vf "eq=contrast=1.06:saturation=1.05:gamma=0.98,colorbalance=rs=0.015:bs=0.03:bm=0.015:gh=-0.01,format=yuv420p" \
  -c:v libx264 -crf 12 -preset medium "$B/clean.mp4"

# 자막·슈퍼·엔드카드 오버레이
python3 scripts/make_overlays_v3.py "${DUR[@]}"
OIN=(); OF=""; k=1; P="[0:v]"
while read -r png a b; do
  OIN+=(-loop 1 -framerate 30 -t "$TOTAL" -i "$png")
  OF+="${P}[$k:v]overlay=enable='between(t,$a,$b)':format=auto[o$k];"; P="[o$k]"; k=$((k+1))
done < "$B/ov/manifest.txt"
VFADE=$(awk -v t="$TOTAL" 'BEGIN{printf "%.3f", t-0.6}')
OF+="${P}fade=t=in:d=0.3,fade=t=out:st=$VFADE:d=0.6,format=yuv420p[vout]"
"$FF" -y -v error -i "$B/clean.mp4" "${OIN[@]}" -i "$B/audio.wav" -filter_complex "$OF" \
  -map "[vout]" -map "$k:a" -c:v libx264 -crf 16 -preset medium -r 30 -c:a aac -b:a 192k -movflags +faststart -t "$TOTAL" "$OUT"
echo "done: $OUT"
