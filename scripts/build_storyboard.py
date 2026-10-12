#!/usr/bin/env python3
"""storyboard.json + assets/*/*_log.json + output/ 를 근거로 storyboard/storyboard.html 생성 후 Chrome headless로 PDF 변환.
실행: python3 scripts/build_storyboard.py   (썸네일·최종 영상 프레임을 ffmpeg로 storyboard/thumbs/ 에 생성)
문서 내용은 로그에 기록된 사실만 사용한다. 재실행 가능.
"""
import html, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SB = json.loads((ROOT / "storyboard/storyboard.json").read_text())
IMGLOG = json.loads((ROOT / "assets/images/generation_log.json").read_text())
AUDLOG = json.loads((ROOT / "assets/audio/audio_log.json").read_text())
VLOG = json.loads((ROOT / "assets/video/video_log.json").read_text())
FF, FP = "/opt/homebrew/bin/ffmpeg", "/opt/homebrew/bin/ffprobe"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TH = ROOT / "storyboard/thumbs"
TH.mkdir(exist_ok=True)
e = html.escape

FINAL = IMGLOG["final"]  # 최종 채택 = COPA gpt-image-2 (scripts/assemble.sh 의 IMG 배열과 동일)
OLD = {1: "scene01_img_v2.png", 2: "scene02_img_v2.png", 3: "scene03_img_v2.png", 4: "scene04_img_v3.png", 5: "scene05_img_v2.png", 6: "scene06_img_v2.png"}  # 1차 Pollinations 채택본
MOTION = {2: "zoompan 좌→우 패닝", 4: "zoompan 줌아웃", 6: "zoompan 줌인"}  # 씬 1·3·5 는 storyboard.json 의 video(COPA veo T2V)


def thumb(name):
    """gpt 이미지(1536x1024)는 assemble.sh 와 같은 중앙 16:9 크롭, Pollinations 이미지는 워터마크 제거 크롭(942:530:41:0)."""
    out = TH / name.replace(".png", ".jpg")
    crop = "crop=1536:864:0:80" if "_gpt" in name else "crop=942:530:41:0"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(ROOT / "assets/images" / name), "-vf",
                    f"{crop},scale=720:-1", "-q:v", "3", str(out)], check=True)
    return f"thumbs/{out.name}"


def vthumb(name, t=4):
    """영상 클립(assets/video)의 t초 프레임 -> thumbs/{name}.jpg"""
    out = TH / name.replace(".mp4", ".jpg")
    subprocess.run([FF, "-y", "-v", "error", "-ss", str(t), "-i", str(ROOT / "assets/video" / name),
                    "-frames:v", "1", "-vf", "scale=720:-1", "-q:v", "3", str(out)], check=True)
    return f"thumbs/{out.name}"


def frame(lay, t):
    """최종 mp4 에서 프레임 캡처 -> thumbs/final_{lay}_t{t}.jpg"""
    out = TH / f"final_{lay}_t{t}.jpg"
    subprocess.run([FF, "-y", "-v", "error", "-ss", str(t), "-i", str(ROOT / f"output/Codyssey_GenAI_Ad_{lay}.mp4"),
                    "-frames:v", "1", "-vf", "scale=-2:480", "-q:v", "3", str(out)], check=True)
    return f"thumbs/{out.name}"


def probe(p):
    o = subprocess.run([FP, "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration,size",
                        "-of", "json", str(p)], capture_output=True, text=True, check=True).stdout
    return json.loads(o)


# 실제 사용된 내레이션(씬 5는 길이 초과로 축약됨) = audio_log 마지막 ok 항목
VO = {}
for a in AUDLOG:
    if a.get("status") == "ok" and a["file"].endswith("_vo_gpt.mp3"):
        VO[int(a["file"][5:7])] = a
vid = {}
for lay in ("16x9", "9x16"):
    p = ROOT / f"output/Codyssey_GenAI_Ad_{lay}.mp4"
    j = probe(p)
    v = next(s for s in j["streams"] if "width" in s)
    a = next(s for s in j["streams"] if "sample_rate" in s)
    vid[lay] = (p.name, float(j["format"]["duration"]), v, a, int(j["format"]["size"]))

b, c, sl = SB["brand"], SB["campaign"], SB["style_lock"]
CSS = """
@page{size:A4;margin:14mm 13mm}
*{box-sizing:border-box}
body{font-family:'Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif;color:#0B1B3F;font-size:9pt;line-height:1.4;margin:0}
h1{font-size:26pt;margin:0 0 4mm}h2{font-size:14pt;border-bottom:2px solid #2F6BFF;padding-bottom:1.5mm;margin:0 0 3mm}h3{break-after:avoid;font-size:10.5pt;margin:3mm 0 1mm;color:#2F6BFF}
.cover{height:262mm;background:linear-gradient(160deg,#0B1B3F,#2F6BFF);color:#F5F7FB;padding:30mm 16mm;border-radius:4mm;page-break-after:always}
.cover h1{font-size:34pt;margin-top:45mm}.cover .sub{font-size:14pt;color:#FFB400}.cover p{font-size:10.5pt}
section{page-break-before:always}section.nb{page-break-before:avoid;margin-top:6mm}
table{border-collapse:collapse;width:100%;margin:2mm 0;font-size:8.6pt}th,td{border:1px solid #c8d1e6;padding:1.4mm 2mm;vertical-align:top;text-align:left}
th{background:#eaf0ff;white-space:nowrap}
.card{border:1.5px solid #2F6BFF;border-radius:3mm;padding:3mm;margin:0 0 5mm;page-break-inside:avoid;display:flex;gap:4mm}
.card .th{width:62mm;flex:none}.card img{width:62mm;border-radius:1.5mm;display:block}
.card .t{font-size:8pt;color:#555;margin-top:1mm}.card table{font-size:8.2pt;margin:0}
.card .hd{font-weight:700;font-size:11pt;margin-bottom:1.5mm}
.pr{font-family:Menlo,monospace;font-size:7pt;line-height:1.35;color:#233}
.ba{display:flex;gap:4mm;margin:2mm 0 3mm}.ba div{flex:1;page-break-inside:avoid}.ba img{width:100%;border-radius:1.5mm}.ba b{display:block;margin-bottom:1mm}
.warn{background:#fff6e0;border-left:4px solid #FFB400;padding:2mm 3mm;margin:2mm 0}
.fl{display:flex;align-items:stretch;gap:2mm;margin:3mm 0}.fl div{flex:1;border:1.5px solid #2F6BFF;border-radius:2mm;padding:2mm;font-size:8.4pt}.fl div.ar{flex:none;border:0;padding:0;align-self:center;font-size:14pt;color:#2F6BFF}
.fl b{display:block;color:#2F6BFF;margin-bottom:1mm}
.fr{display:flex;gap:3mm}.fr img{height:48mm;border-radius:1.5mm}
code{font-family:Menlo,monospace;font-size:8pt}
"""

o = []
w = o.append
w(f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>코디세이 스토리보드</title><style>{CSS}</style></head><body>")
# 표지
w(f"""<div class='cover'><div class='sub'>GenAI 기초 2 · 멀티모달 콘텐츠 제작 스토리보드</div><h1>{e(b['name'])}<br>AI 여정 광고 캠페인</h1>
<p>슬로건 : {e(c['slogan'])}<br>광고 목적 : {e(c['objective'])}</p>
<p style='margin-top:20mm'>최종 영상 : Codyssey_GenAI_Ad_16x9.mp4 (1920x1080) / Codyssey_GenAI_Ad_9x16.mp4 (1080x1920)<br>
총 {vid['16x9'][1]:.0f}초 · 6씬 · 이미지(코디세이 COPA 게이트웨이 gpt-image-2), 영상(씬 1·3·5: COPA veo T2V, 씬 2·4·6: 정지 이미지+ffmpeg 패닝/줌), 음성(gpt-4o-mini-tts), BGM(veo 생성 오디오)</p></div>""")

# 1 브랜드
w(f"""<h2>1. 브랜드 아이덴티티</h2>
<table><tr><th>브랜드</th><td>{e(b['name'])} — 운영: {e(b['operator'])}</td></tr>
<tr><th>정체</th><td>{e(b['what_it_is'])}</td></tr>
<tr><th>프로그램</th><td>{e(' / '.join(b['programs']))}</td></tr>
<tr><th>타겟</th><td>{e(b['target'])}</td></tr>
<tr><th>톤앤매너</th><td>{e(b['tone_and_manner'])}</td></tr>
<tr><th>USP</th><td>{'<br>'.join('· '+e(u) for u in b['usp'])}</td></tr>
<tr><th>출처</th><td>{'<br>'.join(e(s) for s in b['sources'])}</td></tr>
<tr><th>사실 확인 한계</th><td>{e(b['fact_caveats'])}</td></tr></table>
<h2 style='margin-top:6mm'>2. 캠페인 목표 · 핵심 메시지</h2>
<table><tr><th>광고 목적</th><td>{e(c['objective'])}</td></tr>
<tr><th>핵심 메시지(1문장)</th><td><b>{e(c['core_message'])}</b></td></tr>
<tr><th>슬로건 / CTA</th><td>{e(c['slogan'])} / {e(c['cta'])}</td></tr>
<tr><th>구조</th><td>기(문제) 씬1 → 승(심화) 씬2 → 전(전환) 씬3 → 결(해결) 씬4·5 → 브랜드/CTA 엔드카드 씬6(마지막 5초)</td></tr></table>""")

# 3 파이프라인
w("""<h2 style='margin-top:6mm'>3. 제작 파이프라인</h2>
<div class='fl'><div><b>① 기획</b>브랜드 조사(공식 출처만)<br>storyboard.json 확정<br>style_lock·네이밍 규칙 결정<br>→ 이미지 전에 스토리보드를 먼저 확정</div><div class='ar'>▶</div>
<div><b>② 생성</b>1차: Pollinations·gTTS·HF Space<br>2차: scripts/copa.py(COPA 게이트웨이)<br>gen_images_copa.sh / gen_audio_copa.sh / gen_video_copa.sh<br>모든 호출·실패를 로그에 기록</div><div class='ar'>▶</div>
<div><b>③ 검수</b>이미지를 육안 확인<br>채택/불합격 판정을 generation_log.json 에 기록<br>불합격 시 프롬프트 수정 후 재생성(씬당 최대 2회)</div><div class='ar'>▶</div>
<div><b>④ 편집·통합</b>assemble.sh (ffmpeg)<br>veo 클립 정규화·zoompan<br>씬 1 가벼운 eq, 전체 동일 색보정·페이드<br>내레이션+BGM 믹스(덕킹)<br>make_overlays.py 자막·엔드카드<br>16:9 / 9:16 출력</div></div>
<table><tr><th>단계 사이 원칙</th><td>사내 쿼터(크레딧)가 한정되어 있으므로 이미지는 씬당 최대 2회, 영상은 씬당 최대 2회로 제한. 비용이 큰 영상은 이미지 검수·스토리보드 확정 뒤에만 시도. 편집 도구(ffmpeg)는 컷·자막·색보정·오디오 레벨 용도로만 사용.</td></tr></table>""")

# 4 도구
w(f"""<h2 style='margin-top:6mm'>4. 사용 도구 · 선택 이유 · 대체 도구</h2>
<table><tr><th>구분</th><th>최종 사용 도구</th><th>비교·시도·실패</th><th>선택 이유</th><th>대체 도구</th></tr>
<tr><td>이미지</td><td><b>코디세이 COPA 게이트웨이 gpt-image-2</b> (1536x1024, 씬 6장 + 재생성 2회 = 8회)</td><td>1차·비교: Pollinations(요청 model=flux, 실제 sana). 6씬 나란히 비교는 8장</td><td>화풍·팔레트·"얼굴 없는 실루엣" 지시 준수율이 높아 앰버 스카프 식별자와 플랫 벡터 화풍이 6씬에 일관됨(로그 verdict). 워터마크 없음, 해상도 1536x1024</td><td>COPA imagen-4, gpt-image-1.5, gemini-2.5-flash-image(미사용), Pollinations</td></tr>
<tr><td>비디오</td><td><b>COPA veo-3.1-fast</b> T2V(씬 1·5, 8초·720p·24fps·오디오 포함) + <b>veo-3.1</b>(씬 3 채택). 씬 2·4·6은 정지 이미지 + ffmpeg zoompan</td><td>씬 3은 같은 프롬프트로 veo-3.1-fast와 veo-3.1을 모두 생성해 비교(8장). 씬 1·5는 v1→v2 프롬프트 수정(7장). <b>sora-2</b>는 OpenAI가 2026-09-24에 Videos API를 제거해 실패. 키 등록 전에는 veo도 전부 503이었음(8장 도구 접근성 대응). 1차 HF Spaces 4종×3씬은 ZeroGPU 쿼터 실패</td><td>COPA 영상 API는 이미지 입력이 없어 Text-to-Video만 가능. veo는 영상과 오디오를 함께 생성하고, 쿼터 보호를 위해 fast 모델로 시작해 씬 3만 비교용으로 veo-3.1을 추가. 인물 왜곡 위험이 낮은 풍경 씬 1·3·5만 대상</td><td>sora-2(종료), HF Spaces i2v(1차), ffmpeg zoompan(씬 2·4·6 실사용)</td></tr>
<tr><td>오디오(음성)</td><td><b>COPA gpt-4o-mini-tts</b> voice=nova, speed 1.0</td><td>씬 1 문장으로 nova/shimmer/alloy 3종 비교 후 nova 선택. 1차 gTTS(비교본 보존), edge-tts는 HTTP 403 실패</td><td>speed 1.0에서 6씬 모두 씬 길이 이내(4.4~7.3초)라 gTTS 때처럼 atempo 가속·문장 축약이 필요 없었음. 3종 중 nova 선택(점수 기록 없음, 비교 파일 _voice_cmp 보존)</td><td>COPA tts-1-hd, gemini-2.5-flash-tts, gTTS, edge-tts</td></tr>
<tr><td>BGM</td><td><b>veo-3.1-fast 생성 오디오</b>: 씬 1 v2 클립의 오디오를 추출(bgm_veo.m4a, 8초)해 1초 크로스페이드로 7회 이어 붙여 44초로 사용, -19dB·내레이션 덕킹·끝 3초 페이드</td><td>1차 HF MusicGen/Stable Audio Open 실패. 씬 1 v1 오디오는 bgm_veo_v1.m4a로 보존(미채택). 씬 3·5 클립 오디오는 쓰지 않음(-an)</td><td>별도 BGM 모델 호출 없이 영상 호출의 부산물로 청각 AI 요소를 확보(쿼터 절약). 한계: 청취 검수 못 함, volumedetect 평균 -16.9dB·피크 -0.8dB만 확인. 8초 반복이라 반복감이 있을 수 있음</td><td>MusicGen / Stable Audio Open</td></tr>
<tr><td>통합 편집</td><td>ffmpeg 8 + Pillow(자막 PNG)</td><td>—</td><td>무료·재현 가능. drawtext 필터가 없어 자막을 PIL 투명 PNG로 렌더링해 overlay</td><td>—</td></tr></table>
<h3>Text-to-Image vs Image-to-Video vs Text-to-Video 선택 기준</h3>
<table><tr><td>T2I는 구도·화풍을 확정하는 저비용 단계라 이미지를 먼저 여러 번 검수한다. I2V는 확정 이미지를 움직이게 해 일관성에 가장 유리하지만, <b>COPA 영상 API는 이미지 입력을 받지 않아</b> 이번 라운드에서는 선택할 수 없었다(1차 HF I2V는 쿼터 실패). 그래서 영상은 T2V로 가고, 일관성은 영상 프롬프트에 팔레트 hex·플랫 벡터·얼굴 없는 실루엣·앰버 스카프·카메라 거리를 명시해 맞췄다.
<b>실제 결과:</b> 플랫 벡터 화풍, 네이비·블루·앰버 팔레트 계열, 앰버 스카프, 얼굴 없음은 6개 클립 모두 유지됐다. 그러나 구도와 색은 정지 이미지와 다르게 나왔다(씬 1: 여러 갈래 길 → 한 줄기 길+큰 화살표, 씬 3: 네이비 길 → 앰버 길·크림색 구름, 씬 5: 별·동전이 과다하고 인물이 갈림길을 가림). 프롬프트 수정(v2)은 구름색·식기 형상·인물 크기를 잡았지만 구도 자체는 잡지 못했다. 정지 이미지 그대로 움직여야 한다면 I2V가 필요하고, 이번 선택은 "게이트웨이가 지원하는 방식 안에서 최대한 맞춘 것"이다.</td></tr></table>""")

# 5 스타일 고정
w(f"""<h2 style='margin-top:6mm'>5. 스타일 고정 파라미터</h2>
<table><tr><th>seed</th><td>1차 Pollinations: {sl['seed']} 전 씬 고정. 2차 COPA: seed 파라미터 없음(copa.py 인자에 없음) — 모든 프롬프트 끝에 같은 STYLE 문구를 붙여 일관성 확보</td></tr>
<tr><th>팔레트</th><td>navy #0B1B3F · electric blue #2F6BFF · amber #FFB400(주인공 앰버 스카프 식별자) · teal #19C3B1 · off-white #F5F7FB</td></tr>
<tr><th>2차 STYLE 접미(전 씬 동일)</th><td class='pr'>{e(sl['round2_style_suffix'])}</td></tr>
<tr><th>1차 style_suffix</th><td class='pr'>{e(sl['style_suffix'])}</td></tr>
<tr><th>생성 규격</th><td>최종 gpt-image-2 1536x1024(3:2) → 중앙 16:9(1536x864) 크롭 → 1920x1080 업스케일. veo 클립은 8초·720p·16:9 요청, 1280x720 24fps 수신 → 1920x1080 30fps로 정규화. 출력 30fps H.264/AAC. 9:16 은 1080x1920(16:9 중앙 배치 + 블러 배경). 1차 Pollinations는 1024x576 수신, 워터마크 크롭 후 업스케일</td></tr>
<tr><th>실제로 효과 있던 것</th><td>1차: 긴 style_suffix는 sana가 거의 무시, 짧은 'flat vector' 선두 프롬프트가 나았음. 2차: gpt-image-2는 같은 긴 STYLE 문구를 그대로 따라 6씬 화풍·스카프가 일관됨. 단, 인물 스케일 지시("몸통 프레임 밖")는 재생성이 필요했음(씬 2)</td></tr>
<tr><th>일관성 한계(정직 기록)</th><td>cref/sref·ControlNet 미사용. 씬 5 건물 묘사가 다른 씬보다 정교하고 씬 6 별이 우상단 코너에 치우침(로그 기록). 씬 2는 스카프가 의자에 걸린 소품으로만 등장</td></tr>
<tr><th>파일 네이밍</th><td><code>scene{{NN}}_{{kind}}_{{variant}}.{{ext}}</code> kind = img | motion | vo. 1차 scene01_img_v2.png / scene01_vo.mp3, 2차 scene01_img_gpt.png, 수정본 scene02_img_gpt_v2.png / scene01_vo_gpt.mp3. 영상 scene01_motion.mp4(1차 시도) / scene01_motion_v2.mp4(프롬프트 수정본) / scene03_motion_veo31.mp4(모델 변경), BGM bgm_veo.m4a. 최종 output/Codyssey_GenAI_Ad_{{16x9|9x16}}.mp4</td></tr></table>""")

# 6 씬 카드
w("<section><h2>6. 씬별 카드 (최종 채택 소스)</h2>")
for sc in SB["scenes"]:
    n = sc["no"]
    img = FINAL[str(n)]
    L = IMGLOG[img]
    vo = VO[n]
    V = sc.get("video")
    if V:
        th = (f"<img src='{vthumb(V['file'])}'><div class='t'>{V['file']} 4초 프레임(영상 클립)</div>"
              f"<img src='{thumb(img)}' style='margin-top:2mm'><div class='t'>{img} (정지 이미지, 중앙 16:9 크롭). 영상과 나란히 비교용</div>")
        tool = (f"영상: {e(V['tool'])} — 모션 클립(프롬프트로 화풍 맞춤) / 이미지: COPA gpt-image-2 — 키 비주얼(영상 클립과의 일관성 기준) / "
                f"음성: COPA gpt-4o-mini-tts nova — 내레이션(실측 {vo['duration']:.2f}초, speed {vo['speed']})"
                + (" / 오디오(BGM): 이 클립의 생성 오디오를 BGM 소스로 사용" if n == 1 else ""))
        vrows = (f"<tr><th>입력 프롬프트(영상, 원문)</th><td class='pr'>{e(V['prompt'])}<br>model={e(V['model'])}, {V['seconds']}초, {V['resolution']}, job_id={e(V['job_id'])}</td></tr>"
                 f"<tr><th>출력 결과 요약(영상)</th><td>{e(V['output_summary'])}</td></tr>")
        files = f"assets/video/{V['file']} · assets/images/{img} · assets/audio/scene{n:02d}_vo_gpt.mp3. 편집: {e(V['used_as'])}"
    else:
        th = f"<img src='{thumb(img)}'><div class='t'>{img} (중앙 16:9 크롭 썸네일). 이 씬은 영상 클립이 없어 채택 이미지를 썸네일로 사용</div>"
        tool = (f"이미지: COPA gpt-image-2 — 키 비주얼 / 영상: {MOTION[n]}(ffmpeg, AI 영상 아님 — 인물 왜곡·텍스트 오버레이 위험 때문에 의도적으로 정지 이미지 유지) / "
                f"음성: COPA gpt-4o-mini-tts nova — 내레이션(실측 {vo['duration']:.2f}초, speed {vo['speed']})")
        vrows = ""
        files = f"assets/images/{img} · assets/audio/scene{n:02d}_vo_gpt.mp3 · 모션은 편집 단계 zoompan(별도 모션 파일 없음)"
    w(f"""<div class='card'><div class='th'>{th}</div>
<div><div class='hd'>씬 {n} · {sc['duration_sec']}초 · {e(sc['phase'])}</div><table>
<tr><th>목표 메시지</th><td>{e(sc['goal_message'])}</td></tr>
<tr><th>화면 구성</th><td>{e(sc['composition'])}</td></tr>
<tr><th>내레이션</th><td>{e(sc['narration'])}</td></tr>
<tr><th>사용 도구·목적</th><td>{tool}</td></tr>
<tr><th>입력 프롬프트(최종 이미지, 원문)</th><td class='pr'>{e(L['prompt'])}<br>size={e(L['size'])}, request_id={e(L['request_id'])}</td></tr>{vrows}
<tr><th>출력 결과 요약(이미지)</th><td>{e(L['verdict'])} — {e(L['summary'])}</td></tr>
<tr><th>결과 파일명</th><td>{files}</td></tr></table></div></div>""")
w("</section>")

# 7 수정 전/후
def ba(a, bb, ta, tb, why):
    return (f"<div class='ba'><div><b>{ta}</b><img src='{thumb(a)}'><div class='pr'>{e(IMGLOG[a]['prompt'])}</div><p>판정: {e(IMGLOG[a]['verdict'])} — {e(IMGLOG[a]['summary'])}</p></div>"
            f"<div><b>{tb}</b><img src='{thumb(bb)}'><div class='pr'>{e(IMGLOG[bb]['prompt'])}</div><p>판정: {e(IMGLOG[bb]['verdict'])} — {e(IMGLOG[bb]['summary'])}</p></div></div><p><b>수정 이유·결과.</b> {why}</p>")

def vba(sc_no, why):
    V = SB["scenes"][sc_no - 1]["video"]
    vlog = {c["job_id"]: c for c in VLOG["copa"] if c.get("job_id")}
    a, b2 = vlog[V["before_job_id"]], vlog[V["job_id"]]
    pc = b2["prompt_change"]
    return (f"<div class='ba'><div><b>수정 전 (v1, {e(V['before_file'])})</b><img src='{vthumb(V['before_file'])}'><div class='pr'>{e(V['prompt_v1'])}</div><p>{e(a['summary'])}</p></div>"
            f"<div><b>수정 후 (v2, {e(V['file'])}, 채택)</b><img src='{vthumb(V['file'])}'><div class='pr'>{e(V['prompt'])}</div><p>{e(b2['summary'])}</p></div></div>"
            f"<p><b>변경.</b> 전: {e(pc['before'])} → 후: {e(pc['after'])}<br><b>이유.</b> {e(pc['reason'])}<br>{why}</p>")


w("<section><h2>7. 프롬프트 수정 전/후 비교</h2><h3>[2차 COPA 영상] 씬 1 — veo-3.1-fast v1 → v2 (각 4초 프레임)</h3>")
w(vba(1, "<b>결과.</b> 구름·언덕 색과 인물 크기는 의도대로 정리됐다. 구도는 정지 이미지와 달라졌고(갈래 길 → 한 줄기 길) 이는 프롬프트로 잡지 못했다. 씬당 2회 한도라 v3는 만들지 않았고, 편집에서 채도·밝기만 소폭 낮췄다."))
w("<h3>[2차 COPA 영상] 씬 5 — veo-3.1-fast v1 → v2 (각 4초 프레임)</h3>")
w(vba(5, "<b>결과.</b> 식기 형상이 사라지고 Y자 갈림길이 성립했다. 잔여: 길이 크림색, 별·동전 과다, 인물이 갈림길 시작점을 가림."))
w("<h3>[2차 COPA] 씬 2 — gpt → gpt_v2 (이미지 수정)</h3>")
w(ba("scene02_img_gpt.png", "scene02_img_gpt_v2.png", "수정 전 (gpt)", "수정 후 (gpt_v2, 채택)",
     IMGLOG["scene02_before_after"]["why"] + " 변경: " + IMGLOG["scene02_before_after"]["what_changed"] +
     " 결과: 콘티 구도와 일치, 이후 씬 인물 스케일과 정합."))
w("<h3>[2차 COPA] 씬 6 — gpt → gpt_v2</h3>")
w(ba("scene06_img_gpt.png", "scene06_img_gpt_v2.png", "수정 전 (gpt)", "수정 후 (gpt_v2, 채택)",
     "엔드카드의 앰버 별이 약 2%로 너무 작아 모티프로 읽히지 않았다. 프롬프트에 '별 크기 약 4%, 글로우, 흰 궤도 링'을 명시해 재생성했고 중앙·하단 2/3 여백(텍스트 영역)은 유지됐다. 한계: 별이 우상단 코너에 치우침."))
w("<h3>[1차 Pollinations, 기록 유지] 씬 1 (필수 비교) — v1 → v2</h3>")
w(ba("scene01_img_v1.png", "scene01_img_v2.png", "수정 전 (v1)", "수정 후 (v2, 1차 채택)",
     "v1은 'a person feeling lost, AI learning, digital art' 로 피사체·구도·팔레트·텍스트 제약이 모두 없어 얼굴이 보이는 사실적 인물과 청회색 실사풍이 나왔다. "
     "v2는 ① 얼굴 없는 뒷모습 실루엣 ② style_suffix+hex 팔레트 ③ no text ④ wide shot+위치 지정을 추가했다. "
     "결과: 얼굴 비노출, 남색/블루 톤 통일, 글자 없음으로 개선. 한계: 회화풍이고 앰버 스카프·갈림길은 반영되지 않았다. 이 한계는 2차 gpt-image-2 씬 1에서 해소됨(8장 비교)."))
w("<h3>[1차] 씬 1 — v2 → v3 (미채택)</h3>")
w(ba("scene01_img_v2.png", "scene01_img_v3.png", "v2 (채택)", "v3 (보류)",
     "'flat vector'를 앞세운 짧은 프롬프트로 3차 시도. 톤은 더 어두운 남색이었으나 회화풍·스카프 없음이라 v2 대비 개선이 미미해 v2 유지."))
w("<h3>[1차] 씬 3 — v1 → v2</h3>")
w(ba("scene03_img_v1.png", "scene03_img_v2.png", "수정 전 (v1)", "수정 후 (v2, 1차 채택)",
     "긴 style_suffix 프롬프트는 sana가 무시해 사실적인 터널 이미지가 나왔다. 'flat vector illustration'을 맨 앞에 두고 짧게 줄여 앰버 문과 남색→블루 하늘 구도가 성립했다. 인물은 2명이 손잡은 형태(스카프 없음)."))
w("<h3>[1차] 씬 4 — v1 → v3</h3>")
w(ba("scene04_img_v1.png", "scene04_img_v3.png", "수정 전 (v1, v2도 불합격)", "수정 후 (v3, 1차 채택·한계)",
     "v1은 사람 없는 추상 타원, v2는 추상 도형으로 퇴행. v3에서 'four people silhouettes sitting around a round table'로 명시해 협업 장면이 성립했으나 인물이 사실적·흐릿해 faceless 원칙 미달, 3명."))
w("</section>")

# 8 비교/실패
w("<section><h2>8. 다른 도구 재제작 비교(보너스) · 실패/대체 기록</h2><h3>이미지: Pollinations(1차) vs COPA gpt-image-2(2차) — 6씬 나란히</h3>")
for n in range(1, 7):
    a, bb = OLD[n], FINAL[str(n)]
    w(f"<div class='ba'><div><b>씬 {n} · Pollinations {a}</b><img src='{thumb(a)}'><p>{e(IMGLOG[a]['summary'])}</p></div>"
      f"<div><b>씬 {n} · gpt-image-2 {bb}</b><img src='{thumb(bb)}'><p>{e(IMGLOG[bb]['summary'])}</p></div></div>")
w("""<p><b>차이 요약(로그 기준).</b> 1차는 앰버 스카프·갈림길이 반영되지 않고 씬 1 회화풍, 씬 4 사실적 인물이었다. gpt-image-2는 6씬 모두 같은 STYLE 문구로 플랫 벡터·팔레트·얼굴 없는 실루엣·앰버 스카프가 일관되고 워터마크가 없다. 대가로 씬 2·6 재생성이 필요했다(씬당 최대 2회 규칙 내).</p>
<h3>영상: veo-3.1-fast vs veo-3.1 — 씬 3, 같은 프롬프트(보너스: 다른 도구로 재제작)</h3>""")
w(f"""<div class='ba'><div><b>veo-3.1-fast (scene03_motion.mp4, 4초 프레임)</b><img src='{vthumb("scene03_motion.mp4")}'><p>길이 앰버/황금색(정지 이미지는 네이비), 문이 정상 위가 아니라 바위 동굴 입구처럼 생성, 하늘 하단이 청록색. 오디오 평균 -24.3dB.</p></div>
<div><b>veo-3.1 (scene03_motion_veo31.mp4, 4초 프레임, 채택)</b><img src='{vthumb("scene03_motion_veo31.mp4")}'><p>길이 앰버인 점은 같음. 시작 구도가 더 넓어 문이 바위 정상에 있는 정지 이미지에 조금 더 가까움. 다만 돌리인이 진행되며 7초 무렵 문이 화면을 채움(두 모델 공통). 오디오 평균 -34.7dB로 약 10dB 조용해 '바람만' 지시에 더 부합.</p></div></div>
<p><b>차이 요약(실측).</b> 소요 시간은 fast 64초 vs veo-3.1 65초지만 4건을 동시에 제출하고 10초 간격으로 폴링해 차이를 측정할 수 없다. 색 편차(앰버 길·크림 구름)는 두 모델 모두 같아 모델 교체로 풀리지 않았고, 구도 시작점과 오디오 레벨에서만 차이가 보였다. 표본은 1씬 1회씩이라 일반화하지 않는다. <b>veo vs sora는 비교하지 못했다</b>: sora-2는 OpenAI가 2026-09-24에 Videos API를 제거해 실패했다.</p>
<h3>도구 접근성 대응 (실제 있었던 일)</h3>
<table><tr><th>단계</th><th>상황</th><th>대응·결과</th></tr>
<tr><td>1. HF 쿼터 (1차)</td><td>HF Space 4종 × 씬 3개 = 12회가 ZeroGPU 익명 쿼터 초과로 실패(토큰 필요)</td><td>코디세이 COPA 게이트웨이로 전환하고, 영상은 정지 이미지 + zoompan으로 대체(미션 허용 크레딧 부족 전략)</td></tr>
<tr><td>2. COPA 영상 503</td><td>veo-3.1-fast·veo-3.1을 씬 프롬프트와 최소 프롬프트(8초·4초)로 호출해도 전부 HTTP 503 media_provider_unavailable, job 생성 전 거절(COPA 로그의 503은 18건이나 오류 행에 모델 필드가 없어 모델별 집계가 안 된다. `video_log.json`에 기록한 veo 호출은 7회). 같은 시점 imagen-4-fast·gemini-2.5-flash-tts도 503</td><td>모델·프롬프트·길이를 바꿔도 같은 결과여서 프롬프트가 아니라 provider 측 문제로 판단하고 호출 반복을 멈춤(쿼터 보호). 이 구간 동안 zoompan 완성본을 먼저 만들어 일정 유지</td></tr>
<tr><td>3. 원인과 해결</td><td>원인은 QA 기관에 Google provider 키가 등록되지 않은 것이었다. 키 등록 후 veo-3.1-fast 4초 테스트(job vjob_98d442595cfe4d5cb389803f)가 완료·다운로드까지 성공(1280x720 H.264 + AAC)</td><td>그 뒤 씬 1·3·5 생성 및 v2 수정을 진행(씬당 2회 한도 준수). imagen-4-fast·gemini TTS는 대체 도구라 키 등록 후 재호출하지 않았다(같은 원인이었는지 미검증)</td></tr>
<tr><td>4. sora-2 종료</td><td>1차 HTTP 400(resolution은 1280x720|720x1280만 허용)을 고친 뒤 HTTP 503 media_provider_error. OpenAI가 2026-09-24에 Videos API를 제거해 provider 처리 실패</td><td>키 등록과 무관한 영구 실패로 판단, 재시도 안 함. veo-3.1로 대체 비교(위)</td></tr></table>
<h3>실패·대체 기록</h3>
<table><tr><th>영역</th><th>문제</th><th>대응·결과</th></tr>
<tr><td>영상(2차)</td><td>COPA 로그 기준 영상 22건 중 성공 6(veo-3.1-fast 5 + veo-3.1 1), 실패 16(veo 503 11, sora-2 400 1·503 4). 성공 클립의 어긋남은 7장·6장 카드 참조</td><td>실패는 키 등록 전 veo 503과 sora-2 종료. 성공 클립은 씬 1·3·5에 사용, 씬 2·4·6은 정지 이미지 + zoompan 유지</td></tr>
<tr><td>영상(1차)</td><td>HF Space 4종 × 씬 3개 = 12회 ZeroGPU 쿼터 실패</td><td>COPA로 도구 전환(위 도구 접근성 대응)</td></tr>
<tr><td>이미지(1차)</td><td>Pollinations 익명 호출 간헐 HTTP 402, 워터마크, 1024x576 수신, model 파라미터 무시(실제 sana)</td><td>COPA gpt-image-2로 교체해 해소(1차 파일은 비교본으로 보존)</td></tr>
<tr><td>이미지(2차)</td><td>씬 2 상반신 과대(스케일 불일치), 씬 6 별 너무 작음</td><td>각 1회 재생성(gpt_v2)으로 해결</td></tr>
<tr><td>음성</td><td>1차 edge-tts 3회 HTTP 403, gTTS는 atempo 1.3으로도 씬 5 초과해 문장 축약</td><td>COPA gpt-4o-mini-tts로 교체. speed 1.0으로 6씬 모두 씬 길이 이내(씬 5 축약 문장은 그대로 유지)</td></tr>
<tr><td>BGM</td><td>1차 HF MusicGen/Stable Audio Open 실패. 8초 BGM을 stream_loop로 그대로 반복하면 이음새가 끊기는 문제(assemble.sh 버그)</td><td>veo 생성 오디오(씬 1 v2 클립)를 bgm_veo.m4a로 추출하고 1초 acrossfade 7회로 50초를 만든 뒤 44초로 잘라 -19dB·내레이션 덕킹·끝 3초 페이드. 효과음은 없음. 청취 검수는 못 하고 수치(volumedetect)만 확인</td></tr>
<tr><td>편집(assemble.sh)</td><td>영상 경로 버그: <code>sceneNN_motion.mp4</code>만 찾아 video_log.json 의 final 클립(v2·veo31)이 쓰이지 않음</td><td>final 맵을 읽도록 수정. 씬 1 클립만 eq(brightness -0.03, saturation 0.9)로 보정(이웃 네이비 씬 2보다 떠 보임), 씬 3·5는 이웃 씬의 중간 밝기라 보정 안 함</td></tr>
<tr><td>립싱크</td><td>미시도</td><td>미달성</td></tr></table></section>""")

# 9 최종 영상
w("<section><h2>9. 최종 영상 정보</h2><table><tr><th>파일명</th><th>길이</th><th>해상도</th><th>fps</th><th>코덱</th><th>크기</th></tr>")
for lay, (nm, d, v, a, sz) in vid.items():
    w(f"<tr><td>output/{nm}</td><td>{d:.1f}초</td><td>{v['width']}x{v['height']}</td><td>{v['r_frame_rate']}</td><td>{v['codec_name'].upper()} / {a['codec_name'].upper()} {a['sample_rate']}Hz {a['channels']}ch</td><td>{sz/1e6:.1f}MB</td></tr>")
w(f"""</table><p>값은 ffprobe 실측. 씬 길이 {' + '.join(str(s['duration_sec']) for s in SB['scenes'])} = {SB['timing_check']['total_sec']}초(30~60초 범위). 마지막 씬 6(5초)에 'CODYSSEY' 로고 텍스트·슬로건·CTA(codyssey.kr) 엔드카드. 9:16 버전은 16:9 영상을 중앙에 두고 블러 확대 배경을 채운 파생본(보너스: 화면 비율 2종).</p>
<div class='warn'>미션 요건 대비 현황: AI 시각 요소(gpt-image-2 이미지 + veo 영상 클립) 충족, AI 청각 요소(gpt-4o-mini-tts 내레이션 + veo 생성 오디오 BGM) 충족, 다른 도구 재제작(이미지 Pollinations vs gpt-image-2, 영상 veo-3.1-fast vs veo-3.1)·9:16 달성. 미달성: 립싱크, 1:1 비율, veo vs sora 비교(sora 종료). 구성: 씬 1·3·5는 AI 영상 클립(총 24초), 씬 2·4·6은 정지 이미지 + zoompan(20초). 오디오는 청취하지 못했고 수치로만 확인했다.</div>
<div class='fr'><img src='{frame("16x9",3)}'><img src='{frame("16x9",18)}'><img src='{frame("16x9",34)}'><img src='{frame("16x9",42)}'><img src='{frame("9x16",40)}'></div>
<p style='font-size:8pt'>최종 영상 프레임 캡처(16:9 3초·18초·34초·42초 / 9:16 40초).</p></section></body></html>""")


HTML = ROOT / "storyboard/storyboard.html"
HTML.write_text("\n".join(o))
PDF = ROOT / "storyboard/Codyssey_Storyboard.pdf"
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={PDF}", f"file://{HTML}"],
               check=True, capture_output=True)
print("ok", PDF)
