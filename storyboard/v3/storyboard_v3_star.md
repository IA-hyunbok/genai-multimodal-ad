# 코디세이 AI 광고 v3 - 「코디세이로 오세요」 (기사단의 부름)

- 로그라인: 우주를 떠도는 사부가 평범한 사람 셋(문과생 소라, 전역자 도현, 직장인 민석)을 차례로 "코디세이로 오라" 부른다. 셋이 "저 국문과인데요 / 통장이 비었습니다 / 혼자 하면 맨날 포기하는데요" 하고 빼면 사부가 한 방에 받아치고, 마지막엔 셋이 한 줄로 서서 기사단이 된다.
- 슬로건: **문턱은 없고, 동료는 있다.** / 엔드 서브라인: 전공 무관 · 장학금 · 동료학습 / CTA: 코디세이로 오세요~ codyssey.kr
- 길이 55초, 10씬, veo 6클립(영상 5 + BGM 1), gpt-image-2 스틸 5장(+애니메틱 키프레임 5장)
- 구조: 부름(장엄) -> 거절(소박) -> 정적 1초 -> 받아침(무심)을 소라/도현/민석에게 세 번 같은 길이로 반복(각 11초), S08에서 박자 깨고 "나도 동료한테 배웠다"로 회수.
- 화풍: v2 시험 클립 B_S01_test 화풍, `style_lock.style_suffix` 그대로. 설명 내레이션 없음.
- 사실 근거: 전공·경력 무관 / 장학금을 받으며 배움 / 교수 중심이 아닌 동료학습+PBL. 수치·일정·금액 없음. 가상 연출 고지 전 컷.

## 캐릭터와 TTS voice

| 캐릭터 | 외형 | voice | 톤 |
|---|---|---|---|
| 사부(마스터): 은빛 땋은 머리, 별자리 점무늬 코발트 망토, 키보드 검 | | onyx | 깊고 차분한 저음. 부름 대사는 장엄하게 천천히, 받아침 대사는 갑자기 무심하게 평평하게(장엄->무심 낙차가 개그). 마지막 CTA만 따뜻하게 웃는 톤. speed 0.95~1.0 |
| 문과생 소라: 둥근 안경, 노란 머리끈, 크림 카디건 | | nova | 밝고 또렷한 20대 여성. 당황하면 반 박자 늦고 음정이 올라감. |
| 전역자 도현: 짧은 머리, 카키 후디, 경례 | | echo | 씩씩하고 각 잡힌 청년 목소리. 경례 직후 크게, 통장 대사는 급히 꺾여 작아짐. |
| 직장인 민석: 코발트 셔츠, 느슨한 넥타이, 사원증 | | fable | 기운 없는 늘어진 톤, 문장 끝이 흐려짐. S07/S08에서 점점 살아남. |

사부 목소리 근거: 사부 onyx. (1) 이 광고의 개그는 "장엄한 부름 -> 소박한 거절 -> 무심한 받아침"의 낙차라 저음 권위 목소리(onyx)가 앞 박자의 장엄함을 만들고, instructions로 같은 목소리를 받아침에서 평평하게 낮춰야 웃긴다. (2) 소라 nova(밝은 여성), 도현 echo(씩씩한 청년), 민석 fable(힘 빠진 표현형)과 음색이 겹치지 않아 한 번 듣고 구분된다. (3) 마지막 CTA 한 줄만 따뜻하게 웃는 톤으로 바꿔 브랜드 톤(차분하지만 응원)으로 닫는다. (4) 요다식 도치 어순·쉰 목소리를 피해 IP 연상 방지.

## 전체 대본 (재작성)

같은 박자를 세 번 반복한다. 사부가 장엄하게 부르면 상대가 소박한 핑계를 대고, 정적 1초 뒤 사부가 엉뚱하게 받아친다. S08에서 이 박자를 깨고, 설명은 화면 키워드가 맡는다.

```
S01 [0:00~0:03 우주, 구름 위 절벽]
사부     (장엄하게) 별이… 말했다.

S02 [0:03~0:11 도서관 계단]
사부     깨어나라, 그대여. 코디세이로 오라.
소라     …저 국문과인데요?
         (정적 1초. 바람. 사부 한쪽 눈썹만 크게 올라감)
사부     나는 천문과였다.

S03 [0:11~0:16 빈 문틀]
소라     어? 문이… 없네요?
사부     문턱도 없다.
                                         [슈퍼] 전공·경력 무관

S04 [0:16~0:26 담벼락 옆 새벽길]
사부     그대 안의 코드가… 깨어났다.
도현     (경례) 충성! …근데 통장이 비었습니다!
         (빈 지갑을 활짝 열어 보임)
사부     그건 별이 채운다.

S05 [0:26~0:29 별 비가 내리는 담벼락]
         (도현이 열어 둔 빈 지갑으로 작은 금빛 별들이 쏟아져 들어감)
도현     …진짜 채워지는데요?
사부     장학금이다.
                                         [슈퍼] 장학금

S06 [0:29~0:37 야근 사무실, 창밖 우주]
         (사부가 창밖 우주에 떠서 아스트롤라베로 유리를 똑똑 두드림)
사부     지친 자여… 코디세이로 오라.
         (키보드에 엎드려 있던 민석이 고개만 천천히 돌림)
민석     …저 내일 출근인데요.
         (사부가 작게 고개를 끄덕이며 손바닥을 펴 보임)
사부     괜찮다… 24시간 개방이다.

S07 [0:37~0:44 회사 옥상. 뒤쪽에서 사람들이 노트북을 펴고 삼삼오오 함께 공부 중]
         (옥상 끝에 혼자 앉은 민석이 한숨을 쉬며 손을 내려다봄)
민석     혼자서는… 어려워요.
         (사부가 뒤쪽 함께 공부하는 사람들을 손으로 크게 가리킴)
사부     혼자 하지 않는다. 주변 동료들과 함께한다.
                                         [슈퍼] 동료학습

S08 [0:44~0:53 우주 계단]
도현     (민석에게 경례) 충성! 기수가 어떻게 되십니까!
사부     기수 없다. 모두가 함께 동료다.
사부     나도 배우는 중이다.

S09 [0:53~0:59 별자리 하늘, 네 사람 뒷모습]
사부     (돌아보며 비장하게) 코디세이로 와라!
                                         [엔드카드] 문턱은 없고, 동료는 있다.
                                         전공 무관 · 장학금 · 동료학습
                                         CODYSSEY  codyssey.kr
```

※ 위 대본이 최종 편집본(output/v3/Codyssey_v3_cuts_16x9.mp4, 59.0초) 기준이다. 실제로 쓴 컷별 프롬프트는 cuts_v3.md와 build/v3c/에 있다. 아래 씬별 프롬프트 원문은 이전(v3 초안) 기록이다.

## 씬별 프롬프트 원문

### S01 (6초, veo) - 평범한 사람에게도 부름이 온다는 세계관. 코디세이 기사단 등장.
- 파일: v3_s01_veo_call_v01.mp4, v3_s01_img_call_v01.png, v3_s01_tts_master_v01.mp3, v3_s01_ovl_title_v01.png
- still_prompt: Deep navy outer space full of twinkling stars, stars connected by thin lines tracing the outline of a giant keyboard-shaped sword. In the center foreground a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, facing the camera with a solemn look, cloak fluttering. Wide epic composition, empty space in the lower third, subject kept in the central safe area. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: Night outer space, deep navy sky full of twinkling stars. The stars drift together and trace the outline of a giant keyboard-shaped sword, then fade to calm. In the center foreground a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, slowly turns around to face the camera with a solemn look, cloak fluttering. Slow epic push-in, 6 seconds. Sound effects only: soft star twinkles and a low wind, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S02 (8초, veo) - 전공이 달라도(국문과여도) 입구에 전공 칸이 없다.
- 파일: v3_s02_veo_humanities_v01.mp4, v3_s02_img_humanities_v01.png, v3_s02_tts_*_v01.mp3
- still_prompt: Cream and mint colored library steps, a sunny day. a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes, standing frozen on the steps with a sweat drop, while a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, sweeps in from the right with cloak flying and points at her dramatically. Fixed medium shot, both characters fully in frame. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: Cream and mint colored library steps, a sunny day. a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes, walks up the steps. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, sweeps in from the right with cloak flying and points at her dramatically. She freezes, sweat drop, mouth moves in a small hesitant way. A one second silent beat: the mentor only raises one eyebrow. Then the mentor gives a flat dismissive wave to the side and she turns her head to look where he points. Fixed medium shot, 8 seconds, comedic timing with a hard pause. Sound effects only: cloak whoosh and a small record scratch, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S03 (3초, still) - 정말로 문턱이 없다. 전공도 경력도 안 본다.
- 파일: v3_s03_img_nothreshold_v01.png, v3_s03_tts_*_v01.mp3, v3_s03_ovl_kw_v01.png
- still_prompt: An empty wooden doorframe standing alone with no door and no threshold step, floating on white steps in a sunny cream and mint scene, a bright path passing straight through it. In front, a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes, looks back over her shoulder in surprise. In the back a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, leans on his keyboard sword, smug. Wide composition with empty space at the center for a caption, key subjects inside the central 16:9 crop. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: An empty wooden doorframe with no door and no threshold step on cream and mint steps. a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes, walks straight through it and looks back in surprise. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, leans on the keyboard sword, smug. Fixed shot, 4 seconds. Sound effects only: one fanfare note and wind, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S04 (8초, veo) - 돈이 없어도 장학금을 받으며 배울 수 있다.
- 파일: v3_s04_veo_veteran_v01.mp4, v3_s04_img_veteran_v01.png, v3_s04_tts_*_v01.mp3
- still_prompt: Cobalt blue and cream colored parade ground wall, a bright day. a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes, stands at attention with a panicked face and an empty wallet turned inside out, a tiny puff of dust. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, drifts in from above with cloak flapping. Fixed medium shot. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: Cobalt blue and cream colored parade ground wall, a bright day. a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes, stands at attention and snaps a salute. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, drifts in from above with cloak flapping, reaching out a hand. The young man pulls his empty wallet out of the hoodie pocket and turns it inside out, a tiny puff of dust falls out, he looks panicked. A one second silent beat. The mentor swings the keyboard sword up slowly with a confident grin, a glowing scroll with a ribbon unrolls from it. Fixed medium shot, 8 seconds. Sound effects only: salute snap, dust puff, scroll unroll, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S05 (3초, still) - 장학금: 배우는 데만 집중하면 된다.
- 파일: v3_s05_img_scholarship_v01.png, v3_s05_tts_*_v01.mp3, v3_s05_ovl_kw_v01.png
- still_prompt: Star-shaped golden coins pouring down like rain from the top of the frame onto a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes, who looks up with his mouth wide open and one hand frozen in a salute. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, stands beside him draping a glowing ribbon scroll over his shoulder, smiling. Cobalt blue and cream background, space left in the upper center for a caption, key subjects inside the central 16:9 crop. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: Star-shaped golden coins pour down like rain onto a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes, who looks up with his mouth wide open. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, drapes a glowing ribbon scroll over his shoulder. Fixed shot, 4 seconds. Sound effects only: coins pouring, a salute snap, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S06 (8초, veo) - 혼자는 못 해도 된다. 먼저 푼 사람이 가르치는 동료학습.
- 파일: v3_s06_veo_worker_v01.mp4, v3_s06_img_worker_v01.png, v3_s06_tts_*_v01.mp3
- still_prompt: Yellow and coral colored office at night, a big window showing outer space and stars. a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes, slumps over a laptop. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, floats outside the window in space, cloak waving. Fixed medium shot, both characters fully in frame. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: Yellow and coral colored office at night, a big window showing outer space and stars. a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes, slumps over a laptop with his face drooping toward the keyboard. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, rises up outside the window floating in space, cloak waving, and taps on the glass with one finger. The young man looks up slowly and shrugs, drooping. A one second silent beat. Then two small star-shaped lights float in through the window and settle next to him, he blinks at them. Fixed medium shot, 8 seconds. Sound effects only: glass tap, soft chime, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S07 (3초, still) - 별이 이어져 별자리가 되듯 동료와 이어진다.
- 파일: v3_s07_img_constellation_v01.png, v3_s07_tts_laugh_v01.mp3, v3_s07_ovl_kw_v01.png
- still_prompt: Three glowing stars above three people's heads connected by thin sunflower yellow lines into a small constellation, over a yellow and coral night office window. a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes, in the foreground smiles for the first time, eyes bright. Two small silhouettes of other people appear faintly under the other stars. Space left at the center for a caption, key subjects inside the central 16:9 crop. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: Three glowing stars connect with thin sunflower yellow lines into a small constellation over a yellow and coral night office window. a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes, smiles for the first time. Fixed shot, 4 seconds. Sound effects only: three rising star chimes, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S08 (8초, veo) - 세 사람이 모이고, 사부도 동료에게 배웠다. 교수는 없고 동료가 있다.
- 파일: v3_s08_veo_knights_v01.mp4, v3_s08_img_knights_v01.png, v3_s08_tts_*_v01.mp3
- still_prompt: A staircase floating in space with stars all around. a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes, a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes, and a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes, stand on the steps next to a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows. Fixed wide shot, all four fully in frame with distinct outfit colors. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: A staircase floating in space with stars all around. a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes, a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes, and a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes, each arrive through their own empty doorframe and stop awkwardly when they see each other. They look at one another and wave stiffly. a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows, turns his back, arms crossed, then slowly looks over his shoulder. The three look surprised together. In the last two seconds all four raise their keyboard swords like trophies at the same time in a heroic pose while stars connect behind them into a constellation. Fixed wide shot, 8 seconds. Sound effects only: soft footsteps, star chimes, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S09 (3초, still) - 문이 없으니 노크할 필요도 없다(진입장벽 없음 재회수).
- 파일: v3_s09_img_knock_v01.png, v3_s09_tts_*_v01.mp3
- still_prompt: An empty wooden doorframe floating in space in front of four characters in a row, a young woman humanities student, round glasses, yellow hair tie, cream cardigan, hugging a tall stack of paperback books, simple dot eyes, a young man with a buzz cut, khaki hoodie, habit of snapping a salute, duffel bag on his shoulder, simple dot eyes, a young man office worker, cobalt blue shirt, loose navy tie, employee ID badge on a lanyard, tired droopy eyes, simple dot eyes, and a tall calm mentor character with a long silver braid, a cobalt-blue cloak patterned with tiny constellation dots, and a giant glowing mint-green computer keyboard carried on the shoulder like a sword, simple dot eyes, tiny expressive eyebrows. The mentor raises a fist about to knock on the empty air with a deadpan face, while the other three watch him with sweat drops. Cream and mint background. Wide composition, all four inside the central 16:9 crop. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: An empty wooden doorframe floating in space in front of four characters in a row. The mentor raises a fist to knock on the empty air, stops, and lowers it with a deadpan face while the other three watch with sweat drops. Fixed shot, 4 seconds. Sound effects only: a soft wind, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

### S10 (5초, still) - 문턱은 없고, 동료는 있다. 코디세이로 오세요.
- 파일: v3_s10_img_endcard-bg_v01.png, v3_s10_tts_master-end_v01.mp3, v3_s10_ovl_endcard_v01.png
- still_prompt: A clean cream background with a soft ring of tiny constellation stars forming a circle at the center, three small cartoon figures standing on the lower edge looking up at the stars, plenty of empty space for a slogan above and a logo stamp at the center. Keep the lower edge figures small and inside the central 16:9 crop. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9
- video_prompt: A clean cream background with twinkling constellation stars slowly appearing around a central ring and three small cartoon figures at the bottom looking up. Fixed shot, 5 seconds. Sound effects only: one star chime, no speech, no dialogue, no voices. flat 2D vector cartoon animation, uniform thick dark-navy outlines, solid flat colors with no gradients, bright pop palette of coral red, mint green, cobalt blue, sunflower yellow and cream, exaggerated cartoon expressions, simple geometric shapes, clean shadows as single flat color blocks, subtle paper grain, no text, no letters, no logos, 16:9

## 프롬프트 수정 전/후 (S02)
- 전: `A mentor calls a woman student on library stairs, she refuses, cartoon style.`
- 후: S02 video_prompt
- 이유: STYLE 접미어 고정; 캐릭터 블록 고정(은빛 땋은 머리+별자리 망토+키보드 검); "A one second silent beat" 명시; no text 유지
- 결과: 제작 후 기입

## 리스크
- 8초 클립에 4박이 다 안 들어감 -> 증명 박자를 정지컷(S03·S05·S07)으로 이미 분리. 최악엔 S02/S04/S06을 정지컷 2장+줌으로 대체
- S08 3인 의상·얼굴 일관성 -> 의상색 대비, 실패 시 정지컷 3컷
- 사부가 특정 IP 캐릭터로 이탈 -> 키 큰 은빛 땋은 머리+별자리 망토 고정, 도치 어순 금지, 검수표
- S08 사부 "나도 동료한테 배웠다"가 실제 운영 사실로 읽힘 -> 허구 연출. "※ 연출된 가상 상황 · AI로 제작" 전 컷 고지
- "통장이 비었습니다 -> 장학금 받으며"가 금액·조건 약속으로 읽힘 -> 금액·조건 언급 없음. 공식 문구 범위("장학금을 받으며 배우는")만 사용
- Veo 한국어 립싱크 -> TTS 후배치, 입 작게
