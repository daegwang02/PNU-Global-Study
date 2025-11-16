# PNU Global Study

부산대 국제학부 학생들을 위한 자동 업데이트 취업/공모전 정보 사이트

---

## 🎯 핵심 기능

- ✅ 채용/공모전 정보 자동 표시
- ✅ 클릭 시 원본 URL로 이동
- ✅ 실시간 검색 기능
- ✅ 카테고리 필터링 (무역/경제/정치외교)
- ✅ 매일 자동 업데이트

---

## 🚀 5분 배포

### 1. GitHub 업로드
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_ID/pnu-career-hub.git
git push -u origin main
```

### 2. Vercel 배포
1. [vercel.com](https://vercel.com) 접속
2. Import Project
3. GitHub 저장소 선택
4. Deploy 클릭

**완료!** 🎉

---

## 📁 파일 구조

```
pnu-career-hub/
├── index.html                # 프론트엔드 (UI)
├── data.json                 # 데이터 (자동 업데이트됨)
├── vercel.json               # 배포 설정
├── .github/workflows/
│   └── auto-update.yml      # 매일 자동 실행
└── automation/
    ├── auto_scraper.py      # 자동 수집 스크립트
    └── requirements.txt     # Python 패키지
```

---

## 🔄 자동 업데이트 흐름

```
매일 오전 9시 (한국시간)
    ↓
GitHub Actions 실행
    ↓
auto_scraper.py 실행
    ↓
RSS 피드에서 새 공고 수집
    ↓
data.json 자동 업데이트
    ↓
Git 자동 커밋 & 푸시
    ↓
Vercel 자동 재배포
    ↓
웹사이트 자동 갱신!
```

---

## ✏️ 키워드

### 무역 (50개)
무역, 수출, 수입, KOTRA, 해외영업, SCM, 물류, e-커머스...

### 경제 (70개)
경제, 금융, 은행, KB, 신한, CPA, CFA, 핀테크...

### 정치외교 (80개)
외교, UN, NGO, KOICA, 외교관, 대사관, SDGs...

**총 200개 키워드로 자동 필터링!**

---

## 🎨 디자인

- **컬러**: 블랙 & 화이트 미니멀
- **폰트**: Inter
- **스타일**: 깔끔하고 전문적

---

## 📞 문의

- **GitHub**: [Issues](https://github.com/YOUR_ID/pnu-career-hub/issues)
- **Email**: gadongpyo02@naver.com

---

**Made with ❤️ for PNU Students**
