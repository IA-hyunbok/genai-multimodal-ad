# 사용: words.py clip.mp4 [...]  -> 단어별 타임스탬프 (자막 타이밍용, faster-whisper medium)
import sys
from faster_whisper import WhisperModel

m = WhisperModel("medium", compute_type="int8")
for f in sys.argv[1:]:
    segs, _ = m.transcribe(f, language="ko", word_timestamps=True)
    print("==", f.rsplit("/", 1)[-1])
    for s in segs:
        print(" ".join(f"{w.start:.2f}-{w.end:.2f}:{w.word.strip()}" for w in s.words))
