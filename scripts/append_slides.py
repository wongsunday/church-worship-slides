#!/usr/bin/env python3
"""
append_slides.py  –  Append a new song's slides to an existing worship PPTX.

Usage:
  python append_slides.py \
    --existing  WorshipSet.pptx \
    --lyrics    new_song/lyrics.json \
    --bg        new_song/background.jpg \
    --output    WorshipSet_updated.pptx \
    [--overlay-color  "0,0,0"] \
    [--overlay-alpha  185] \
    [--font-size      0] \
    [--delivery-mode  standard]

The script:
  1. Opens the existing PPTX and counts its current slides.
  2. Renders the new song's slides using the same pipeline as render_slides.py.
  3. Appends them to the existing presentation and saves to --output.
     (--output may be the same path as --existing to overwrite in-place.)

Slide indices in the new song's lyrics.json are automatically offset so they
do not collide with existing slide image filenames in _slide_imgs/.
"""

import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches

# ── Import shared helpers from render_slides in the same directory ────────────
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from render_slides import (
    validate_background,
    auto_font_size,
    render_slide,
    DELIVERY_QUALITY,
)


def parse_color(s):
    parts = [int(x.strip()) for x in s.split(",")]
    assert len(parts) == 3 and all(0 <= p <= 255 for p in parts)
    return tuple(parts)


def main():
    p = argparse.ArgumentParser(
        description="Append a new song's slides to an existing worship PPTX"
    )
    p.add_argument("--existing",       required=True,  help="Path to existing .pptx")
    p.add_argument("--lyrics",         required=True,  help="Path to new song lyrics JSON")
    p.add_argument("--bg",             required=True,  help="Path to background image")
    p.add_argument("--output",         required=True,  help="Output .pptx path (may equal --existing)")
    p.add_argument("--overlay-color",  default="0,0,0")
    p.add_argument("--overlay-alpha",  type=int, default=185)
    p.add_argument("--font-size",      type=int, default=0)
    p.add_argument("--delivery-mode",  default="standard",
                   choices=list(DELIVERY_QUALITY.keys()))
    args = p.parse_args()

    jpeg_quality = DELIVERY_QUALITY[args.delivery_mode]
    overlay_rgb  = parse_color(args.overlay_color)

    # Load existing presentation
    prs = Presentation(args.existing)
    existing_count = len(prs.slides)
    print(f"Existing PPTX: {existing_count} slide(s)  →  appending new song…")

    # Validate background
    bg_img = validate_background(args.bg)

    # Load and prepare new lyrics
    with open(args.lyrics, "r", encoding="utf-8") as f:
        lyrics_data = json.load(f)

    all_lines = [l for s in lyrics_data for l in s["text"].split("\n")]
    font, used_size = auto_font_size(all_lines, args.font_size)
    print(f"Font: {used_size}px  |  overlay: rgb{overlay_rgb} alpha={args.overlay_alpha}  |  JPEG quality: {jpeg_quality}")

    # Use a shared _slide_imgs directory next to the output file
    tmp_dir = os.path.join(os.path.dirname(os.path.abspath(args.output)), "_slide_imgs")
    os.makedirs(tmp_dir, exist_ok=True)

    for slide in lyrics_data:
        # Offset filename index to avoid overwriting existing slide images
        file_index = existing_count + slide["index"]
        img_path   = os.path.join(tmp_dir, f"slide_{file_index:02d}.jpg")

        render_slide(slide["text"], bg_img, font,
                     overlay_rgb, args.overlay_alpha).save(
                         img_path, "JPEG", quality=jpeg_quality, optimize=True)

        sl = prs.slides.add_slide(prs.slide_layouts[6])
        sl.shapes.add_picture(img_path, 0, 0,
                              width=prs.slide_width, height=prs.slide_height)
        size_kb = os.path.getsize(img_path) // 1024
        print(f"  Appended slide {file_index:02d}: {size_kb} KB")

    prs.save(args.output)
    total = len(prs.slides)
    final_size = os.path.getsize(args.output)
    print(f"Saved: {args.output}  ({total} slides total, {final_size // 1024} KB)")


if __name__ == "__main__":
    main()
