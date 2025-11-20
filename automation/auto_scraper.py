import json
import random
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# -----------------------------------
# 랜덤 User-Agent 생성
# -----------------------------------
def get_random_headers():
    user_agents = [
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110 Safari/537.36",
        # Mobile
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15 Mobile Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103 Mobile Safari/537.36",
    ]
    return {"User-Agent": random.choice(user_agents)}


# -----------------------------------
# 안전한 요청 (Retry 포함)
# -----------------------------------
def safe_request(url, retries=3, delay=1):
    for attempt in range(retries):
        try:
            res = requests.get(url, headers=get_random_headers(), timeout=10)
            if res.status_code == 200:
                return res
        except Exception:
            time.sleep(delay)
    return None


# -----------------------------------
# 링크 리스트 (취준 + 공모전)
# -----------------------------------
JOB_LINKS = [
    "https://www.saramin.co.kr/zf_user/jobs/hot100",
    "https://job.incruit.com/entry/",
    "https://www.jobkorea.co.kr/theme/entry-level-internship",
]

CONTEST_LINKS = [
    "https://www.wevity.com/?c=find",
    "https://www.campuspick.com/contest",
]


# -----------------------------------
# 공고 파싱 함수 (사이트 공통용)
# -----------------------------------
def parse_job_list(url):
    results = []
    res = safe_request(url)
    if not res:
        print(f"[ERROR] Failed to fetch: {url}")
        return results

    soup = BeautifulSoup(res.text, "html.parser")

    # 매우 단순한 범용 파서 (모든 사이트 호환)
    items = soup.find_all(["a", "div"], limit=25)

    for item in items:
        title = (item.text or "").strip().replace("\n", " ")
        if len(title) < 5:
            continue

        href = item.get("href")
        if href and href.startswith("/"):
            href = url.split("/")[0] + "//" + url.split("/")[2] + href

        if not href or "javascript" in href:
            continue

        results.append({"title": title, "url": href})

    return results


# -----------------------------------
# 전체 수집
# -----------------------------------
def scrape_all():
    final_data = {"jobs": [], "contests": []}

    for url in JOB_LINKS:
        print(f"[JOB] Scraping: {url}")
        final_data["jobs"].extend(parse_job_list(url))
        time.sleep(1)

    for url in CONTEST_LINKS:
        print(f"[CONTEST] Scraping: {url}")
        final_data["contests"].extend(parse_job_list(url))
        time.sleep(1)

    return final_data


# -----------------------------------
# 저장
# -----------------------------------
def save_to_json(data):
    output = {
        "lastUpdated": datetime.now().isoformat(),
        "jobs": data["jobs"],
        "contests": data["contests"]
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("[SAVE] data.json updated")


# -----------------------------------
# 메인 실행
# -----------------------------------
if __name__ == "__main__":
    print("=== Auto Scraper Started ===")
    data = scrape_all()
    save_to_json(data)
    print("=== Done ===")



