---
name: im-draft
description: 핀테크 / 디지털자산 기업 투자 검토 보고서(IM) 초안 작성. 기업명 입력 시 시장 조사 → 10섹션 IM 구조 작성까지 자동화. Triggers on "IM 작성", "투자 검토", "im draft", "investment memo", 기업명 + "분석".
argument-hint: [기업명]
---

# IM Draft (Investment Memorandum)

내부 투자 의사결정용 검토 보고서 초안. 외부 IR 자료가 아닌 팀 내부 판단 문서.  
**인턴 역할**: 섹션 2·3·4·5·7·8·9 초안 작성. 섹션 1·6은 시니어 검토 후 완성.

## 실행

```bash
python src/research.py --company "[기업명]"
python src/report.py --type im --company "[기업명]"
```

출력: `outputs/reports/im_[기업명]_YYYYMMDD.md`

## IM 10섹션 구조

```
# Investment Memorandum — [기업명]
> 작성일: YYYY-MM-DD | 초안 (Draft)

## 1. Executive Summary
[투자 논리 3-5문장]
**투자 의견:** ☐ 관심  ☐ 검토  ☐ 보류

## 2. Company Overview
**사업 모델:** [어떻게 수익을 내는가]
**핵심 제품/서비스:** [목록]

## 3. 경영진
| 이름 | 직책 | 주요 이력 |

## 4. Market Opportunity
**시장 규모:** [TAM/SAM 추정치 + 출처]
**경쟁사:** [목록]

## 5. 재무 실적
| 연도 | 매출 | 순이익 | 마진 |
![Revenue Trend](../charts/revenue_trend_YYYYMMDD.png)

## 6. Investment Thesis
**Bull Case:** (3개 이상)
**Bear Case:** (3개 이상)

## 7. 밸류에이션
| 지표 | 회사 | 동종업계 평균 |

## 8. Key Risks
[규제·경쟁·사이버·시장 리스크]

## 9. 최근 동향
[최근 6개월 내 주요 이벤트 3건]

## 10. 다음 단계
- [ ] 확인 필요 항목
- [ ] 미팅 요청 여부
```

## 작성 원칙

- 인턴 초안 섹션 (2·3·4·5·7·8·9): 사실 기반, None 없이
- 재무 수치: 반드시 출처 명기 — `"(Bloomberg, 2026-02)"`
- 확인 불가 수치: `None` 아닌 `"확인 필요"` 또는 `"—"` 기재
- Bull/Bear: 균형 있게 — 단점 숨기지 말 것
- 차트: 재무 실적에는 `revenue_trend_*.png` 임베드 시도
- 분량: 3-5페이지 (초안 기준)
- 상세 지침: `references/im-structure.md` 참조
