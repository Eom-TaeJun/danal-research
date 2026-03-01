---
name: im-draft
description: 핀테크 / 디지털자산 기업 투자 검토 보고서(IM) 초안 작성. 기업명 입력 시 시장 조사 → IM 구조 작성까지 자동화. Triggers on "IM 작성", "투자 검토", "im draft", "investment memo", 기업명 + "분석".
---

# IM Draft (Investment Memorandum)

내부 투자 의사결정용 검토 보고서 초안. 외부 IR 자료가 아닌 팀 내부 판단 문서.

## 실행

```bash
python src/research.py --company "[기업명]"
python src/report.py --type im --company "[기업명]"
```

출력: `outputs/reports/im_[기업명]_YYYYMMDD.md`

## IM 구조

```
# Investment Memorandum — [기업명]
작성일: YYYY-MM-DD

## 1. Executive Summary (1/2 페이지)
- 투자 논리 핵심 2-3문장
- 투자 의견: 관심 / 검토 / 보류

## 2. Company Overview
- 사업 모델 (어떻게 돈 버는가)
- 핵심 제품/서비스
- 창업팀 배경

## 3. Market Opportunity
- TAM / SAM / SOM 추정
- 시장 성장률 및 드라이버
- 경쟁사 맵

## 4. Investment Thesis
- Bull Case: 잘 될 이유 3가지
- Bear Case: 안 될 이유 3가지

## 5. Key Risks & Mitigants
- 규제 리스크
- 경쟁 리스크
- 실행 리스크

## 6. 다음 단계
- 추가 확인 필요 사항
- 미팅 요청 여부
```

## 작성 원칙

- 인턴 담당 파트: 2(Company), 3(Market), 5(Risks) — 초안 수준
- 모든 수치는 출처 명기: "(CoinGecko, 2026-03)"
- Bull/Bear는 균형 있게 — 단점을 숨기지 말 것
- 분량: 3-5페이지 (초안 기준)
