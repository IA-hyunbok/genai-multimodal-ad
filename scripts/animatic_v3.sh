#!/bin/sh
# animatic v3: assets/v3 stills+VO -> output/v3/animatic_v3.mp4 (system python3 + Pillow)
cd "$(dirname "$0")/.." && python3 scripts/animatic_v3.py
