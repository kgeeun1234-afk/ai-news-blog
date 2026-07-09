from pathlib import Path
import hashlib


def thumbnail_name(title: str) -> str:
    return hashlib.md5(title.encode("utf-8")).hexdigest()[:16] + ".svg"


def write_default_thumbnail(path: Path, title: str):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
<rect width="100%" height="100%" fill="#0f172a"/>
<text x="60" y="180"
      font-size="56"
      fill="white"
      font-family="Arial,sans-serif">AI NEWS</text>
<text x="60" y="280"
      font-size="36"
      fill="#cbd5e1"
      font-family="Arial,sans-serif">{title[:50]}</text>
</svg>"""
    path.write_text(svg, encoding="utf-8")


def write_all_thumbnails(articles_dir: Path, articles):
    image_dir = articles_dir / "images"
    image_dir.mkdir(exist_ok=True)

    for article in articles:
        title = article["title"]
        filename = thumbnail_name(title)
        article["thumbnail"] = f"images/{filename}"
        write_default_thumbnail(image_dir / filename, title)

