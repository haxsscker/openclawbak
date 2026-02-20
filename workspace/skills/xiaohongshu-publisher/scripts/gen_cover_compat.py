#!/usr/bin/env python3
"""
Generate 小红书 cover image (1080x1440) with gradient background and CJK text.
Compatible version for older Pillow (5.1.1).
"""
import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

W, H = 1080, 1440

GRADIENTS = {
    "purple": ((102, 126, 234), (240, 147, 251)),
    "blue":   ((30, 60, 180),   (100, 180, 255)),
    "green":  ((34, 139, 87),   (144, 238, 144)),
    "orange": ((255, 140, 0),   (255, 200, 100)),
    "dark":   ((30, 30, 60),    (80, 80, 120)),
}

# Font paths for our system
CJK_BOLD_FONT = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"
CJK_REG_FONT = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc"

def draw_gradient(draw, color_top, color_bot):
    for y in range(H):
        r = y / H
        c = tuple(int(color_top[i] + (color_bot[i] - color_top[i]) * r) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)

def create_cover(title, subtitle=None, tags=None, badge="OpenClaw", gradient="purple", output="cover.png"):
    # Create base image
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    color_top, color_bot = GRADIENTS[gradient]
    draw_gradient(draw, color_top, color_bot)
    
    # Title font
    try:
        font_huge = ImageFont.truetype(CJK_BOLD_FONT, 82)
        font_med = ImageFont.truetype(CJK_BOLD_FONT, 48)
        font_small = ImageFont.truetype(CJK_BOLD_FONT, 34)
    except OSError:
        print(f"Error: Cannot load font files. Check if {CJK_BOLD_FONT} exists.")
        sys.exit(1)
    
    # Draw title
    tw, th = draw.textsize(title, font=font_huge)
    x = (W - tw) // 2
    y = H // 2 - 100
    draw.text((x, y), title, fill="white", font=font_huge)
    
    # Draw subtitle
    if subtitle:
        sw, sh = draw.textsize(subtitle, font=font_med)
        sx = (W - sw) // 2
        sy = y + th + 30
        draw.text((sx, sy), subtitle, fill="white", font=font_med)
    
    # Draw badge
    bw, bh = draw.textsize(badge, font=font_small)
    bx = W - bw - 50
    by = 60
    draw.rectangle([bx-10, by-5, bx+bw+10, by+bh+5], fill=(255, 255, 255, 128))
    draw.text((bx, by), badge, fill="white", font=font_small)
    
    # Save
    img.save(output, "PNG", quality=95)
    print(f"Cover saved: {output}")

def main():
    parser = argparse.ArgumentParser(description="Generate 小红书 cover image (compatible)")
    parser.add_argument("--title", required=True, help="Main title text")
    parser.add_argument("--subtitle", default=None, help="Subtitle text")
    parser.add_argument("--tags", default=None, help="Comma-separated feature tags")
    parser.add_argument("--badge", default="OpenClaw", help="Badge text (top-right)")
    parser.add_argument("--output", default="cover.png", help="Output file path")
    parser.add_argument("--gradient", default="purple", choices=GRADIENTS.keys(),
                        help="Color scheme")
    args = parser.parse_args()
    
    create_cover(
        title=args.title,
        subtitle=args.subtitle,
        tags=args.tags,
        badge=args.badge,
        gradient=args.gradient,
        output=args.output
    )

if __name__ == "__main__":
    main()