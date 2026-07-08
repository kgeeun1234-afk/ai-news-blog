from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI()

def write_article(news_items):
    source_text = "\n".join([f"- {n['title']}\n{n['link']}" for n in news_items])

    prompt = f"""
다음 AI 뉴스 목록을 바탕으로 한국어 블로그 글을 작성해줘.

조건:
- 제목 1개
- 본문 1200자 이상
- 소제목 포함
- 뉴스 링크 출처 포함
- 애드센스 승인에 유리하게 복붙 느낌 없이 자연스럽게 작성
- 마지막에 해시태그 5개

뉴스:
{source_text}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
