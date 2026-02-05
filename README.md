# 역대 암호화폐 퍼포먼스

월별 암호화폐 수익률 비교 및 역사적 패턴 분석 대시보드

## 🖥️ 데모

GitHub Pages로 배포: `https://[your-username].github.io/[repo-name]`

## ✨ 기능

- **실시간 가격**: Binance WebSocket을 통한 실시간 가격 표시
- **역대 월별 차트**: 과거 같은 달의 수익률을 한 차트에서 비교
  - 🟢 역대 최고 수익률
  - 🔴 역대 최저 수익률
  - ⚪ 평균 수익률
  - 🟡 현재 연도
  - 🔵 선택한 연도
- **월별 히트맵**: 연도별 월간 수익률 테이블
- **지원 코인**: Bitcoin, Ethereum, Solana, XRP, BNB

## 📊 데이터

- **출처**: CoinGecko
- **업데이트**: 매일 오전 7시 (KST) 자동 업데이트
- **기간**: 각 코인의 상장일부터 현재까지

| 코인 | 데이터 시작일 |
|------|--------------|
| Bitcoin | 2013년 4월 |
| Ethereum | 2015년 8월 |
| Solana | 2020년 4월 |
| XRP | 2013년 8월 |
| BNB | 2017년 9월 |

## 🚀 배포 방법

### 1. GitHub Repository 생성

1. GitHub에서 새 repository 생성
2. 이 프로젝트의 모든 파일 업로드

### 2. GitHub Pages 활성화

1. Repository Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` / `root`
4. Save

### 3. 자동 업데이트 설정

GitHub Actions가 매일 자동으로 데이터를 업데이트합니다.
- 스케줄: 매일 오전 7시 KST (22:00 UTC)
- 수동 실행: Actions 탭 → "Daily Price Update" → "Run workflow"

## 📁 프로젝트 구조

```
├── index.html              # 메인 대시보드
├── update_prices.py        # 데이터 업데이트 스크립트
├── data/
│   ├── bitcoin.csv
│   ├── ethereum.csv
│   ├── solana.csv
│   ├── xrp.csv
│   └── bnb.csv
└── .github/workflows/
    └── daily_update.yml    # GitHub Actions 워크플로우
```

## 🛠️ 로컬 개발

```bash
# 로컬 서버 실행
python -m http.server 8000

# 브라우저에서 열기
open http://localhost:8000
```

## 📝 수동 데이터 업데이트

```bash
pip install requests
python update_prices.py
```

## 📜 라이선스

MIT License

## 🙏 크레딧

- 데이터: [CoinGecko](https://www.coingecko.com/)
- 실시간 가격: [Binance WebSocket](https://binance-docs.github.io/apidocs/spot/en/)
- 차트: [Chart.js](https://www.chartjs.org/)
