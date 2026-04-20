#!/usr/bin/env python3
"""
render_slides.py  –  Church Worship Slides Generator
Usage:
  python render_slides.py \
    --lyrics   lyrics.json \
    --bg       background.jpg \
    --output   Song_Title.pptx \
    [--overlay-color  "0,0,0"]      # R,G,B  default black
    [--overlay-alpha  185]           # 0-255  default 185 (~73%)
    [--font-size      0]             # px     default 0 (auto-scales)
    [--delivery-mode  standard]      # screen | standard | print

Resolution Policy:
  - Minimum accepted background: 1280x720 (exits with error if below)
  - 1280x720–1919x1079: accepted with upscale warning
  - 1920x1080–3839x2159: ideal, used as-is
  - 4K and above: downsampled to 3840x2160 before rendering

Delivery Modes (JPEG quality for embedded slide images):
  screen   = 75   (small file, web/email sharing)
  standard = 92   (default, balanced quality for church use)
  print    = 98   (archival / high-fidelity)

lyrics.json format:
  [
    {"index": 1, "text": "Line one\nLine two"},
    {"index": 2, "text": "Line three\nLine four\nLine five"}
  ]
"""

import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches

# ── Render Resolution (always Full HD internally) ─────────────────────────────
W, H           = 1920, 1080
LINE_GAP       = 24
PAD_H          = 80
PAD_V          = 45
BOX_RADIUS     = 18
SHADOW_OFFSET  = 4
MAX_FONT_SIZE  = 90
MIN_FONT_SIZE  = 48
MAX_LINE_WIDTH = int(W * 0.78)

# ── Resolution Policy ─────────────────────────────────────────────────────────
RES_MIN_W, RES_MIN_H       = 1280, 720    # hard minimum – reject below this
RES_WARN_W, RES_WARN_H     = 1920, 1080  # warn if below Full HD
RES_DOWNSAMPLE_W           = 3840        # downsample width if source exceeds 4K

# ── Delivery Mode → JPEG Quality ─────────────────────────────────────────────
DELIVERY_QUALITY = {
    "screen":   75,
    "standard": 92,
    "print":    98,
}

FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]


def validate_background(bg_path):
    """
    Validate and pre-process background image per resolution policy.
    Returns a PIL Image ready for rendering, or raises SystemExit on failure.
    """
    img = Image.open(bg_path).convert("RGBA")
    w, h = img.size

    if w < RES_MIN_W or h < RES_MIN_H:
        print(f"ERROR: Background image is too low-resolution ({w}x{h}). "
              f"Minimum required is {RES_MIN_W}x{RES_MIN_H}. "
              f"Please source a higher-resolution image.", file=sys.stderr)
        sys.exit(1)

    if w < RES_WARN_W or h < RES_WARN_H:
        print(f"WARNING: Background image ({w}x{h}) is below Full HD "
              f"({RES_WARN_W}x{RES_WARN_H}). Slides will be upscaled; "
              f"quality may be slightly reduced.")

    if w > RES_DOWNSAMPLE_W:
        scale = RES_DOWNSAMPLE_W / w
        new_w = RES_DOWNSAMPLE_W
        new_h = int(h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        print(f"INFO: Source image downsampled from {w}x{h} to {new_w}x{new_h} "
              f"(exceeds 4K cap).")

    return img


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def auto_font_size(lines, requested_size):
    """Scale font down if any line exceeds MAX_LINE_WIDTH."""
    size = requested_size if requested_size > 0 else MAX_FONT_SIZE
    while size >= MIN_FONT_SIZE:
        font = load_font(size)
        dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        widths = []
        for line in lines:
            x0, _, x1, _ = dummy.textbbox((0, 0), line, font=font)
            widths.append(x1 - x0)
        if max(widths) <= MAX_LINE_WIDTH:
            return font, size
        size -= 4
    return load_font(MIN_FONT_SIZE), MIN_FONT_SIZE


def measure_lines(draw, lines, font):
    ink_bboxes = []
    for line in lines:
        x0, y0, x1, y1 = draw.textbbox((0, 0), line, font=font)
        ink_bboxes.append((x1 - x0, y1 - y0, y0))
    max_ink_w   = max(b[0] for b in ink_bboxes)
    total_ink_h = sum(b[1] for b in ink_bboxes) + LINE_GAP * (len(lines) - 1)
    return max_ink_w, total_ink_h, ink_bboxes


def draw_rounded_rect(draw, x0, y0, x1, y1, r, fill):
    draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
    draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
    draw.ellipse([x0,     y0,     x0+2*r, y0+2*r], fill=fill)
    draw.ellipse([x1-2*r, y0,     x1,     y0+2*r], fill=fill)
    draw.ellipse([x0,     y1-2*r, x0+2*r, y1],     fill=fill)
    draw.ellipse([x1-2*r, y1-2*r, x1,     y1],     fill=fill)


def render_slide(text, bg_img, font, overlay_rgb, overlay_alpha):
    """Render a single slide at W×H using a pre-validated PIL Image as background."""
    bg = bg_img.copy()
    bg_r = bg.width / bg.height
    tgt_r = W / H
    if bg_r > tgt_r:
        nh = H; nw = int(nh * bg_r)
        bg = bg.resize((nw, nh), Image.Resampling.LANCZOS)
        bg = bg.crop(((nw - W) // 2, 0, (nw - W) // 2 + W, H))
    else:
        nw = W; nh = int(nw / bg_r)
        bg = bg.resize((nw, nh), Image.Resampling.LANCZOS)
        bg = bg.crop((0, (nh - H) // 2, W, (nh - H) // 2 + H))

    bg = Image.alpha_composite(bg, Image.new("RGBA", (W, H), (0, 0, 0, 50)))

    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = text.split("\n")
    max_ink_w, total_ink_h, ink_bboxes = measure_lines(dummy, lines, font)

    box_w  = max_ink_w + PAD_H * 2
    box_h  = total_ink_h + PAD_V * 2
    box_x0 = max(20, (W - box_w) // 2)
    box_y0 = max(30, int(H / 4 - box_h / 2))
    box_x1, box_y1 = box_x0 + box_w, box_y0 + box_h

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_rounded_rect(ImageDraw.Draw(ov),
                      box_x0, box_y0, box_x1, box_y1,
                      BOX_RADIUS,
                      (*overlay_rgb, overlay_alpha))
    bg = Image.alpha_composite(bg, ov)

    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td  = ImageDraw.Draw(txt)
    cur_y = box_y0 + PAD_V
    for (ink_w, ink_h, y0_off), line in zip(ink_bboxes, lines):
        x      = (W - ink_w) // 2
        draw_y = cur_y - y0_off
        td.text((x + SHADOW_OFFSET, draw_y + SHADOW_OFFSET),
                line, font=font, fill=(0, 0, 0, 200))
        td.text((x, draw_y), line, font=font, fill=(255, 255, 255, 255))
        cur_y += ink_h + LINE_GAP

    return Image.alpha_composite(bg, txt).convert("RGB")


def create_pptx(lyrics_data, bg_path, output_path,
                overlay_rgb, overlay_alpha, font_size, jpeg_quality):
    # Validate and pre-load background once
    bg_img = validate_background(bg_path)

    all_lines = [l for s in lyrics_data for l in s["text"].split("\n")]
    font, used_size = auto_font_size(all_lines, font_size)
    print(f"Render: {W}x{H}  |  font: {used_size}px  |  "
          f"overlay: rgb{overlay_rgb} alpha={overlay_alpha}  |  "
          f"JPEG quality: {jpeg_quality}")

    tmp_dir = os.path.join(os.path.dirname(output_path), "_slide_imgs")
    os.makedirs(tmp_dir, exist_ok=True)

    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)

    for slide in lyrics_data:
        img_path = os.path.join(tmp_dir, f"slide_{slide['index']:02d}.jpg")
        render_slide(slide["text"], bg_img, font,
                     overlay_rgb, overlay_alpha).save(
                         img_path, "JPEG", quality=jpeg_quality, optimize=True)
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        sl.shapes.add_picture(img_path, 0, 0,
                              width=prs.slide_width, height=prs.slide_height)
        size_kb = os.path.getsize(img_path) // 1024
        print(f"  Slide {slide['index']:02d}: {size_kb} KB")

    prs.save(output_path)
    final_size = os.path.getsize(output_path)
    print(f"Saved: {output_path}  ({final_size // 1024} KB)")


def parse_color(s):
    parts = [int(x.strip()) for x in s.split(",")]
    assert len(parts) == 3 and all(0 <= p <= 255 for p in parts)
    return tuple(parts)


def main():
    p = argparse.ArgumentParser(description="Generate worship slides PPTX")
    p.add_argument("--lyrics",         required=True,  help="Path to lyrics JSON")
    p.add_argument("--bg",             required=True,  help="Path to background image")
    p.add_argument("--output",         required=True,  help="Output .pptx path")
    p.add_argument("--overlay-color",  default="0,0,0",
                   help="Overlay RGB e.g. '0,0,0' for black")
    p.add_argument("--overlay-alpha",  type=int, default=185,
                   help="Overlay opacity 0-255 (default 185 ≈ 73%%)")
    p.add_argument("--font-size",      type=int, default=0,
                   help="Font size in px (0 = auto-scale to fit)")
    p.add_argument("--delivery-mode",  default="standard",
                   choices=list(DELIVERY_QUALITY.keys()),
                   help="Output quality: screen (75), standard (92), print (98)")
    args = p.parse_args()

    jpeg_quality = DELIVERY_QUALITY[args.delivery_mode]

    with open(args.lyrics, "r", encoding="utf-8") as f:
        lyrics_data = json.load(f)

    create_pptx(
        lyrics_data,
        bg_path       = args.bg,
        output_path   = args.output,
        overlay_rgb   = parse_color(args.overlay_color),
        overlay_alpha = args.overlay_alpha,
        font_size     = args.font_size,
        jpeg_quality  = jpeg_quality,
    )


if __name__ == "__main__":
    main()
