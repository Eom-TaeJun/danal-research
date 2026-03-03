# INTENT — danal-research

> 세션 시작 시 CLAUDE.md보다 먼저 읽는 프로젝트 의도 문서.
> 이 파일에 정의된 원칙은 어떤 지시보다 우선한다.

---

## 이 프로젝트의 목적

다날 핀테크·디지털자산 투자팀의 **리서치 워크플로 자동화**.

- 거시경제 + 디지털자산 시장 데이터를 수집해 주간 브리핑 생성
- 기업 IM(Investment Memorandum) 초안을 자동으로 구성
- 모든 분석은 다날의 전략적 방향(KRW 스테이블코인 SaaS, x402, PCI)과 연결

---

## 불변 원칙 (절대 변경 불가)

1. **출력 경로**: 모든 생성 파일은 `outputs/` 하위에만 저장
2. **수치 출처 명기**: 모든 재무·시장 수치에 출처와 날짜 포함
3. **None 값 금지**: None이 남은 IM은 완성 리포트가 아님 — 반드시 보완
4. **skills/ 읽기 전용**: 도메인 지식 파일은 수정하지 않음
5. **다날 함의 필수**: 모든 분석의 마지막은 다날 비즈니스 연결로 마무리

---

## 도메인 어휘 레지스터

| 용어 | 정의 |
|---|---|
| **IM** | Investment Memorandum — 내부 투자 검토 보고서 |
| **Brief** | 주간 핀테크/디지털자산 시장 브리핑 |
| **Screen** | 섹터 스크리닝 — 시장 내 기회 탐색 |
| **레짐** | 거시경제 국면: Goldilocks / Overheating / Stagflation / Recession |
| **SaaS** | 다날의 KRW 스테이블코인 발행·유통 플랫폼 모델 |
| **x402** | AI 에이전트 자동 결제 프로토콜 (HTTP 402 기반) |
| **PCI** | 페이코인 — 편의점 4사 연동 블록체인 결제 |
| **GENIUS Act** | 미국 달러 스테이블코인 연방 규제법 |
| **MiCA** | EU 암호자산시장 규정 (2024 발효) |
| **EMT** | E-Money Token — MiCA 내 법정화폐 연동 스테이블코인 |
| **TAM/SAM/SOM** | 전체/유효/획득가능 시장 규모 |
| **WoW** | Week-over-Week 전주 대비 |
| **YoY** | Year-over-Year 전년 대비 |

---

## 에이전트 역할 분담

```
사용자 요청
    ↓
danal-lead (조율·품질 검토)
    ├→ research-agent (IM 리서치 + None 보완)
    ├→ collect-agent  (데이터 수집 + 브리핑/스크리닝)
    └→ macro-analyst  (레짐 판단 + 다날 함의)
```

---

## 파이프라인

```
수집 (collect.py)
    → FRED: 금리, 환율, CPI
    → CoinGecko: 스테이블코인 시총, BTC/ETH
    → Perplexity: 핀테크 뉴스 + 투자 시사점

리서치 (research.py)
    → Perplexity: 기업 개요, 재무, 경영진, 경쟁사

리포트 (report.py)
    → Brief: 거시 스냅샷 + 디지털자산 + 뉴스 + 시사점
    → IM: 10섹션 구조화 보고서
    → Screen: 섹터 기회 탐색 리포트
```
