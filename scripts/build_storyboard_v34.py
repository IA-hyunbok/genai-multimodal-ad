#!/usr/bin/env python3
"""최종 제출본 v3(바다판)·v4(booth) 스토리보드 PDF 생성. v1 build_storyboard.py와 같은 양식(CSS)을 쓴다.
실행: python3 scripts/build_storyboard_v34.py
  -> storyboard/v3/Codyssey_Storyboard_v3.pdf, storyboard/v4/Codyssey_Storyboard_v4_booth.pdf
근거: cuts_v3.json·cuts_v3.md·timeline_v3c.json·storyboard_v3.md / storyboard_v4_booth.md·edit_v4.py SEGS / build/*/*.prompt.txt·*.log / README.
썸네일은 ffmpeg로 storyboard/thumbs/v3·v4 에 만든다. 재실행 가능.
"""
import ast, html, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FF, FP = "/opt/homebrew/bin/ffmpeg", "/opt/homebrew/bin/ffprobe"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
e = html.escape
BRAND = json.loads((ROOT / "storyboard/storyboard.json").read_text())["brand"]
CSS = re.search(r'CSS = """(.*?)"""', (ROOT / "scripts/build_storyboard.py").read_text(), re.S).group(1)  # v1과 같은 양식
CSS += "html{zoom:.74}.fr{flex-wrap:wrap}.fr img{height:40mm}\n"  # v1 PDF와 같은 밀도(v1은 넘친 프레임 띠 때문에 Chrome이 약 0.74배로 축소 인쇄됨)
CSS += ".scr{white-space:pre-wrap;font-family:Menlo,monospace;font-size:7.6pt;line-height:1.45;background:#f5f7fb;border:1px solid #c8d1e6;padding:3mm;border-radius:2mm}\n"


def ff(*a):
    subprocess.run([FF, "-y", "-v", "error", *map(str, a)], check=True)


def shot(src, t, out, h=None):
    """영상 src의 t초 프레임(또는 이미지) -> out(jpg). 상대경로 반환"""
    out.parent.mkdir(parents=True, exist_ok=True)
    pre = ["-ss", f"{t:.2f}"] if t is not None else []
    ff(*pre, "-i", ROOT / src, "-frames:v", 1, "-vf", f"scale={'-2:' + str(h) if h else '720:-1'}", "-q:v", 3, out)
    return out


def probe(p):
    j = json.loads(subprocess.run([FP, "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration,size",
                                   "-of", "json", str(ROOT / p)], capture_output=True, text=True, check=True).stdout)
    v = next(s for s in j["streams"] if "width" in s)
    a = next(s for s in j["streams"] if "sample_rate" in s)
    return float(j["format"]["duration"]), v, a, int(j["format"]["size"])


def prompt(path):
    p = ROOT / path
    return p.read_text().strip() if p.exists() else ""


def job(log):
    p = ROOT / log
    m = re.search(r"job (vjob_\w+)", p.read_text()) if p.exists() else None
    return m.group(1) if m else ""


def md_table(md, header):
    """md에서 header로 시작하는 표의 행들 -> [[셀...]]"""
    lines = md.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith(header))
    rows = []
    for l in lines[i + 2:]:
        if not l.startswith("|"):
            break
        rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    return rows


def head(title):
    return f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{e(title)}</title><style>{CSS}</style></head><body>"


def brand_table():
    b = BRAND
    return f"""<h2>1. 브랜드 아이덴티티</h2>
<table><tr><th>브랜드</th><td>{e(b['name'])} — 운영: {e(b['operator'])}</td></tr>
<tr><th>정체</th><td>{e(b['what_it_is'])}</td></tr>
<tr><th>타겟</th><td>{e(b['target'])}</td></tr>
<tr><th>USP</th><td>{'<br>'.join('· ' + e(u) for u in b['usp'])}</td></tr>
<tr><th>출처</th><td>{'<br>'.join(e(s) for s in b['sources'])}</td></tr>
<tr><th>사실 확인 한계</th><td>{e(b['fact_caveats'])}</td></tr></table>"""


def flow(steps):
    return "<div class='fl'>" + "<div class='ar'>▶</div>".join(f"<div><b>{e(t)}</b>{d}</div>" for t, d in steps) + "</div>"


def final_info(path, times, th):
    dur, v, a, size = probe(path)
    imgs = "".join(f"<img src='../{shot(path, t, th / f'final_t{t}.jpg', 480).relative_to(th.parent.parent).as_posix()}'>" for t in times)
    return dur, f"""<table><tr><th>파일명</th><th>길이</th><th>해상도</th><th>fps</th><th>코덱</th><th>크기</th></tr>
<tr><td>{e(path)}</td><td>{dur:.1f}초</td><td>{v['width']}x{v['height']}</td><td>{e(v['r_frame_rate'])}</td>
<td>{e(v['codec_name'].upper())} / {e(a['codec_name'].upper())} {a['sample_rate']}Hz {a['channels']}ch</td><td>{size / 1e6:.1f}MB</td></tr></table>
<div class='fr'>{imgs}</div><p class='t'>최종 영상 프레임 캡처({', '.join(f'{t}초' for t in times)}). 값은 ffprobe 실측.</p>"""


def pdf(html_path, pdf_path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, capture_output=True)


# ---------------------------------------------------------------- v3 바다판
def build_v3():
    SBD = ROOT / "storyboard/v3"
    TH = ROOT / "storyboard/thumbs/v3"
    rel = lambda p: "../" + Path(p).relative_to(SBD.parent).as_posix()
    cuts = json.loads((SBD / "cuts_v3.json").read_text())
    tl = json.loads((SBD / "timeline_v3c.json").read_text())
    md = (SBD / "cuts_v3.md").read_text()
    sb = (SBD / "storyboard_v3.md").read_text()
    FINAL = "output/final/Codyssey_Final_1st_v3_ocean_16x9.mp4"
    # 컷별 편집 위치(타임라인 순서 = c01..c19)
    starts, t = {}, 0.0
    for s in tl["segs"]:
        cid = Path(s["src"]).stem
        starts[cid] = (t, s["dur"])
        t += s["dur"]
    supers = {Path(tl["segs"][i]["src"]).stem: txt for i, _, _, txt in tl["supers"]}
    rows = {r[0].lower(): r for r in md_table(md, "| 컷 | 씬 |")}  # c01 -> [컷, 씬, 길이, 말하는 사람, 대사, 화면, 슈퍼]
    chars = md_table(md, "| 인물 | 디자인 시트 |")
    final_dur, final_html = final_info(FINAL, [3, 12, 22, 33, 44, 55], TH)
    loglines = [l[2:] for l in sb.split("## ")[0].splitlines() if l.startswith("- ")]

    o = [head("코디세이 스토리보드 v3")]
    w = o.append
    w(f"""<div class='cover'><div class='sub'>GenAI 기초 2 · 멀티모달 콘텐츠 제작 스토리보드 · 최종 1순위</div><h1>{e(BRAND['name'])}<br>「코디세이로 오라」 바다판</h1>
<p>슬로건 : 문턱은 없고, 동료는 있다.<br>엔드 서브라인 : 전공 무관 · 장학금 · 동료학습 / CTA : 코디세이로 와라! codyssey.kr</p>
<p style='margin-top:20mm'>최종 영상 : {e(Path(FINAL).name)} (1920x1080)<br>
총 {final_dur:.1f}초 · 9씬 19컷 · 캐릭터 디자인 시트·씬 키프레임(코디세이 COPA gpt-image-2) → 컷별 영상(COPA veo-3.1 Text-to-Video, 한 컷 한 사람 대사) → 받아쓰기(faster-whisper) 기준 싱크 편집(ffmpeg)</p></div>""")
    w(brand_table())
    w("<h2 style='margin-top:6mm'>2. 캠페인 목표 · 핵심 메시지</h2><table>" +
      "".join(f"<tr><th>{e(l.split(':', 1)[0])}</th><td>{e(l.split(':', 1)[1].strip()).replace('**', '')}</td></tr>" for l in loglines if ':' in l) +
      "</table>")
    w("<h2 style='margin-top:6mm'>3. 제작 파이프라인</h2>" + flow([
        ("① 캐릭터 디자인 시트", "gpt-image-2로 인물 4명<br>정면·옆모습·얼굴 한 장씩<br>scripts/design_sheets.py"),
        ("② 씬 키프레임", "씬마다 gpt-image-2 1장으로<br>구도 먼저 확정<br>scripts/cuts.py v3 keys"),
        ("③ 컷별 영상", "veo-3.1 T2V 4·6초 19컷<br><b style='display:inline;color:#0B1B3F'>한 컷 = 한 사람 대사</b><br>scripts/shoot.sh v3c cNN"),
        ("④ 싱크 편집", "faster-whisper로 받아써 대사 앞뒤만 남김<br>자막·키워드 슈퍼·엔드카드<br>sync_cuts.py · edit_cut.py"),
    ]) + "<table><tr><th>단계 사이 원칙</th><td>COPA 영상 API가 이미지 입력을 받지 않아(7장 테스트) 디자인 시트에서 본 생김새를 글로 옮겨 매 컷 프롬프트에 똑같이 넣었다. "
      "한 클립에 여러 사람 대사를 넣으면 veo가 대사를 엉뚱한 인물에게 배정해, 대사가 여럿이어도 같은 사람 것만 한 컷에 둔다.</td></tr></table>")

    w("<section><h2>4. 캐릭터 디자인 시트 · 고정 묘사</h2>")
    for name, img, desc in chars:
        src = re.search(r"\((.*?)\)", img).group(1).replace("../../", "")
        th = shot(src, None, TH / f"sheet_{Path(src).stem}.jpg")
        w(f"<div class='card'><div class='th'><img src='{rel(th)}'><div class='t'>{e(src)}</div></div><div><div class='hd'>{e(name)}</div>"
          f"<table><tr><th>고정 묘사(프롬프트에 그대로)</th><td class='pr'>{e(desc)}</td></tr></table></div></div>")
    w(f"""<h2 style='margin-top:6mm'>5. 스타일 고정 파라미터</h2><table>
<tr><th>룩(전 컷 공통 접미)</th><td class='pr'>{e(cuts['look'])}</td></tr>
<tr><th>싱크 조건</th><td>말하는 사람의 얼굴·입이 보이고 음절에 맞춰 입이 움직일 것 · 대사마다 시작/끝 초와 "정확히 한 번, 글자 그대로" · 그 외 시간엔 입을 닫을 것 · 다른 인물은 말하지 않을 것 · 인물별 고정 목소리 · 배경음악·내레이션 금지 · 괄호 속 동작은 VISUAL ACTION으로 시간과 함께 따로 적음</td></tr>
<tr><th>생성 규격</th><td>veo-3.1, 720p, 16:9, 컷 4초 또는 6초(합계 82초 생성) → 편집에서 대사 앞 0.15초~뒤 0.2초만 남겨 {final_dur:.1f}초</td></tr>
<tr><th>편집</th><td>음량 -16 LUFS 맞춤 · 대본 글자를 실제 발화 시간에 맞춘 자막 · 키워드 슈퍼({' / '.join(e(s) for s in supers.values())}) · 엔드카드 · 전 컷 "연출된 가상 상황 · AI로 제작" 고지</td></tr>
<tr><th>파일 네이밍</th><td>프롬프트 build/v3c/cNN.prompt.txt · 클립 assets/v3c/cNN.mp4 · 키프레임 assets/v3c/keys/SNN.png · 편집 타임라인 storyboard/v3/timeline_v3c.json</td></tr></table></section>""")

    w("<section><h2>6. 씬별 카드 (최종 채택 소스)</h2>")
    for sc in cuts["scenes"]:
        key = shot(f"assets/v3c/keys/{sc['id']}.png", None, TH / f"key_{sc['id']}.jpg")
        frames = ""
        for c in sc["cuts"]:
            st, d = starts[c["id"]]
            fr = shot(FINAL, st + d / 2, TH / f"cut_{c['id']}.jpg")
            frames += f"<img src='{rel(fr)}' style='margin-top:2mm'><div class='t'>{c['id'].upper()} · 완성본 {st:.1f}~{st + d:.1f}초</div>"
        w(f"<div class='card'><div class='th'><img src='{rel(key)}'><div class='t'>키프레임 assets/v3c/keys/{sc['id']}.png (gpt-image-2)</div>{frames}</div>"
          f"<div style='flex:1'><div class='hd'>{sc['id']} · {e(sc['name'])}</div><table>")
        for c in sc["cuts"]:
            cid = c["id"]
            r = rows[cid]
            st, d = starts[c["id"]]
            w(f"<tr><th>{c['id'].upper()} · {e(r[3])}</th><td><b>{r[4]}</b><br>생성 {c['dur']}초 → 편집 {d:.2f}초"
              f"{' · 슈퍼 「' + e(supers[c['id']]) + '」' if c['id'] in supers else ''} · job {job(f'build/v3c/{cid}.log')}</td></tr>"
              f"<tr><th>입력 프롬프트(원문)</th><td class='pr'>{e(prompt(f'build/v3c/{cid}.prompt.txt'))}</td></tr>")
        w("</table></div></div>")
    w("</section>")

    # 7 수정 전/후
    old = shot("build/v3live/fr/shot02.png", None, TH / "rev_live_shot02.jpg")
    new2 = shot(FINAL, starts["c02"][0] + starts["c02"][1] / 2, TH / "rev_c02.jpg")
    new3 = shot(FINAL, starts["c03"][0] + starts["c03"][1] / 2, TH / "rev_c03.jpg")
    sheet = shot("assets/v5/design/captain.png", None, TH / "rev_sheet.jpg")
    i2v = shot("assets/v5/design/i2v_test.mp4", 2, TH / "rev_i2v.jpg")
    w(f"""<section><h2>7. 프롬프트 수정 전/후 비교</h2>
<h3>S02 국문과 — 한 클립 여러 화자(v3 실사) → 한 컷 한 화자(바다판 C02·C03)</h3>
<div class='ba'><div><b>수정 전 (build/v3live/shot02, 폐기)</b><img src='{rel(old)}'><div class='pr' style='margin-top:1mm'>{e(prompt('build/v3live/shot02.prompt.txt'))}</div></div>
<div><b>수정 후 (C02 사부 / C03 소라, 채택)</b><img src='{rel(new2)}'><img src='{rel(new3)}' style='margin-top:2mm'><div class='pr' style='margin-top:1mm'>{e(prompt('build/v3c/c03.prompt.txt'))}</div></div></div>
<p><b>변경.</b> 사부·소라 두 사람의 대사 세 줄을 한 클립에 넣던 것을, 사부(C02) · 소라(C03) · 사부(C04) 세 컷으로 나누고 컷마다 말하는 사람 한 명만 두었다. 대사마다 시작·끝 초, "exactly once and word for word", 그 외 시간 입 닫기, 다른 인물 침묵, 동작(VISUAL ACTION)을 따로 적었다.<br>
<b>이유.</b> 한 클립에 두세 명의 대사를 넣자 veo가 대사를 엉뚱한 인물에게 배정했다(사부가 "저 국문과인데요"를 말함). 세계관도 별·우주(키보드 검)에서 바다로 바꿨다.<br>
<b>결과.</b> 19컷 모두 말하는 순간의 프레임으로 화자를 확인했고, 받아쓰기로 대사를 대조했다.</p>
<h3>Image-to-Video 테스트 — 디자인 시트를 영상 재료로 (불채택)</h3>
<div class='ba'><div><b>입력: 선장 디자인 시트 (assets/v5/design/captain.png)</b><img src='{rel(sheet)}'></div>
<div><b>결과: assets/v5/design/i2v_test.mp4 (2초 프레임)</b><img src='{rel(i2v)}'></div></div>
<p>COPA 영상 API에 이미지 필드를 붙여 1회 요청(job vjob_8cc5911c52864c939087d7ce). 접수는 됐지만 결과에 이미지가 반영되지 않았다(다른 인물·배경). 그래서 시트의 생김새를 글로 옮겨 매 컷 같은 문장으로 넣었다(4장 고정 묘사).</p></section>""")

    w(f"""<section><h2>8. 실패 · 대체 기록과 남은 한계</h2><table><tr><th>영역</th><th>문제</th><th>대응·결과</th></tr>
<tr><td>화자 배정</td><td>한 클립 여러 대사 → veo가 대사를 다른 인물에게 배정</td><td>한 컷 한 화자로 재설계(7장)</td></tr>
<tr><td>이미지 입력</td><td>Image-to-Video 요청에 이미지 미반영</td><td>디자인 시트 묘사를 글로 고정해 T2V</td></tr>
<tr><td>사용량 예산</td><td>19컷 일괄 생성 중 COPA가 budget_exceeded(429)로 13컷 거절(4초 클립 1개에 약 53만 normalized tokens)</td><td>예산이 다시 들어온 뒤 남은 컷만 이어서 생성</td></tr>
<tr><td>군말·자막</td><td>대본 앞뒤에 섞인 군말, 박혀 나온 깨진 자막·레터박스</td><td>대본 첫·끝 글자로 찾아 잘라냄, 크롭(sync_cuts.py)</td></tr>
<tr><td>남은 한계</td><td colspan='2'>엔드컷 인원·의상(네 명 대신 세 명, 소라가 재킷 차림) · S06 사부가 망원경으로 유리를 두드리는 동작이 안 보임 · 첫 컷이 2초로 짧음</td></tr></table>
<h2 style='margin-top:6mm'>9. 최종 영상 정보</h2>{final_html}</section></body></html>""")
    out = SBD / "storyboard_v3.html"
    out.write_text("".join(o))
    pdf(out, SBD / "Codyssey_Storyboard_v3.pdf")
    return SBD / "Codyssey_Storyboard_v3.pdf"


# ---------------------------------------------------------------- v4 booth
def build_v4():
    SBD = ROOT / "storyboard/v4"
    TH = ROOT / "storyboard/thumbs/v4"
    rel = lambda p: "../" + Path(p).relative_to(SBD.parent).as_posix()
    md = (SBD / "storyboard_v4_booth.md").read_text()
    src = (ROOT / "scripts/edit_v4.py").read_text()
    V3, V4 = "assets/v3/live", "assets/v4"
    segs = ast.literal_eval(re.search(r"SEGS = (\[.*?\n\])", src, re.S).group(1).replace('f"{V4}', '"' + V4).replace('f"{V3}', '"' + V3)
                            .replace("VF_02", "'crop'").replace("VF_10", "'flip'"))
    FINAL = "output/final/Codyssey_Final_2nd_v4_booth_16x9.mp4"
    final_dur, final_html = final_info(FINAL, [3, 9, 18, 27, 37, 47, 54], TH)
    chars = md_table(md, "| 이름 | 설정 |")
    look = re.search(r"조정실 공통 룩: (.*)", md).group(1)
    script = re.search(r"## 전체 대본\n\n```\n(.*?)```", md, re.S).group(1)
    bullets = [l[2:] for l in md.split("## ")[0].splitlines() if l.startswith("- ")]

    o = [head("코디세이 스토리보드 v4 booth")]
    w = o.append
    w(f"""<div class='cover'><div class='sub'>GenAI 기초 2 · 멀티모달 콘텐츠 제작 스토리보드 · 최종 2순위</div><h1>{e(BRAND['name'])}<br>「코디세이 홍보영상이 망한 이유」</h1>
<p>슬로건 : 문턱은 없고, 동료는 있다. / CTA : codyssey.kr<br>설명회 조정실에서 AI로 홍보영상을 만들다 프롬프트를 고칠 때마다 결과가 엉뚱해지는 메타 코미디</p>
<p style='margin-top:20mm'>최종 영상 : {e(Path(FINAL).name)} (1920x1080)<br>
총 {final_dur:.1f}초 · 15세그먼트 · 조정실·완성 클립(COPA veo-3.1 / B06만 veo-3.1-fast) + v3 실사 클립 재사용 + 프롬프트 입력창 그래픽(Pillow) · 편집 scripts/edit_v4.py(ffmpeg)</p></div>""")
    w(brand_table())
    w("<h2 style='margin-top:6mm'>2. 캠페인 목표 · 핵심 메시지</h2><table>" +
      "".join(f"<tr><th>{e(b.split(':', 1)[0])}</th><td>{e(b.split(':', 1)[1].strip()).replace('**', '')}</td></tr>" for b in bullets if ':' in b and not b.startswith("길이")) + "</table>")
    w("<h2 style='margin-top:6mm'>3. 제작 파이프라인</h2>" + flow([
        ("① 구조 차용", "레퍼런스(fTHUtHvAUe4)의<br>조정실 + 'AI로 금방 만들게요'<br>+ 고칠수록 엉뚱한 결과<br>구조만, 장면·대사는 새로"),
        ("② 신규 클립", "조정실 B01~B06 + 완성 F01<br>veo-3.1 T2V<br>대사는 says in Korean,<br>'All dialogue in Korean only'"),
        ("③ 받아쓰기 검수", "faster-whisper로 실제 대사가<br>한국어인지·대본과 맞는지 확인<br>→ 틀린 클립만 재생성"),
        ("④ 편집", "v3 실사 클립 재사용(AI 결과물 ①②)<br>프롬프트 입력창 타이핑 그래픽<br>자막·키워드·엔드카드<br>scripts/edit_v4.py"),
    ]))
    w("<section><h2>4. 등장인물 · 공통 룩</h2><table><tr><th>이름</th><th>설정</th><th>고정 묘사(veo 프롬프트에 그대로)</th></tr>" +
      "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td class='pr'>{e(c)}</td></tr>" for a, b, c in chars) +
      f"<tr><th>조정실 공통 룩</th><td colspan='2' class='pr'>{e(look)}</td></tr></table>"
      f"<h2 style='margin-top:6mm'>5. 전체 대본</h2><div class='scr'>{e(script)}</div><p class='t'>※ 촬영 전 대본 기준 시각. 완성본에서는 B06(팀장 「…안디아모.」)을 엔드카드 앞으로 옮겼다(6장 순서, 8장).</p></section>")

    w("<section><h2>6. 씬별 카드 (최종 편집 순서)</h2>")
    t = 0.0
    for i, (s, ss, dur, vf, mute, subs, badge) in enumerate(segs, 1):
        fr = shot(FINAL, t + dur / 2, TH / f"seg{i:02d}.jpg")
        if s == "PROMPT":
            kind, pr, info = "프롬프트 입력창 그래픽 (Pillow 타이핑 애니메이션)", "", f"입력 문구: 「{e(badge)}」"
        else:
            stem = Path(s).stem
            new = s.startswith(V4)
            kind = f"{'신규 veo' if new else 'v3 실사 재사용'} · {e(s)} ({ss}초부터)"
            pr = prompt(f"build/v4/{stem}.prompt.txt" if new else f"build/v3live/{stem}.prompt.txt")
            info = " / ".join(e(x[2]) for x in subs)
            if badge:
                info = f"<span style='color:#c33'>● {e(badge)}</span> " + info
            if mute:
                info += " · 묵음 구간 " + ", ".join(f"{a}~{b}초" for a, b in mute)
            if new and job(f"build/v4/{stem}.log"):
                kind += f" · job {job(f'build/v4/{stem}.log')}"
        w(f"<div class='card'><div class='th'><img src='{rel(fr)}'><div class='t'>완성본 {t:.1f}~{t + dur:.1f}초</div></div>"
          f"<div style='flex:1'><div class='hd'>씬 {i:02d} · {dur}초</div><table><tr><th>소스</th><td>{kind}</td></tr><tr><th>대사·자막</th><td>{info}</td></tr>"
          + (f"<tr><th>입력 프롬프트(원문)</th><td class='pr'>{e(pr)}</td></tr>" if pr else "") + "</table></div></div>")
        t += dur
    w("</section>")

    def ba(stem, why, t1=2):
        a = shot(f"assets/v4/{stem}.mp4", t1, TH / f"rev_{stem}.jpg")
        b = shot(f"assets/v4/{stem}_v2.mp4", t1, TH / f"rev_{stem}_v2.jpg")
        return (f"<h3>{stem} → {stem}_v2</h3><div class='ba'><div><b>수정 전 ({stem}.mp4, {t1}초 프레임)</b><img src='{rel(a)}'><div class='pr' style='margin-top:1mm'>{e(prompt(f'build/v4/{stem}.prompt.txt'))}</div></div>"
                f"<div><b>수정 후 ({stem}_v2.mp4, 채택)</b><img src='{rel(b)}'><div class='pr' style='margin-top:1mm'>{e(prompt(f'build/v4/{stem}_v2.prompt.txt'))}</div></div></div><p>{why}</p>")
    w("<section><h2>7. 프롬프트 수정 전/후 비교</h2>"
      "<h3>광고 속 프롬프트 ① → ② → ③ (미션 연결: 수정 전/후가 화면에 그대로 나온다)</h3><table><tr><th>순서</th><th>입력창 문구</th><th>AI 결과물</th></tr>"
      "<tr><td>①</td><td>코디세이 홍보영상 만들어줘. 웅장하게.</td><td>우주 절벽 위 사부 「별이 말했다.」 → 팀장 「교육 플랫폼이 왜 우주 전쟁을 해!」</td></tr>"
      "<tr><td>②</td><td>칼 빼고, 배우는 사람 얘기로.</td><td>국문과·통장 장면은 괜찮다가 끝에 갑자기 이탈리아어 「Andiamo insieme!」</td></tr>"
      "<tr><td>③</td><td>전공 몰라도, 돈 걱정 없이, 동료랑 같이 배우는 곳.</td><td>셋이 「같이 갑니다!」, 사부 「여기 교수는 없다. 동료가 있다.」</td></tr></table>"
      + ba("B02", "<b>이유·결과.</b> B02·F01은 1차 생성의 발음/인물 불일치로 재생성(storyboard_v4_booth.md 제작 결과). v2 프롬프트는 0~2초 정적 후 2~6초에 \"every syllable distinct\"로 천천히 외치게 했고, 편집에서 1.0초부터 4.3초 길이를 썼다.")
      + ba("F01", "<b>이유·결과.</b> B02·F01은 1차 생성의 발음/인물 불일치로 재생성(storyboard_v4_booth.md 제작 결과). 편집에서 v2의 0~7.2초를 썼다.")
      + "</section>")
    w(f"""<section><h2>8. 실패 · 대체 기록</h2><table><tr><th>영역</th><th>문제</th><th>대응·결과</th></tr>
<tr><td>B06 생성</td><td>veo-3.1 생성이 두 번 멈춤</td><td>veo-3.1-fast로 생성(B06_v2)</td></tr>
<tr><td>B05 대사</td><td>민준의 "…네!"를 veo가 다른 대사로 생성</td><td>1.05초 이후 묵음 처리, 지은 "같이 고치자."만 사용</td></tr>
<tr><td>v3 이탈리아어</td><td>v3 클립이 실제로 이탈리아어로 나옴(언어 감지 it 0.98, "La strada è ancora lunga, andiamo insieme!")</td><td>결함을 "AI가 엉뚱하게 만든 결과물"로 쓰고, 마지막 팀장 「…안디아모.」의 복선으로 회수</td></tr>
<tr><td>순서 변경</td><td>B06이 엔드카드 뒤에 있으면 마지막 5초가 브랜드가 아님</td><td>B06을 엔드카드 앞으로 옮겨 마지막 5초를 브랜드/CTA로 고정</td></tr>
<tr><td>검증</td><td colspan='2'>완성본을 faster-whisper로 다시 받아써 자막 시각과 대조, 모든 대사 자막이 실제 발화 ±0.4초 안</td></tr></table>
<h2 style='margin-top:6mm'>9. 최종 영상 정보</h2>{final_html}</section></body></html>""")
    out = SBD / "storyboard_v4_booth.html"
    out.write_text("".join(o))
    pdf(out, SBD / "Codyssey_Storyboard_v4_booth.pdf")
    return SBD / "Codyssey_Storyboard_v4_booth.pdf"


if __name__ == "__main__":
    for f in (build_v3, build_v4):
        print(f())
