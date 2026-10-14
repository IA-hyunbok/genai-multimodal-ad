#!/usr/bin/env python3
"""컷 리스트 JSON -> veo 프롬프트 + 스토리보드 md (+ 씬 키프레임 이미지)
사용: .venv/bin/python scripts/cuts.py v4          프롬프트 build/v4c/cNN.prompt.txt(+.dur), storyboard/v4/cuts_v4.md
      .venv/bin/python scripts/cuts.py v4 keys     씬 키프레임 assets/v4c/keys/SNN.png (gpt-image-2)
캐릭터 고정 묘사는 assets/v5/design/<name>.png 디자인 시트를 보고 옮겨 적은 것이다.
"""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARS = {  # 태그: (짧은 이름, 고정 묘사, 디자인 시트)
    "CAPTAIN": ("the captain", "a fictional Korean woman in her 60s, a sea captain, very long silver-white hair in one thick braid hanging over her left shoulder, deeply wrinkled tanned stern face, dark navy captain's cap with a thin gold band, long weathered dark navy double-breasted coat with brass buttons over an off-white collared shirt, black boots, a brass spyglass in her hand", "captain"),
    "MASTER": ("the Master", "a fictional Korean woman in her 60s, very long silver-white hair pulled back into one thick braid over her left shoulder, no hat, wrinkled stern face, a long deep navy hooded cloak embroidered with small silver stars and constellation lines over a dark navy wrap robe with a thin silver chain belt, a small brass astrolabe in her hand, no sword, no weapon", "master"),
    "SORA": ("the student", "a fictional Korean woman in her 20s, round thin gold wire-frame glasses, black hair with wispy bangs in a low ponytail tied with a bright yellow scrunchie, cream knit cardigan over a white t-shirt, light blue jeans, white sneakers, hugging a stack of paperback books", "sora"),
    "DOHYUN": ("the young man", "a fictional Korean man in his 20s, very short black buzz-cut hair, plain olive-khaki hoodie, black jogger pants, black sneakers, a big olive duffel bag on his right shoulder, civilian clothes, no uniform, no camouflage", "dohyun"),
    "MINSEOK": ("the office worker", "a fictional Korean man in his 30s, messy black hair, heavy eye bags, light stubble, cobalt-blue dress shirt with rolled-up sleeves, loose navy tie, white ID badge on a navy lanyard, charcoal slacks", "minseok"),
    "SHIP": ("the ship", "an old three-masted wooden sailing ship with huge cream-white sails and warm brass lanterns, no flags, no writing on the hull", None),
}
CHARS["SABU"] = ("the old captain", CHARS["CAPTAIN"][1], "captain")  # v3 바다판 사부 = 선장 디자인 시트
KR = {"SABU": "사부", "CAPTAIN": "선장", "MASTER": "사부", "SORA": "소라", "DOHYUN": "도현", "MINSEOK": "민석"}
KO = "All dialogue is spoken in Korean only, never in any other language."


def expand(text):
    """첫 등장은 '짧은 이름 (고정 묘사)', 이후는 짧은 이름만."""
    seen = set()

    def rep(m):
        tag = m.group(1)
        name, desc, _ = CHARS[tag]
        if tag in seen:
            return name
        seen.add(tag)
        return f"{name} ({desc})"
    return re.sub(r"\{([A-Z]+)\}", rep, text)


VOICE = {  # 컷이 바뀌어도 같은 목소리로 들리게 매 컷 같은 문장을 넣는다
    "CAPTAIN": "a low, calm, slightly husky elderly woman's voice",
    "MASTER": "a low, calm, slightly husky elderly woman's voice",
    "SABU": "a low, calm, slightly husky elderly woman's voice",
    "SORA": "a bright, clear young woman's voice",
    "DOHYUN": "a loud, crisp young man's voice",
    "MINSEOK": "a tired, low, drawling voice of a man in his 30s",
}


def video_prompt(sc, c, look):
    w = c["who"]
    s = f"Setting: {sc['set']}. {c['shot']} "
    if c.get("note"):
        s += c["note"] + " "
    if c.get("action"):  # 괄호 속 상황: 시간과 함께 '화면에 분명히' 보이게 따로 적는다
        s += "VISUAL ACTION, clearly visible and large in frame, not skipped: " + " ".join(
            f"From {t.rstrip('s').split('-')[0]}s to {t.rstrip('s').split('-')[1]}s, {d}." for t, d in c["action"]) + " "
    if not c["lines"]:
        s += "AUDIO: nobody speaks in this clip, no voices at all; only the sound effects described and quiet natural ambience, no music."
        return f"{expand(s)} {look}"
    s += (f"DIALOGUE AND LIP-SYNC: only {{{w}}} speaks in this clip, in {VOICE[w]}. While speaking, the speaker's face and mouth "
          f"are clearly visible to the camera and the lips move in exact sync with every Korean syllable. ")
    for t, tone, line in c["lines"]:
        a, b = t.rstrip("s").split("-")
        s += f'From {a}s to {b}s, the speaker says {tone}, exactly once and word for word, in Korean: "{line}" '
    s += ("Outside these times the speaker's mouth stays closed. Everyone else in the frame stays completely silent with mouth closed "
          "and never speaks. Only one voice is heard in the whole clip, no other speech, no extra words. The last line ends at least "
          "0.5 seconds before the clip ends. AUDIO: clean, clear, close-miked dialogue at a natural speaking pace, quiet natural ambience "
          "under it, no background music, no narration, no laughter, no singing.")
    return f"{expand(s)} {look} {KO}"


def key_prompt(sc, look):
    return expand(f"Cinematic live-action film still, wide 16:9 frame. {sc['key']} Setting: {sc['set']}.") + " " + look


def main(ver, mode=None):
    T = json.loads((ROOT / f"storyboard/{ver}/cuts_{ver}.json").read_text())
    B, A = ROOT / f"build/{ver}c", ROOT / f"assets/{ver}c"
    B.mkdir(parents=True, exist_ok=True)
    if mode == "keys":
        (A / "keys").mkdir(parents=True, exist_ok=True)

        def gen(sc):
            out = A / "keys" / f"{sc['id']}.png"
            r = subprocess.run([str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/copa.py"), "image", "gpt-image-2", str(out),
                                key_prompt(sc, T["look"]), "1536x1024"], capture_output=True, text=True)
            return sc["id"], r.returncode, (r.stdout + r.stderr).strip()[-150:]
        with ThreadPoolExecutor(3) as ex:
            for res in ex.map(gen, T["scenes"]):
                print(*res)
        return

    md = [f"# {T['title']}", "",
          "만드는 순서: 캐릭터 디자인 시트(gpt-image-2) → 씬 키프레임(gpt-image-2) → 컷별 veo 클립 → 편집.",
          "COPA 영상 API가 이미지 입력을 받지 않아(테스트로 확인) 시트에서 본 생김새를 글로 옮겨 매 컷 프롬프트에 똑같이 넣는다.",
          "말하는 사람이 섞이지 않도록 **한 컷에 한 사람만 말한다.** 대사가 여럿이어도 같은 사람의 대사만 한 컷에 둔다.", "",
          "## 캐릭터", "", "| 인물 | 디자인 시트 | 고정 묘사(프롬프트에 그대로) |", "|---|---|---|"]
    used = {c["who"] for sc in T["scenes"] for c in sc["cuts"]}
    for tag in [t for t in KR if t in used]:
        md.append(f"| {KR[tag]} | ![](../../assets/v5/design/{CHARS[tag][2]}.png) | {CHARS[tag][1]} |")
    md += ["", "## 컷 리스트", "", "| 컷 | 씬 | 길이 | 말하는 사람 | 대사 | 화면 | 슈퍼 |", "|---|---|---|---|---|---|---|"]
    n, total = 0, 0
    for sc in T["scenes"]:
        for c in sc["cuts"]:
            n += "id" not in c  # id가 있는 컷(끼워 넣은 컷)은 번호를 밀지 않는다
            total += c["dur"]
            cid = c.get("id", f"c{n:02d}")
            (B / f"{cid}.prompt.txt").write_text(video_prompt(sc, c, T["look"]))
            (B / f"{cid}.dur").write_text(str(c["dur"]))
            lines = " / ".join(l for _, _, l in c["lines"]) or "(대사 없음)"
            if c.get("action"):
                lines += "<br>동작: " + " / ".join(f"{t} {d}" for t, d in c["action"])
            shot = re.sub(r"\{([A-Z]+)\}", lambda m: KR.get(m.group(1), "배"), c["shot"])
            md.append(f"| {cid.upper()} | {sc['id']} {sc['name']} | {c['dur']}초 | {KR[c['who']] if c['lines'] else '-'} | {lines} | {shot} | {c.get('super', '엔드카드' if c.get('end') else '')} |")
    md += ["", f"총 {sum(len(s["cuts"]) for s in T["scenes"])}컷, 생성 길이 합계 {total}초. 편집에서 컷마다 대사 앞뒤만 남겨 57~60초로 줄인다.", "",
           "## 씬 키프레임", ""]
    for sc in T["scenes"]:
        md += [f"### {sc['id']} {sc['name']}", f"![](../../assets/{ver}c/keys/{sc['id']}.png)", ""]
    md += ["## 프롬프트 예시 (C02)", "", "```", (B / "c02.prompt.txt").read_text(), "```", "",
           f"전체 프롬프트는 `build/{ver}c/cNN.prompt.txt`. 재생성은 `.venv/bin/python scripts/cuts.py {ver}`."]
    (ROOT / f"storyboard/{ver}/cuts_{ver}.md").write_text("\n".join(md) + "\n")
    assert all("{" not in f.read_text() for f in B.glob("c*.prompt.txt"))
    print(ver, sum(len(s["cuts"]) for s in T["scenes"]), "cuts", total, "s")


if __name__ == "__main__":
    main(*sys.argv[1:])
