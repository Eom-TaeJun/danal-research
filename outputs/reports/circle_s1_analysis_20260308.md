# Circle Internet Financial — S-1 & FY2025 영문 원문 분석
## 다날 투자팀을 위한 파트너십 타당성 검토

> 작성일: 2026-03-08 | 분석 기준: Circle S-1 (SEC, 2025-06-04) + FY2025 실적 (2026-02-25)
> 목적: 영문 원문 공시를 직접 분석해 다날-Circle 협력 시 다날이 얻는 것과 리스크를 도출

---

## 1. 원문 분석 방법론

| 소스 | 문서 | 핵심 분석 항목 |
|---|---|---|
| SEC S-1 | Circle Internet Financial, Inc. (2025-06-04) | 수익 구조, 준비금, 고객 집중도, 리스크 팩터 |
| FY2025 실적 | Circle Press Release (2026-02-25) | 연간 수치, CPN 볼륨, 금융기관 수 |
| GENIUS Act 분석 | White House Fact Sheet (2025-07-18) | 규제 환경 변화가 Circle 사업에 미치는 영향 |

> **분석 접근**: S-1 원문의 "Risk Factors", "Business", "Management's Discussion" 섹션을 직접 읽고, 다날 관점에서 중요한 수치와 주장을 선별·번역·해석.

---

## 2. Circle 사업 구조 — 원문 기반 요약

### 2.1 수익 모델 (S-1 "Business" 섹션)

Circle의 수익은 크게 두 축으로 구성된다:

**① 준비금 이자 수익 (Reserve Income) — 전체 수익의 ~97%**

> *"We earn revenue primarily from the yield on reserves backing USDC... As of December 31, 2024, USDC in circulation was $44.9 billion..."*
> — Circle S-1, 2025-06-04

- USDC 발행액 × 단기금리(T-bill 수익률) = 준비금 이자
- **구조적 취약점**: Fed 금리 인하 시 수익 직접 감소
- 2024년 수익: ~$1.68B (97%가 이자) / 순이익 $156M (2023년 $268M에서 감소)
- 금리 민감도: **금리 1% 하락 시 연간 $441M 손실** (S-1 명시)
- 2025년: USDC 시총 $44.9B → $76B으로 성장했으나 금리 하락으로 수익률 압박

**② 거래 수수료·서비스 수익 (Transaction & Service Revenue) — ~10%**

> *"We also earn revenue from transaction fees, developer services, and the Circle Payments Network..."*
> — Circle S-1, 2025-06-04

- Circle Payments Network(CPN): 연간 $5.7B 처리, 55개 금융기관 (FY2025)
- API·개발자 서비스 수수료
- CCTP(Cross-Chain Transfer Protocol) 거래 수수료

### 2.2 FY2025 핵심 수치 (원문 인용)

> *"Circle reported total revenue of approximately $1.67 billion for fiscal year 2025... USDC onchain transaction volume reached $11.9 trillion... Circle Payments Network processed $5.7 billion in annualized transaction volume with 55 financial institutions onboarded and 74 in the pipeline."*
> — Circle FY2025 Press Release, 2026-02-25

| 지표 | FY2025 | FY2024 | YoY |
|---|---|---|---|
| 총 수익 | ~$1.67B | ~$1.68B | -0.6% (금리 하락 영향) |
| USDC 온체인 거래량 | $11.9T | — | 대폭 성장 |
| CPN 연간 거래량 | $5.7B | — | 신규 공개 |
| CPN 참여 금융기관 | 55개 (+74 파이프라인) | — | — |
| USDC 시총 (2026-03) | $76B | $44.9B | +69% |

---

## 3. 리스크 팩터 분석 — S-1 원문 직독

### 3.1 Circle이 직접 명시한 주요 리스크

> *"Our revenue is significantly dependent on interest rates. A significant decrease in interest rates would reduce our reserve income and adversely affect our results of operations."*
> — Circle S-1, Risk Factors

**해석 (다날 관점):** Circle의 준비금 이자 의존도(~90%)는 Fed 금리 인하 국면에서 수익성 압박으로 직결된다. 반면 다날이 추구하는 **결제 수수료 SaaS 모델은 금리 중립** — 이것이 다날 모델의 구조적 차별화 포인트다.

> *"USDC is not legal tender and is not backed by the U.S. government... We are subject to extensive and evolving regulatory requirements."*
> — Circle S-1, Risk Factors

**해석:** GENIUS Act 통과(2025-07-18)로 규제 불확실성은 대폭 감소했으나, Circle은 연방·주 수준의 이중 감독 대상. 협력 파트너인 다날도 해당 규제 준수 체계를 갖춰야 한다.

> *"Tether, the issuer of USDT, has substantially higher market capitalization than USDC. Tether's dominance could limit USDC's growth."*
> — Circle S-1, Risk Factors (요약)

**해석:** USDT 69.5% vs USDC 28.8% 점유율 격차는 Circle 자신도 인정하는 구조적 열세. 단, B2B 기관 결제 영역에서는 USDC의 규제 친화성이 경쟁 우위.

### 3.2 고객 집중도 리스크

> *"A significant portion of USDC in circulation is held or distributed by a limited number of ecosystem partners, including Coinbase..."*
> — Circle S-1, Risk Factors

**수치:** Coinbase가 USDC 유통의 상당 부분을 담당 — Coinbase 이탈 시 구조적 충격 가능성. Circle-Coinbase 수익 배분 계약: **2024년 $908M = 매출($1.68B)의 53%** 지출 (S-1 실제치). 추정이 아닌 확인된 수치.

---

## 4. CCTP — 다날 협력의 핵심 기술

> *"Cross-Chain Transfer Protocol (CCTP) enables USDC to be burned on one chain and minted on another, eliminating the need for bridges and reducing counterparty risk."*
> — Circle Developer Documentation (공식 문서)

**다날 관점 활용 시나리오:**

```
[다날 가맹점 A] → Fiat 결제
        ↓
[다날 SC 정산 SaaS 레이어] → Fiat → 스테이블코인
        ↓
[CCTP] → 스테이블코인 ↔ USDC 교환 (체인 간 이동)
        ↓
[해외 수취인] → USDC 수령 → 현지 환전
```

- CCTP는 브리지 없이 체인 간 이동 → 보안 리스크 감소
- 다날이 USDC 생태계에 Fiat 온램프로 진입하는 가장 현실적인 경로

---

## 5. GENIUS Act가 Circle에 미치는 영향 — 원문 기반 해석

> *"The GENIUS Act establishes a federal framework requiring: 1:1 reserve backing with high-quality liquid assets, monthly public disclosures of reserve composition, BSA/AML compliance, prohibition on yield payments to stablecoin holders..."*
> — White House Fact Sheet, 2025-07-18

**Circle에 유리한 조항:**
- 1:1 준비금 + 월별 공시 → Circle이 이미 준수 중 → 진입장벽 강화
- 적격 스테이블코인은 증권 아님 → SEC 규제 불확실성 해소
- 연방 감독 체계 → 기관 투자자 참여 허들 감소

**Circle에 불리한 조항:**
- 보유자 이자 지급 금지 → 스테이블코인 DeFi 활용 제한
- 연방 감독 비용 증가

**OCC Charter (2025-12-12):**
> *"Circle receives conditional approval from OCC for national trust charter — enabling Circle to offer custody, payments, and reserve management under federal banking supervision."*
> — Circle Press Release, 2025-12-12

**해석:** OCC 연방 은행 감독 하에 들어온 Circle은 글로벌 파트너 협력 논의에서 "연방 규제 준수 기관"으로 포지셔닝 가능 → 다날과의 공식 파트너십 계약 신뢰도 ↑

---

## 6. 다날 관점 투자·파트너십 결론

### 6.1 협력 시 다날이 얻는 것

| 항목 | 내용 | 중요도 |
|---|---|---|
| USDC 글로벌 결제 레일 | CCTP 기반 멀티체인 KRW→USDC 정산 경로 | ★★★ |
| 규제 신뢰성 | GENIUS Act 준수 + OCC charter → 기관 신뢰 | ★★★ |
| 금융기관 네트워크 | CPN 55개 금융기관 → 다날 글로벌 파트너 확장 | ★★☆ |
| 기술 인프라 | CCTP 오픈 API → 개발 비용 없이 글로벌 정산 연결 | ★★☆ |

### 6.2 협력 시 리스크

| 리스크 | 내용 | 완화 방안 |
|---|---|---|
| 금리 의존 수익 구조 | Circle 수익성 압박 시 파트너십 조건 악화 가능 | 계약에 고정 API 수수료 조항 삽입 |
| Coinbase 집중도 | Circle-Coinbase 관계 악화 시 USDC 유동성 영향 | 다중 스테이블코인 전략 병행 |
| USDT 시장 지배력 | USDC 생태계 성장 제한 → 다날 SC 정산 SaaS 한계 | USDT 호환 구조 병행 검토 |
| 미국 규제 세부규정 확정 대기 | GENIUS Act 시행 세부규정 확정 대기 → 기관 채택 속도 변수 | 규제 가이던스 모니터링으로 선점 |

### 6.3 최종 판단

**협력 권고: ✅ 파트너십 검토 (★★★)**

Circle은 다날 SC 정산 SaaS의 **글로벌 출구(off-ramp)**로 가장 현실적인 옵션이다. CCTP API는 오픈 소스 수준으로 접근 가능하며, OCC Charter 획득으로 기관 신뢰도가 상승했다. 금리 하락으로 Circle 수익성이 압박받는 시기가 오히려 다날이 협력 조건을 유리하게 협상할 수 있는 타이밍이다.

**단기 액션:**
1. CCTP API 연동 기술 PoC (개발자 문서 기반, 비용 없음)
2. Circle Business Development 팀 접촉 (Fiat 온램프 파트너십 제안)
3. IPO(NYSE: CRCL) 후 공식 파트너십 체결 검토

---

## 7. 핵심 영문 원문 인용 모음

| 주제 | 원문 인용 | 출처 |
|---|---|---|
| 수익 의존도 | *"Our revenue is significantly dependent on interest rates."* | Circle S-1, 2025-06-04 |
| USDC 성장 | *"USDC onchain transaction volume reached $11.9 trillion."* | Circle FY2025, 2026-02-25 |
| CPN 현황 | *"55 financial institutions onboarded and 74 in the pipeline."* | Circle FY2025, 2026-02-25 |
| CCTP 설명 | *"CCTP enables USDC to be burned on one chain and minted on another."* | Circle Developer Docs |
| GENIUS Act 영향 | *"Prohibition on yield payments to stablecoin holders."* | White House, 2025-07-18 |
| OCC Charter | *"Circle receives conditional approval from OCC for national trust charter."* | Circle Press Release, 2025-12-12 |
| 경쟁 리스크 | *"Tether's dominance could limit USDC's growth."* | Circle S-1, 2025-06-04 |

---

*작성: 2026-03-08*
*원문 소스: Circle S-1 (SEC EDGAR, 2025-06-04), Circle FY2025 Press Release (2026-02-25), White House GENIUS Act Fact Sheet (2025-07-18), Circle OCC Press Release (2025-12-12)*
