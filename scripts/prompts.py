#!/usr/bin/env python3
"""veo 프롬프트 치환본 생성 -> build/<ver>/sNN.prompt.txt
사용: python3 scripts/prompts.py v4    (storyboard/v4/storyboard_v4.md 의 {TAG} 치환)
      python3 scripts/prompts.py v3n   (v3 실사 캐릭터 바이블 + storyboard_v3.md 재작성 대본)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ver = sys.argv[1]
out = os.path.join(ROOT, "build", ver)
os.makedirs(out, exist_ok=True)
KO = "All dialogue is spoken in Korean only, never in any other language."

if ver == "v4":
    md = open(os.path.join(ROOT, "storyboard/v4/storyboard_v4.md")).read()
    tags = dict(re.findall(r"^\| (\{[A-Z]+\}) \| [^|]+ \| ([^|]+?) \|", md, re.M))
    tags.update((k, v) for k, v in re.findall(r"^- (\{[A-Z]+\}) = `(.+)`", md, re.M))
    prompts = re.findall(r"\*\*프롬프트 원문 \(veo\)\*\*\n```\n(.+?)\n```", md, re.S)
else:  # v3n: v3 실사 캐릭터·룩 그대로, 대사만 재작성 대본으로
    d = json.load(open(os.path.join(ROOT, "storyboard/v3/live_shotlist.json")))
    cb = d["character_bible"]
    tags = {"{" + k + "}": v for k, v in cb.items()}
    tags["{LOOK}"] = d["look_block"]
    tags["{KO}"] = KO
    prompts = [
        'Epic wide shot of a vast night sky full of stars, slow dramatic push-in to a lone figure on a rocky cliff edge above clouds: {MASTER}. She faces the camera with a grave, unblinking expression, cloak whipping in the wind. 0-3s: she says in Korean in a deep, solemn, slow voice: "별이… 말했다." 3-4s: complete silence, music cuts dead, she just stares. 4-6s: she says in Korean in a sudden flat, bored, matter-of-fact voice: "원서 접수 시작했다고." Sound: a huge orchestral brass hit and choir under the first line, then dead silence, then only wind. {LOOK} {KO}',
        'Medium two-shot, locked camera, sunlit university library steps in cream stone. On the left {SORA} walks up the steps. On the right {MASTER} stands heroically with her keyboard sword raised toward the sky, cloak blowing. 0-2.5s: the Master says in Korean in a booming epic voice: "깨어나라, 그대여. 코디세이로 오라." 2.5-4.5s: the young woman stops and says in Korean with a small confused voice: "…저 국문과인데요?" 4.5-5.5s: one second of total silence, the Master only slowly raises one eyebrow. 5.5-8s: the Master lowers the sword and says in Korean in a flat, casual voice: "나는 천문과였다." Sound: grand orchestral hit on the first line, then a record scratch and dead silence. {LOOK} {KO}',
        'Locked wide shot. A plain empty wooden doorframe stands alone on the cream library steps, with no door and no threshold step, sunlight passing through it. {SORA} walks through it and looks back over her shoulder in surprise. In the background {MASTER} leans casually on her keyboard sword, expressionless. 0-2s: the young woman says in Korean: "어? 문이… 없네요?" 2-4s: the Master says in Korean in a flat deadpan voice: "문턱도 없다." Sound: one proud brass fanfare note, light wind. {LOOK} {KO}',
        'Medium two-shot, locked camera, in front of a sunny military parade-ground wall. {DOHYUN} stands at attention. {MASTER} descends slowly from above, cloak flapping, and points her keyboard sword at him. 0-2.5s: the Master says in Korean in a booming epic voice: "그대 안의 코드가… 깨어났다." 2.5-5s: the young man snaps a salute and shouts in Korean: "충성!", then his voice drops small and quick: "…근데 통장이 비었습니다!" and he turns his empty wallet inside out, a tiny puff of dust falls. 5-6s: one second of silence. 6-8s: the Master says in Korean, flat and calm: "그건 별이 채운다." Sound: salute snap, dust puff, silence. {LOOK} {KO}',
        'Locked medium shot, slightly low angle, same parade ground. Glowing golden star-shaped coins rain down from the sky onto {DOHYUN}, who looks up with his mouth wide open, one hand frozen mid-salute. {MASTER} stands beside him, expressionless. 0-1.5s: the young man says in Korean, stunned: "…진짜 채워지는데요?" 1.5-3s: the Master says in Korean, flat: "장학금이다." Sound: coins jingling. {LOOK} {KO}',
        'Locked medium shot of a late-night office lit only by a monitor. {MINSEOK} is slumped over his desk. Outside the large window there is outer space full of stars, and {MASTER} floats outside the glass, cloak waving, tapping on the window with one finger. 0-2.5s: the Master says in Korean, muffled through the glass, in a grand voice: "지친 자여… 코디세이로 오라." 2.5-4.5s: the office worker only turns his head toward the window and says in Korean, exhausted: "…저 내일 출근인데요." 4.5-5.5s: one second of silence. 5.5-8s: the Master says in Korean, flat and tired: "나도 월요일은 싫다." Sound: glass taps, fluorescent hum, silence. {LOOK} {KO}',
        'Close-up of {MINSEOK} in the dark office, sighing. Above his head one small glowing star appears, then two more stars appear and thin golden lines connect the three into a small constellation. 0-2s: the office worker says in Korean, quietly: "혼자 하면… 사흘을 못 가요." 2-4s: the Master\'s voice from off-screen says in Korean, calm: "별 하나는 금방 꺼진다. 셋이면 별자리다." Sound: three soft rising chimes. {LOOK} {KO}',
        'Wide locked shot of a long stone staircase floating in the starry cosmos. {SORA}, {DOHYUN} and {MINSEOK} arrive from three separate empty wooden doorframes and stop awkwardly facing each other. {MASTER} stands at the top. 0-1.5s: the office worker says in Korean: "…저분들도 불려 오신 거예요?" 1.5-3s: the army man salutes and says in Korean: "충성! 기수가 어떻게 되십니까!" 3-4.5s: the Master says in Korean, flat: "기수 없다. 동료다." 4.5-6s: the Master says in Korean: "나도 아직 배우는 중이다." 6-8s: all three young people shout in Korean in unison: "같이 갑니다!" Sound: awkward silence with wind, then a grand orchestral swell on the shout. {LOOK} {KO}',
        'Locked wide shot. An empty wooden doorframe floats in the starry cosmos in front of four people in a row: {MASTER}, {SORA}, {DOHYUN} and {MINSEOK}. The Master raises a fist to knock on the empty air inside the frame, then freezes. 0-1.5s: the young woman says in Korean, deadpan: "…문 없다면서요." 1.5-3s: the Master clears her throat, lowers her fist, and says in Korean: "…습관이다." Sound: soft wind. {LOOK} {KO}',
        'Locked wide shot from behind, empty background plate for a title card: four silhouettes stand in a row on a cliff, seen from the back, under a huge sky of glittering constellations: {MASTER} and three young people in a cream cardigan, olive-khaki hoodie and cobalt-blue shirt. Upper half of the frame is clear starry sky with calm empty space. 1.5-4s: the Master turns her head slightly and says in Korean in a grand, solemn, commanding voice: "코디세이로 와라!" Sound: a grand orchestral finale, gentle wind. No text in the sky. {LOOK} {KO}',
    ]

assert len(prompts) == 10, len(prompts)
for i, p in enumerate(prompts, 1):
    for k, v in tags.items():
        p = p.replace(k, v)
    assert "{" not in p, (i, p)
    open(os.path.join(out, f"s{i:02d}.prompt.txt"), "w").write(p)
print(ver, "10 prompts ->", out)
