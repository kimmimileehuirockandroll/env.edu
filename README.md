# 🌿 제주 에코 네트워크

네트워크 사이언스 × 데이터 사이언스 × 환경 교육 — 제주 중학생 대상 1시간 체험 웹 프로그램

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 메뉴 구성

| 메뉴 | 설명 |
|------|------|
| 🏠 홈 | 교육 취지 소개, 개념 설명 |
| 🎮 삼다수 에코 레이스 | 제주 6개 생태 거점 네트워크 탐험 게임 |
| 📊 우리 반 환경행동 네트워크 | NAM·VBN·TPB 기반 설문 + 실시간 네트워크 시각화 |

## 기술 스택

- **Streamlit** — 웹 인터페이스 + `st.session_state` 실시간 데이터 관리
- **NetworkX** — 그래프 모델링 (게임 경로, 응답 유사도 네트워크)
- **Matplotlib** — 네트워크 시각화 (한글 폰트 포함)
- **NumPy / Pandas** — 설문 데이터 통계 처리

## 게임 구조 (에코 레이스)

- 노드 6개: 제주공항, 협재해변, 곶자왈도립공원, 서귀포치유의숲, 성산일출봉, 함덕해변
- 엣지 11개: 가중치 3종 (시간·탄소·비용)
- 이동 수단 트레이드오프:
  - 🚌 버스: 저탄소·저비용 but 랜덤 대기 패널티
  - ⚡ 전기렌터카: 고속·정확 but 고비용·고탄소

## 설문 이론 배경

- **NAM** (Schwartz, 1977): 결과 인지 + 책임 귀속
- **VBN** (Stern, 2000): 생태적 가치관
- **TPB** (Ajzen, 1991): 주관적 규범 + 지각된 행동 통제감

## Streamlit Community Cloud 배포

1. GitHub에 `app.py` + `requirements.txt` 업로드
2. [share.streamlit.io](https://share.streamlit.io) 에서 배포
3. 100명 동시 접속 지원 (session_state 기반 경량 설계)
