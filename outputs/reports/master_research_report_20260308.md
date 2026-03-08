# B2B 스테이블코인 결제 인프라 섹터 리서치 리포트
## 다날 핀테크·디지털자산 투자팀을 위한 투자·파트너십 기회 분석

> 작성일: 2026-03-08 | 분석 기준: 2026년 3월 시장 데이터
> 목적: 다날의 전략 방향에 부합하는 투자·파트너십 대상 선별 및 의사결정 근거 제공

---

## Executive Summary

**핵심 테제:**
> GENIUS Act(2025-07 시행)·MiCA(2024-06 시행)로 스테이블코인 B2B 결제 인프라가 제도권에 편입되고 있다. B2B 스테이블코인 payments는 이미 연 $36B 규모로 검증됐으며(Artemis, 2025-05), Visa·Circle 등 기관이 본격 참여 중이다. 현재 거시 레짐은 **Goldilocks with sticky inflation** — 성장은 유지되지만 금리 인하는 제한적이어서, 준비금 이자 의존형보다 **결제 수수료 SaaS 모델**이 구조적으로 유리하다. 다날의 KRW SaaS·x402 전략은 이 전환의 최적 타이밍에 위치하며, 이를 가속할 투자·파트너십 대상 선별이 현재 가장 중요한 의사결정이다.

**분석 범위:** 거시 레짐 → 다날 전략 이해 → 섹터 선택 → 기업 스크리닝 → 심층 IM → 권고

**의사결정 권고 요약:**

| 기업 | 역할 | 권고 | 우선순위 |
|---|---|---|---|
| **Circle** | 글로벌 USDC 인프라 파트너 | 파트너십 검토 | ★★★ |
| **Ripple** | 크로스보더 정산·KSC 인프라 | 관심 → IPO 후 검토 상향 | ★★☆ |
| **슈퍼블록** | 국내 L1 기술 파트너 (기투자) | 후속 모니터링 + 2차 투자 검토 | ★★☆ |

> 데이터 CSV: 완료 (`outputs/csv/` — 시나리오 모델·스코어카드·거시지표 3종)
> PPT 프레젠테이션: 준비 중 (`outputs/ppt/` — `[TODO]`)

---

## Part 1. 거시 환경 분석 — "왜 지금인가"

### 1.1 현재 거시 레짐: **Goldilocks with Sticky Inflation** (확신: Medium)

순수 Goldilocks라기보다, 성장·고용은 버티는데 코어 인플레와 제조업 비용 압력이 끈적한 **변형 Goldilocks**다. Overheating도 Stagflation도 Recession도 아니며, 연착륙이 유지되지만 금리 인하 폭은 제한된다.

**확장 지표 수렴 판단 (8개):**

| 지표 | 최신값 | 해석 | 출처 |
|---|---|---|---|
| CPI (미국) | **2.4% YoY** (Jan 2026) | Dec 2.7%에서 둔화 — 디스인플레 재개 | BLS, 2026-02-13 |
| Core CPI | **2.5% YoY** (Jan 2026) | 헤드라인보다 낮으나 2% 상회 지속 | BLS, 2026-02-13 |
| Core PCE | **3.0% YoY** (Dec 2025) | Fed 목표 2% 대비 +1.0%p — 인하 제약 | BEA, 2026-02-20 |
| 실업률 U-3 | **4.4%** (Feb 2026) | 큰 악화 없음 — 노동시장 연착륙 유지 | BLS, 2026-03-06 |
| ISM 제조업 PMI | **52.4** (Feb 2026) | 50 상회 확장 국면, 단 Prices Index **70.5** 급등 | ISM, 2026-03-02 |
| DXY | **97.81** (2026-03-02) | 약세 후 반등, 강달러 재가속보다 박스권 복귀 | Investing.com, 2026-03-02 |
| Fed Dot Plot | **2026년말 중간값 3.4%** | 현 3.50~3.75% → 연내 인하 1회 내외 컨센서스 | Fed SEP, 2025-12-10 |
| 5Y BEI | **2.42%** (2026-02-13) | 시장 기대 2%대 초중반 — 목표 안착 미확인 | FRED, 2026-02-13 |
| USD/KRW | **1,445.97** | 원화 약세 지속 — 수출형 SaaS에 유리 | FRED, 2026-03-06 |

```
              인플레이션 高 (Core PCE ≥ 3%)   인플레이션 低 (Core PCE < 2.5%)
성장 ↑  →      Overheating                    ★ Goldilocks (pure)
성장 ↓  →      Stagflation                    Recession

현재 위치: Goldilocks with sticky inflation
  → 성장(ISM 52.4, 실업 4.4%) ↑ + 인플레(Core PCE 3.0%) 끈적 → 중간지대
```

**레짐 시나리오 확률:**
- Goldilocks with sticky inflation 지속 (65%): 관세 협상 진전·Core PCE 완만 둔화 가정
- Overheating 전환 (20%): ISM Prices 70.5 → 관세발 물가 재상승 + 금리 인하 중단 시
- Recession 가능성 (15%): 관세 충격 전면화 → 기업 투자 위축 + 고용 급락 시

### 1.2 Goldilocks가 스테이블코인 섹터에 갖는 의미

Goldilocks 환경에서 스테이블코인 섹터에는 두 가지 상반된 힘이 작동한다:

| 힘 | 방향 | 영향 대상 |
|---|---|---|
| 위험선호 회복 → 디지털자산 채택 ↑ | 긍정 | 결제 볼륨 증가 |
| 금리 하락 → 준비금 이자수익 ↓ | 부정 | Circle·Tether 수익성 |
| 달러 약세 기조 | 긍정 | 크로스보더 스테이블코인 수요 |

**핵심 인사이트:** 금리 하락은 **준비금 이자 의존형 모델**(Tether, Circle)에는 역풍이지만, **결제 수수료 기반 SaaS 모델**(다날 방향)에는 중립~긍정이다. 이것이 다날이 지금 KRW SaaS 모델로 전환해야 하는 거시적 근거다.

### 1.3 규제 환경: 3단계 명확화 — 미국 완료 / EU 집행 중 / 한국 미확정

| 규제 | 지역 | 현재 상태 | 다날 영향 |
|---|---|---|---|
| **GENIUS Act** | 미국 | ✅ **2025-07-18 서명 완료** (시행 중) | Circle·Coinbase 등 글로벌 파트너 신뢰도·기관 채택 가속 |
| **MiCA** | EU | ✅ **2024-06-30부터 시행** (집행·라이선싱 본격화) | Circle France EMT 준수, SG-FORGE 참여 — 국제 스탠다드 형성 |
| **디지털자산기본법** | 한국 | ⚠️ **2단계법 핵심 내용 미확정** | 스테이블코인 발행 주체·컨소시엄 구성 아직 미결 |

**GENIUS Act 핵심 조항 (영문 원문 기반):**
> *"The GENIUS Act establishes a federal framework for payment stablecoins: 1:1 reserve backing, monthly reserve disclosures, BSA/AML compliance, federal supervision for large issuers (>$10B), state supervision for smaller issuers, payment stablecoins not classified as securities."*
> — White House Fact Sheet, 2025-07-18

- Circle: OCC 조건부 national trust charter 승인 (2025-12) — GENIUS 준수 인프라 강화
- Visa 미국 내 USDC 연간 정산: **$3.5B** (2025-12-16) — 기관 채택 선행지표
- Coinbase: "USDC 기관 결제·유동성 관리·PSP 채택 가속" (2025-07-21)

**MiCA 집행 현황:**
- Circle France: USDC·EURC MiCA-compliant EMT 발행 (2024-07-01, Circle)
- SG-FORGE: EUR/USD CoinVertible MiCA 준수 발행 (2025-11-27, Deutsche Börse)
- EBA 전환 유예 **2026-03-02 종료** — 비준수 사업자 퇴출 진행 중
- 한국 기업 MiCA 라이선스 취득: 공개 사례 **미확인** (공개 근거 부족)

**한국 디지털자산기본법 현황:**
- 2026년 3월 기준 시행령 미확정, 2단계법 핵심 쟁점 미결
- FSC 공식 입장: 스테이블코인 발행 주체·주주구성·은행 컨소시엄 "확정된 바 없음" (2026-01-06/07)
- 최근 당국 톤: 발행 허용 확대보다 **이용자 보호·내부통제 강화** 방향 (빗썸 오지급 사고 후, 2026-02-09)

**결론:** 미국은 규제 완료 → 기관 채택 가속화 단계, EU는 라이선싱·집행 본격화 단계, 한국은 제도 설계 미완 단계. 3개 지역의 규제 성숙도 차이가 **다날의 기회이자 리스크**다. 한국 제도 공백이 지속되는 동안 글로벌 파트너와의 기술 협력을 선점하는 것이 최적 전략이다.

### 1.4 반론 및 대응

이 분석의 테제에 제기될 수 있는 주요 반론과 그에 대한 대응:

| 반론 | 대응 |
|---|---|
| "스테이블코인은 아직 기업 결제에서 비주류다" | 맞다. 그러나 B2B 스테이블코인 결제 YoY +733%(2025, Modern Treasury)로 급증 중. 비주류이기 때문에 선점 가치가 있다. |
| "Circle·Ripple이 다날과 협력할 이유가 없다" | Circle의 CCTP는 개방형 API다. 한국 PG 1위 사업자가 유일한 KRW 온램프를 제공한다면 Circle 입장에서도 한국 시장 진입 채널이 된다. 실제로 2026-03 다날×바이낸스페이×Circle 3자 협력 공식 발표. |
| "규제 리스크가 여전히 크다" | 동의한다. 단, 규제 방향이 '금지'에서 '표준화'로 전환된 것이 핵심이다. 리스크가 아니라 **규제 불확실성의 방향**이 바뀌었다. |
| "Goldilocks가 끝나면 전략이 무의미해진다" | Overheating 전환 시에도 결제 수수료 SaaS 모델은 금리 중립이다. Recession 시에는 투자 속도를 조정하면 된다. 레짐 의존도가 낮은 사업 모델이다. |
| "다날 자체 재무가 악화되고 있다" | 사실이다. 2025 3Q 누적 매출 -17.1% YoY, **순손실 -1627% YoY** (스테이블코인 선투자 비용). 이는 성장 투자 비용이며, KBW 시연 완료·MOU 다수 체결을 감안하면 **투자 집행 단계의 정상적 적자**로 해석 가능. 단, 1~2년 내 상용화 실증이 없으면 지속 불가능한 구조. |

### 1.5 이 분석을 틀리게 만드는 조건 (반증 가능 신호)

분석의 신뢰도는 **틀렸을 때를 미리 정의할 수 있는가**에 달려 있다:

- 🔴 **테제 무효 신호**: GENIUS Act 시행 후 주요 스테이블코인 발행사 규제 위반·제도 붕괴 + 한국 디지털자산기본법 시행 2년 이상 지연 → 규제 명확화 논거 붕괴
- 🔴 **전략 재검토 신호**: Fed 긴급 인상 재개(FF ≥ 5%) → Stagflation 전환 → 기업 디지털자산 투자 위축
- 🟡 **속도 조정 신호**: 슈퍼블록 x402 PoC 1년 내 상용화 실패 → 기술 파트너십 타당성 재평가
- 🟢 **테제 강화 신호**: USDC 시총 $100B 돌파 + 국내 KRW 스테이블코인 첫 상용 거래 성사
- 🟡 **다날 재무 모니터링**: 2025 3Q 누적 순손실 -1627% YoY 지속 중. 2026년 연간 실적에서 스테이블코인 수익 첫 인식 여부가 투자 판단의 핵심 신호

---

## Part 2. 다날의 전략 방향 이해 — "무엇을 찾는가"

### 2.1 다날의 3축 전략

다날은 국내 1위 PG 사업자로서의 캐시카우를 기반으로 3개 성장 축을 구축하고 있다:

| 축 | 사업 | 현황 |
|---|---|---|
| **KRW 스테이블코인 SaaS** | 원화 스테이블코인(KSC) 발행·정산 플랫폼 | **KBW 2025 실제 시연 완료** (2025-09-23) |
| **x402** | AI 에이전트 자동 결제 프로토콜 (HTTP 402 기반) | 기술검증 단계 (슈퍼블록 공동 개발) |
| **PCI (페이코인)** | 편의점 4사 연동 블록체인 결제 | 운영 중 — 누적 사용자 **320만명**, 가맹점 **15만개** |

**3개 계열사 분업 구조 (2025-10 확정):**

| 계열사 | 역할 |
|--------|------|
| 다날 (본사) | PG 인프라·가맹점망·AML 컴플라이언스 |
| 다날핀테크 | SaaS 플랫폼 개발·AI 인프라(Sahara AI)·Paycoin 앱 |
| 페이프로토콜 | 스테이블코인 발행 주체(법인 분리 예정)·유통 플랫폼 |

출처: 더벨 2025-10-15, The Fintech Times 2025

**KBW 2025 시연 의의 (2025-09-23):**
> 참가자가 실제로 원화를 KSC로 mint하고 행사장 내 가맹점 바코드 결제 수행. "전략" 단계를 넘어 **실물 결제 PoC 검증** 완료.
> — 뉴시스, 2025-09-24

**추가 협력 파트너십 (2025년 하반기):**
- Mastercard 네트워크 연결 (2025-06) — 스테이블코인 결제 구조 구축
- Axelar 파트너십 — 크로스체인 결제·무역송금·환전 연계
- iM금융지주 MOU — 디지털 금융 자산 공동 개발
- OK저축은행 MOU — 동남아(인도네시아·캄보디아) 진출

### 2.2 전략 전환의 필연성

기존 PG 사업의 구조적 한계가 전환을 강제하고 있다:

```
기존 PG 모델          vs.     스테이블코인 SaaS 모델
─────────────────────────────────────────────────
결제망: 카드사 VAN 의존        자체 온체인 정산 레일
수수료: 카드사 공유             수수료 전액 내재화
정산: T+1 ~ T+3 지연           실시간(수초 내) 가능
크로스보더: 환전·송금 비용      스테이블코인으로 우회
AI 에이전트: 지원 불가          x402로 자동화 가능
```

**전환을 강제하는 3가지 외부 충격:**

1. **AI 에이전트 경제의 부상**: 2025년 이후 AI 에이전트가 인간 대신 결제·구매를 실행하는 사례 급증. 카드 기반 PG는 "카드 소지자 인증" 전제이므로 에이전트 결제 구조적 불가. x402(HTTP 402 기반) 프로토콜이 유일한 현실적 대안.

2. **크로스보더 결제 수요 증가**: 전통 SWIFT 송금(T+1~3, 수수료 $15~$50)에 비해 스테이블코인 크로스보더(수초, 수수료 $0.01 미만)는 이미 B2B 거래에서 채택 중. 한국 수출기업의 정산 다변화 수요로 연결.

3. **국내 PG 시장 성숙**: 국내 PG 시장 점유율 경쟁은 가격 경쟁 위주. 마진 방어보다 새로운 수익원 발굴이 전략적 과제. KRW SaaS는 기존 가맹점망(다날 PG)에 온체인 정산 레이어를 얹는 구조 — 신규 투자 대비 수익 효율이 높다.

### 2.3 투자·파트너십 대상의 조건

위 전략을 기반으로, 다날이 찾는 기업의 조건은 다음과 같이 도출된다:

| 조건 | 구체적 의미 |
|---|---|
| **기술 보완성** | 다날이 없는 기술 (L1 블록체인, 글로벌 USDC 네트워크, 크로스보더 레일) 보유 |
| **규제 대응력** | GENIUS Act·MiCA·한국법 준수 가능한 컴플라이언스 체계 |
| **시장 접근성** | 다날이 진입하려는 시장(글로벌, 크로스보더, AI 결제)으로의 경로 제공 |
| **협력 현실성** | 독점 계약 불가·기술 공유 의지·다날과의 이해 충돌 최소 |

---

## Part 3. 섹터 선택 논거 — "왜 이 섹터인가"

### 3.1 섹터 정의: B2B 스테이블코인 결제 인프라

개인 간(P2P) 암호화폐 거래가 아닌, **기업 간(B2B) 스테이블코인 기반 정산·결제 인프라**를 타깃 섹터로 설정한다.

구체적 범위:
- 스테이블코인 발행·관리 인프라 (Circle, Tether 등)
- 블록체인 정산 레일 (Ripple/XRPL, Over Protocol 등)
- 결제 미들웨어·API SaaS (람다256, 헥슬란트 등)
- AI 에이전트 결제 프로토콜 (x402 계열)

### 3.2 시장 규모 (TAM → SAM → SOM)

**글로벌 TAM — 3단계 정제 방법론 (Flagship Advisory Partners 기준):**

> "Raw on-chain volume에서 비유기적 거래를 제거해야 실질적 결제 시장 규모가 산출된다." — Flagship Advisory Partners, 2025

```
총 온체인 스테이블코인 거래액: $46T/년
    ↓ [Step 1] 80% 비유기적 제거 (봇·차익거래·DeFi 순환)
$9.2T
    ↓ [Step 2] 98% 비결제 거래 제거 (투기·담보·청산·브리지)
$140~195B (실질 결제용 스테이블코인 TAM)
    ↓ [Step 3] B2B 비중 분리 (전체의 ~18~26%)
$36B/년 (B2B 스테이블코인 결제 실증 규모, Artemis 2025-05)
```

> ⚠️ "$36B"는 단순 시총 기반이 아닌, 실제 결제 흐름을 측정한 **Observed Flow** 수치다. 이 방법론이 시총($263B) 대비 현실적 TAM을 제공한다.

> "TAM의 본질은 '스테이블코인 시총'이 아니라 '기업 정산 흐름의 대체 가능 금액'이다." — Codex 리서치, 2026-03-08

| 시장/지표 | 규모 | 출처 |
|---|---|---|
| **B2B 스테이블코인 payments (annual run-rate)** | **$36B/년** | Artemis/Castle Island/Dragonfly, 2025-05 |
| B2B 성장 추이 | 2023년 초 월 <$1억 → 2025년 월 $30억+ | Artemis, 2025-05 |
| 전체 stablecoin payments run-rate | $72.3B/년 (B2B가 최대 카테고리) | Artemis, 2025-05 |
| Visa USDC settlement (미국 annualized) | **$3.5B/년** | Visa, 2025-12-16 |
| Visa stablecoin settlement (CEMEA) | $2.5B+/년 | Visa, 2025-12-17 |
| Circle CPN annualized volume | **$5.7B/년** (금융기관 55개) | Circle FY2025, 2026-02-25 |
| USDC on-chain transaction volume | **$11.9T/년** | Circle FY2025, 2026-02-25 |
| 글로벌 B2B 크로스보더 결제 (전체) | ~$40T/년 | McKinsey Global Payments, 2024 |

**SAM — 한국 기업의 접근 가능 시장:**

| 시장 | 규모 | 근거 |
|---|---|---|
| 국내 전자결제(PG) 시장 | ~50조원/년 | 한국은행 지급결제 통계, 2024 |
| 국내 B2B 크로스보더 결제 (무역 정산) | ~300조원/년 | 관세청 통관 기준 추정 |
| 국내 디지털자산 B2B 정산 전환 가능분 | ~2,000~5,000억원/년 | 규제 명확화 이후 전환 추정, 업계 |

**SOM — 다날의 획득 가능 시장 (3년 목표 기준):**

- 다날 PG 가맹점망 활용 → 가맹점의 5~10% KRW SaaS 전환
- Take rate 0.1~0.3% (Visa/Circle 수준 참고) → SOM ~수백억원/년
- Ripple ODL 방식 크로스보더 prefunding 수요까지 포함 시 확장 가능

> ⚠️ SOM은 내부 가맹점·거래량 데이터 없이 산출한 추정치. 실제 인턴 업무 중 정밀화 필요.
> 수익화 구조: **정산 흐름 × take rate + SaaS 고정요금 + FX/유동성 수익** (issuer economics와 PSP economics 혼용 금지)

### 3.3 섹터를 선택한 이유: 3가지 수렴

1. **거시 수렴**: Goldilocks + 규제 명확화 → 지금이 선점 타이밍
2. **전략 수렴**: 다날 3축(KRW SaaS·x402·PCI) 모두 이 섹터와 직결
3. **경쟁 수렴**: 한국 PG 사업자 중 이 섹터에 포지셔닝한 기업이 사실상 다날뿐

---

## Part 4. 기업 스크리닝 — "누구를 선택했는가"

### 4.1 스크리닝 기준

| 기준 | 가중치 | 측정 방법 |
|---|---|---|
| 다날 전략 적합도 | 40% | KRW SaaS·x402·PCI 3축 중 보완하는 축의 수 |
| 기술 보완성 | 30% | 다날이 내재화하지 못한 기술 보유 여부 |
| 규제 대응력 | 20% | GENIUS Act·MiCA·한국법 준수 체계 |
| 협력 현실성 | 10% | 기존 관계·이해 충돌 수준 |

### 4.1-b 국내 KRW 스테이블코인 경쟁 지형 (Tiger Research, 2025)

현재 screen_stablecoin 분석은 글로벌 경쟁사 중심으로 작성되어 있으나, 다날의 직접 경쟁자는 국내 KRW 스테이블코인 추진 기업들이다:

| 플레이어 | 체인 | 현황 | 다날 대비 |
|---------|------|------|---------|
| BDACS + 우리은행 | Avalanche | KRW1 테스트넷, Circle ARC 네트워크 연계 | 은행 백킹 → 신뢰도 高, 속도 低 |
| 네이버-두나무 | 카이아(Kaia) | 부산 동백전 연계, 네이버파이낸셜 지갑 | 대형 플랫폼 + 지자체 채널 |
| 카카오뱅크 | 미정 | 2025년 중 KRW 스테이블코인 목표 공표 | 2,400만 사용자 기반 강점 |
| 프랙스-IQ | 미정 | KRW 스테이블코인 개발 중 | 알고리즘 스테이블코인 경험 |

**다날의 차별화 포인트:**
- 15만 가맹점 + 320만 페이코인 사용자 = **기존 결제 인프라 기반 즉시 전환 가능**
- 경쟁사 대부분 발행·유통 단계; 다날은 **실물 결제 시연(KBW 2025) 완료**
- 은행 컨소시엄 의존 없이 독립 발행 가능한 구조(페이프로토콜)

**규제 갈등 구도:** 비은행(디지털자산으로 분류, 민간 발행 허용) vs 은행(통화로 분류, 은행만 발행) 이원화. 한은·기재부·금융위 3자 규제 권한 경쟁 중 — 결론 따라 다날 포지셔닝이 유리/불리로 급변 가능.

출처: Tiger Research, *Korea Stablecoin Landscape*, 2025

---

### 4.2 롱리스트 → 숏리스트

**롱리스트 (검토 후보군 8개):**

| 기업 | 탈락/선택 | 이유 |
|---|---|---|
| **Circle** | ✅ 선택 | USDC 글로벌 인프라 + GENIUS Act 수혜 최대 수혜 + CCTP 기술 보완 |
| **Ripple** | ✅ 선택 | XRPL = 다날 KSC 기반 인프라, RLUSD+ODL 수직 통합 |
| **슈퍼블록** | ✅ 선택 | 기투자 완료, Over Protocol L1 = 국내 스테이블코인 정산 레이어 |
| **Tether** | ❌ 탈락 | 준비금 불투명·공식 파트너십 채널 부재·규제 리스크 잔존 |
| **Coinbase** | ❌ 탈락 | 미국 중심 규제 환경·한국 PG 연계 구조적 어려움·규모 격차 |
| **토스** | ❌ 제외 | 경쟁사 (투자 대상 아님) → 별도 경쟁사 분석으로 활용 |
| **람다256** | ❌ 탈락 | 카카오 계열 종속·독립 협력 어려움 |
| **카이아 (Kaia)** | ❌ 탈락 | 스테이블코인 B2B 정산 특화 부족·라인-야후 계열 이해 충돌 가능 |

### 4.3 선별 기업 스코어카드

| 기업 | 전략 적합도 (40%) | 기술 보완성 (30%) | 규제 대응 (20%) | 협력 현실성 (10%) | 종합 |
|---|---|---|---|---|---|
| Circle | 38 | 28 | 19 | 8 | **93/100** |
| Ripple | 32 | 27 | 17 | 7 | **83/100** |
| 슈퍼블록 | 30 | 25 | 14 | 10 | **79/100** |

---

## Part 5. 심층 분석 요약 — "무엇을 발견했는가"

> 전문 분석: `im_Circle_20260306.md`, `im_Ripple_20260306.md`, `im_슈퍼블록_20260308.md` 참조

### 5.1 Circle — 글로벌 인프라 파트너 관점

**포지션:** USDC 발행사·CCTP 멀티체인 정산 인프라 운영. 2024년 흑자 전환 후 NYSE IPO(CRCL) 진행 중.

**다날과의 연결:**
- CCTP를 통해 KRW SaaS의 글로벌 USDC 정산 레일 활용 가능
- GENIUS Act 수혜로 미국 기관 채택 확대 → USDC 네트워크 효과 강화
- 단, Circle 수익의 **~97%가 준비금 이자** (S-1 실제치) → 금리 1% 하락 시 $441M 손실 (S-1 명시)
- Coinbase 수익 배분: 매출의 53%($908M) — 파트너 집중 리스크 존재

**투자 의견:** ☑ 검토 (상장 후 기관 접근 가능 시 관심 상향)

**핵심 리스크:** USDC vs. USDT 점유율 격차 (28.8% vs. 69.5%) — 네트워크 효과 역전 가능성 제한적

*(상세: im_Circle_20260306.md)*

### 5.2 Ripple — 크로스보더 정산 인프라 관점

**포지션:** XRPL 기반 크로스보더 결제 + RLUSD 스테이블코인 + ODL(On-Demand Liquidity) 수직 통합. 다날 KSC의 기반 인프라.

**다날과의 연결:**
- 다날 KSC(페이코인 스테이블코인)는 XRPL 위에서 운영 → Ripple은 기술 인프라 파트너
- SEC 소송 종결 + XRP ETF 가능성 → 기관 자금 유입 시 Ripple 기업가치 재평가
- RLUSD-KSC 공존 시나리오: RLUSD는 글로벌 정산, KSC는 국내 결제로 역할 분리

**투자 의견:** ☑ 관심 (비상장 — IPO 타임라인 확정 후 검토 상향)

**핵심 리스크:** 비상장 재무 접근 제한 + XRP 가격 변동성 → ODL 비용 구조 불안정

*(상세: im_Ripple_20260306.md)*

### 5.3 슈퍼블록 — 국내 L1 기술 파트너 (기투자 완료)

**포지션:** 오버 프로토콜(Over Protocol) 경량 L1 블록체인 운영사. 2025-12 다날 전략적 투자 완료. 김재윤 CEO 다날핀테크 CSO 겸직.

**다날 투자 배경 분석:**
- 다날의 KRW SaaS에 스테이블코인 정산 레이어(Over Protocol) 제공
- x402 AI 에이전트 결제 미들웨어 공동 개발 추진
- 오버플렉스 600만+ 사용자 → 온보딩 파이프라인 활용 가능

**투자 의견 (사후 검증):** 전략적 투자 타당성 확인 ✅ — PoC 진행 상황 모니터링 필요

**핵심 리스크:** $OVER FDV $3.8M으로 토큰 유동성 극히 낮음 + 매출 ~3.6억원(추정) — BM 증명이 핵심 관문

*(상세: im_슈퍼블록_20260308.md)*

---

## Part 6. 의사결정 권고

### 6.1 종합 권고

| 기업 | 권고 | 액션 | 이유 |
|---|---|---|---|
| **Circle** | 파트너십 검토 | CCTP API 연동 PoC 제안 | IPO 후 공식 파트너십 채널 형성 + USDC 네트워크 편입이 KRW SaaS 글로벌화 가장 빠른 경로 |
| **Ripple** | 관심 유지 | IPO 모니터링 + KSC-XRPL 연동 심화 | 이미 기반 인프라로 연결됨 — 전략적 심화는 IPO 이후 재무 투명성 확보 후 결정 |
| **슈퍼블록** | 후속 관리 | PoC 마일스톤 KPI 설정 + 상용화 시 2차 투자 검토 | 기투자 완료 — 의사결정 이슈는 "얼마나 더"이며, 이는 x402·KSC PoC 성과에 달려 있음 |

### 6.2 모니터링 지표

**Circle:**
- [ ] IPO(CRCL) 공모가 확정 → 밸류에이션 적정성 재평가
- [ ] CCTP v2 출시 일정 및 한국 원화 연동 계획 공표 여부
- [ ] GENIUS Act 최종 통과 → 기관 USDC 채택 속도

**Ripple:**
- [ ] IPO 타임라인 공식 발표
- [ ] RLUSD 시총 성장 추이 (현재 소규모)
- [ ] 다날 KSC 메인넷 거래량 기반 XRPL 트랜잭션 비용 추이

**슈퍼블록:**
- [ ] x402 미들웨어 상용화 거래량 (첫 공시 시점 중요)
- [ ] Over Protocol 생태계 TVL 성장 (DeFiLlama 추적 시작 시점)
- [ ] 오버 프로토콜 메인넷 안정성 (런칭 2024-12-11 이후 9개월차)

### 6.3 다음 액션

1. **단기 (1개월)**: Circle CCTP 개발자 문서 분석 → 다날 KRW SaaS 연동 기술 타당성 검토
2. **중기 (3개월)**: Ripple IPO 모니터링 → 상장 후 IM 업데이트 + 투자 의견 재검토
3. **장기 (6개월)**: 슈퍼블록 x402 PoC 성과 기반 → 2차 투자 여부 의사결정

---

## Appendix

### A. 데이터 출처

**거시지표 (영어 원문):**

| 데이터 | 출처 | 날짜 |
|---|---|---|
| CPI 2.4% YoY | [BLS CPI Jan 2026](https://www.bls.gov/news.release/archives/cpi_02132026.htm) | 2026-02-13 |
| Core PCE 3.0% | [BEA Personal Income and Outlays Dec 2025](https://www.bea.gov/news/2026/personal-income-and-outlays-december-2025) | 2026-02-20 |
| 실업률 4.4% | [BLS Employment Situation Feb 2026](https://www.bls.gov/news.release/archives/empsit_03062026.htm) | 2026-03-06 |
| ISM PMI 52.4 | [ISM Feb 2026 Manufacturing](https://www.ismworld.org/supply-management-news-and-reports/news-publications/inside-supply-management-magazine/blog/2026/2026-03/ism-pmi-reports-roundup-february-2026-manufacturing/) | 2026-03-02 |
| Fed Dot Plot 3.4% | [Fed SEP Dec 2025](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20251210.htm) | 2025-12-10 |
| 5Y BEI 2.42% | [FRED T5YIE](https://fred.stlouisfed.org/series/T5YIE) | 2026-02-13 |
| DXY 97.81 | Investing.com | 2026-03-02 |

**규제 (영어 원문):**

| 데이터 | 출처 | 날짜 |
|---|---|---|
| GENIUS Act 서명 | [White House Fact Sheet](https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-president-donald-j-trump-signs-genius-act-into-law/) | 2025-07-18 |
| Circle OCC charter | [Circle Press Release](https://www.circle.com/en/pressroom/circle-receives-conditional-approval-from-occ-for-national-trust-charter) | 2025-12-12 |
| Coinbase on GENIUS Act | [Coinbase Blog](https://www.coinbase.com/blog/the-genius-act-passed-here-is-what-it-means-for-usdc) | 2025-07-21 |
| Circle MiCA compliance | [Circle Press Release](https://www.circle.com/pressroom/circle-is-first-global-stablecoin-issuer-to-comply-with-mica-eus-landmark-crypto-law) | 2024-07-01 |
| EBA 전환 유예 종료 | [EBA Press Release](https://www.eba.europa.eu/publications-and-media/press-releases/eba-advises-national-authorities-actions-take-end-transition-period-under-its-no-action-letter) | 2026-02-12 |
| FSC 스테이블코인 입장 | [FSC 설명자료](https://www.fsc.go.kr/no010102/85997) | 2026-01-06 |

**B2B 채택 데이터:**

| 데이터 | 출처 | 날짜 |
|---|---|---|
| B2B stablecoin $36B/년 | [Artemis Stablecoin Payments](https://www.stablecoin.fyi/) | 2025-05 |
| Visa USDC settlement $3.5B | [Visa US stablecoin settlement](https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-launches-stablecoin-settlement-in-the-united-states.html) | 2025-12-16 |
| Circle CPN $5.7B, USDC $11.9T | [Circle FY2025 Results](https://www.circle.com/en/pressroom/circle-reports-fourth-quarter-and-full-fiscal-year-2025-financial-results) | 2026-02-25 |
| Ripple RLUSD Payments | [Ripple Press](https://ripple.com/ripple-press/ripple-integrates-rlusd-into-ripple-payments-driving-enterprise-demand-and-utility/) | 2025-04-02 |

**기업 데이터:**

| 데이터 | 출처 | 날짜 |
|---|---|---|
| 슈퍼블록 투자 이력 | 한국경제, 플래텀 | 2021-09, 2023-02 |
| 다날-슈퍼블록 협력 | 머니투데이, 뉴스핌 | 2025-12-10 |
| 람다256 밸류에이션 | CoinDesk | 2021-12-16 |

### B. 참조 산출물

| 파일 | 내용 |
|---|---|
| `regime_report_20260306.md` | 거시 레짐 상세 분석 |
| `screen_stablecoin_20260306.md` | 스테이블코인 섹터 스크리닝 |
| `im_Circle_20260306.md` | Circle 10섹션 심층 IM |
| `im_Ripple_20260306.md` | Ripple 10섹션 심층 IM |
| `im_슈퍼블록_20260308.md` | 슈퍼블록 10섹션 심층 IM |
| `brief_20260306.md` | 주간 시장 브리핑 |

### C. 분석 방법론 및 한계

**방법론:**
| 분석 영역 | 방법 | 주요 소스 |
|---|---|---|
| 거시 레짐 판단 | 3개 지표(Fed Funds, 10Y-FF 스프레드, 위험선호) 수렴 → 2×2 매트릭스 | FRED, CoinGecko |
| 섹터 스크리닝 | 4개 기준 가중 점수제 (전략 적합도 40%, 기술 보완성 30%, 규제 20%, 협력 현실성 10%) | 공개 재무 데이터, 언론 보도 |
| IM 심층 분석 | 10섹션 구조화 보고서 (Executive Summary → 다날 전략 연결) | Perplexity 리서치, SEC 공시, 국내 언론 |
| 밸류에이션 | 피어 비교(EV/Revenue) + 토큰 FDV 기반 하한선 추정 | CoinGecko, CoinMarketCap, 업계 데이터 |

**분석 한계 (투명하게 명기):**
1. **비공개 재무 데이터**: 슈퍼블록·Ripple 등 비상장사의 실제 재무는 접근 불가 — 추정치·참고치 사용
2. **거시 지표 제한**: 현재 3개 신호(FRED 자동 수집) 기반 — CPI, Core PCE, PMI 등 추가 지표 반영 시 정밀도 향상 가능
3. **내부 데이터 부재**: 다날 가맹점 수·거래량·SaaS 전환율 등 내부 데이터 없이 SOM 추정 — 실제 인턴 업무 중 보완 가능
4. **시장 예측의 불확실성**: 규제 통과 일정, 기술 상용화 속도는 예측 범위 밖 — 시나리오 확률은 정성적 판단

### D. 산출물 현황

**완료:**
- `outputs/csv/kwrw_stablecoin_scenario_20260308.csv` ✅ — KRW SaaS 수익 시나리오 27개 (3규제×3전환율×3take rate)
- `outputs/csv/screening_scorecard_20260308.csv` ✅ — 기업 스크리닝 스코어카드 7개사 (100점 척도)
- `outputs/csv/macro_snapshot_20260308.csv` ✅ — 거시지표 스냅샷 9개 (BLS·BEA·ISM·Fed·FRED 출처)
- `outputs/reports/circle_s1_analysis_20260308.md` ✅ — Circle SEC S-1 영문 원문 직독 분석

**진행 중/예정:**
- `outputs/ppt/danal_research_deck_20260308.pptx` — PPT 프레젠테이션 *[TODO]*
- `outputs/csv/stablecoin_market_20260308.csv` — 스테이블코인 시장 데이터 *[TODO]*
- `outputs/reports/macro_deepdive_20260308.md` — 거시 심화 분석 *[TODO]*
- `outputs/reports/regulation_update_20260308.md` — GENIUS Act·MiCA·한국법 규제 현황 상세 *[TODO]*

---

*작성: 2026-03-08 | 분석 도구: Claude Sonnet 4.6 (설계·편집) + Codex gpt-5.4 (데이터 리서치)*
*이 리포트는 다날 핀테크·디지털자산 투자팀의 의사결정 지원을 목적으로 작성된 내부 연구 문서입니다.*
