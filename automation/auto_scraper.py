import json
import datetime
from html_scraper import scrape_saramin, scrape_incruit, scrape_jobkorea, scrape_wevity, scrape_campuspick

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"lastUpdated": None, "jobs": [], "contests": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("==================================================")
    print("📡 HTML 기반 스크래핑 시작!")

    data = load_data()

    all_jobs = []
    all_contests = []

    # 🧹 기존 데이터 제거 (항상 최신 목록으로 유지)
    print("🧹 기존 데이터 초기화")

    # 📌 각 사이트에서 데이터 수집
    print("🔎 사람인 채용 수집 중...")
    all_jobs += scrape_saramin()

    print("🔎 인크루트 채용 수집 중...")
    all_jobs += scrape_incruit()

    print("🔎 잡코리아 채용 수집 중...")
    all_jobs += scrape_jobkorea()

    print("🔎 위비티 공모전 수집 중...")
    all_contests += scrape_wevity()

    print("🔎 캠퍼스픽 공모전 수집 중...")
    all_contests += scrape_campuspick()

    # 🔄 JSON 업데이트
    data["lastUpdated"] = datetime.datetime.now().isoformat()
    data["jobs"] = all_jobs
    data["contests"] = all_contests

    save_data(data)

    print("✅ 완료! data.json 업데이트됨.")
    print(f"   - 채용: {len(all_jobs)}개")
    print(f"   - 공모전: {len(all_contests)}개")

if __name__ == "__main__":
    main()


