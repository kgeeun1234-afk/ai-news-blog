import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

def publish_post(title, content):
    endpoint = f"{WP_URL}/wp-json/wp/v2/posts"

    data = {
        "title": title,
        "content": content,
        "status": "draft"
    }

    r = requests.post(
        endpoint,
        json=data,
        auth=HTTPBasicAuth(WP_USER, WP_APP_PASSWORD),
        timeout=30
    )

    if r.status_code not in [200, 201]:
        raise Exception(f"WordPress 오류: {r.status_code} {r.text}")

    return r.json()
