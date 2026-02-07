#!/usr/bin/env python3
"""
Extract the idle squirrel (wagging tail) frames from the sprite sheet for the fight scene.

Sprite sheet layout: 256x192, 32x32 per frame, 8 columns x 6 rows.
Row 5 (0-indexed row 4, y=128–159) = 4 frames of squirrel sitting and wagging tail.

Usage:
  python3 extract_idle_squirrel.py "Squirrel Sprite Sheet.png"
  python3 extract_idle_squirrel.py "Squirrel Sprite Sheet.png" --out idle.txt
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except Exception as exc:
    raise SystemExit(
        "Pillow is required. Install with: python3 -m pip install pillow"
    ) from exc


def rgba_to_hex(rgba: tuple[int, int, int, int]) -> str:
    r, g, b, _ = rgba
    return f"#{r:02x}{g:02x}{b:02x}"


def extract_frame(
    img: Image.Image, fx: int, fy: int, fw: int, fh: int, alpha_min: int
) -> list[list]:
    out: list[list] = []
    for y in range(fh):
        for x in range(fw):
            r, g, b, a = img.getpixel((fx + x, fy + y))
            if a >= alpha_min:
                out.append([x, y, rgba_to_hex((r, g, b, a))])
    return out


def group_by_color(pixels: list[list]) -> dict[str, list[list[int]]]:
    grouped: dict[str, list[list[int]]] = {}
    for x, y, col in pixels:
        grouped.setdefault(col, []).append([x, y])
    return grouped


# Idle row (wagging tail): row index 4, y = 128..159; 4 frames at x = 0, 32, 64, 96
FRAME_W = 32
FRAME_H = 32
SHEET_COLS = 8
IDLE_ROW = 4
IDLE_FRAME_COUNT = 4


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extract idle (wagging tail) squirrel frames for the fight scene."
    )
    ap.add_argument("sheet", type=Path, help="Path to Squirrel Sprite Sheet.png")
    ap.add_argument("--alpha-min", type=int, default=10, help="Alpha cutoff (0–255)")
    ap.add_argument("--out", type=Path, default=Path("idle.txt"), help="Output JSON file")
    ap.add_argument("--compact", action="store_true", help="Compact JSON (no whitespace)")
    args = ap.parse_args()

    img = Image.open(args.sheet).convert("RGBA")
    if img.width < FRAME_W * IDLE_FRAME_COUNT or img.height < FRAME_H * (IDLE_ROW + 1):
        raise SystemExit(
            f"Sheet too small: need at least {FRAME_W * IDLE_FRAME_COUNT}x{FRAME_H * (IDLE_ROW + 1)}"
        )

    payload = []
    for i in range(IDLE_FRAME_COUNT):
        fx = i * FRAME_W
        fy = IDLE_ROW * FRAME_H
        pixels = extract_frame(img, fx, fy, FRAME_W, FRAME_H, args.alpha_min)
        payload.append(group_by_color(pixels))

    out_text = (
        json.dumps(payload, separators=(",", ":"))
        if args.compact
        else json.dumps(payload, indent=2)
    )
    args.out.write_text(out_text)
    print(f"Wrote {len(payload)} idle frames to {args.out}")


if __name__ == "__main__":
    main()
