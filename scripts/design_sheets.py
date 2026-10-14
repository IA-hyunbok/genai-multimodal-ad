#!/usr/bin/env python3
"""v5 캐릭터 디자인 시트 (gpt-image-2). 결과는 assets/v5/design/<name>.png
사용: .venv/bin/python scripts/design_sheets.py [name ...]   (인자 없으면 전부)
"""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHEET = ("Character design reference sheet in photorealistic live-action film style. The same single person shown three times "
         "side by side on a plain light grey studio background: left = full body front view, middle = full body side profile, "
         "right = head-and-shoulders close-up facing camera. Even soft studio light, identical outfit and face in all three views. "
         "No text, no labels, no letters, no logos, no watermark. ")
CHARS = {
    "captain": "a fictional Korean woman in her 60s, a sea captain, very long silver-white hair in a single thick braid over her left shoulder, "
               "wrinkled sun-tanned stern face, thin straight eyebrows, long weathered dark navy double-breasted captain's coat with brass buttons "
               "over an off-white collared shirt, dark navy captain's cap with a thin gold band, dark trousers, worn black boots, holding a brass spyglass",
    "master": "a fictional Korean woman in her 60s called the Master, very long silver-white hair in a single thick braid over her left shoulder, "
              "wrinkled stern face, thin straight eyebrows, a long deep navy hooded cloak embroidered with small silver star and constellation dots "
              "over a plain dark navy robe, a thin silver belt, holding a small brass astrolabe in one hand, no sword, no weapon",
    "sora": "a fictional Korean woman in her 20s, a literature student, round thin gold wire-frame glasses, black shoulder-length straight hair "
            "tied low with a bright yellow hair tie, cream knit cardigan over a white t-shirt, light blue jeans, white sneakers, "
            "hugging a tall stack of paperback books",
    "dohyun": "a fictional Korean man in his 20s just discharged from the army, very short buzz-cut black hair, square jaw, plain olive-khaki hoodie "
              "with no print, black jogger pants, black sneakers, a large olive duffel bag on his right shoulder, upright military posture, "
              "civilian clothes only, no uniform, no camouflage",
    "minseok": "a fictional Korean man in his 30s, an exhausted office worker, messy black hair, heavy eye bags, light stubble, cobalt-blue dress shirt "
               "with rolled-up sleeves, loose navy tie, white employee ID badge on a navy lanyard, charcoal slacks, black leather shoes",
}


def run(name):
    out = ROOT / "assets/v5/design" / f"{name}.png"
    r = subprocess.run([str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/copa.py"), "image", "gpt-image-2", str(out),
                        SHEET + "The character: " + CHARS[name] + ".", "1536x1024"], capture_output=True, text=True)
    return name, r.returncode, (r.stdout + r.stderr).strip()[-200:]


if __name__ == "__main__":
    (ROOT / "assets/v5/design").mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(3) as ex:
        for res in ex.map(run, sys.argv[1:] or CHARS):
            print(*res)
