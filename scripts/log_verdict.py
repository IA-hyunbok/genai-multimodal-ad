#!/usr/bin/env python
"""Read 도구 육안 검수 결과를 generation_log.json 에 기록 (생성 호출 없음)."""
import json, pathlib
LOG = pathlib.Path(__file__).resolve().parent.parent / "assets/images/generation_log.json"
V = {
 "scene01_img_v1.png": ("불합격", "수정 전: 얼굴 옆모습이 보이는 사실적 인물+숲, 화풍·팔레트 불일치, 갈림길·앰버 식별자 없음, 팔레트 이탈(청회색 실사풍)"),
 "scene01_img_v2.png": ("채택", "수정 후: 뒷모습 실루엣+안개 낀 남색 숲길, 얼굴 비노출·남색/블루 톤 통일·글자 없음. 단 플랫 벡터가 아닌 회화풍, 앰버 스카프·갈림길은 미반영"),
 "scene01_img_v3.png": ("보류", "'flat vector'를 앞세운 3차: 더 어두운 남색으로 톤은 맞지만 여전히 회화풍·스카프 없음, v2 대비 개선 미미(최대 3회 소진)"),
 "scene02_img_v1.png": ("불합격", "유리 돔 속 모래시계 클로즈업만 나오고 손·노트북·동전 누락, 의도 구도와 불일치"),
 "scene02_img_v2.png": ("채택", "플랫 기하 스타일+남색/앰버 팔레트로 톤 일치, 책더미·동전컵·모래시계 모티프 존재. 손·키보드는 추상화됨"),
 "scene03_img_v1.png": ("불합격", "두 실루엣이 손잡고 터널로 걸어가는 사실적 이미지, 앰버 문 없음, 전환(문 열림) 메시지 약함"),
 "scene03_img_v2.png": ("채택", "앰버 아치 문+남색→블루 하늘, 어두운 길에서 빛으로 향하는 전환 구도 성립. 인물이 2명이며 손잡음(스카프 없음)"),
 "scene04_img_v1.png": ("불합격", "프롬프트 과다로 사람 없이 추상 타원 도형만 생성, 협업 장면 아님"),
 "scene04_img_v2.png": ("불합격", "플랫 지시를 줬으나 대칭 추상 도형으로 퇴행, 인물·테이블 없음"),
 "scene04_img_v3.png": ("채택(한계)", "둥근 테이블에 3명이 앉아 협업하는 장면 성립, 블루 톤 일치. 단 인물이 사실적·흐릿한 얼굴로 faceless 원칙 미달, 4명 미충족(3회 소진)"),
 "scene05_img_v1.png": ("보류", "별 하늘+도시 스카이라인+길 위 뒷모습, 구도 적합하나 실사풍·두 갈래 길 없음"),
 "scene05_img_v2.png": ("채택", "플랫 톤의 블루 하늘+도시 실루엣+앰버 길 양옆, 뒷모습 인물 중앙. 두 갈래 길은 좌우 앰버 노면으로 암시, 별 조각 약함"),
 "scene06_img_v1.png": ("보류", "빛나는 흰 타원이 중앙을 차지, 앰버 별/궤도 모티프 없음, 텍스트 영역 부족"),
 "scene06_img_v2.png": ("채택", "남색 그라디언트 위 앰버 구체+궤도 링, 브랜드 팔레트 일치. 중앙이 비지는 않아 텍스트는 상/하단 배치 필요"),
}
log = json.loads(LOG.read_text())
for k, (v, s) in V.items():
    log[k].update(verdict=v, summary=s)
log["_notes"] = {
 "watermark": "Pollinations 응답 우하단에 'pollinations.ai' 워터마크가 찍힘(nologo=true 무시, 익명 티어). 편집 단계에서 하단/우측 크롭+스케일로 제거.",
 "model_param_ignored": "model=flux/turbo/sana 모두 응답 바이트 동일(md5 일치), EXIF manufacturer=sana, 1024x576 JPEG. storyboard의 'flux 고정'은 사실과 다름 -> 실제 모델은 sana.",
 "size": "width=1280&height=720 요청, 실제 수신 1024x576 JPEG -> ffmpeg로 PNG 변환(업스케일은 편집 단계).",
 "http_402": "익명 호출이 간헐적으로 HTTP 402(본문 {})를 반환, 25초 간격 재시도(최대 8회)로 극복. 실패 시도는 스크립트 stdout에만 남음(총 20여 회).",
 "style_suffix_ineffective": "긴 style_suffix 프롬프트는 모델이 거의 무시(실사풍). 짧게 줄이고 'flat vector illustration'을 앞에 둔 v2가 팔레트·화풍 일관성 개선.",
 "bonus_alt_failed": "scene03/05 FLUX.1-schnell(HF Space) 대조 시도: ZeroGPU 쿼터 소진('exceeded your ZeroGPU quota') -> alt 파일 없음. Pollinations model 파라미터 대조는 동일 바이트라 무효.",
}
LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1))
