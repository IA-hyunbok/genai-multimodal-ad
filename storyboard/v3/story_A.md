# v3 시안 A — 「코디세이로 오라」 (정공법 서사형)

## 0. 한 줄 요약

| 항목 | 내용 |
|---|---|
| 로그라인 | 은하 맨 끝 24시 편의점의 야간 알바생이 "난 자격이 없다"고 말하던 밤, 낯선 사부가 나타나 "자격은 안 묻는다, 코디세이로 오라"고 부르고, 혼자서는 막히던 길을 동료들과 별자리처럼 이어 간다. |
| 슬로건 (시청자가 기억할 문장) | **"자격은 안 묻습니다. 코디세이로 오세요."** (영상 속 사부 대사는 "코디세이로 오라") |
| CTA | 엔드카드: `codyssey.kr` + "기사단 모집 확인하기" (일정·금액·인원 수치 없음) |
| 톤 | 스케일은 장대, 말투는 B급(장삐쭈풍). 마지막은 차분하고 응원하는 톤(brand.tone_and_manner). 설명 내레이션 없음, 대사와 장면만 사용. |
| 총 길이 | 56초 (5+8+4+5+6+6+8+3+6+5) |
| 씬 수 | 10씬 = veo 7클립 + gpt-image 정지컷 3장 (veo 예비 1클립: 리테이크 또는 BGM용) |
| 화풍 | v2 시험 클립 B_S01_test 화풍 유지, `style_lock.style_suffix` 문자 그대로 재사용 |

## 1. 메시지 3개는 어디서 "보이는가"

| 메시지 | 보여지는 씬 | 장면·대사 (설명 아님) | 비중 |
|---|---|---|---|
| ① 동료학습 | S04, S05, S06, S09 | 혼자 출항하면 소행성 에러 구름에 막혀 멈춘다. 먼저 푼 동료가 "이렇게 끼워"라며 알려주고, 주인공이 다음 동료에게 똑같이 알려준다. 사부는 "가르치는 사람은 따로 없다. 먼저 푼 사람이 가르친다"고 말하고, 마지막에 "사부님은?" → "나도 동료한테 배우는 중"으로 웃음과 함께 못 박는다. 서로 잇는 손에서 빛줄기가 나와 별자리가 된다. | 약 21초 |
| ② 진입장벽 없음 (전공·경력 무관) | S01, S02, S03 | 주인공은 "전 자격이 없는데요"라며 뒷걸음질한다. 사부가 "전공?" "경력?"을 묻고, 주인공은 "없는데요"와 "삼각김밥 유통기한 확인이요"로 답하며, 사부는 "충분하다"고 답한다. 자격 석판의 빈칸이 줄줄이 초록 도장으로 찍히고 사부가 "문턱은 없다. 따라와"라고 말한다. | 약 17초 |
| ③ 장학금 | S07 (+S09 선서) | 별 모양 보급선이 빛나는 보급 상자를 떨어뜨리고, 기사단이 모닥불 앞에서 컵라면을 먹는다. 사부는 "보급은 장학금이 댄다. 너희는 배우는 데만 집중해"라고 하고, 주인공은 "…진짜요?"라고 되묻는다. 장학금은 여정의 보급선이라는 은유다. 수치와 금액은 없고, 문구는 공식 사이트 표현("학비·시간 제약 없이 장학금을 받으며")의 범위 안에 둔다. | 약 8초 |

세 메시지를 각각 충분한 비중으로 두기 위해 동료학습 21초, 진입장벽 17초, 장학금 8초로 배분했고, 장학금은 보급선 은유 하나에 집중시켰다.

## 2. 캐릭터 블록 (모든 프롬프트에 문자 그대로 복붙)

- HERO: `a young night-shift convenience store clerk, messy short black hair, tired eyes with faint dark circles, mint-green store vest over a cream shirt, name-tag-less chest, simple dot eyes`
- MENTOR: `a tall elderly woman master with a silver bun hairstyle, round gold glasses, a long cobalt-blue cloak scattered with small yellow stars, a wooden walking stick topped with a giant keyboard keycap, calm knowing smile`
- KEYBOARD_BLADE (보조): `a slim sword whose glowing mint-green blade is shaped like a thin mechanical keyboard with tiny lit keys`
- CREW_1: `a cheerful woman with flour-dusted coral apron and a rolled-up sleeve, hair in a short ponytail, simple dot eyes`
- CREW_2: `a lanky young man delivery rider with a yellow helmet and cobalt jacket, backpack shaped like a square box, simple dot eyes`
- CREW_3: `a quiet middle-aged man in a beige cardigan with a tote bag full of books, small round spectacles, simple dot eyes`
- SHIP: `a small round cream-colored spaceship with a coral stripe and one big porthole`
- SUPPLY_SHIP: `a star-shaped yellow supply spaceship that glows warmly`

STYLE (모든 프롬프트 끝에 동일 부착, 한 글자도 변경 금지):
`flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9`

## 3. 전체 대본 (초 단위)

범례: **대사**는 TTS 더빙(HERO=echo, MENTOR=shimmer(할머니 톤 instructions), CREW=alloy/nova). Veo는 인물 입 모양을 단순하게 그리게 하고 대사는 더빙으로 덮는다. 한국어 립싱크 실패 위험을 피하기 위해 대사 구간은 뒷모습이나 와이드 샷 위주로 구성한다. 자막은 Pillow PNG 오버레이이며 키워드 위주로 쓰고 대사 문장은 반복하지 않는다.

| 시간 | 씬 | 화면 | 대사 | 사운드 | 화면 자막 |
|---|---|---|---|---|---|
| 0:00-0:05 | S01 | 은하 맨 끝, 별 하나 없는 어둠 속에 외로이 켜진 24시 편의점. 주인공이 졸며 바닥을 닦는다. 창밖으로 거대 고래형 우주 생물이 느리게 지나간다. | (없음) 주인공 한숨 | 냉장고 웅웅, 먼 고래 울음, 낮은 호른 한 음 | 은하의 맨 끝, 24시 편의점 |
| 0:05-0:13 | S02 | 자동문이 열리고 별가루 바람과 함께 사부가 들어온다. 주인공은 뒷걸음질. 사부가 지팡이로 바닥을 한 번 짚으면 키캡이 달깍 하고 울린다. | HERO "저… 전 자격이 없는데요." MENTOR "전공?" HERO "없는데요." MENTOR "경력?" HERO "…삼각김밥 유통기한 확인이요." MENTOR "충분하다." | 자동문 띵동(우주 버전), 키캡 달깍, 호른 상승 | (없음) |
| 0:13-0:17 | S03 | 두루마리 자격 석판이 펼쳐진다. 칸이 전부 비어 있는데 초록 도장이 쿵쿵쿵 찍힌다. 주인공이 눈을 동그랗게 뜬다. | MENTOR "문턱은 없다. 따라와." | 도장 쿵쿵쿵, 작은 팡파르 | **전공 무관 · 경력 무관** (150px 쾅) |
| 0:17-0:22 | S04 | 주인공이 둥근 작은 우주선을 타고 첫 출항. 소행성처럼 떠 있는 거대한 "에러 말풍선" 덩어리 사이에서 우주선이 끼어 멈춘다. 주인공이 손으로 얼굴을 감싼다. | HERO "…혼자는 안 되겠는데." MENTOR(통신, 목소리만) "혼자 가려니까 막히지." | 삑삑 경고음(코믹), 우주선 끼익, 호른 하강 | (없음) |
| 0:22-0:28 | S05 | 옆 소행성에서 밀가루 묻은 앞치마 동료가 나타나 주인공 우주선의 막힌 부품을 "이렇게 끼워" 하며 밀어 넣는다. 소행성이 풀리며 둘 사이로 빛줄기가 연결된다. | CREW_1 "거기, 이렇게 끼워." HERO "…됐다!" | 달깍 끼움음, 반짝 연결음(별 하나 점등) | **동료학습** (150px 쾅) |
| 0:28-0:34 | S06 | 이번에는 주인공이 헬멧 쓴 배달 라이더 동료의 막힌 우주선을 가리키며 같은 방식으로 알려준다. 빛줄기가 하나씩 늘어나 별자리 선이 그려진다. 사부 통신 목소리가 이어진다. | HERO "여기, 이렇게!" MENTOR(통신) "가르치는 사람은 따로 없다. 먼저 푼 사람이 가르친다." | 연결음 두 번째·세 번째 별 점등, 현악 상승 | (없음) 강조어 "먼저 푼 사람" 84px |
| 0:34-0:42 | S07 | 별 모양 보급선이 따뜻한 빛으로 날아와 빛나는 보급 상자를 떨어뜨린다. 기사단이 우주 한복판 모닥불에 둘러앉아 컵라면을 먹는다. 사부는 흐뭇하게 바라본다. | HERO "…진짜요?" MENTOR "보급은 장학금이 댄다. 너희는 배우는 데만 집중해." CREW_2 "(후루룩)" | 보급선 윙, 상자 쿵, 모닥불 타닥, 라면 후루룩, 현악 따뜻하게 | **장학금 = 보급선** (150px 쾅, 마지막 단어 줌펀치) |
| 0:42-0:45 | S08 | 별자리 전체 컷. 여섯 명이 빛줄기로 이어진 거대한 별자리가 우주를 가득 채우고, 가장 끝의 한 별이 주인공이다. | (없음) | 별자리 완성 차임, 호른 클라이맥스 | 혼자가 아니라 별자리 |
| 0:45-0:51 | S09 | 입단 선서. 기사단이 키보드 검을 하늘로 들자 칼날의 키가 하나씩 불을 켠다. 주인공이 사부에게 슬쩍 묻는다. | HERO "근데 사부님은 언제 가르쳐 주세요?" MENTOR "나? 나도 동료한테 배우는 중." 모두 "우리 같이 간다!" | 키 불 켜지는 타다닥, 환호, 호른 풀 | (없음) |
| 0:51-0:56 | S10 | 크림 배경에 도장 원. 중앙에 CODYSSEY 워드마크와 슬로건, 별자리 문양 배경. | MENTOR(목소리) "코디세이로 오라." | 마지막 호른 한 음, 별 반짝 | 슬로건 120px + 워드마크 64px + `codyssey.kr` 44px |

BGM: 오리지널 영웅풍 호른·현악 팡파르에 B급 코미디 스팅(작은 실로폰/키보드 효과음)을 섞는다. 영화 음악 선율은 비슷하게 만들지 않는다. 예비 veo 1클립(오디오 중심)에서 음원을 확보하고 실패하면 gemini-2.5-flash-tts 대신 ffmpeg로 효과음만 합성한다.

## 4. 씬 표

| 씬 | 길이 | 목표 메시지 | 화면 구성 | 대사·자막 | 도구 | 입력 프롬프트 (영어) | 파일명 | 정지컷 대체 |
|---|---|---|---|---|---|---|---|---|
| S01 | 5초(6초 생성 후 트림) | 도입: 평범한 주인공, 우주 변방 | 와이드. 어둠 속 편의점, 창밖 고래, 졸며 닦는 주인공 | 자막 "은하의 맨 끝, 24시 편의점" | veo-3.1-fast (Text-to-Video 6초) | `Wide establishing shot at the very edge of the galaxy: a lonely 24-hour convenience store floating in dark starry space, warm cream light from its windows. Inside, a young night-shift convenience store clerk, messy short black hair, tired eyes with faint dark circles, mint-green store vest over a cream shirt, name-tag-less chest, simple dot eyes, sleepily mops the floor and yawns. Outside the window a giant friendly whale-shaped space creature drifts by slowly. Soft ambient hum, distant whale song, no dialogue. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S01_veo.mp4` | 가능 (gpt-image 정지컷 + 천천히 줌) |
| S02 | 8초 | ②: "자격 없는데요" → 전공·경력 묻기 | 편의점 안 미디엄. 자동문에서 사부 입장, 뒷걸음질하는 주인공, 지팡이 키캡 달깍 | HERO/MENTOR 문답 대사 (TTS) | veo-3.1 (T2V 8초, 표정 중요) | `Medium shot inside a small space convenience store at night. The automatic door slides open with a swirl of star dust and a tall elderly woman master with a silver bun hairstyle, round gold glasses, a long cobalt-blue cloak scattered with small yellow stars, a wooden walking stick topped with a giant keyboard keycap, calm knowing smile, steps in. A young night-shift convenience store clerk, messy short black hair, tired eyes with faint dark circles, mint-green store vest over a cream shirt, name-tag-less chest, simple dot eyes, backs away nervously with both hands raised and shakes his head. The master taps her stick on the floor and the keycap clicks. Comedic timing, small mouth movements only, no speech audio, only sound effects. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S02_veo.mp4` | 부분 가능 (두 컷 정지 + 컷 전환) |
| S03 | 4초 | ②: 빈칸이 전부 통과 | 클로즈업. 펼쳐진 두루마리 자격 석판, 모든 칸이 비어 있고 초록 도장이 줄줄이 찍힘, 주인공 눈 동그래짐 | 대사 "문턱은 없다. 따라와." / 자막 **전공 무관 · 경력 무관** | gpt-image-2 정지컷 + ffmpeg 도장 쾅 줌펀치 | `Close-up of a long parchment scroll unrolled across a counter, with rows of empty blank checkbox bars and plain blank lines, and big round mint-green approval stamps slamming down on every row. At the edge of the frame a wide-eyed young convenience store clerk, messy short black hair, mint-green store vest over a cream shirt, simple dot eyes, stares in surprise. Centered composition with a cream and mint background. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S03_img.png` → `v3A_S03_zoom.mp4` | **정지컷 (기본)** |
| S04 | 5초(6초 생성 후 트림) | ①: 혼자는 막힌다 (시련) | 와이드. 둥근 우주선이 거대 에러 말풍선 소행성 사이에 끼어 멈춤, 주인공이 얼굴 감쌈 | 대사 HERO/MENTOR(통신) | veo-3.1-fast (T2V 6초) | `Wide shot in deep space: a small round cream-colored spaceship with a coral stripe and one big porthole is jammed between giant floating asteroid-sized speech bubbles that have angry red exclamation shapes, with a young night-shift convenience store clerk, messy short black hair, tired eyes with faint dark circles, mint-green store vest over a cream shirt, simple dot eyes, visible in the porthole covering his face with both hands. The ship sputters with small comic smoke puffs and wobbles. Comedic alarm beeps, no speech audio. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S04_veo.mp4` | 가능 |
| S05 | 6초 | ①: 동료가 알려준다 | 두 우주선이 나란히. 앞치마 동료가 막힌 부품을 밀어 넣자 소행성이 풀리고 둘 사이에 빛줄기 연결 | 대사 CREW_1/HERO / 자막 **동료학습** | veo-3.1-fast (T2V 6초) | `Medium two-shot in space: a cheerful woman with flour-dusted coral apron and a rolled-up sleeve, hair in a short ponytail, simple dot eyes, leans out of a small coral spaceship and pushes a stuck glowing part into the cream-colored round spaceship next to her. The giant red speech-bubble asteroids crumble into confetti, and a thin glowing mint line of light connects the two ships like a constellation line. A young night-shift convenience store clerk, messy short black hair, mint-green store vest over a cream shirt, simple dot eyes, in the porthole cheers with raised arms. Warm chime sound effect, no speech audio. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S05_veo.mp4` | 가능 |
| S06 | 6초 | ①: 이번엔 내가 알려준다 (릴레이) | 주인공이 라이더 동료의 막힌 우주선을 손짓으로 도와주고 별자리 선이 3개로 늘어남 | 대사 HERO/MENTOR(통신) / 강조어 "먼저 푼 사람" | veo-3.1-fast (T2V 6초) | `Medium two-shot in space: a young night-shift convenience store clerk, messy short black hair, mint-green store vest over a cream shirt, simple dot eyes, leans out of a round cream spaceship and points to show a lanky young man delivery rider with a yellow helmet and cobalt jacket, backpack shaped like a square box, simple dot eyes, how to fit a glowing part into his stuck ship. The part clicks in, and a second and third glowing mint light line extend between the three ships, forming a growing constellation shape. Cheerful chime effects, no speech audio. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S06_veo.mp4` | 가능 |
| S07 | 8초 | ③: 장학금 = 여정의 보급선 | 별 모양 보급선이 보급 상자를 떨어뜨림 → 모닥불 앞 기사단이 컵라면 먹는 와이드, 사부 흐뭇 | 대사 HERO/MENTOR/CREW_2 / 자막 **장학금 = 보급선** | veo-3.1 (T2V 8초) | `Wide shot in deep space: a star-shaped yellow supply spaceship that glows warmly flies in and drops a glowing wooden supply crate that lands with a thud. Then the crew sit around a cozy campfire floating on a tiny asteroid and happily slurp cup noodles: a young night-shift convenience store clerk, messy short black hair, mint-green store vest over a cream shirt, simple dot eyes, a cheerful woman with flour-dusted coral apron, a lanky young man delivery rider with a yellow helmet and cobalt jacket. A tall elderly woman master with a silver bun hairstyle, round gold glasses, a long cobalt-blue cloak scattered with small yellow stars, calm knowing smile, watches proudly from the side. Warm crackling fire sound, slurping effects, no speech audio. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S07_veo.mp4` | 부분 가능 (보급선 정지 + 모닥불 정지 2컷) |
| S08 | 3초 | ① 총정리: 혼자가 아니라 별자리 | 초광각. 여섯 명의 우주선이 빛줄기로 이어진 거대한 별자리, 끝 별이 주인공 | 자막 "혼자가 아니라 별자리" | gpt-image-2 정지컷 + ffmpeg 느린 줌인 (자막 규칙상 느린 줌은 금지이므로 0.1초 줌펀치만 사용하고 나머지는 정지) | `Ultra wide view of deep space where six small colorful spaceships are connected by thin glowing mint light lines forming one big constellation shape across a deep cobalt starry sky, one small cream round ship with a coral stripe at the end of the constellation glowing brightest. Symmetric epic composition with sunflower yellow stars. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S08_img.png` | **정지컷 (기본)** |
| S09 | 6초 | ①: 사부도 동료에게 배운다(개그) + 입단 선서 | 기사단이 키보드 검을 들어 올리자 키가 하나씩 점등. 주인공이 사부에게 속삭이고 사부가 능청스럽게 답함 | 대사 HERO/MENTOR/전원 | veo-3.1 (T2V 6초) | `Medium low-angle shot: a group of five cheerful companions raise their swords toward the sky, each a slim sword whose glowing mint-green blade is shaped like a thin mechanical keyboard with tiny lit keys, and the keys light up one by one in a ripple. A young night-shift convenience store clerk, messy short black hair, mint-green store vest over a cream shirt, simple dot eyes, leans toward a tall elderly woman master with a silver bun hairstyle, round gold glasses, a long cobalt-blue cloak scattered with small yellow stars, who gives a sly shrug and wink. Joyful cheering sound effects, no speech audio. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S09_veo.mp4` | 부분 가능 |
| S10 | 5초 | 슬로건·CTA | 크림 배경 중앙, 도장 원, 별자리 문양, 사부 목소리만 | 사부 "코디세이로 오라." / 자막 슬로건 120px + CODYSSEY 64px + `codyssey.kr` 44px | gpt-image-2 배경(글자 없음) + Pillow 오버레이 | `Clean cream background with a large round stamp-style circle in the center in dark navy outline, and a faint constellation pattern of small mint and sunflower yellow stars scattered around the edges, with the tall elderly master's cobalt cloak hem and wooden walking stick keycap peeking in at the bottom corner. Plenty of empty space in the center for later text. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9` | `v3A_S10_endcard.png` | **정지컷 (기본)** |

veo 클립 수: 7개 (S01, S02, S04, S05, S06, S07, S09). 한도 8개 대비 1개 여유로 S02(표정·대사 비중이 큼) 또는 S07 리테이크에 쓰거나 오디오(BGM) 확보용으로 둔다.

크레딧 부족 시 축소 전략: S01, S04, S06은 gpt-image 정지컷으로 대체 가능하고, 이때 veo는 최소 4개(S02, S05, S07, S09)가 된다.

## 5. 프롬프트 수정 전/후 예시 (미션 필수 항목 후보: S02)

- 수정 전: "an old wizard walks into a convenience store" → 스타워즈풍 수염 노인이 나올 위험이 있고 화풍이 흔들림.
- 수정 후: MENTOR 캐릭터 블록(은발 쪽머리 할머니, 금테 안경, 별무늬 남색 망토, 키캡 지팡이)으로 고정하고 STYLE 접미어를 붙임. 이유는 특정 IP 연상 방지와 화풍 일관성 확보.

## 6. IP 회피 체크

| 피한 것 | 대체한 것 |
|---|---|
| 제다이·포스·라이트세이버·시스 등 고유어 | "코디세이 기사단", "사부", "키보드 검", "별자리" |
| 요다·오비완 등 닮은 캐릭터(작은 녹색 노인, 수염 도사) | 은발 쪽머리 할머니 사부, 금테 안경, 별무늬 남색 망토, 키캡 지팡이 |
| 라이트세이버 관(튜브형 광선검) | 칼날 자체가 얇은 기계식 키보드 모양인 "키보드 검" |
| 오프닝 크롤(노란 글자가 기울어 올라가는 연출)·스타워즈 서체 | 정면 고정 키워드 자막(Apple SD Gothic Neo ExtraBold 흰 글자+남색 외곽선), 크롤 없음 |
| 존 윌리엄스 음악·메인 테마 선율 | 오리지널 호른·현악 팡파르 + 코미디 스팅, 기존 선율 인용 금지 |
| "May the Force be with you"류 대사, "I am your father"류 패러디 | "자격은 안 묻는다", "먼저 푼 사람이 가르친다", "코디세이로 오라" |
| 데스스타·AT-AT 등 상징 소품·우주선 디자인 | 둥근 크림색 우주선, 별 모양 보급선, 고래형 우주 생물 |

스타워즈의 "평범한 사람이 부름을 받는다"는 서사 구조(영웅 서사의 일반 원형)만 오마주로 남겼다.

## 7. 사실 점검

- 사용한 브랜드 사실은 storyboard.json brand 섹션 범위 안으로 한정: 전공·경력 무관(S02·S03), 동료학습·PBL(S04-S06·S09), 장학금(S07), 모험(오디세이) 은유 톤.
- 새 수치·일정·금액은 없음. 과정명(AI 올인원, AI 네이티브)과 개월 수는 이 시안에서는 쓰지 않음(S10 엔드카드에 필요하면 brand 섹션 문구로만 추가).
- 주의 1: S07 "배우는 데만 집중해"는 공식 문구 "학비·시간 제약 없이 장학금을 받으며"를 줄인 말이라 전액 면제·지급 조건을 암시하지 않도록 장학금 상세를 말하지 않음.
- 주의 2: S09 "사부도 동료에게 배우는 중"은 연출된 허구이며 실제 운영 방식에 대한 사실 주장이 아님. 엔드카드나 설명란에 "AI로 제작한 연출 영상" 고지 권장(v2 notice 규칙 재사용).
- 주의 3: 등장 동료(제빵사·라이더·사서풍)는 허구의 인물이며 실제 수강생 후기로 보이지 않게 함.
