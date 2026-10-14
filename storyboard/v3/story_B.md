# v3-B 「코디세이로 오세요」 — 패러디 개그형 (기사단 모집)

## 0. 한 줄 요약

- **로그라인**: 우주를 떠도는 사부가 평범한 사람 셋을 차례로 "코디세이로 오라" 부르는데, 셋이 "전공이 아닌데요 / 돈이 없는데요 / 혼자는 못 하는데요" 하고 빼는 족족 사부가 한 방에 받아치고, 마지막엔 셋이 한 줄로 서서 기사단이 된다.
- **슬로건(시청자가 기억할 문장 1개)**: **"문턱은 없고, 동료는 있다."**
- **CTA**: "코디세이로 오세요~" + codyssey.kr (엔드카드 + 사부 음성)
- **길이 / 씬 / veo**: 55초 / 10씬 / veo 클립 6개(영상 5 + BGM 1, 한도 8 이내, 재시도 여유 2) + gpt-image-2 정지컷 5장
- **톤**: 스타워즈풍 장대한 '부름'을 진지하게 시작 -> 대답이 소박해서 터지는 B급 갭 개그(장삐쭈식 정적 -> 한 방). 브랜드 톤(차분·응원, 공포·과장 소구 없음)은 사부의 따뜻한 마무리로 지킨다.
- **화풍**: 시험 클립 B_S01_test.mp4의 2D 플랫 카툰 유지. `storyboard_v2.json`의 `style_lock.style_suffix`를 모든 프롬프트 끝에 한 글자도 바꾸지 않고 붙인다.
- **내레이션 없음**: 설명 문장 없이 사부의 부름, 인물의 거절, 사부의 받아침 대사와 장면만으로 메시지를 전한다. 자막은 키워드(전공 무관/장학금/동료학습)와 엔드카드뿐.

## 1. 메시지 3개가 "보여지는" 곳 (설명 아님)

| 메시지 | 거절 대사(문제) | 받아침(해결) | 화면에서 보이는 것 | 씬 | 길이 |
|---|---|---|---|---|---|
| 진입장벽 없음 (전공·경력 무관) | 문과생 "저 국문과인데요?" | 사부 "입구에 전공 칸 없다." | 입구라던 곳이 문도 문턱도 없는 빈 문틀. 문과생이 그냥 걸어 들어감 | S02-S03 | 11초 |
| 장학금 | 전역자 "충성! 통장이 비었습니다." | 사부 "장학금 받으며 배운다." | 텅 빈 지갑 위로 별 모양 동전이 쏟아지고, 사부가 두루마리 리본을 둘러줌 | S04-S05 | 11초 |
| 동료학습 | 직장인 "혼자 하면 맨날 포기하는데요." | 사부 "혼자 안 한다. 서로 가르친다." | 세 사람 머리 위 별이 선으로 이어져 별자리가 되고, 엔딩에서 "여기 교수 없다, 나도 동료한테 배웠다" | S06-S07, S08 | 11초 + 10초 |

균형: 세 메시지 모두 11초씩 동일 비중. 동료학습은 마지막 반전(S08)에서 한 번 더 회수한다.
사실 근거(brand): 전공·경력 무관, 학비·시간 제약 없이 장학금을 받으며 배움, 교수 중심 강의가 아닌 동료학습+PBL. 금액·기간·일정·취업률 등 수치는 대사·자막 어디에도 쓰지 않는다.

## 2. 캐릭터 (오리지널, v2 DOHYUN·MINSEOK 재사용)

- **사부 "마스터 오디"** (오디세이에서 따옴): 키 큰 차분한 멘토, 긴 은빛 땋은 머리, 별자리 점무늬 코발트 망토, 어깨에 멘 민트색 거대 키보드 검. 눈은 점, 눈썹만 코믹하게 움직임. 음성 TTS `onyx`(장엄하게 시작, 받아칠 때 무심하게).
- **문과생 "소라"**: 둥근 안경, 노란 머리끈, 크림 가디건, 책 더미를 안고 있음. TTS `nova`.
- **전역자 "도현"**: 짧은 머리, 카키 후디, 경례 버릇, 더플백. TTS `echo`(씩씩).
- **직장인 "민석"**: 코발트 셔츠, 느슨한 남색 넥타이, 목걸이 사원증, 지친 눈. TTS `fable`(힘 빠진 톤).
- 일관성 방법: 캐릭터 블록 문자 그대로 복붙 + 동일 style_suffix + 팔레트 6색 고정. 씬마다 배경 색 변경(S02 크림+민트, S04 코발트+크림, S06 노랑+코랄)으로 연속성 요구를 줄임. 3인 동시 등장은 S08 한 컷, 실패 시 S07 정지컷 방식(gpt-image-2)으로 대체.

## 3. 전체 대본 (55초)

범례: [화면] / 사부·소라·도현·민석 = 대사(TTS) / [SFX·BGM] / 자막(Pillow PNG 오버레이)

| 시각 | 화면 | 대사 | 사운드 | 자막 |
|---|---|---|---|---|
| 0.0-6.0 (S01) | 깊은 밤 우주. 별들이 모여 키보드 모양 검의 윤곽을 그리고, 그 앞으로 사부가 천천히 돌아선다 | 사부(0.8) "별이 말했다." (2.2) "평범한 자에게도, 힘은 있다고." | [BGM] 오리지널 브라스 팡파르 시작(웅장), 별 반짝 SFX | 4.4-6.0 "코디세이 기사단" (흰 글자+남색 외곽선) |
| 6.0-14.0 (S02) | 크림+민트 도서관 계단. 소라가 책 더미를 안고 걷는다. 사부가 망토를 휘날리며 앞에 선다 | 사부(6.4) "깨어나라, 그대여. 코디세이로 오라." / 소라(9.4) "...저 국문과인데요?" / (정적 1초, 사부 눈썹만 올라감) / 사부(11.4) "입구에 전공 칸 없다." | [BGM] 멈춤 -> 레코드 스크래치(9.9) -> 정적 -> 짧은 "띵"(12.8) | 없음 |
| 14.0-17.0 (S03) | 정지컷. 사부가 가리킨 '입구'는 문도 문턱도 없는 빈 문틀. 소라가 뒤돌아 확인 | 소라(14.2) "어? 문턱이 없네?" | [SFX] 팡파르 한 음, 바람 소리 | 14.1-17.0 "전공 무관" (노랑 강조, 중앙 150px) |
| 17.0-25.0 (S04) | 코발트+크림 연병장 담벼락 앞. 도현이 더플백을 멘 채 경례. 사부가 등장 | 사부(17.4) "그대 안의 코드도 깨어났다. 코디세이로 오라." / 도현(20.3) "충성! ...통장이 비었습니다!" / (정적, 도현이 빈 지갑을 뒤집어 털음) / 사부(22.8) "장학금 받으며 배운다." | [BGM] 행진 리듬 -> 멈춤(20.8) -> 빈 지갑 먼지 "휘이" -> 사부 대사와 함께 BGM 복귀 | 없음 |
| 25.0-28.0 (S05) | 정지컷. 별 모양 동전이 비처럼 쏟아지고 도현이 입 벌리고 올려다봄. 사부는 리본 두루마리를 어깨에 둘러줌 | 도현(25.2) "...받으며요?!" | [SFX] 동전 쏟아지는 소리, 경례 "착!" | 25.1-28.0 "장학금" (노랑 강조) |
| 28.0-36.0 (S06) | 노랑+코랄 야근 사무실 창가, 밤. 민석이 노트북 앞에서 늘어짐. 사부가 창문 밖(우주)에서 떠올라 등장 | 사부(28.4) "지친 자여. 코디세이로 오라." / 민석(30.6) "혼자 하면 맨날 포기하는데요..." / 사부(33.2) "혼자 안 한다. 서로 가르친다." | [BGM] 낮은 첼로 한 줄(지침) -> 사부 대사에 맞춰 BGM 밝아짐 | 없음 |
| 36.0-39.0 (S07) | 정지컷. 민석의 머리 위 별이 옆 두 별과 선으로 이어져 별자리를 이룸. 민석이 처음으로 웃음 | (대사 없음, 민석 작은 웃음 TTS) | [SFX] 별 이어지는 "띠링띠링" 3음 | 36.1-39.0 "동료학습" (노랑 강조) |
| 39.0-47.0 (S08) | 우주 계단 위, 세 명이 각자의 문 없는 입구로 도착해 어색하게 마주침. 사부가 돌아서서 팔짱 | 민석(39.4) "...저분들도요?" / 도현(40.8) "충성! 동료입니까!" / 사부(42.4) "여기 교수는 없다." / 셋(44.0) "...네?" / 사부(44.8) "동료가 있다. 나도 동료한테 배웠다." | [BGM] 어색한 침묵 -> 팡파르 복귀(46.0), 마지막 3인 키보드 검 포즈 쾅 | 없음 |
| 47.0-50.0 (S09) | 정지컷 코다. 네 명이 빈 문틀 앞. 사부가 빈 허공에 노크 포즈 | 사부(47.4) "노크는... 하세요." | [SFX] 허공 "똑똑"(소리는 나지 않음 -> 정적 개그) | 없음 |
| 50.0-55.0 (S10) | 엔드카드. 크림 배경, 가운데 도장 원 안에 CODYSSEY 워드마크. 위에 슬로건, 아래 CTA | 사부(50.3) 따뜻하게 "코디세이로 오세요~" | [BGM] 팡파르 마무리 + 별 "띠링" 1음 | 슬로건 "문턱은 없고, 동료는 있다."(120px, "문턱", "동료" 노랑) / "CODYSSEY" 64px / "코디세이로 오세요" / codyssey.kr 44px |

※ 시각은 TTS 길이에 따라 +-0.3초 조정. 대사는 컷 단위로 분리 TTS 후 ffmpeg `adelay`로 배치. 한 대사 최대 약 3초.

장삐쭈식 박자: 부름(장엄) -> 거절(소박) -> 정적 1초 -> 한 방 받아침, 이 4박을 세 번 같은 길이로 반복해 리듬을 학습시키고, S08에서 박자를 깨는(셋이 동시에 등장, 사부가 돌아서 "교수는 없다") 반전으로 마무리.

## 4. 씬 표

프롬프트 원문은 아래 5장에 씬 ID별로 모았다(표 가독성 때문). 정지컷 대체 가능 여부는 "대체" 열.

| 씬 | 길이 | 목표 메시지 | 화면 구성 | 대사·자막 | 도구 | 프롬프트 | 파일명 | 대체 |
|---|---|---|---|---|---|---|---|---|
| S01 | 6초 | 부름의 세계관(장대한 시작, 기사단) | 우주, 별로 그린 키보드 검, 사부 정면 중앙, 하단 여백 | 사부 "별이 말했다..." / 자막 "코디세이 기사단" | veo-3.1-fast, 오디오 SFX만 | P-S01 | B_S01_call.mp4 | 가능(정지컷+줌 6초) |
| S02 | 8초 | 진입장벽 없음 -> 문제 제기와 한 방 | 크림+민트 도서관 계단, 미디엄 샷 2인, 사부 우측 | 사부·소라 대사 / 자막 없음 | veo-3.1-fast | P-S02 | B_S02_humanities.mp4 | 어려움(연기 중심) |
| S03 | 3초 | 진입장벽 없음 -> 증명(빈 문틀) | 빈 문틀 클로즈업, 소라 뒤돌아봄 | 소라 대사 / 자막 "전공 무관" | gpt-image-2 + ffmpeg 줌 | P-S03 | B_S03_nothreshold.png | 정지컷 기본 |
| S04 | 8초 | 장학금 -> 문제 제기와 한 방 | 코발트+크림 담벼락, 도현 경례, 빈 지갑 털기 | 사부·도현 대사 | veo-3.1-fast | P-S04 | B_S04_veteran.mp4 | 어려움 |
| S05 | 3초 | 장학금 -> 증명(별 동전 비) | 동전 비, 올려다보는 도현, 두루마리 리본 | 도현 대사 / 자막 "장학금" | gpt-image-2 + ffmpeg 줌 | P-S05 | B_S05_scholarship.png | 정지컷 기본 |
| S06 | 8초 | 동료학습 -> 문제 제기와 한 방 | 노랑+코랄 야근 사무실, 창밖 우주에서 사부 등장 | 사부·민석 대사 | veo-3.1-fast | P-S06 | B_S06_worker.mp4 | 어려움 |
| S07 | 3초 | 동료학습 -> 증명(별자리) | 별 3개가 선으로 연결, 민석 웃음 | 자막 "동료학습" | gpt-image-2 + ffmpeg 줌 | P-S07 | B_S07_constellation.png | 정지컷 기본 |
| S08 | 8초 | 동료학습 회수 + 셋이 함께 서는 반전 | 우주 계단, 세 명 도착, 사부 돌아섬, 마지막에 4인 키보드 검 포즈 | 5개 대사 | veo-3.1-fast | P-S08 | B_S08_knights.mp4 | 실패 시 S07식 정지컷 3컷 |
| S09 | 3초 | 개그 코다(문턱 없음 회수) | 빈 문틀 앞 4인, 사부가 허공 노크 | 사부 "노크는... 하세요." | gpt-image-2 + ffmpeg 줌 | P-S09 | B_S09_knock.png | 정지컷 기본 |
| S10 | 5초 | 브랜드·CTA | 크림 배경, 도장 원 워드마크, 슬로건, URL | 사부 "코디세이로 오세요~" / 슬로건·URL 자막 | gpt-image-2(배경, 글자 없음) + Pillow | P-S10 | B_S10_endcard_bg.png -> B_S10_endcard.png | 정지컷 기본 |
| BGM | 8초 | 오리지널 코믹 팡파르(장엄 -> 소박) | 어두운 단색 화면(영상 미사용) | 없음 | veo-3.1-fast 오디오 추출, 루프·크로스페이드 | P-BGM | B_BGM_fanfare.mp4 -> .m4a | 대체: gemini 음악 불가 시 Veo 다른 시드 재시도 |

파일명 규칙: `B_S{번호}_{키워드}.{mp4|png}` (시험 클립 B_S01_test.mp4와 동일 규칙). 공통 후처리: 1080p lanczos 업스케일, 24fps, 동일 미세 그레인, H.264/AAC.

### 4-1. 프롬프트 원문 (영어)

공통 규칙: 각 프롬프트 끝에 아래 STYLE을 그대로 붙인다.

STYLE = `flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9`

캐릭터 블록(문자 그대로 복붙):
- MASTER = `a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows`
- SORA = `a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes`
- DOHYUN = `a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes`
- MINSEOK = `a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes`

공통: 대사는 TTS로 따로 얹으므로 Veo 프롬프트에 "no speech, no dialogue, no voices, sound effects only"를 넣고, 입은 말없이 작게 움직이도록 둔다.

**P-S01** (veo-3.1-fast, 6초)
`Night outer space, deep navy sky full of twinkling stars. The stars drift together and trace the outline of a giant keyboard-shaped sword, then fade to calm. In the center foreground MASTER slowly turns around to face the camera with a solemn look, cloak fluttering. Slow epic push-in, 6 seconds. Sound effects only: soft star twinkles and a low wind, no speech, no dialogue, no voices. [STYLE]`

**P-S02** (veo-3.1-fast, 8초)
`Cream and mint colored library steps, a sunny day. SORA walks up the steps hugging her books. MASTER sweeps in from the right with cloak flying and points at her dramatically. SORA freezes, sweat drop, mouth moves in a small hesitant way. A one second silent beat: MASTER only raises one eyebrow. Then MASTER gestures a flat dismissive wave to the side, SORA turns her head to look where he points. Fixed medium shot, 8 seconds, comedic timing with a hard pause. Sound effects only: cloak whoosh and a small record scratch, no speech, no dialogue, no voices. [STYLE]`
(MASTER, SORA 블록은 위 문구를 해당 위치에 그대로 풀어쓴다.)

**P-S03** (gpt-image-2, 정지컷)
`An empty wooden doorframe standing alone with no door and no threshold step, floating on white steps in a sunny cream and mint scene, a bright path passing straight through it. In front, SORA looks back over her shoulder in surprise, a stack of books in her arms. In the back MASTER leans on his keyboard sword, smug. Wide composition with empty space at the center for a caption. [STYLE]`

**P-S04** (veo-3.1-fast, 8초)
`Cobalt blue and cream colored parade ground wall, a bright day. DOHYUN stands at attention and snaps a salute. MASTER drifts in from above with cloak flapping, reaching out a hand. DOHYUN pulls his empty wallet out of the hoodie pocket and turns it inside out, a tiny puff of dust falls out, he looks panicked. A one second silent beat. MASTER swings his keyboard sword up slowly with a confident grin, a glowing scroll with a ribbon unrolls from it. Fixed medium shot, 8 seconds. Sound effects only: salute snap, dust puff, scroll unroll, no speech, no dialogue, no voices. [STYLE]`

**P-S05** (gpt-image-2, 정지컷)
`Star-shaped golden coins pouring down like rain from the top of the frame onto DOHYUN, who looks up with his mouth wide open and one hand frozen in a salute. MASTER stands beside him draping a glowing ribbon scroll over his shoulder, smiling. Cobalt blue and cream background, space left in the upper center for a caption. [STYLE]`

**P-S06** (veo-3.1-fast, 8초)
`Yellow and coral colored office at night, a big window showing outer space and stars. MINSEOK slumps over a laptop with his face drooping toward the keyboard. MASTER rises up outside the window floating in space, cloak waving, and taps on the glass with one finger. MINSEOK looks up slowly and shrugs, drooping. A one second silent beat. Then two small star-shaped lights float in through the window and settle next to MINSEOK, who blinks at them. Fixed medium shot, 8 seconds. Sound effects only: glass tap, soft chime, no speech, no dialogue, no voices. [STYLE]`

**P-S07** (gpt-image-2, 정지컷)
`Three glowing stars above three people's heads connected by thin sunflower yellow lines into a small constellation, over a yellow and coral night office window. MINSEOK in the foreground smiles for the first time, eyes bright. Two small silhouettes of other people appear faintly under the other stars. Space left at the center for a caption. [STYLE]`

**P-S08** (veo-3.1-fast, 8초)
`A staircase floating in space with stars all around. SORA, DOHYUN and MINSEOK each arrive through their own empty doorframe and stop awkwardly when they see each other. They look at one another and wave stiffly. MASTER turns his back, arms crossed, then slowly looks over his shoulder. The three look surprised together. In the last two seconds all four raise their keyboard swords at the same time in a heroic pose while stars connect behind them into a constellation. Fixed wide shot, 8 seconds. Sound effects only: soft footsteps, star chimes, no speech, no dialogue, no voices. [STYLE]`
(세 명이 같은 컷에서 서로 다른 의상을 유지하도록 SORA, DOHYUN, MINSEOK 블록을 풀어쓴다. 전원이 키보드 검을 드는 것은 마지막 2초 포즈이며 장난감 소품 연출로, 위협·무기 표현이 아님. 검수에서 위협적이면 검을 "glowing keyboard held up like a trophy"로 수정.)

**P-S09** (gpt-image-2, 정지컷)
`An empty wooden doorframe floating in space in front of four characters in a row, SORA, DOHYUN, MINSEOK and MASTER. MASTER raises a fist and is about to knock on the empty air, deadpan face, while the other three watch him with sweat drops. Cream and mint background. Wide composition. [STYLE]`

**P-S10** (gpt-image-2, 배경만. 글자·도장·URL은 Pillow로 합성)
`A clean cream background with a soft ring of tiny constellation stars forming a circle at the center, three small cartoon figures standing on the lower edge looking up at the stars, plenty of empty space for a slogan above and a logo stamp at the center. [STYLE]`

**P-BGM** (veo-3.1-fast, 8초, 오디오 추출용)
`A plain dark navy screen with slowly twinkling small stars. Audio only matters: an original comedic brass fanfare, solemn and grand at first with timpani, then a tiny kazoo and a plucky pizzicato playful ending, 8 seconds, loopable, no melody from any existing film. [STYLE]`

### 4-2. 오버레이·사운드 (ffmpeg 합성 메모)

- 자막: Pillow 투명 PNG, Apple SD Gothic Neo ExtraBold, 흰 글자 + 남색(#1B1F3B) 외곽선(글자 크기의 약 12%), 강조어만 해바라기 노랑(#FFC933), 0.2초 팝인 후 하드컷 아웃. 키워드 자막 150px(중앙), 대사 강조 없음(대사 반복 금지), 엔드카드 슬로건 120px.
- 가상 연출 표기: 하단 좌측에 작게 "※ 연출된 가상 상황 · AI로 제작" 30px(전 컷 공통).
- 오디오: TTS 컷별 생성(gpt-4o-mini-tts, instructions로 톤 지정: 사부 장엄 -> 무심, 민석 힘 없음) 후 `adelay`로 배치, BGM은 duck(-12dB)로 대사 위에 얹음. TTS 대체: gemini-2.5-flash-tts.

## 5. IP 회피 체크

| 피한 것 | 이유 | 대체한 것 |
|---|---|---|
| "제다이", "포스", "라이트세이버", "스타워즈" 단어 | 상표·IP | "코디세이 기사단", "그대 안의 코드", "키보드 검" |
| 요다 닮은 캐릭터(작은 키, 뾰족 귀, 녹색 피부, 도치 어순 말투) | 캐릭터 IP | 키 큰 은빛 땋은 머리 멘토, 코발트 별자리 망토, 평서 어순 말투 |
| 오프닝 크롤(노란 글자가 원근으로 올라가는 연출, 파란 "a long time ago" 문구) | 시그니처 연출 | 정적 타이틀 카드(흰 글자+남색 외곽선) "코디세이 기사단", 대사 "별이 말했다" |
| 존 윌리엄스 테마·유사 선율, 광선검 웅웅 소리 | 저작권·사운드 IP | 오리지널 코믹 팡파르(브라스+카주 반전), 키보드 타건/별 반짝 SFX. 프롬프트에 "no melody from any existing film" 명시 |
| 다스 베이더형 검은 투구·호흡 소리 | 캐릭터 IP | 등장 악역 없음 |
| 폭력·위협(검 휘두름, 무기 겨눔) | 가이드라인·브랜드 톤 | 검은 소품(키보드), 휘두르지 않고 들어 올리는 포즈만 |
| 새 수치·일정·금액 | 브랜드 사실 규칙 | 숫자 대사·자막 없음, 장학금은 이미지(별 동전)와 단어만 |

패러디 수준: "먼 곳의 멘토가 평범한 자를 부르고 거절당한다"는 신화적 구조(부름 -> 거부)는 보편적 서사이며 특정 IP의 표현이 아님. 시청자가 "아 그거네" 하고 웃을 만한 분위기만 가져온다.

## 6. 리스크·대체

- Veo 한국어 대사 의존 없음(TTS 후배치). 입 모양 불일치는 캐릭터 입을 작게 그리는 프롬프트 + 컷 전환(대사 사이 클로즈업 컷)으로 완화, 심하면 입을 가린 구도(뒷모습·손으로 입 가림)로 재생성.
- 한 클립 8초 안에 4박(부름·거절·정적·받아침)이 모두 안 들어가면 정지컷(S03/S05/S07)이 받아침 박을 맡도록 이미 분리해 두었다. 실패 시 S02/S04/S06을 gpt-image-2 정지컷 2장 + 줌으로 대체 가능.
- 프롬프트 수정 전/후(미션 권장): S02 1차 "a woman refuses and a mentor points at the doorway"에서 문턱이 그려지는 문제 -> 2차에서 "empty doorframe with no door and no threshold step"로 수정 예정(제작 시 실제 결과 기록).
