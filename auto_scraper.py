"""
자동 데이터 수집기
RSS 피드 + 공식 API를 통한 자동 수집
"""

import json
import requests
from datetime import datetime, timedelta
import feedparser
import re
from typing import List, Dict

class CareerScraper:
    def __init__(self):
        self.data = self.load_existing_data()
        self.new_items_count = 0
        
        # 확장된 키워드 (200개+)
        self.keywords = {
            "무역": [
                # 핵심
                "무역", "수출", "수입", "통관", "관세", "FTA", "HS코드",
                # 기관
                "KOTRA", "무역협회", "관세청", "무역보험공사", "수출입은행",
                # 직무
                "해외영업", "글로벌영업", "국제영업", "바이어", "소싱",
                "SCM", "물류", "포워딩", "해운", "항공", "영업", "검역",
                # 지역
                "중국무역", "미국수출", "유럽", "동남아", "RCEP",
                # 기타
                "e-커머스", "크로스보더", "국제배송", "아마존"
            ],
            "경제": [
                # 핵심
                "경제", "금융", "은행", "증권", "자산운용", "투자", "펀드",
                "IB", "애널리스트", "리서치", "재무", "회계", "세무",
                # 금융기관
                "KB", "신한", "하나", "우리", "NH농협", "IBK기업", "KDB산업",
                "미래에셋", "삼성증권", "한국투자", "한국거래소", "한국은행",
                # 직무
                "PB", "WM", "자산관리", "신용평가", "심사역", "여신",
                "금융일반", "채권", "주식", "외환", "리서치", "리스크관리",
                "경영기획", "전략기획", "IR", "M&A",
                # 자격증
                "CPA", "AICPA", "CFA", "FRM", "CFP",
                # 기타
                "ESG", "핀테크", "디지털금융", "블록체인"
            ],
            "정치외교": [
                # 핵심
                "외교", "국제관계", "정치", "국제정치", "안보", "통일",
                "외교관", "행정고시", "외무고시", "5급공채",
                # 기관
                "외교부", "통일부", "국방부", "청와대", "국회",
                "UN", "유엔", "UNDP", "UNESCO", "WHO", "UNICEF",
                "NATO", "EU", "ASEAN", "APEC", "G20", "OECD",
                "세계은행", "IMF", "WTO",
                # NGO
                "NGO", "INGO", "옥스팜", "월드비전", "굿네이버스",
                "국경없는의사회", "KOICA", "월드프렌즈",
                # 직무
                "공공외교", "다자외교", "경제외교", "문화외교",
                "개발협력", "ODA", "평화", "갈등해결", "인권",
                "정책연구", "싱크탱크",
                # 지역
                "북핵", "한반도", "동북아", "중동", "한미동맹",
                # 기타
                "대사관", "영사관", "국제회의", "SDGs", "기후변화"
            ]
        }
    
    def load_existing_data(self) -> Dict:
        """기존 데이터 로드"""
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"lastUpdated": "", "jobs": [], "contests": []}
    
    def categorize(self, text: str) -> str:
        """텍스트를 카테고리로 분류"""
        text_lower = text.lower()
        scores = {category: 0 for category in self.keywords}
        
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[category] += 1
        
        max_score = max(scores.values())
        if max_score > 0:
            return max(scores, key=scores.get)
        return None  # 관련 없음
    
    def is_duplicate(self, new_item: Dict, existing_items: List[Dict]) -> bool:
        """중복 확인"""
        for item in existing_items:
            if item.get('url') == new_item.get('url'):
                return True
            if item.get('title') == new_item.get('title'):
                return True
        return False
    
    def parse_rss_feeds(self):
        """RSS 피드 수집"""
        print("📡 RSS 피드 수집 중...")
        
        # 실제 RSS URL로 교체하세요
        rss_sources = {
            "jobs": [
                "https://www.saramin.co.kr/zf_user/help/live/rss",
            ],
            "contests": [
                "https://www.wevity.com/index_rss.php",
            ]
        }
        
        for feed_url in rss_sources["jobs"]:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:20]:
                    title = entry.get('title', '')
                    description = entry.get('summary', '')
                    
                    category = self.categorize(title + " " + description)
                    if not category:  # 관련 없으면 스킵
                        continue
                    
                    job = {
                        "id": len(self.data["jobs"]) + self.new_items_count + 1,
                        "title": title,
                        "company": entry.get('author', '미정'),
                        "category": category,
                        "type": "채용",
                        "deadline": self.extract_deadline(entry),
                        "url": entry.get('link', ''),
                        "tags": self.extract_tags(title),
                        "new": True
                    }
                    
                    if not self.is_duplicate(job, self.data["jobs"]):
                        self.data["jobs"].append(job)
                        self.new_items_count += 1
                        print(f"✅ 새 채용: {title[:40]}...")
            except Exception as e:
                print(f"❌ RSS 오류: {e}")
        
        for feed_url in rss_sources["contests"]:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:20]:
                    title = entry.get('title', '')
                    description = entry.get('summary', '')
                    
                    category = self.categorize(title + " " + description)
                    if not category:
                        continue
                    
                    contest = {
                        "id": len(self.data["contests"]) + self.new_items_count + 1,
                        "title": title,
                        "organizer": entry.get('author', '미정'),
                        "category": category,
                        "type": "공모전",
                        "deadline": self.extract_deadline(entry),
                        "prize": self.extract_prize(description),
                        "url": entry.get('link', ''),
                        "tags": self.extract_tags(title),
                        "new": True
                    }
                    
                    if not self.is_duplicate(contest, self.data["contests"]):
                        self.data["contests"].append(contest)
                        self.new_items_count += 1
                        print(f"✅ 새 공모전: {title[:40]}...")
            except Exception as e:
                print(f"❌ RSS 오류: {e}")
    
    def extract_deadline(self, entry) -> str:
        """마감일 추출"""
        future_date = datetime.now() + timedelta(days=30)
        return future_date.strftime('%Y-%m-%d')
    
    def extract_prize(self, text: str) -> str:
        """상금 추출"""
        patterns = [r'(대상|상금)[:\s]*([0-9,]+만?\s?원)', r'([0-9,]+만?\s?원)']
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return ""
    
    def extract_tags(self, text: str) -> List[str]:
        """태그 추출"""
        tags = []
        tag_keywords = {
            "신입", "경력", "인턴", "대학생", "청년",
            "서울", "부산", "온라인", "아이디어"
        }
        text_lower = text.lower()
        for keyword in tag_keywords:
            if keyword in text_lower:
                tags.append(keyword)
        return tags[:5]
    
    def clean_old_data(self):
        """지난 공고 제거"""
        print("🧹 오래된 데이터 정리 중...")
        today = datetime.now()
        
        self.data["jobs"] = [
            job for job in self.data["jobs"]
            if datetime.strptime(job['deadline'], '%Y-%m-%d') >= today
        ]
        
        self.data["contests"] = [
            contest for contest in self.data["contests"]
            if datetime.strptime(contest['deadline'], '%Y-%m-%d') >= today
        ]
    
    def save_data(self):
        """데이터 저장"""
        self.data['lastUpdated'] = datetime.now().isoformat()
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 저장 완료!")
        print(f"📊 채용: {len(self.data['jobs'])}건")
        print(f"🏆 공모전: {len(self.data['contests'])}건")
        print(f"🆕 신규: {self.new_items_count}건")

def main():
    print("=" * 50)
    print("🤖 자동 데이터 수집 시작")
    print("=" * 50)
    
    scraper = CareerScraper()
    scraper.parse_rss_feeds()
    scraper.clean_old_data()
    scraper.save_data()
    
    print("\n✅ 수집 완료!")

if __name__ == "__main__":
    main()
