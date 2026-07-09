from pathlib import Path
from thumbnail import make_thumbnail
from datetime import datetime
import html
import re

BASE = Path(__file__).resolve().parent
ARTICLES = BASE / "articles"
SITE_TITLE = "AI 뉴스 블로그"
SITE_URL = "https://kgeeun1234-afk.github.io/ai-news-blog"
SITE_DESCRIPTION = "AI 뉴스와 생성형 AI 트렌드를 자동으로 정리하는 뉴스 블로그"
GOOGLE_SITE_VERIFICATION = "e1hYipw5-poqCtw-1dqegl9XVNq-MH-S0lbprYt_hDU"

EXCLUDE_FROM_INDEX = {
    "index.html",
    "about.html",
    "privacy.html",
    "contact.html",
    "404.html",
}

STATIC_SITEMAP_PAGES = ["about.html", "privacy.html", "contact.html"]

PAGE_META = {
    "about.html": ("소개", "AI 뉴스 블로그 소개 페이지입니다."),
    "privacy.html": ("개인정보처리방침", "AI 뉴스 블로그 개인정보처리방침입니다."),
    "contact.html": ("문의", "AI 뉴스 블로그 문의 페이지입니다."),
    "404.html": ("페이지를 찾을 수 없습니다", "요청하신 페이지를 찾을 수 없습니다."),
}


def clean_title(filename):
    name = Path(filename).stem
    name = re.sub(r"^\d{4}-\d{2}-\d{2}_?", "", name)
    return name.replace("_", " ").strip()


def get_date(filename):
    m = re.match(r"(\d{4}-\d{2}-\d{2})", Path(filename).name)
    return m.group(1) if m else ""


def extract_summary(article_path):
    md_path = article_path.with_suffix(".md")
    if md_path.exists():
        for line in md_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line == "---":
                continue
            return line

    content = article_path.read_text(encoding="utf-8")
    match = re.search(r"<article>(.*?)</article>", content, re.DOTALL | re.IGNORECASE)
    if match:
        body = re.sub(r"<br\s*/?>", "\n", match.group(1), flags=re.IGNORECASE)
        body = re.sub(r"<[^>]+>", "", body)
        for line in body.splitlines():
            line = line.strip().lstrip("#").strip()
            if line and line != "---":
                return line

    return f"{clean_title(article_path.name)}에 관한 AI 뉴스 요약입니다."


def page_loc(filename):
    if SITE_URL:
        return f"{SITE_URL.rstrip('/')}/{filename}"
    return f"/{filename}"


def sitemap_loc():
    if SITE_URL:
        return f"{SITE_URL.rstrip('/')}/sitemap.xml"
    return "/sitemap.xml"


def write_robots_txt():
    (ARTICLES / "robots.txt").write_text(
        f"""User-agent: *
Allow: /

Sitemap: {sitemap_loc()}
""",
        encoding="utf-8",
    )


def footer_html():
    year = datetime.now().year
    return f"""
<footer class="site-footer">
  <nav class="footer-nav">
    <a href="index.html">Home</a> |
    <a href="about.html">About</a> |
    <a href="privacy.html">Privacy</a> |
    <a href="contact.html">Contact</a>
  </nav>
  <p>© {year} AI 뉴스 블로그</p>
</footer>"""


def meta_tags(title, description, url, og_type="article", robots="index,follow"):
    esc_title = html.escape(title)
    esc_desc = html.escape(description)
    esc_url = html.escape(url)
    return f"""<meta name="description" content="{esc_desc}">
<meta name="robots" content="{robots}">
<meta property="og:title" content="{esc_title}">
<meta property="og:description" content="{esc_desc}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{esc_url}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc_title}">
<meta name="twitter:description" content="{esc_desc}">"""


def render_head(title, description, url, og_type="article", robots="index,follow"):
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">
{meta_tags(title, description, url, og_type, robots)}
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>"""


def extract_body(content):
    match = re.search(r"<body[^>]*>(.*)</body>", content, re.DOTALL | re.IGNORECASE)
    if not match:
        return content
    body = match.group(1)
    body = re.sub(
        r"<footer[^>]*>.*?</footer>",
        "",
        body,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return body.strip()


def page_info(filename):
    if filename in PAGE_META:
        title, description = PAGE_META[filename]
        og_type = "website"
        robots = "noindex,follow" if filename == "404.html" else "index,follow"
        return title, description, og_type, robots

    title = clean_title(filename)
    description = f"{title} - AI 뉴스 요약"
    return title, description, "article", "index,follow"


def enhance_html_page(path):
    content = path.read_text(encoding="utf-8")
    filename = path.name
    title, description, og_type, robots = page_info(filename)
    body = extract_body(content)

    path.write_text(
        f"""<!doctype html>
<html lang="ko">
{render_head(title, description, page_loc(filename), og_type, robots)}
<body>
{body}
{footer_html()}
</body>
</html>
""",
        encoding="utf-8",
    )


def is_article(filename):
    return filename.endswith(".html") and filename not in EXCLUDE_FROM_INDEX


def main():
    ARTICLES.mkdir(exist_ok=True)

    article_files = sorted(
        [p for p in ARTICLES.glob("*.html") if is_article(p.name)],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    cards = []
    sitemap_urls = []
    rss_items = []

    for p in article_files:
        title = clean_title(p.name)
        date = get_date(p.name)
        link = p.name
        summary = extract_summary(p)
        img_name = p.stem + ".jpg"
        img_path = Path("articles/images") / img_name
        make_thumbnail(title, str(img_path))
        thumb = "images/" + img_name

        cards.append(f"""
        <article class="card">
          <img class="card-thumb" src="{html.escape(thumb)}" alt="AI 뉴스 썸네일">
          <div class="date">{html.escape(date)}</div>
          <h2>{html.escape(title)}</h2>
          <p class="card-summary">{html.escape(summary)}</p>
          <a href="{html.escape(link)}">기사 읽기 →</a>
        </article>
        """)

        sitemap_urls.append(f"<url><loc>{page_loc(link)}</loc></url>")
        rss_items.append(f"""
        <item>
          <title>{html.escape(title)}</title>
          <link>{page_loc(link)}</link>
          <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0900')}</pubDate>
        </item>
        """)

    for page in STATIC_SITEMAP_PAGES:
        sitemap_urls.append(f"<url><loc>{page_loc(page)}</loc></url>")

    (ARTICLES / "style.css").write_text("""
body{font-family:Arial,'Noto Sans KR',sans-serif;margin:0;background:#f5f6f8;color:#222}
header{background:#111827;color:white;padding:32px 20px;text-align:center}
main{max-width:900px;margin:30px auto;padding:0 16px}
.card{background:white;margin:16px 0;padding:22px;border-radius:14px;box-shadow:0 2px 10px rgba(0,0,0,.08)}
.card-thumb{width:100%;max-width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:10px;margin:0 0 14px;display:block}
.card h2{font-size:22px;margin:8px 0 14px;line-height:1.35}
.card-summary{color:#4b5563;font-size:15px;line-height:1.5;margin:0 0 14px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card a{color:#2563eb;text-decoration:none;font-weight:bold}
.date{color:#6b7280;font-size:14px}
footer.site-footer{text-align:center;color:#777;padding:30px}
.footer-nav{margin-bottom:8px}
.footer-nav a{color:#2563eb;text-decoration:none;margin:0 4px}
""", encoding="utf-8")

    index_description = SITE_DESCRIPTION
    (ARTICLES / "index.html").write_text(
        f"""<!doctype html>
<html lang="ko">
{render_head(SITE_TITLE, index_description, page_loc("index.html"), "website")}
<body>
<header>
  <h1>{SITE_TITLE}</h1>
  <p>매일 업데이트되는 AI 뉴스 요약</p>
</header>
<main>
{''.join(cards) if cards else '<p>아직 등록된 기사가 없습니다.</p>'}
</main>
{footer_html()}
</body>
</html>
""",
        encoding="utf-8",
    )

    (ARTICLES / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>{page_loc('index.html')}</loc></url>
{''.join(sitemap_urls)}
</urlset>
""",
        encoding="utf-8",
    )

    (ARTICLES / "rss.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{SITE_TITLE}</title>
<link>{SITE_URL or page_loc('index.html')}</link>
<description>AI 뉴스 자동 요약 블로그</description>
{''.join(rss_items)}
</channel>
</rss>
""",
        encoding="utf-8",
    )

    for path in ARTICLES.glob("*.html"):
        if path.name != "index.html":
            enhance_html_page(path)

    write_robots_txt()

    print("사이트 생성 완료: articles/index.html, sitemap.xml, rss.xml, style.css, robots.txt")
    print(f"기사 {len(article_files)}건, 정적 페이지 메타/푸터 갱신 완료")


if __name__ == "__main__":
    main()

