---
name: weekly-brief
description: 핀테크 & 디지털자산 주간 시장 브리핑 생성. 거시경제 지표, 스테이블코인 시장, 글로벌 핀테크 주요 동향을 수집해 투자 시사점까지 정리. Triggers on "주간 브리핑", "핀테크 동향", "디지털자산 현황", "weekly brief", "시장 요약".
---

# Weekly Brief

핀테크 & 디지털자산 투자팀을 위한 주간 브리핑. 2분 안에 읽을 수 있도록 작성.

## 실행

```bash
python src/collect.py --mode brief
python src/report.py --type brief
```

출력: `outputs/reports/brief_YYYYMMDD.md`

## 브리핑 구조

```
# 핀테크/디지털자산 주간 브리핑 — YYYY-MM-DD

## 1. 거시경제 스냅샷
- Fed Funds Rate / 한국 기준금리
- USD/KRW 환율 (WoW 변화)
- 10Y 미국채 수익률

## 2. 디지털자산 시장
- 스테이블코인 전체 시총 (WoW)
- USDT / USDC 도미넌스
- BTC 가격 (WoW)

## 3. 이번 주 핵심 뉴스 (3건)
- 뉴스 + 투자 시사점 한 줄

## 4. 투자 시사점
- 이번 주 데이터가 말하는 것
- 다음 주 주목할 이벤트
```

## 작성 원칙

- 수치는 단위와 변화율 함께: "4.25%", "+2.1% WoW"
- 뉴스는 요약이 아닌 **함의** 중심으로
- "변화 없음"도 유효한 브리핑 — 억지로 의미 만들지 않기
