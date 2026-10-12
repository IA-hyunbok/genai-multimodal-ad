# 코디세이(Codyssey) AI 여정 광고 — GenAI 멀티모달 콘텐츠 제작

코디세이 광고 영상(44초)과 스토리보드를 생성형 AI 도구로 제작한 프로젝트다. 1차는 무료 도구(Pollinations, gTTS, HF Spaces)로, 2차는 코디세이 COPA 게이트웨이(gpt-image-2, gpt-4o-mini-tts, veo)로 만들었다. 최종 영상은 2차 결과물이다. 씬 1·3·5는 veo T2V 클립, 씬 2·4·6은 정지 이미지 + ffmpeg 패닝/줌이다. 모든 생성 호출은 `scripts/`에 재실행 가능한 형태로 남겼고, 성공과 실패를 구분해 기록했다.

## 결과물

| 구분 | 경로 |
|---|---|
| 광고 영상 16:9 | [output/Codyssey_GenAI_Ad_16x9.mp4](output/Codyssey_GenAI_Ad_16x9.mp4) |
| 광고 영상 9:16 (파생) | [output/Codyssey_GenAI_Ad_9x16.mp4](output/Codyssey_GenAI_Ad_9x16.mp4) |
| 스토리보드 PDF (14쪽) | [storyboard/Codyssey_Storyboard.pdf](storyboard/Codyssey_Storyboard.pdf) |
| 스토리보드 원본 | [storyboard/storyboard.json](storyboard/storyboard.json), [storyboard/storyboard.html](storyboard/storyboard.html) |
| 생성 로그 | `assets/copa_log.jsonl`(COPA 전 호출), `assets/images/generation_log.json`, `assets/video/video_log.json`, `assets/audio/audio_log.json` |

## 최종 영상 스펙 (ffprobe 실측)

| 파일 | 길이 | 해상도 | fps | 코덱 |
|---|---|---|---|---|
| Codyssey_GenAI_Ad_16x9.mp4 | 44.0초 | 1920x1080 | 30 | H.264 / AAC |
| Codyssey_GenAI_Ad_9x16.mp4 | 44.0초 | 1080x1920 | 30 | H.264 / AAC |

구성: 6씬(7+7+8+8+9+5초). 씬 6에 CODYSSEY 텍스트, 슬로건, CTA(codyssey.kr)를 넣었다.

| 씬 | 구간 | 소스 | 편집 |
|---|---|---|---|
| 1 | 0~7초 | veo-3.1-fast `scene01_motion_v2.mp4` | 24→30fps, 8초 중 7초 사용, eq(brightness -0.03, saturation 0.9) |
| 2 | 7~14초 | gpt-image `scene02_img_gpt_v2` + zoompan(pan) | 없음 |
| 3 | 14~22초 | veo-3.1 `scene03_motion_veo31.mp4` | 24→30fps, 8초 전체 |
| 4 | 22~30초 | gpt-image `scene04_img_gpt` + zoompan(out) | 없음 |
| 5 | 30~39초 | veo-3.1-fast `scene05_motion_v2.mp4` | 24→30fps, 8초 뒤 마지막 프레임 1초 유지 |
| 6 | 39~44초 | gpt-image `scene06_img_gpt_v2` + zoompan(in) + 엔드카드 | 없음 |

6개 씬을 이은 뒤 전체에 동일한 색보정(contrast/saturation/colorbalance)을 한 번 더 적용했다. 클립의 생성 오디오는 버리고(`-an`), 씬 1 v2 클립의 오디오만 BGM으로 쓴다.

## 사용 도구

| 구분 | 최종 | 비교·시도 | 선택 이유 | 대체 도구 |
|---|---|---|---|---|
| 이미지 | 코디세이 COPA 게이트웨이 gpt-image-2 (1536x1024, 8회: 6씬 + 씬 2·6 재생성) | 1차·비교: Pollinations(실제 모델 sana) | 화풍·팔레트·"얼굴 없는 실루엣" 지시 준수, 워터마크 없음, 앰버 스카프 식별자 반영 | COPA imagen-4, gpt-image-1.5, gemini-2.5-flash-image(미사용) |
| 비디오 | COPA veo-3.1-fast T2V(씬 1·5) + veo-3.1(씬 3 채택). 8초·720p, 6 job. 씬 2·4·6은 ffmpeg zoompan | 씬 3은 fast와 veo-3.1을 같은 프롬프트로 비교. sora-2는 업스트림 종료로 실패. 1차 HF Spaces 4종은 익명 쿼터로 실패 | COPA 영상 API는 이미지 입력이 없어 T2V만 가능. veo는 영상·오디오를 함께 생성. 인물 왜곡 위험이 낮은 풍경 씬 1·3·5만 영상 대상 | sora-2(종료), HF Spaces i2v, zoompan(씬 2·4·6 실사용) |
| 음성 | COPA gpt-4o-mini-tts, voice nova, speed 1.0 | nova/shimmer/alloy 비교, 1차 gTTS, edge-tts 403 실패 | 6씬 모두 씬 길이 이내라 가속·축약 불필요 | COPA tts-1-hd, gemini-2.5-flash-tts, gTTS |
| BGM | veo 생성 오디오(씬 1 v2 클립에서 추출, `assets/audio/bgm_veo.m4a`) | 씬 1 v1 오디오(`bgm_veo_v1.m4a`, 미채택). 1차 HF MusicGen 계열 실패 | 별도 BGM 모델 호출 없이 영상 호출의 부산물로 확보(쿼터 절약) | MusicGen, Stable Audio Open |

## 도구 접근성 대응

실제 있었던 일을 순서대로 적는다.

1. **HF ZeroGPU 익명 쿼터 소진(1차).** HF Space 4종 x 씬 3개 = 12회가 쿼터 초과로 실패했다. COPA 게이트웨이로 전환했고, 영상은 정지 이미지 + zoompan으로 대체했다.
2. **COPA 영상 503.** veo-3.1-fast·veo-3.1을 씬 프롬프트와 최소 프롬프트(8초·4초)로 호출해도 전부 HTTP 503 `media_provider_unavailable`이었고 job 생성 전에 거절됐다(COPA 로그의 503은 18건이나 오류 행에 모델 필드가 없어 모델별 집계가 안 된다. `video_log.json`에 기록한 veo 호출은 7회). 같은 시점 imagen-4-fast, gemini-2.5-flash-tts도 503이었다. 모델·프롬프트·길이를 바꿔도 같아서 프롬프트가 아니라 provider 쪽 문제로 판단하고 호출 반복을 멈췄다(쿼터 보호). 그동안은 zoompan 완성본으로 일정을 유지했다.
3. **원인과 해결.** QA 기관에 Google provider 키가 등록되지 않은 것이 원인이었다. 키 등록 후 veo-3.1-fast 4초 테스트(job `vjob_98d442595cfe4d5cb389803f`)가 완료·다운로드까지 성공했다(1280x720 H.264 + AAC). 이후 씬 1·3·5를 생성했다. imagen-4-fast, gemini TTS는 대체 도구라 키 등록 후 재호출하지 않았고, 같은 원인이었는지는 검증하지 않았다.
4. **sora-2 종료.** 1차 HTTP 400(resolution은 1280x720|720x1280만 허용)을 고친 뒤 HTTP 503 `media_provider_error`가 났다. OpenAI가 2026-09-24에 Videos API를 제거해서 생긴 실패로, 키 등록과 무관한 영구 실패로 보고 재시도하지 않았다.

## 현재 상태와 한계 (먼저 읽을 것)

해결된 항목:
- **이미지 일관성**: 앰버 스카프·플랫 벡터 화풍·얼굴 없는 실루엣이 6씬에 반영됐다(1차에서는 스카프 미반영, 씬 1 회화풍, 씬 4 사실적 인물).
- **TTS**: gTTS에서 COPA gpt-4o-mini-tts로 교체했다. atempo 가속과 씬 5 문장 축약이 필요 없어졌다.
- **AI 영상 생성**: 키 등록으로 veo가 동작해 씬 1·3·5에 AI 클립을 썼다. "비디오 생성 AI 1종 이상" 요건을 충족한다.
- **BGM**: veo 생성 오디오를 BGM으로 썼다. 8초 BGM을 1초 acrossfade 7회로 이어 붙여 44초로 만든다(기존 `stream_loop`는 이음새가 끊겼다).
- **보너스**: 이미지 도구 재제작 비교(Pollinations vs gpt-image-2), 영상 도구 재제작 비교(씬 3 veo-3.1-fast vs veo-3.1), 9:16 버전을 달성했다.

남은 한계:
- **T2V는 정지 이미지와 구도·색이 어긋났다.** 화풍(플랫 벡터), 팔레트 계열, 앰버 스카프, 얼굴 없음은 6개 클립 모두 유지됐다. 어긋난 것: 씬 1은 여러 갈래 길이 한 줄기 구불길과 큰 화살표로 바뀌었고 길이 #2F6BFF보다 밝은 시안이다. 씬 3은 네이비 길이 앰버 길로, 흰 구름이 크림색 구름으로 바뀌었고 문이 바위 입구 모양이며 7초 무렵 문이 화면을 채운다. 씬 5는 길이 크림색이고 별·동전이 정지 이미지보다 많으며 인물이 갈림길 시작점을 가린다. 프롬프트 수정(v2)은 구름색·식기 형상·인물 크기를 잡았지만 구도는 잡지 못했다. 씬당 2회 한도라 v3는 만들지 않았다.
- **오디오를 들어보지 못했다.** 수치(volumedetect)와 ffprobe로만 확인했다. BGM 소스는 평균 -16.9dB·피크 -0.8dB였고, 프롬프트가 요청한 앰비언트 피아노·신스 패드가 실제로 그렇게 나왔는지, 8초 반복이 거슬리는지는 확인하지 못했다. 효과음은 없다.
- **veo vs sora 비교는 못 했다.** sora-2가 종료돼 결과 영상이 없다. 대신 veo-3.1-fast vs veo-3.1로 비교했다(표본 1씬 1회).
- **씬 2·4·6은 AI 영상이 아니다.** 손(2)·다인원(4) 왜곡 위험과 텍스트 오버레이(6) 때문에 의도적으로 정지 이미지 + zoompan을 유지했다. 키 등록 후 씬 6 영상은 재시도하지 않았다.
- **씬 5 길이**: veo 클립은 8초이고 씬이 9초라 마지막 1초는 정지 프레임이다. 24fps 클립을 30fps로 올려 프레임이 복제된다.
- **립싱크, 1:1 비율 미달성.**
- **이미지 일관성 잔여 문제**: 씬 5 건물 묘사가 다른 씬보다 정교하고 길이 차이(5개월/18개월)가 약하다. 씬 6 별이 우상단 코너에 치우친다. 씬 2는 스카프가 의자 소품으로만 나온다. COPA는 seed 파라미터가 없어 seed 고정은 1차에만 적용됐다.

## 폴더 구조

```
assets/images/   scene{NN}_img_v{n}.png(1차 Pollinations), scene{NN}_img_gpt[_v2].png(2차 COPA) + generation_log.json
assets/video/    scene{NN}_motion[_v2|_veo31].mp4 (씬 1·3·5, 6 job) + video_log.json (final 맵 = 편집에 쓰는 클립)
assets/audio/    scene{NN}_vo.mp3(1차 gTTS), scene{NN}_vo_gpt.mp3(2차 COPA), bgm_veo.m4a(+_v1), _voice_cmp/ + audio_log.json
assets/copa_log.jsonl   COPA 호출 43건(키 없음, 키 등록 후 4초 테스트 job은 이 로그에 없고 `video_log.json`에만 있음)
storyboard/      storyboard.json / storyboard.html / Codyssey_Storyboard.pdf / thumbs/
scripts/         copa.py(COPA 클라이언트), gen_images_copa.sh, gen_audio_copa.sh, gen_video_copa.sh,
                 assemble.sh, make_overlays.py, build_storyboard.py,
                 gen_images.py, gen_images_alt.py, gen_video.py, gen_audio.py, log_verdict.py (1차)
build/           중간 산출물 (gitignore)
output/          최종 mp4 2종
```

## 재현 방법

`.env`에 `COPA_BASE_URL`, `COPA_API_KEY`를 설정한다. 사전: `.venv`(requests), ffmpeg/ffprobe(/opt/homebrew/bin), Pillow가 있는 시스템 python3, Chrome. 영상은 기관에 Google provider 키가 등록돼 있어야 한다.

```bash
scripts/gen_images_copa.sh all gpt         # 이미지 6장 (재생성: scripts/gen_images_copa.sh 2 gpt_v2, 6 gpt_v2)
VOICE=nova scripts/gen_audio_copa.sh       # 내레이션 (voice 비교: scripts/gen_audio_copa.sh compare)
scripts/gen_video_copa.sh 1v2              # 영상(1|3|5|1v2|5v2|3q|6|3sora). 최종 클립은 1v2, 3q(veo-3.1), 5v2
bash scripts/assemble.sh                   # 통합 편집 -> output/*.mp4
python3 scripts/build_storyboard.py        # 스토리보드 HTML -> PDF
```

`assemble.sh`는 `assets/video/video_log.json`의 `final` 맵에 적힌 클립을 씬 1·3·5에 쓰고(없으면 zoompan), `assets/audio/bgm_veo.*`가 있으면 BGM으로 믹스한다(-19dB, 내레이션 덕킹, 끝 3초 페이드).

## 동료 평가 질문 답변

**1. 기획→생성→검수→편집/통합 파이프라인 순서**
기획(공식 출처로 브랜드 조사, storyboard.json 확정, style_lock·네이밍) → 생성(이미지 → 음성 → 영상) → 검수(이미지·영상 프레임을 육안으로 보고 채택/불합격을 로그에 기록, 불합격이면 프롬프트 수정 후 재생성) → 편집/통합(`assemble.sh`: veo 클립 30fps 정규화, 이미지는 16:9 크롭·zoompan, 색보정, 오디오 믹스, 자막). 영상은 이미지가 확정된 뒤에만 시도하도록 설계했다.

**2. 크레딧/대기열 제약을 고려한 씬 수·생성 횟수·대체 도구 설계**
씬은 6개로 제한했다. COPA는 사내 쿼터라 이미지·영상 모두 씬당 최대 2회로 제한했다. 이미지는 8회(6씬 + 씬 2·6 재생성), 영상은 6 job(씬 1: fast v1+v2, 씬 3: fast+veo-3.1, 씬 5: fast v1+v2)에 키 등록 확인용 4초 테스트 1 job이다. 영상 대상은 인물 왜곡 위험이 낮은 풍경 씬 1·3·5만 잡았다. 대기열은 영상 3~4건을 동시 제출하고 10초 간격으로 폴링했으며 job당 53~65초가 걸렸다. 대체는 실제로 발동했다: HF 쿼터 실패 → COPA 전환, COPA 영상 503 → 호출을 멈추고 zoompan으로 완성본을 먼저 확보, 키 등록 후 veo로 교체. sora-2는 종료돼 veo-3.1로 대체했다. 음성은 edge-tts 403 → gTTS → COPA TTS 순이다.

**3. 에셋 규격과 생성 파라미터 표준화**
이미지는 전 씬 gpt-image-2, size 1536x1024, 같은 STYLE 문구(팔레트 hex navy #0B1B3F · blue #2F6BFF · amber #FFB400 · off-white #F5F7FB, 얼굴 없는 실루엣, 앰버 스카프, 글자 금지)를 모든 프롬프트 끝에 붙였다. 영상은 전 클립 8초·720p·16:9로 요청하고 같은 STYLE 문구(+ "no speech")를 붙였다. 음성은 전 씬 nova speed 1.0. 편집에서 이미지는 중앙 16:9(1536x864) 크롭, veo 클립은 1280x720 24fps를 모두 1920x1080 30fps H.264/AAC로 통일했고 전 구간 동일 색보정을 한 번만 적용했다.

**4. 파일 네이밍/정리 규칙**
`scene{NN}_{kind}_{variant}.{ext}` (img/motion/vo)와 `bgm_*`. 1차는 v1~v3, 2차 COPA는 `gpt`, 수정본은 `gpt_v2`/`motion_v2`, 모델을 바꾼 비교본은 `motion_veo31`. 채택하지 않은 버전도 지우지 않고 전/후 비교 근거로 남긴다. 판정은 로그의 verdict/final 맵에 기록한다. 최종물은 `Codyssey_GenAI_Ad_{16x9|9x16}.mp4`다.

**5. Text-to-Image vs Image-to-Video vs Text-to-Video 차이와 선택 기준**
T2I는 구도·화풍을 확정하는 저비용 단계라 먼저 여러 번 검수한다. I2V는 확정 이미지를 움직이게 해 일관성에 가장 유리하다. T2V는 프롬프트만으로 영상을 만들어 화풍 통제가 약하다. COPA 영상 API는 이미지 입력을 받지 않아 I2V를 선택할 수 없었고(1차 HF I2V도 쿼터로 실패) T2V로 갔다. 정지 이미지와의 일관성은 영상 프롬프트에 팔레트 hex·플랫 벡터·얼굴 없는 실루엣·앰버 스카프·카메라 거리를 명시해 맞췄다. 결과는 절반만 맞았다. 화풍·팔레트 계열·스카프·얼굴 없음은 6개 클립 모두 유지됐지만, 구도와 색은 정지 이미지와 달랐다(씬 1 갈래 길 → 한 줄기 길, 씬 3 네이비 길 → 앰버 길, 씬 5 별·동전 과다). 프롬프트 수정으로 구름색·식기 형상·인물 크기는 잡았고 구도는 못 잡았다. 정지 이미지 그대로 움직여야 한다면 I2V가 필요하다.

**6. 품질/제어/속도/비용 중 우선순위와 이유**
사내 쿼터를 낭비하지 않는 것(비용)이 제약이었고, 그 안에서 제어(프롬프트 구조·검수·재생성 횟수 제한)를 1순위, 품질을 2순위로 뒀다. 속도는 후순위다. 영상은 이미지·음성을 확정한 뒤 fast 모델로 시작했고, 비교는 씬 3 한 곳에만 비싼 모델을 썼다. 영상이 막혔을 때도 완성본이 나오도록 zoompan 경로를 항상 열어 두었다.

**7. 프롬프트 A→B 결과 변화와 원인**
이미지 1차 씬 1: v1 `a person feeling lost, AI learning, digital art`는 얼굴이 보이는 실사 인물이 나왔다. v2에서 뒷모습 실루엣·팔레트 hex·no text·wide shot을 추가해 얼굴 비노출과 남색 톤으로 개선됐다(제약이 없어 모델 기본 분포로 간 것이 원인). 이미지 2차 씬 2: 'body cut off above the wrist, no head and no torso visible'를 넣은 gpt_v2가 손+노트북+소품만 남겼다. 영상 씬 1: v1은 구름이 크림/베이지, 길이 시안으로 나와 팔레트가 깨졌다. v2에서 구름·언덕을 네이비/슬레이트로, 흰·베이지·피치·주황 구름을 금지, 화살표를 #2F6BFF로, 인물을 좌하단에 작게 지정하자 구름·인물 크기가 정리됐다(원인: '구름'이라는 단어의 모델 기본값이 팔레트 문장보다 우선). 영상 씬 5: v1은 'fork'가 포크 식기 형상, 'road'가 차선 있는 도로로 해석됐다. v2에서 Y자 리본 길, 차선·아스팔트 금지, 식기 금지, 카메라 고정에 가깝게 바꾸자 식기 형상이 사라졌다. 비교 이미지는 스토리보드 7장에 있다.

**8. 캐릭터/스타일 일관성 제어 방법**
모든 프롬프트에 같은 STYLE 문구(화풍·팔레트 hex·얼굴 없는 실루엣·앰버 스카프 식별자)를 고정하고, 얼굴을 그리지 않아 캐릭터 닮음·딥페이크 위험을 피했으며, 전 구간 동일 색보정을 썼다. 1차 Pollinations는 seed=42를 고정했으나 COPA는 seed 파라미터가 없다. cref/sref·ControlNet은 쓰지 않았다. 한계: 씬 5 건물 디테일, 씬 2의 스카프가 소품으로만 등장, 영상 클립의 주인공 체형·복장이 클립마다 조금씩 다르다(스카프만 공통 식별자).

**9. 도구 간 불일치(해상도/비율/색감/톤) 보정 기준·절차**
해상도·비율: gpt-image-2의 3:2(1536x1024)를 중앙 16:9로 크롭한 뒤 업스케일해 zoompan하고, veo 클립(1280x720, 24fps)은 lanczos로 1920x1080, 30fps로 정규화한다. 9:16은 블러 배경 위 중앙 배치. 색감: 클립 중간 프레임과 이웃 정지 이미지의 평균색을 나란히 비교해, 이웃 네이비 씬 2보다 떠 보인 씬 1 클립에만 eq(brightness -0.03, saturation 0.9)를 적용했다. 씬 3·5는 이웃 씬의 중간 밝기라 보정하지 않았다. 이후 전체에 동일 contrast/saturation/colorbalance를 한 번만 적용한다. 오디오: 씬별 TTS를 씬 시작 +0.3초에 배치하고, BGM은 -19dB로 낮춰 내레이션 구간에서 덕킹한 뒤 loudnorm -16 LUFS로 맞춘다. 클립 오디오 레벨 차이(평균 -16.9~-35.8dB)가 커서 클립 오디오는 믹스하지 않고 BGM 소스 하나만 쓴다.

**10. 같은 스토리보드를 다른 도구로 만들면 무엇이 달라질지**
이미지는 실제로 비교했다. Pollinations(sana)는 스카프·갈림길 미반영, 씬 1 회화풍, 씬 4 사실적 인물이었고, gpt-image-2는 6씬 화풍·스카프가 일관됐다. 대신 씬 2·6은 재생성이 필요했다. 영상은 씬 3을 같은 프롬프트로 veo-3.1-fast와 veo-3.1로 만들어 비교했다. 실측: 두 모델 모두 길이 앰버, 구름이 크림색이라 색 편차는 모델 교체로 풀리지 않았다. veo-3.1은 시작 구도가 더 넓어 문이 바위 정상에 있는 정지 이미지에 조금 더 가까웠고, 오디오가 fast보다 약 10dB 조용했다(평균 -34.7dB vs -24.3dB). 소요 시간은 64초 vs 65초지만 동시 제출·10초 폴링이라 차이를 측정할 수 없다. 표본이 1씬 1회라 일반화하지 않는다. sora는 종료돼 비교하지 못했다.

**11. 크레딧 부족 시 전략 변경**
실제로 일어난 일이다. 1차에서 HF ZeroGPU 쿼터가 소진되어 영상 변환을 zoompan으로 바꾸고 BGM을 포기했다. 2차에서는 사내 쿼터 보호를 위해 이미지·영상 호출을 씬당 2회로 제한했다. 영상이 503일 때는 같은 호출을 반복하지 않고 모델·프롬프트·길이를 바꿔 몇 건만 시도해 원인이 provider 쪽임을 확인하고 멈췄으며, 그동안 zoompan 완성본을 만들어 일정을 유지했다. 이미지 단계에서 스토리보드를 확정하고 변환 대상을 3씬으로 줄여 둔 덕이다. 키 등록 후에는 씬 1·3·5만 영상으로 만들었고, 씬 6은 정지 엔드카드를 유지해 호출을 아꼈다.

**12. 60초 → 15초 축약 시 유지/삭제 씬과 메시지 재구성**
현재 44초 6씬 기준으로 씬 1(문제, 7초) → 씬 3(전환, 8초) → 씬 6(엔드카드, 5초)을 남기되 15초로 만든다. 실측 TTS 길이(6.5+6.3+4.4초)의 합이 17초라 문장 단축이 필요하다. 씬 1과 3은 AI 영상 클립이 있어 앞쪽 3~4초씩만 잘라 쓸 수 있다. 씬 1은 "막막함"으로 공감을 만들고, 씬 3 내레이션 "그래서 코디세이는 강의 대신, 직접 만들며 동료와 함께 배우는 길을 엽니다"가 핵심 메시지를 한 문장으로 전달하며, 씬 6이 슬로건과 CTA를 준다. 삭제: 씬 2(비용·시간 장벽)는 씬 1의 문제 제기에 흡수, 씬 4(동료·프로젝트)는 씬 3 문장에 이미 포함, 씬 5(장학금·두 트랙)는 구체 정보라 codyssey.kr CTA로 넘긴다. 대가로 장학금 USP가 빠지므로 필요하면 엔드카드에 "장학금" 한 단어를 넣는다.
