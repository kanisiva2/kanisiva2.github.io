#!/usr/bin/env python3
"""
Extract pixel coordinates/colors from a sprite sheet.

Usage:
  python3 extract_squirrel_pixels.py "Squirrel Sprite Sheet.png" --frame 0
  python3 extract_squirrel_pixels.py "Squirrel Sprite Sheet.png" --frames 0-5
  python3 extract_squirrel_pixels.py "Squirrel Sprite Sheet.png" --frames 12-19 --out squirrel_move.json --compact
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except Exception as exc:  # pragma: no cover - run-time hint
    raise SystemExit(
        "Pillow is required. Install with: python3 -m pip install pillow"
    ) from exc


def rgba_to_hex(rgba: tuple[int, int, int, int]) -> str:
    r, g, b, _ = rgba
    return f"#{r:02x}{g:02x}{b:02x}"


def extract_frame(img: Image.Image, fx: int, fy: int, fw: int, fh: int, alpha_min: int) -> list[list]:
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


def parse_frames(spec: str) -> list[int]:
    frames: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            start, end = int(a), int(b)
            step = 1 if end >= start else -1
            frames.extend(list(range(start, end + step, step)))
        else:
            frames.append(int(part))
    if not frames:
        raise SystemExit("No frames parsed from --frames.")
    return frames


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet", type=Path, help="Path to sprite sheet PNG")
    ap.add_argument("--frame", type=int, default=None, help="Single frame index (0-based)")
    ap.add_argument("--frames", type=str, default=None, help="Frame list/range, e.g. 0-5 or 0,2,4")
    ap.add_argument("--frame-w", type=int, default=32, help="Frame width in px")
    ap.add_argument("--frame-h", type=int, default=32, help="Frame height in px")
    ap.add_argument("--columns", type=int, default=0, help="Columns in sheet (0=auto)")
    ap.add_argument("--alpha-min", type=int, default=10, help="Alpha cutoff (0-255)")
    ap.add_argument("--group-by-color", action="store_true", help="Output color->coords map")
    ap.add_argument("--compact", action="store_true", help="Compact JSON (no whitespace)")
    ap.add_argument("--out", type=Path, default=None, help="Write output to file")
    args = ap.parse_args()

    img = Image.open(args.sheet).convert("RGBA")
    fw, fh = args.frame_w, args.frame_h
    cols = args.columns or (img.width // fw)
    if cols <= 0:
        raise SystemExit("Could not infer columns. Pass --columns.")
    if args.frames and args.frame is not None:
        raise SystemExit("Use only one of --frame or --frames.")
    if args.frames:
        frame_list = parse_frames(args.frames)
    else:
        frame_list = [args.frame if args.frame is not None else 0]

    payload = []
    for fr in frame_list:
        fx = (fr % cols) * fw
        fy = (fr // cols) * fh
        if fx + fw > img.width or fy + fh > img.height:
            raise SystemExit("Frame is outside the sheet. Check --frame/--frames/--columns.")
        pixels = extract_frame(img, fx, fy, fw, fh, args.alpha_min)
        payload.append(group_by_color(pixels) if args.group_by_color else pixels)

    if args.compact:
        out_text = json.dumps(payload, separators=(",", ":"))
    else:
        out_text = json.dumps(payload, indent=2)
    if args.out:
        args.out.write_text(out_text)
    else:
        print(out_text)


if __name__ == "__main__":
    main()
