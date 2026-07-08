import feedparser

RSS_URL = "https://news.google.com/rss/search?q=(AI%20OR%20%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5)%20(%EC%83%9D%EC%84%B1%ED%98%95AI%20OR%20ChatGPT%20OR%20Claude%20OR%20Gemini%20OR%20AI%EB%8F%84%EA%B5%AC)%20when:1d&hl=ko&gl=KR&ceid=KR:ko"

BLOCK_WORDS = ["월드컵", "축구", "야구", "농구", "스포츠", "Vietnam.vn"]

def get_news():
    feed = feedparser.parse(RSS_URL)
    items = []

    for entry in feed.entries:
        title = entry.title
        summary = getattr(entry, "summary", "")

        if any(word in title or word in summary for word in BLOCK_WORDS):
            continue

        items.append({
            "title": title,
            "link": entry.link,
            "summary": summary
        })

        if len(items) >= 5:
            break

    return items
