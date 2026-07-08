import subprocess
from pathlib import Path
from datetime import datetime

from news import get_news
from writer import write_article


def extract_title(article):
    lines = article.splitlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            return line.replace("제목:", "").strip()
    return "오늘의_AI_뉴스_정리"


import re

def safe_filename(text):
    # Windows에서 사용할 수 없는 문자 제거
    text = re.sub(r'[\\/:*?"<>|]', "", text)

    # 공백을 '_'로 변경
    text = re.sub(r"\s+", "_", text.strip())

    # 연속된 '_' 정리
    text = re.sub(r"_+", "_", text)

    # 파일명을 30자로 제한
    return text[:30] or "article"


def main():
    print("뉴스 수집 중...")
    news_items = get_news()

    if not news_items:
        print("뉴스가 없습니다.")
        return

    print("AI 글 생성 중...")
    article = write_article(news_items)

    title = extract_title(article)
    filename = safe_filename(title)

    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path("articles")
    out_dir.mkdir(exist_ok=True)

    html_path = out_dir / f"{today}_{filename}.html"
    md_path = out_dir / f"{today}_{filename}.md"

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{title}</title>
</head>
<body>
<article>
{article.replace(chr(10), "<br>")}
</article>
</body>
</html>
"""

    html_path.write_text(html, encoding="utf-8")
    md_path.write_text(article, encoding="utf-8")

    print("저장 완료")

    print("사이트 갱신 중...")
    subprocess.run(["python3", "build_site.py"], check=True)
    print("사이트 갱신 완료")
    print("HTML:", html_path)
    print("MD:", md_path)


if __name__ == "__main__":
    main()
