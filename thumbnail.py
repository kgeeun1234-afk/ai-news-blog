from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

OUT_DIR = Path("articles/images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1280
HEIGHT = 720

COLORS = {
    "OpenAI": (16, 45, 90),
    "Google": (20, 80, 180),
    "Gemini": (80, 40, 170),
    "Microsoft": (0, 120, 215),
    "NVIDIA": (30, 120, 30),
    "default": (30, 60, 140),
}


def color_from_title(title):
    for k, v in COLORS.items():
        if k.lower() in title.lower():
            return v
    return COLORS["default"]


def make_thumbnail(title, outfile):
    img = Image.new("RGB", (WIDTH, HEIGHT), color_from_title(title))

    d = ImageDraw.Draw(img)

    try:
        font_big = ImageFont.truetype(
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", 72
        )
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", 38
        )
    except OSError:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    d.text((70, 60), "AI NEWS", fill="white", font=font_small)

    lines = textwrap.wrap(title, width=20)

    y = 180

    for line in lines[:4]:
        d.text((70, y), line, fill="white", font=font_big)
        y += 90

    d.text((70, 620), "AI NEWS BLOG", fill=(220, 220, 220), font=font_small)

    img.save(outfile, quality=95)
