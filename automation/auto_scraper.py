import requests
from bs4 import BeautifulSoup
import json
import datetime

# -------------------------------
# 키워드 사전
# -------------------------------
KEYWORDS = {
    "무역": ["무역", "수출", "수입", "통관", "관세", "FTA", "HS코드", "KOTRA", "무역협회", "관세청",
            "무역보험공사", "수출입은행", "해외영업", "글로벌영업", "국제영업", "바이어", "소싱",
            "SCM", "물류", "포워딩", "해운", "항공", "영업", "검역", "중국무역", "미국수출", "유럽",
            "동남아", "RCEP", "e-커머스", "크로스보더", "국제배송", "아마존"],
    "경제": ["경제", "금융", "은행", "증권", "자산운용", "투자", "펀드", "IB", "애널리스트", "리서치",
            "재무", "회계", "세무", "KB", "신한", "하나", "우리", "NH농협", "IBK기업", "KDB산업",
            "미래에셋", "삼성증권", "한국투자", "한국거래소", "한국은행", "PB", "WM", "자산관리",
            "신용평가", "심사역", "여신", "금융일반", "채권", "주식", "외환", "리스크관리", "경영기획",
            "전략기획", "IR", "M&A", "CPA", "AICPA", "CFA", "FRM", "CFP", "ESG", "핀테크",
            "디지털금융", "블록체인"],
    "정치외교": ["외교", "국제관계", "정치", "국제정치", "안보", "통일", "외교관", "행정고시",
              "외무고시", "5급공채", "외교부", "통일부", "국방부", "청와대", "국회", "UN", "유엔",
              "UNDP", "UNESCO", "WHO", "UNICEF", "NATO", "EU", "ASEAN", "APEC", "G20",
              "OECD", "세계은행", "IMF", "WTO", "NGO", "INGO", "옥스팜", "월드비전", "굿네이버스",
              "국경없는의사회", "KOICA", "월드프렌즈", "공공외교", "다자외교", "경제외교", "문화외교",
              "개발협력", "ODA", "평화", "갈등해결", "인권", "정책연구", "싱크탱크", "북핵", "한반도",
              "동북아", "중동", "한미동맹", "대사관", "영사관", "국제회의", "SDGs", "기후변화"]
}

# -------------------------------
# 공고 결과 담는 리스트
# -------------------------------
results = []

# -------------------------------
# helper 함수: 키워드 매칭
# -------------------------------
def match_category(text):
    for category, keywords in KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category
    return None

# -------------------------------
# 사람인
# -------------------------------
def scrape_saramin():
    print("[JOB] Scraping Saramin...")
    url = "https://www.saramin.co.kr/zf_user/jobs/hot100"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    
    # 실제 공고 HTML 구조 확인 필요
    for job_item in soup.select("div.job-item"):
        a_tag = job_item.select_one("a.job-title")
        if not a_tag:
            continue
        title = a_tag.text.strip()
        job_url = a_tag['href']
        category = match_category(title)
        if category:
            results.append({
                "title": title,
                "url": job_url,
                "category": category,
                "type": "채용"
            })

# -------------------------------
# 인크루트
# -------------------------------
def scrape_incruit():
    print("[JOB] Scraping Incruit...")
    url = "https://www.job.incruit.com/entry/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    
    for job_item in soup.select("div.entry-list-item"):
        a_tag = job_item.select_one("a")
        if not a_tag:
            continue
        title = a_tag.text.strip()
        job_url = a_tag['href']
        category = match_category(title)
        if category:
            results.append({
                "title": title,
                "url": job_url,
                "category": category,
                "type": "채용"
            })

# -------------------------------
# 잡코리아
# -------------------------------
def scrape_jobkorea():
    print("[JOB] Scraping JobKorea...")
    url = "https://www.jobkorea.co.kr/theme/entry-level-internship"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    
    for job_item in soup.select("div.tplJobList > ul > li"):
        a_tag = job_item.select_one("a")
        if not a_tag:
            continue
        title = a_tag.text.strip()
        job_url = a_tag['href']
        category = match_category(title)
        if category:
            results.append({
                "title": title,
                "url": job_url,
                "category": category,
                "type": "채용"
            })

# -------------------------------
# 캠퍼스픽
# -------------------------------
def scrape_campuspick():
    print("[CONTEST] Scraping CampusPick...")
    url = "https://www.campuspick.com/contest"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    
    for item in soup.select("div.contest-item"):
        a_tag = item.select_one("a")
        if not a_tag:
            continue
        title = a_tag.text.strip()
        url = a_tag['href']
        category = match_category(title)
        if category:
            results.append({
                "title": title,
                "url": url,
                "category": category,
                "type": "공모전"
            })

# -------------------------------
# main
# -------------------------------
if __name__ == "__main__":
    print("=== Auto Scraper Started ===")
    scrape_saramin()
    scrape_incruit()
    scrape_jobkorea()
    scrape_campuspick()
    
    # 저장
    data = {
        "lastUpdated": str(datetime.datetime.now()),
        "items": results
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"=== Done: {len(results)} items scraped ===")
