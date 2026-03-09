# spec.md — Danal Research 워크플로 상세

> 보고서 포맷·데이터 흐름·섹터별 분석 기준을 다룬다.
> 레짐 정의·임계값·출처 표준·4축 명칭의 단일 진실 원천은 **`INTENT.md`**.
> CLAUDE.md / AGENTS.md와 충돌 시 INTENT.md → 이 파일 순서로 우선.

---

## 1. 인턴 업무 범위 (소개.txt 기준)

| 업무 | 상세 | 산출물 |
|------|------|--------|
| 투자 리포트 작성 보조 | 국내외 기업·산업 분석 조사, IM 초안 작성 | `im_[기업명]_YYYYMMDD.md` |
| 금융·거시경제 데이터 분석 | 주요 금융 지표 수집, 핀테크·디지털자산 시장 조사 | `snapshot_YYYYMMDD.json`, `brief_YYYYMMDD.md` |
| 전략 보고 및 시각화 | 데이터 차트화, 핵심 인사이트 도출 지원 | `outputs/charts/*.png`, 보고서 임베드 |

**포지셔닝**: 인턴의 역할은 **초안 수준**의 리서치 및 정리. 최종 투자 판단은 시니어가 수행.

---

## 2. 워크플로 유형

### Brief (주간 브리핑)

**목적**: 투자팀이 2분 안에 읽을 수 있는 핀테크·디지털자산 주간 요약

**데이터 흐름**:
```
collect.py --mode brief
    → FRED (FEDFUNDS, DGS10, DEXKOUS ← 3개 필수)
    → CoinGecko (스테이블코인 시총·USDT·USDC·BTC)
    → Perplexity (핀테크 뉴스 3건 + 투자 시사점)
    → outputs/context/snapshot_YYYYMMDD.json

report.py --type brief
    → outputs/reports/brief_YYYYMMDD.md
    → outputs/charts/stablecoin_pie_YYYYMMDD.png (차트 임베드)
```

**보고서 포맷** (실제 산출물 기준):
```markdown
# 핀테크/디지털자산 주간 브리핑 — YYYY-MM-DD

## 1. 거시경제 스냅샷
| 지표 | 값 |

## 2. 디지털자산 시장
| 항목 | 값 | 7일 변화 |
![Stablecoin Market Share](../charts/stablecoin_pie_YYYYMMDD.png)

## 3. 이번 주 핵심 동향
뉴스 3건 (함의 중심 서술)

## 4. 투자 시사점
- ko: **[키워드]**: [시사점 내용]  ← "ko:" 접두어 필수

---
*Generated: TIMESTAMP | Source: FRED, CoinGecko, Perplexity*
```

---

### IM (Investment Memorandum)

**목적**: 내부 투자 의사결정용 기업 검토 보고서 초안 — **10섹션 구조**

**데이터 흐름**:
```
research.py --company "[기업명]"
    → Perplexity: 기업 개요·재무·경영진·경쟁사
    → outputs/context/research_[기업명]_YYYYMMDD.json

report.py --type im --company "[기업명]"
    → outputs/reports/im_[기업명]_YYYYMMDD.md
    → outputs/charts/revenue_trend_YYYYMMDD.png (차트 임베드)
```

**IM 10섹션 구조** (실제 산출물 기준):

| # | 섹션 | 내용 | 인턴 담당 |
|---|------|------|----------|
| 1 | Executive Summary | 투자 논리 3-5문장 + 투자 의견 체크박스 | 시니어 검토 |
| 2 | Company Overview | 사업 모델·매출 방식 | ✅ 초안 |
| 3 | 경영진 | 창업팀·CLO 등 표 형식 | ✅ 초안 |
| 4 | Market Opportunity | TAM/SAM 추정 + 경쟁사 목록 | ✅ 초안 |
| 5 | 재무 실적 | 연도별 매출·순이익·마진 표 + 차트 임베드 | ✅ 초안 |
| 6 | Investment Thesis | Bull Case 3개 / Bear Case 3개 | 시니어 검토 |
| 7 | 밸류에이션 | 시총·EV/Rev·P/E + 동종업계 비교 | ✅ 초안 |
| 8 | Key Risks | 규제·경쟁·사이버·시장 리스크 | ✅ 초안 |
| 9 | 최근 동향 | 최근 6개월 내 주요 이벤트 3건 | ✅ 초안 |
| 10 | 다음 단계 | 체크리스트 형식 (`- [ ] 항목`) | 팀 논의 |

**투자 의견 포맷** (섹션 1 필수):
```markdown
**투자 의견:** ☐ 관심  ☐ 검토  ☐ 보류
```

**차트 임베드 위치**:
- 재무 실적(섹션 5): `![Revenue Trend](../charts/revenue_trend_YYYYMMDD.png)`
- 시장점유율 필요 시: `![Market Share](../charts/market_share_YYYYMMDD.png)`

---

### Screen (섹터 스크리닝)

**목적**: 스테이블코인·핀테크·DeFi 등 섹터 기회 탐색

**데이터 흐름**:
```
collect.py --mode screen --sector [sector]
    → CoinGecko + Perplexity
    → outputs/context/snapshot_YYYYMMDD.json
    → outputs/reports/screen_[sector]_YYYYMMDD.md
    → outputs/charts/macro_dashboard_YYYYMMDD.png
```

---

## 3. 레짐 판단 기준

> **정의 원천**: `INTENT.md §3` (5개 레짐, 임계값, 다날 KSC 함의 포함).
> `analyze.py` 임계값: `growth_norm ≥ 0.2` → positive, `≤ -0.2` → negative, 그 외 → neutral → **Late-Cycle**.
> 판단 원칙: 단일 지표 아닌 3개 이상 지표 수렴.

---

## 3-b. 거시 전파 분석 (Macro Transmission Cascade)

> IM 작성 전 macro-analyst가 아래 4단계 순서로 전파 강도를 산출한다.
> 하드코딩 금지 — 매 IM마다 당시 거시 데이터 기반으로 동적 생성.

```
[L1] 글로벌 거시  →(α)→  [L2] 한국 시장  →(β)→  [L3] 섹터  →(γ)→  [L4] 기업
```

**전파율 (α·β·γ) 판단 기준:**

| 레벨 | 전파율 | High 조건 | Low 조건 |
|------|:------:|---------|---------|
| α: 글로벌→한국 | 0.2~1.0 | 외인 자본 이동 직접 경로, KRW 환율 충격 | 국내 정책이 충격 흡수, 반사이익 발생 |
| β: 한국→섹터 | 0.2~1.0 | 유동성 장세 + 테마 섹터 | 방어적 섹터, 글로벌 독립 사업모델 |
| γ: 섹터→기업 | 0.2~1.0 | 순수 국내 기업, 섹터 내 높은 노출 | 글로벌 자산, 섹터 탈동조화 |

**최종 영향 = 글로벌 신호 강도 × α × β × γ**

전파 분석 출력 형식 → `macro-analyst.md` Step 7 참조.

---

## 4. 출처 명기 표준

> **표준 원천**: `INTENT.md §7`. 핵심 규칙:
> - 모든 수치에 `(출처, YYYY-MM-DD)` 필수
> - 확인 불가 수치: `"확인 필요"` (None·빈칸 금지)
> - Brief 투자 시사점: `- ko: **[키워드]**: [내용]` 형식 (접두어 필수)

---

## 5. 다날 비즈니스 연결 원칙

> **4축 명칭 원천**: `INTENT.md §4`. 모든 분석의 마지막은 4축 연결로 마무리.
> 제품 상세 컨텍스트: `.claude/skills/danal-context/SKILL.md` 참조.

---

*Last Updated: 2026-03-06 | 소개.txt + 실제 산출물 기준*
