---
name: stablecoin-market
description: 글로벌 스테이블코인 시장 분석. 시총·도미넌스·규제 동향·경쟁 구도를 구조화. 다날 스테이블코인 SaaS 사업 맥락에서 시장 기회 평가. Triggers on "스테이블코인", "stablecoin", "USDT", "USDC", "원화 스테이블코인", "KRW stablecoin".
---

# Stablecoin Market Analysis

## 시장 분류

| 유형 | 대표 | 담보 | 핵심 리스크 |
|------|------|------|-----------|
| Fiat-backed | USDT, USDC | 현금·국채 | 준비금 투명성 |
| Crypto-backed | DAI | ETH 등 | 담보 변동성 |
| Algorithmic | (LUNA 실패 사례) | 없음 | 탈페깅 위험 |
| CBDC 연계 | 각국 CBDC | 중앙은행 | 규제·채택 속도 |

## 핵심 지표

```
python src/collect.py --mode stablecoin
```

수집 지표:
- 전체 시총 (CoinGecko)
- USDT / USDC / BUSD 도미넌스
- 30일 거래량 추이
- DeFiLlama TVL (스테이블코인 파킹 비중)

## 규제 프레임워크

- **EU MiCA** (2024 발효): EMT/ART 인허가, 준비금 공시 의무
- **미국 GENIUS Act**: 달러 연동 스테이블코인 연방 규제 추진 중
- **한국 디지털자산기본법**: 가상자산 사업자 규제, 스테이블코인 정의 미확정

## 다날 관련 분석 포인트

- 원화(KRW) 스테이블코인 SaaS: 발행·유통·결제·정산 통합
- x402 프로토콜: AI 에이전트 자동 결제 인프라
- 페이코인(PCI): 편의점 4사 실물 결제 연동

## 경쟁사 맵 (글로벌)

| 구분 | 기업 | 강점 |
|------|------|------|
| 발행사 | Circle (USDC) | 규제 친화, 기관 신뢰 |
| 발행사 | Tether (USDT) | 유동성 1위 |
| 인프라 | Stripe (USDC 결제) | 가맹점 네트워크 |
| 국내 | 카카오페이·토스 | 결제 UX |

## 분석 원칙

- 시총 수치는 항상 날짜 명기
- 규제 상태는 "확정 / 추진 중 / 미정" 구분
- 다날 비즈니스와의 연관성을 마지막에 한 문단으로 요약
