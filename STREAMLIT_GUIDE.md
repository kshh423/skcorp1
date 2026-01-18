# Streamlit 실행 가이드

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 앱 실행
```bash
streamlit run streamlit_app.py
```

### 3. 브라우저 접속
자동으로 브라우저가 열립니다 (기본: http://localhost:8501)

---

## 📁 파일 구조

```
프로젝트/
├── streamlit_app.py          # Streamlit 메인 앱
├── main.py                    # Tkinter 버전 (기존)
├── sp500.csv                  # 데이터 (1928~2025)
├── requirements.txt           # 패키지 의존성
│
├── data/                      # 데이터 처리
│   ├── __init__.py
│   ├── loader.py
│   └── calculator.py
│
├── analysis/                  # 분석 엔진
│   ├── __init__.py
│   ├── monte_carlo.py
│   └── quant_metrics.py
│
└── visualizations/            # 시각화
    ├── __init__.py
    ├── simulation.py
    ├── distribution.py
    ├── percentile.py
    └── quant_panel.py
```

---

## 🎨 주요 기능

### Tab 1: 종합 분석 (Monte Carlo)
- ✅ 몬테카를로 시뮬레이션 (10,000회)
- ✅ 예상 수익률 시나리오 (90%, 50% 신뢰구간)
- ✅ 확률 분포 히스토그램
- ✅ 역사적 순위 지표
- ✅ 가격 배경 옵션
- ✅ 수익률 수치 표시 옵션

### Tab 2: 퀀트 리스크 분석
- ✅ 백분위 순위
- ✅ 복합 리스크 지수
- ✅ Z-score 통계적 괴리도

### 전역 설정 (사이드바)
- ✅ 분석 시작일 선택
- ✅ 분석 기간 설정
- ✅ 순위 모드 선택 (relative/absolute)
- ✅ 실시간 연동

---

## 🔧 고급 설정

### 포트 변경
```bash
streamlit run streamlit_app.py --server.port 8502
```

### 외부 접속 허용
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### 자동 재실행 비활성화
```bash
streamlit run streamlit_app.py --server.runOnSave false
```

---

## 📊 Streamlit vs Tkinter 비교

| 기능 | Streamlit | Tkinter |
|------|-----------|---------|
| 웹 기반 | ✅ | ❌ |
| 반응형 | ✅ | ❌ |
| 배포 용이성 | ✅ | ❌ |
| 설치 필요 | 브라우저만 | Python 앱 |
| UI 품질 | 모던 | 전통적 |
| 속도 | 약간 느림 | 빠름 |

---

## 🌐 배포 옵션

### 1. Streamlit Cloud (무료)
1. GitHub에 코드 push
2. https://share.streamlit.io 접속
3. 레포지토리 연결
4. 배포 완료!

### 2. Heroku
```bash
# Procfile 생성
echo "web: streamlit run streamlit_app.py --server.port $PORT" > Procfile

# 배포
git push heroku main
```

### 3. AWS/GCP
Docker 컨테이너로 배포 가능

---

## ⚠️ 주의사항

1. **첫 실행 시**: yfinance가 2026년 데이터를 가져오므로 약간의 지연 발생
2. **메모리**: 대용량 시뮬레이션 시 메모리 사용량 주의
3. **캐싱**: Streamlit은 자동으로 결과를 캐싱합니다

---

## 🐛 문제 해결

### 한글 폰트 깨짐 (Linux/Mac)
```python
# 시스템에 한글 폰트 설치 필요
# Ubuntu: sudo apt-get install fonts-nanum
# Mac: 시스템 폰트 사용
```

### 포트 충돌
```bash
# 다른 포트 사용
streamlit run streamlit_app.py --server.port 8502
```

### 데이터 로딩 실패
- sp500.csv 파일이 같은 디렉토리에 있는지 확인
- 인터넷 연결 확인 (yfinance)

---

## 📝 라이선스

MIT License
