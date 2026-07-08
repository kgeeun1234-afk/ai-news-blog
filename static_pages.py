from pathlib import Path
from datetime import datetime

from build_site import write_robots_txt

BASE = Path(__file__).resolve().parent
ARTICLES = BASE / "articles"

def page(filename, title, body):
    ARTICLES.mkdir(exist_ok=True)
    (ARTICLES / filename).write_text(f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="style.css">
<meta name="robots" content="index,follow">
</head>
<body>
<header>
  <h1>{title}</h1>
</header>
<main>
  <article class="card">
    {body}
  </article>
</main>
<footer>
  <a href="index.html">홈으로</a> · © {datetime.now().year} AI 뉴스 블로그
</footer>
</body>
</html>
""", encoding="utf-8")

def main():
    page("about.html", "소개", """
<h2>AI 뉴스 블로그 소개</h2>
<p>AI 뉴스 블로그는 인공지능, 생성형 AI, 자동화, 디지털 기술 관련 소식을 정리하는 정보 사이트입니다.</p>
<p>독자가 빠르게 핵심 흐름을 이해할 수 있도록 주요 뉴스를 요약하고 정리합니다.</p>
""")

    page("privacy.html", "개인정보처리방침", """
<h2>개인정보처리방침</h2>
<p>본 사이트는 기본적으로 방문자의 개인정보를 직접 수집하지 않습니다.</p>
<p>향후 광고, 분석 도구 또는 문의 기능을 사용할 경우 관련 정책을 이 페이지에 추가로 고지합니다.</p>
""")

    page("contact.html", "문의", """
<h2>문의</h2>
<p>사이트 운영, 콘텐츠 수정 요청, 제휴 문의는 별도 문의 채널을 통해 접수할 수 있습니다.</p>
<p>문의 이메일은 추후 등록 예정입니다.</p>
""")

    page("404.html", "페이지를 찾을 수 없습니다", """
<h2>404</h2>
<p>요청하신 페이지를 찾을 수 없습니다.</p>
<p><a href="index.html">메인 페이지로 이동</a></p>
""")

    write_robots_txt()

    (ARTICLES / "ads.txt").write_text("""# Google AdSense 승인 후 아래 형식으로 교체
# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
""", encoding="utf-8")

    print("기본 페이지 생성 완료: about, privacy, contact, 404, robots, ads")

if __name__ == "__main__":
    main()
