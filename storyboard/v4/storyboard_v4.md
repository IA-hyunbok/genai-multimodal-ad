# 코디세이 AI 광고 v4 — 「코디세이호, 승선하라」 (항해판)

> **제출 대상 아님.** 이 항해판 v4는 v3가 바다 컨셉으로 바뀌면서 세계관이 겹쳐 중단했다(2026-10-14). 영상 `output/v4/Codyssey_v4_sail_16x9.mp4`와 컷 리스트 `cuts_v4.md`(미촬영 계획)는 기록으로만 남긴다. v4 최종은 booth판(`storyboard_v4_booth.md`).

v3 구조는 그대로 둔다. 노선장이 평범한 세 사람을 차례로 부르고, 마지막에 셋이 동료가 되는 10씬 구성이다. 바뀐 것은 두 가지다.
- 무대를 우주에서 **항해**로 옮겼다. 코디세이(Co + Odyssey)는 이름부터 "같이 떠나는 긴 항해"라서 우주 기사단보다 브랜드에 맞는다. 우주·망토·검처럼 특정 영화를 떠올리게 하는 요소도 함께 없앴다.
- 대본을 전부 새로 썼다.

## 1. 개요

| 항목 | 내용 |
|---|---|
| 브랜드 | 코디세이(CODYSSEY) |
| 타깃 | 개발을 배우고 싶지만 "전공이 아니라서 / 돈이 없어서 / 혼자 하면 포기해서" 망설이는 20~30대 |
| 톤앤매너 | 진지한 해양 대서사 화면에 김빠지는 대사. 장엄 → 정적 1초 → 무심한 한마디 |
| USP | 전공·경력 무관 · 장학금 받으며 배움 · 교수 없이 동료끼리 배우는 동료학습 |
| 광고 목적 | 인지 (브랜드와 3가지 USP를 한 번에 기억시키기) |
| 핵심 메시지 | 문턱은 없고, 동료는 있다. |
| CTA | 코디세이로 와라! / codyssey.kr (마지막 5초) |
| 길이·규격 | 57초, 10씬 / 1920x1080, 30fps, H.264 + AAC |

**v3 대본에서 바꾼 이유**
- v3 대사는 "입구에 전공 칸 없다", "장학금 받으며 배운다", "먼저 푼 사람이 가르친다"처럼 광고 카피를 사람 입에 넣은 문장이었다.
- v4에서 선장은 설명하지 않는다. 짧게 되받아치고, 설명은 화면 카피(키워드 슈퍼)가 맡는다.
  - "국문과인데요" → "그래서?"
  - "돈이 없습니다" → "알고 있다. 그래서 준다."
- 반복 구조: 부름 → 핑계 → 정적 1초 → 한마디. 이 박자를 세 번 반복한 뒤 S08에서 깬다.
- 콜백: S04의 "알고 있다"를 S09 마지막 개그에서 다시 쓴다.

## 2. 등장인물 (veo 프롬프트에 글자 그대로 넣는 고정 묘사)

| 태그 | 인물 | 고정 묘사 | 말투 |
|---|---|---|---|
| {CAPTAIN} | 노선장 | a fictional Korean woman in her 60s, the captain of an old wooden sailing ship, very long silver hair in a single thick braid over her shoulder, wrinkled sun-tanned stern face, wearing a long weathered navy captain's coat with brass buttons and a navy captain's cap, holding a brass spyglass | 부를 땐 장엄하고 느리게, 받아칠 땐 갑자기 평평하고 무심하게 |
| {SORA} | 소라 (국문과) | a fictional Korean woman in her 20s, a literature student, round wire-frame glasses, black shoulder-length hair with a yellow hair tie, cream cardigan, hugging a tall stack of paperback books | 밝고 또렷함, 당황하면 음이 올라감 |
| {DOHYUN} | 도현 (전역자) | a fictional Korean man in his 20s just discharged from the army, short buzz-cut hair, olive-khaki hoodie, olive duffel bag on his shoulder, upright posture | 각 잡힌 큰 목소리, 돈 얘기에선 급히 작아짐 |
| {MINSEOK} | 민석 (직장인) | a fictional Korean man in his 30s, an exhausted office worker, messy hair, cobalt-blue dress shirt, loose navy tie, white employee ID badge on a lanyard, heavy eye bags | 기운 없이 늘어지고 문장 끝이 흐려짐 |
| {SHIP} | 코디세이호 | an old three-masted wooden sailing ship with huge cream-white sails and warm brass lanterns, no flags, no writing on the hull | - |

공통 접미어:
- {LOOK} = `Cinematic live-action Korean TV commercial, 35mm anamorphic lens, shallow depth of field, golden-hour natural light, deadpan comedic tone with a perfectly serious epic sea-adventure look, natural skin texture, 16:9, no outer space, no swords, no weapons, no on-screen text, no subtitles, no captions, no logos, no watermark.`
- {KO} = `All dialogue is spoken in Korean only, never in any other language.`

프롬프트 원문은 위 태그를 글자 그대로 치환한 문장이다. 치환본은 `build/v4/sNN.prompt.txt`에 저장한다.

## 3. 사용 도구

| 단계 | 도구 | 목적 | 고른 이유 | 대체 도구 |
|---|---|---|---|---|
| 이미지 | gpt-image-2 (코디세이 COPA) | 씬별 콘티 이미지 10장. 스토리보드를 확정한 뒤에만 영상으로 넘어간다 | 인물 묘사를 잘 재현하고, 사내 게이트웨이로 바로 쓸 수 있다 | imagen-4 |
| 비디오 | veo-3.1 (코디세이 COPA) | 씬별 4/6/8초 실사 클립, 한국어 대사·효과음 동시 생성 | 대사 입모양과 효과음을 한 번에 생성한다. v3 실사에서 10샷 중 9샷이 한국어로 정상 생성됐다 | veo-3.1-fast |
| 오디오 | veo-3.1 내장 오디오 / gpt-4o-mini-tts | 대사·효과음은 veo가 생성하고, veo가 틀리게 말한 대사만 TTS로 다시 입힌다 | 입모양과 소리가 같은 생성물에서 나와야 어긋나지 않는다 | gTTS |
| 검수 | faster-whisper medium (watch-video 스킬) | 클립마다 받아써서 한국어 여부, 대본 일치, 대사 시각을 확인한다 | v3에서 한 클립이 이탈리아어로 나온 것을 잡아냈다 | - |
| 편집 | ffmpeg + Pillow | 컷, 자막, 키워드 슈퍼, 엔드카드, 음량 맞춤 | 통합 편집 용도로만 쓴다 | - |

파일 이름 규칙: `v4_s{씬번호}_{img|veo|tts}_{장면이름}_v{버전}.{png|mp4|mp3}` (예: `v4_s02_veo_humanities_v01.mp4`)

## 4. 전체 대본

```
S01 [폭풍 직전의 바다, 코디세이호 뱃머리]
선장     (장엄하게) 바람이… 바뀌었다.
         (정적 1초. 파도 소리만)
선장     (갑자기 무심하게) 모집 기간이다.

S02 [강변 도서관 앞 부두. 배가 들어와 닿는다]
선장     그대. 승선하라.
소라     저요? …저 국문과인데요.
         (정적 1초. 갈매기. 선장 눈썹만 올라감)
선장     그래서?

S03 [승선 사다리 앞 빈 문틀]
소라     …어? 표 검사 안 해요?
선장     원래 없었다, 문턱.
                                         [슈퍼] 전공·경력 무관

S04 [군항 부두]
선장     그대 안에서… 코드가 깨어났다.
도현     충성! …근데 저 돈이 없습니다!
         (빈 지갑을 뒤집자 먼지 한 줌. 정적 1초)
선장     알고 있다. 그래서 준다.

S05 [갑판, 보물상자]
도현     …뭘요?
선장     장학금.
                                         [슈퍼] 장학금

S06 [야근 사무실, 창밖 구름 위에 떠 있는 배]
선장     (창밖 뱃전에서 망원경으로 유리를 똑똑) 지친 자여… 코디세이로 오라.
민석     (고개만 돌려) …여기 23층인데요.
         (정적 1초. 배는 그대로 떠 있음)

S07 [민석 클로즈업]
민석     저 혼자 하면… 맨날 포기해요.
선장     그래서 혼자 안 시킨다.
                                         [슈퍼] 동료학습

S08 [먼바다로 나아가는 코디세이호 갑판]
도현     (경례) 충성! 동기입니까!
선장     동료다.
선장     이 배에선 서로가 선장이고 선생이다.
셋       같이 갑시다!

S09 [선실 앞 빈 문틀]
         (선장이 허공에 노크하려다 멈춤)
도현     (작게) …문 없는데요.
선장     (헛기침) 알고 있다.

S10 [해 뜨는 바다로 나아가는 배, 뱃머리의 네 사람 뒷모습]
선장     (돌아보며 비장하게) 코디세이로 와라!
                                         [엔드카드] 문턱은 없고, 동료는 있다.
                                         전공 무관 · 장학금 · 동료학습
                                         CODYSSEY  codyssey.kr
```

## 5. 씬별 스토리보드

### S01 · 출항 신호 — 0:00~0:06 (6초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 평범한 사람에게도 떠날 기회가 온다. 장엄하게 열고 첫 6초 안에 김을 빼서 광고의 톤을 알린다. |
| 화면 구성 | **구도:** 항공 와이드에서 뱃머리 미디엄으로 느린 푸시인 · **피사체:** 망원경을 든 노선장, 정면 · **배경:** 먹구름이 몰려오는 거친 바다 위 코디세이호 · **텍스트:** 없음 (하단 1/3은 자막 여백) |
| 대사 | 선장(0.5s, 장엄) "바람이… 바뀌었다." / 정적 1초 / 선장(4.0s, 무심) "모집 기간이다." |
| 사운드 | 오케스트라 히트와 파도 → 정적(파도 소리만) → 바람 |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사, 효과음 (8초로 생성해 6초 사용) |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s01_img_departure_v01.png · v4_s01_veo_departure_v01.mp4 |

**프롬프트 원문 (veo)**
```
Aerial wide shot of {SHIP} cutting through rough dark sea under gathering storm clouds, slowly pushing in to a medium shot of {CAPTAIN} standing at the bow, facing the camera, coat and braid whipping in the wind. 0-3s: she says in Korean in a grand, slow, solemn voice: "바람이… 바뀌었다." 3-4s: silence except waves, she just stares into the camera. 4-6s: she says in Korean in a sudden flat, bored, matter-of-fact voice: "모집 기간이다." Sound: one huge orchestral hit with crashing waves at the start, then only waves, then soft wind. {LOOK} {KO}
```

### S02 · 국문과 — 0:06~0:14 (8초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 전공이 달라도 상관없다. |
| 화면 구성 | **구도:** 고정 미디엄 투샷 · **피사체:** 왼쪽에 책 더미를 안은 소라, 오른쪽 뱃전에서 망원경으로 소라를 가리키는 선장 · **배경:** 맑은 날 강변 도서관 앞 나무 부두, 뒤로 코디세이호 선체가 닿아 있다 · **텍스트:** 없음 |
| 대사 | 선장(0.5s) "그대. 승선하라." / 소라(2.5s, 당황) "저요? …저 국문과인데요." / 정적 1초 (선장은 한쪽 눈썹만 올린다) / 선장(6.3s, 무심) "그래서?" |
| 사운드 | 배 닿는 소리, 정적 구간엔 갈매기와 물결만 |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (8초) |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s02_img_humanities_v01.png · v4_s02_veo_humanities_v01.mp4 |

**프롬프트 원문 (veo)**
```
Fixed medium two-shot on a sunny wooden pier in front of a riverside university library; the hull of {SHIP} has just docked behind. {SORA} stands on the pier on the left. {CAPTAIN} leans over the ship's rail on the right and points the spyglass at her dramatically. 0-2s: the captain says in Korean in a grand voice: "그대. 승선하라." 2-5s: the student blinks, points at herself, and says in Korean, flustered, voice rising: "저요? …저 국문과인데요." 5-6s: one second of silence, only seagulls and water; the captain raises one eyebrow and nothing else. 6-8s: the captain says in Korean, completely flat and unimpressed: "그래서?" Sound: wooden creak of docking, then only seagulls and lapping water during the pause. {LOOK} {KO}
```

**프롬프트 수정 전/후 (이 씬)**
- **수정 전:** `A ship captain calls a student on a pier and she says she is a literature major, comedy, Korean dialogue.`
- **수정 후:** 위 원문
- **무엇을 왜 바꿨나:**
  1. 대사마다 초 단위 구간을 지정했다. 개그의 핵심은 정적 1초인데, 지정하지 않으면 veo가 대사를 붙여 버린다.
  2. 대사를 따옴표 원문으로 넣고 `says in Korean`과 {KO}를 붙였다. v3에서 한 클립이 이탈리아어로 생성됐기 때문이다.
  3. 인물과 배를 고정 묘사({SORA}·{CAPTAIN}·{SHIP})로 넣었다. 씬이 바뀌어도 같은 사람, 같은 배로 보이게 하기 위해서다.
  4. "그래서?"의 말투를 `completely flat and unimpressed`로 못 박았다. 웃음 포인트가 장엄에서 무심으로 떨어지는 낙차이기 때문이다.
- **결과:** 제작 후 기입 (수정 전·후 둘 다 생성해 받아쓰기 결과를 비교)

### S03 · 빈 문틀 — 0:14~0:18 (4초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 진입장벽이 실제로 없다. |
| 화면 구성 | **구도:** 고정 와이드 · **피사체:** 승선 사다리 앞에 문짝도 문턱도 없는 나무 문틀만 서 있다. 소라가 표를 내밀며 머뭇거리다 그냥 통과해 뒤돌아본다. 선장은 갑판 위에서 팔짱을 끼고 있다 · **배경:** S02 부두 · **텍스트:** 키워드 슈퍼 "전공·경력 무관" (편집 단계에서) |
| 대사 | 소라(0.5s) "…어? 표 검사 안 해요?" / 선장(2.3s) "원래 없었다, 문턱." |
| 화면 카피 | 전공·경력 무관 (2.5~4.0s) |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (4초) · Pillow: 슈퍼 |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s03_img_nothreshold_v01.png · v4_s03_veo_nothreshold_v01.mp4 |

**프롬프트 원문 (veo)**
```
Fixed wide shot on the same sunny pier. At the foot of the ship's boarding gangway stands an empty wooden doorframe with no door, no gate and no threshold step. {SORA} holds out a paper ticket, hesitates, then simply walks through the frame and looks back over her shoulder in surprise. Above on the deck, {CAPTAIN} stands with arms crossed. 0-2s: the student says in Korean, puzzled: "…어? 표 검사 안 해요?" 2-4s: the captain says in Korean, flat: "원래 없었다, 문턱." Sound: footsteps on wood, one soft fanfare note. {LOOK} {KO}
```

### S04 · 통장 — 0:18~0:26 (8초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 돈이 없어도 배울 수 있다. |
| 화면 구성 | **구도:** 고정 미디엄 투샷 · **피사체:** 더플백을 멘 채 차렷 자세의 도현, 밧줄을 타고 내려와 앞에 착지하는 선장 · **배경:** 맑은 날 회색 군함들이 보이는 항구 부두 · **텍스트:** 없음 |
| 대사 | 선장(0.3s, 장엄) "그대 안에서… 코드가 깨어났다." / 도현(2.8s, 경례) "충성! …근데 저 돈이 없습니다!" (빈 지갑을 뒤집자 먼지가 떨어진다) / 정적 1초 / 선장(6.2s, 무심) "알고 있다. 그래서 준다." |
| 사운드 | 밧줄 소리, 경례 소리, 먼지 푸스스, 정적 |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (8초) |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s04_img_veteran_v01.png · v4_s04_veo_veteran_v01.mp4 |

**프롬프트 원문 (veo)**
```
Fixed medium two-shot on a sunny harbor pier with distant grey navy ships. {DOHYUN} stands at attention. {CAPTAIN} slides down a rope from the ship above and lands in front of him, coat flapping. 0-2.5s: the captain says in Korean in a grand, slow voice: "그대 안에서… 코드가 깨어났다." 2.5-5s: the young man snaps a salute and shouts in Korean: "충성!", then his voice suddenly drops small and quick: "…근데 저 돈이 없습니다!" and he turns his empty wallet inside out, a tiny puff of dust falls. 5-6s: one second of silence, only water. 6-8s: the captain says in Korean, flat and calm: "알고 있다. 그래서 준다." Sound: rope whizz, salute snap, dust puff, silence. {LOOK} {KO}
```

### S05 · 장학금 — 0:26~0:30 (4초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 장학금을 받으며 배운다. |
| 화면 구성 | **구도:** 고정 미디엄, 약간 로우앵글 · **피사체:** 선장이 낡은 보물상자 뚜껑을 열자 금빛이 도현의 얼굴을 비춘다. 도현은 경례한 채 입을 벌리고 굳는다 · **배경:** 코디세이호 갑판 · **텍스트:** 키워드 슈퍼 "장학금" |
| 대사 | 도현(0.3s) "…뭘요?" / 선장(1.5s, 무심) "장학금." |
| 화면 카피 | 장학금 (1.8~4.0s) |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (4초) · Pillow: 슈퍼 |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s05_img_scholarship_v01.png · v4_s05_veo_scholarship_v01.mp4 |

**프롬프트 원문 (veo)**
```
Fixed slightly low-angle medium shot on the deck of {SHIP}. {CAPTAIN} flips open the lid of an old wooden treasure chest and warm golden light floods the face of {DOHYUN}, who freezes mid-salute with his mouth wide open. 0-1.5s: the young man says in Korean, stunned and quiet: "…뭘요?" 1.5-3s: the captain says in Korean, flat: "장학금." Sound: chest creak, a shimmering chime. {LOOK} {KO}
```

### S06 · 23층 — 0:30~0:37 (7초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 혼자 하다 지친 사람에게도 부름이 온다. |
| 화면 구성 | **구도:** 고정 미디엄 · **피사체:** 책상에 엎드린 민석. 창밖 구름 위에 코디세이호가 떠 있고, 선장이 뱃전에서 망원경으로 유리를 두드린다 · **배경:** 모니터 불빛만 남은 고층 야근 사무실 · **텍스트:** 없음 |
| 대사 | 선장(0.5s, 창밖, 장엄) "지친 자여… 코디세이로 오라." / 민석(3.4s, 고개만 돌려) "…여기 23층인데요." / 정적 1초 (배는 그대로 떠 있다) |
| 사운드 | 유리 똑똑, 형광등 웅웅, 멀리 파도 소리, 정적 |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (8초로 생성해 7초 사용) |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s06_img_worker_v01.png · v4_s06_veo_worker_v01.mp4 |

**프롬프트 원문 (veo)**
```
Fixed medium shot of a late-night high-rise office lit only by a monitor. {MINSEOK} is slumped over his desk. Outside the large window, {SHIP} floats impossibly on a sea of night clouds right next to the building, and {CAPTAIN} leans over the ship's rail, tapping on the window glass with her brass spyglass. 0-3s: the captain says in Korean, muffled through the glass, in a grand voice: "지친 자여… 코디세이로 오라." 3-5s: the office worker only turns his head toward the window, deadpan and exhausted, and says in Korean: "…여기 23층인데요." 5-7s: silence, the ship and the captain keep floating there without blinking. Sound: glass taps, fluorescent hum, faint distant waves, silence. {LOOK} {KO}
```

### S07 · 혼자 — 0:37~0:41 (4초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 혼자 하지 않는다. 동료와 함께 배운다. |
| 화면 구성 | **구도:** 민석 클로즈업에서 살짝 줌아웃 · **피사체:** 한숨 쉬는 민석. 창밖에서 따뜻한 랜턴 불빛이 들어와 양옆 빈 의자에 두 사람의 실루엣을 만든다 · **배경:** S06 사무실 · **텍스트:** 키워드 슈퍼 "동료학습" |
| 대사 | 민석(0.2s, 작게) "저 혼자 하면… 맨날 포기해요." / 선장(2.3s, 무심) "그래서 혼자 안 시킨다." |
| 화면 카피 | 동료학습 (2.5~4.0s) |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (4초) · Pillow: 슈퍼 |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s07_img_peers_v01.png · v4_s07_veo_peers_v01.mp4 |

**프롬프트 원문 (veo)**
```
Close-up of {MINSEOK} in the dark office, sighing, then the camera slowly pulls back: warm golden lantern light from the ship outside the window falls on the two empty chairs beside him and forms two soft glowing human silhouettes sitting next to him. 0-2s: the office worker says in Korean, quietly: "저 혼자 하면… 맨날 포기해요." 2-4s: the captain's voice from outside the window says in Korean, flat: "그래서 혼자 안 시킨다." Sound: soft rising chimes, faint waves. {LOOK} {KO}
```

### S08 · 동료 — 0:41~0:49 (8초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 여기엔 교수 대신 동료가 있고, 서로 가르친다. |
| 화면 구성 | **구도:** 고정 와이드 · **피사체:** 갑판에 각자 다른 사다리로 올라와 어색하게 마주친 소라·도현·민석, 키를 잡은 선장 · **배경:** 돛을 활짝 펴고 먼바다로 나아가는 코디세이호, 파도와 물보라 · **텍스트:** 없음 |
| 대사 | 도현(0.8s, 경례) "충성! 동기입니까!" / 선장(2.4s) "동료다." / 선장(3.6s) "이 배에선 서로가 선장이고 선생이다." / 셋(6.0s, 함께) "같이 갑시다!" |
| 사운드 | 어색한 정적과 파도 → "같이 갑시다!"에서 돛이 펄럭이며 오케스트라 고조 |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (8초) |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s08_img_crew_v01.png · v4_s08_veo_crew_v01.mp4 |

**프롬프트 원문 (veo)**
```
Fixed wide shot on the deck of {SHIP} sailing out to the open sea, sails full, sea spray in golden light. {SORA}, {DOHYUN} and {MINSEOK} each climb up onto the deck from different rope ladders and stop awkwardly, facing each other. {CAPTAIN} stands at the ship's wheel behind them. 0-2s: the army man snaps a salute and shouts in Korean: "충성! 동기입니까!" 2-3.5s: the captain says in Korean, flat: "동료다." 3.5-5.5s: the captain says in Korean, calm: "이 배에선 서로가 선장이고 선생이다." 5.5-8s: the three young people grab the same rope together, pull, and shout in Korean in unison: "같이 갑시다!" as the sails snap open. Sound: awkward silence with waves, then a grand orchestral swell and flapping sails on the shout. {LOOK} {KO}
```

### S09 · 노크 — 0:49~0:52 (3초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 문이 없으니 노크할 필요도 없다. 진입장벽이 없다는 메시지를 개그로 한 번 더 회수한다. |
| 화면 구성 | **구도:** 고정 와이드 · **피사체:** 선실 입구의 문짝 없는 문틀 앞 네 사람. 선장이 허공에 노크하려다 멈추고, 셋은 선장을 쳐다본다 · **배경:** 항해 중인 갑판 · **텍스트:** 없음 |
| 대사 | 도현(0.4s, 작게) "…문 없는데요." / 선장(1.6s, 헛기침 후 무심) "알고 있다." (S04 콜백) |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (4초로 생성해 3초 사용) |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s09_img_knock_v01.png · v4_s09_veo_knock_v01.mp4 |

**프롬프트 원문 (veo)**
```
Fixed wide shot on the sailing deck of {SHIP}. The cabin entrance is an empty wooden doorframe with no door. Four people stand in front of it in a row: {CAPTAIN}, {SORA}, {DOHYUN} and {MINSEOK}. The captain raises a fist to knock on the empty air inside the frame, then stops. 0-1.5s: the army man says in Korean, quietly: "…문 없는데요." 1.5-3s: the captain clears her throat, lowers her fist, and says in Korean, deadpan: "알고 있다." Sound: waves, creaking wood. {LOOK} {KO}
```

### S10 · 엔드카드 — 0:52~0:57 (5초)

| 필드 | 내용 |
|---|---|
| 목표 메시지 | 문턱은 없고, 동료는 있다. 코디세이로 와라. |
| 화면 구성 | **구도:** 고정 와이드, 뒷모습. 화면 위쪽 절반은 하늘로 비워 둔다 · **피사체:** 뱃머리에 나란히 선 네 사람 · **배경:** 해가 떠오르는 잔잔한 바다로 나아가는 코디세이호 · **텍스트:** 엔드카드 (편집 단계에서) |
| 대사 | 선장(1.8s, 돌아보며 비장하게) "코디세이로 와라!" |
| 화면 카피 | 문턱은 없고, 동료는 있다. / 전공 무관 · 장학금 · 동료학습 / CODYSSEY / codyssey.kr / ※ 연출된 가상 상황 · AI로 제작 |
| 사용 도구 | gpt-image-2: 콘티 이미지 · veo-3.1: 영상, 대사 (6초로 생성해 5초 사용) · Pillow: 엔드카드 |
| 출력 결과 요약 | 제작 후 기입 |
| 파일 | v4_s10_img_endcard_v01.png · v4_s10_veo_endcard_v01.mp4 |

**프롬프트 원문 (veo)**
```
Locked wide shot from behind: four people stand in a row at the bow of {SHIP}, seen from the back, sailing toward a rising sun over a calm golden sea: {CAPTAIN} and three young people in a cream cardigan, an olive-khaki hoodie and a cobalt-blue shirt. The upper half of the frame is clear open sky with calm empty space. 1.5-4s: the captain turns her head slightly and says in Korean in a grand, solemn, commanding voice: "코디세이로 와라!" Sound: a grand orchestral finale, waves. No text in the sky. {LOOK} {KO}
```

## 6. 제작 순서와 검수 (승인 후)

1. gpt-image-2로 씬별 콘티 이미지 10장을 만든다. 인물·배·구도를 확인하고 스토리보드 PDF에 넣는다.
2. veo-3.1로 클립 10개를 만든다.
3. 클립마다 faster-whisper로 받아써서 세 가지를 확인한다.
   - 한국어인지
   - 대본과 같은 대사인지
   - 정적 1초가 살아 있는지

   틀린 클립만 다시 만들고, 한 클립당 재생성은 최대 2번까지 한다.
4. 두 번 다시 만들어도 틀린 대사는 gpt-4o-mini-tts로 그 줄만 다시 입힌다.
5. 자막 시각은 받아쓰기 단어 타임스탬프로 정한다.
6. 편집한다: 컷 → 자막 → 키워드 슈퍼 → 엔드카드 → 음량 맞춤.
7. 완성본을 다시 받아써서 자막과 소리를 최종 대조한다.

크레딧 계획: veo 기본 10회에 재생성 여유 5회를 더한다. 부족하면 S03·S05·S07(4초 증명 컷)을 콘티 이미지에 줌을 넣은 컷과 TTS 대사로 바꾼다.

## 7. 리스크

| 리스크 | 대응 |
|---|---|
| veo가 다른 언어로 말함 | 모든 프롬프트에 {KO}를 넣고, 클립마다 받아써서 검수한다 |
| 정적 1초가 사라짐 | 초 단위 구간을 지정한다. 그래도 사라지면 편집에서 정적 프레임을 늘린다 |
| 씬마다 선장 얼굴이나 배가 달라짐 | 고정 묘사를 글자 그대로 넣는다. 재생성 기준은 은빛 땋은 머리, 선장 코트와 모자, 크림색 돛 |
| 해적 영화 연상 | 해적 모자·칼·해골 깃발을 쓰지 않는다. 깃발과 선체 글자도 없앤다 |
| "그래서 준다"가 금액 약속으로 읽힘 | 금액·조건은 언급하지 않는다. 공식 문구("장학금을 받으며 배우는") 범위만 쓰고, 모든 컷에 가상 연출임을 고지한다 |
| "서로가 선장이고 선생이다"가 운영 사실 단정으로 읽힘 | 공식 소개의 "교수 없이 동료학습" 범위 안의 표현만 쓴다 |
