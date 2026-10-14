import subprocess, json, os
from PIL import Image, ImageDraw, ImageFont
R = "/Users/hyunbok/Desktop/genai-multimodal-ad"; B = f"{R}/build/v3"
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
def font(sz):
    return ImageFont.truetype(FONT, sz, index=6)  # Bold (ExtraBold not in this ttc)
NAVY, YEL = (27, 31, 59), (255, 201, 51)
def text_png(path, items):
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for t, sz, cy, fill in items:
        f = font(sz); w = d.textlength(t, font=f)
        d.text(((1920 - w) / 2, cy), t, font=f, fill=fill, stroke_width=max(2, sz // 9), stroke_fill=NAVY)
    im.save(path)
def wm_png(path, notice):
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((40, 30), "ANIMATIC", font=font(30), fill=(255, 255, 255, 200), stroke_width=2, stroke_fill=NAVY)
    if notice: d.text((60, 1080 - 90), notice, font=font(30), fill=(255, 255, 255, 235), stroke_width=3, stroke_fill=NAVY)
    im.save(path)
W, Y = (255, 255, 255), YEL
# scene: (dur, [(lines (file idx, gap_before))], captions [(t0,t1,items)], zoom dir)
S = {
 1: (6, [(0, .3), (1, .3)], [(4.2, 6, [("코디세이 기사단", 120, 800, W)])]),
 2: (8, [(0, .2), (1, .2), (2, 1.0)], []),
 3: (3, [(0, .1), (1, .2)], [(.1, 3, [("전공·경력 무관", 150, 60, W)])]),
 4: (8, [(0, .2), (1, .2), (2, 1.0)], []),
 5: (3, [(0, .1), (1, .1)], [(.1, 3, [("장학금", 170, 120, Y)])]),
 6: (8, [(0, .2), (1, .2), (2, 1.0)], []),
 7: (3, [], [(.1, 3, [("동료학습", 170, 40, W)])]),
 8: (8, [(0, .1), (1, .1), (2, .1), (3, .1), (4, .1)], []),
 9: (3, [(0, .1), (1, .5)], []),
 10: (5, [(0, .3)], [(.1, 5, [("문턱은 없고,", 120, 150, W), ("동료는 있다.", 120, 290, Y), ("전공 무관 · 장학금 · 동료학습", 64, 470, W), ("CODYSSEY", 90, 600, Y), ("codyssey.kr", 54, 730, W)])]),
}
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
def sh(*a): subprocess.run(a, check=True, stderr=subprocess.DEVNULL)
os.makedirs(B, exist_ok=True)
report = []
for n, (D, lines, caps) in S.items():
    # trimmed vo
    clips = []
    for i, gap in lines:
        t = f"{B}/vo{n:02d}_{i}.wav"
        sh("ffmpeg","-y","-i",f"{R}/assets/v3/vo/scene{n:02d}_{i}.mp3","-af",
           "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,aresample=44100","-ac","1",t)
        clips.append((t, gap, dur(t)))
    tot = sum(c[1] + c[2] for c in clips)
    fac = max(1.0, tot / (D - 0.15)) if clips else 1.0
    fac = min(fac, 1.6)
    # place
    t0 = 0; inputs = []; filt = []; mix = []
    for k, (f, gap, dd) in enumerate(clips):
        t0 += gap / (1 if fac == 1 else fac)
        inputs += ["-i", f]
        filt.append(f"[{k}:a]atempo={fac:.3f},adelay={int(t0*1000)}|{int(t0*1000)}[a{k}]"); mix.append(f"[a{k}]")
        t0 += dd / fac
    end = t0
    report.append((n, round(tot, 2), round(fac, 2), round(end, 2), D))
    out = f"{B}/aud{n:02d}.wav"
    if clips:
        sh("ffmpeg","-y",*inputs,"-filter_complex",";".join(filt)+";"+"".join(mix)+f"amix=inputs={len(mix)}:normalize=0,apad=whole_dur={D},atrim=0:{D}[o]","-map","[o]","-ar","44100","-ac","2",out)
    else:
        sh("ffmpeg","-y","-f","lavfi","-i",f"anullsrc=r=44100:cl=stereo","-t",str(D),out)
    # overlays
    ovs = []
    for j, (a, b, items) in enumerate(caps):
        p = f"{B}/cap{n:02d}_{j}.png"; text_png(p, items); ovs.append((p, a, b))
    wp = f"{B}/wm{n:02d}.png"; wm_png(wp, "※ 연출된 가상 상황 · AI로 제작" if n == 10 else None)
    ovs.insert(0, (wp, 0, D))
    frames = D * 30
    zin = n % 2 == 0
    z = "min(zoom+0.0007,1.12)" if zin else "if(eq(on,0),1.12,max(zoom-0.0007,1.0))"
    cmd = ["ffmpeg","-y","-loop","1","-t",str(D),"-i",f"{R}/assets/v3/stills/scene{n:02d}.png"]
    for p,_,_ in ovs: cmd += ["-loop","1","-t",str(D),"-i",p]
    cmd += ["-i", out]
    fc = f"[0:v]crop=1536:864:0:80,scale=3840:2160,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30,format=yuv420p[v0]"
    for k,(p,a,b) in enumerate(ovs, 1):
        fc += f";[v{k-1}][{k}:v]overlay=enable='between(t,{a},{b})'[v{k}]"
    cmd += ["-filter_complex", fc, "-map", f"[v{len(ovs)}]", "-map", f"{len(ovs)+1}:a", "-t", str(D), "-r","30","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k", f"{B}/seg{n:02d}.mp4"]
    sh(*cmd)
with open(f"{B}/list.txt","w") as f:
    for n in S: f.write(f"file 'seg{n:02d}.mp4'\n")
sh("ffmpeg","-y","-f","concat","-safe","0","-i",f"{B}/list.txt","-c","copy",f"{R}/output/v3/animatic_v3.mp4")
for r in report: print("scene, vo_total, tempo, vo_end, dur:", r)
