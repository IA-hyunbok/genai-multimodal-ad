"""Image-to-Video via HuggingFace Spaces (gradio_client). 재실행 가능.
사용: .venv/bin/python scripts/gen_video.py [scene ...]   (기본: 1 3 5)
Space를 순서대로 시도, 모든 시도를 assets/video/video_log.json 에 기록한다.
"""
import json, shutil, subprocess, sys, time
from pathlib import Path
from gradio_client import Client, handle_file

ROOT = Path(__file__).resolve().parent.parent
VID = ROOT / "assets/video"
LOG = VID / "video_log.json"
FF = "/opt/homebrew/bin/ffprobe"

# 채택 이미지 + 모션 프롬프트 (storyboard.json motion_plan 기반)
SCENES = {
    1: ("scene01_img_v2.png", "slow drifting fog over the dark navy forest path, the faceless silhouette stands still, gentle subtle camera push-in, soft glowing light, smooth cinematic motion"),
    3: ("scene03_img_v2.png", "warm amber light from the glowing doorway slowly spreads and brightens along the path, gentle camera push-in toward the light, smooth cinematic motion"),
    5: ("scene05_img_v2.png", "small amber sparkles and stars drift gently over the road, clouds slowly move across the bright blue sky, subtle camera push-in, smooth cinematic motion"),
}

# (space, api_name, kwargs builder) — 최대 4개 교체 시도
def wan22(img, prompt, dur):
    return dict(input_image=handle_file(img), prompt=prompt,
                steps=6, duration_seconds=dur, guidance_scale=1, guidance_scale_2=1,
                seed=42, randomize_seed=False, api_name="/generate_video")

def ltx(img, prompt, dur):
    return dict(prompt=prompt, negative_prompt="worst quality, inconsistent motion, blurry, jittery, distorted",
                input_image_filepath=handle_file(img), input_video_filepath=None, height_ui=512, width_ui=704,
                mode="image-to-video", duration_ui=dur, ui_frames_to_use=9, seed_ui=42, randomize_seed=False,
                ui_guidance_scale=1, improve_texture_flag=True, api_name="/image_to_video")

def wan21(img, prompt, dur):
    return dict(input_image=handle_file(img), prompt=prompt, height=480, width=832, negative_prompt="static, blurry, low quality",
                duration_seconds=dur, guidance_scale=1, steps=4, seed=42, randomize_seed=False, api_name="/generate_video")

def wan22b(img, prompt, dur):
    return dict(input_image=handle_file(img), last_image=None, prompt=prompt, steps=6, negative_prompt="static, blurry",
                duration_seconds=dur, guidance_scale=1, guidance_scale_2=1, seed=42, randomize_seed=False,
                quality=6, scheduler="UniPCMultistep", flow_shift=3.0, frame_multiplier=16, video_component=True,
                safe_mode=False, enable_safety_checker=False, api_name="/generate_video")

SPACES = [
    ("Upsampler/wan-2-2-14b-image-to-video", wan22, 3.5),
    ("Lightricks/ltx-video-distilled", ltx, 2.0),
    ("multimodalart/wan2-1-fast", wan21, 2.0),
    ("r3gm/wan2-2-fp8da-aoti-preview", wan22b, 2.0),
]


def probe(f):
    out = subprocess.run([FF, "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(f)],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    return f'{s["width"]}x{s["height"]} {s["r_frame_rate"]}fps {float(d["format"]["duration"]):.2f}s'


def main():
    scenes = [int(a) for a in sys.argv[1:]] or [1, 3, 5]
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    for n in scenes:
        img, prompt = SCENES[n]
        rec = {"scene": n, "input": img, "prompt": prompt, "attempts": [], "status": "failed", "file": None}
        for space, build, dur in SPACES:
            t = time.time()
            a = {"space": space, "duration_seconds": dur, "steps": 6, "seed": 42}
            try:
                res = Client(space).predict(**build(str(ROOT / "assets/images" / img), prompt, dur))
                vid = res[0]["video"] if isinstance(res[0], dict) else res[0]
                dst = VID / f"scene{n:02d}_motion.mp4"
                shutil.copy(vid, dst)
                a.update(result="ok", info=probe(dst), sec=round(time.time() - t))
                rec.update(status="success", file=dst.name, tool=space, params=a)
                rec["attempts"].append(a)
                break
            except Exception as e:
                a.update(result="fail", error=str(e)[:300], sec=round(time.time() - t))
                rec["attempts"].append(a)
                print(n, space, "FAIL", str(e)[:200])
        log[str(n)] = rec
        LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1))
        print(n, rec["status"], rec["file"])


if __name__ == "__main__":
    main()
