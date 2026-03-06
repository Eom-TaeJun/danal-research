# AGENTS.md — Danal Research Harness

> **Vibe**: "Rigorous, Source-Cited, Danal-Connected."
> 우리는 단순히 리포트를 쓰는 것이 아니라, 다날 투자팀이 실제 의사결정에 쓸 수 있는 '근거'를 만드는 하니스를 구축한다.

## 🎯 Project Goal

다날 핀테크·디지털자산 투자팀의 **리서치 워크플로 자동화**.
FRED·CoinGecko·Perplexity 데이터를 조합해 주간 브리핑·IM·섹터 스크리닝을 자동 생성한다.

---

## 🏗️ Harness Architecture

```
사용자 요청
    ↓
danal-lead (조율·품질 검토)    ← 모든 워크플로의 시작점
    ├→ research-agent           (IM 리서치 + None 보완)
    ├→ collect-agent            (데이터 수집 + Brief/Screen)
    └→ macro-analyst            (레짐 판단 + 다날 함의)
         ↓
    sanity-checker              (품질 게이트 — None값·출처 최종 확인)
```

| 레이어 | 위치 | 역할 | 핵심 규칙 |
|-------|------|------|---------| 
| **데이터** | `src/*.py` | 수치 수집·계산만 | 해석·마크다운 없음 |
| **지식** | `.claude/skills/*/SKILL.md` | 도메인 지식, 해석 기준 | 코드 없음; 상세는 `references/`로 분리 |
| **에이전트** | `.claude/agents/*.md` | 자율 실행, Skills 조합 | Hub-Spoke 패턴 |
| **커맨드** | `.claude/commands/*.md` | 슬래시 진입점, 흐름 제어 | Skills/Agents 호출 지시 포함 |
| **훅** | `.claude/settings.json` | 세션 시작 자동화 | SessionStart 환경 확인 |
| **계약** | `agents/contracts.json` | 에이전트 역할 명세 | 새 에이전트 추가 시 반드시 등록 |

**핵심 원칙**: 지능은 Skills에 → 데이터는 Python에 → 조율은 Agents에.
**SKILL.md 크기**: 핵심 지침만 (~100줄), 상세 내용은 `references/` 서브파일로 분리.

---

## 🗺️ Skill Activation Mapping

| 작업 | 자동 활성화 스킬/에이전트 |
|------|----------------------|
| IM 초안 작성 (`--im`) | skill: `im-draft` → agent: `research-agent` |
| 주간 브리핑 (`--brief`) | skill: `weekly-brief` → agent: `collect-agent` |
| 섹터 스크리닝 (`--screen`) | skill: `stablecoin-market` → agent: `collect-agent` |
| 레짐 분석 (`--analyze`) | skill: `danal-context` → agent: `macro-analyst` |
| 품질 검증 | agent: `sanity-checker` (자동 활성) |

---

## 🚫 Critical Constraints (Never)

- **NEVER** `outputs/` 외부 저장 금지
- **NEVER** `.env` API KEY 노출 금지
- **NEVER** `SKILL.md`에 200줄 이상 작성 금지 — `references/` 서브파일로 분리
- **NEVER** 수치 출처(CoinGecko·FRED·Perplexity) 생략
- **NEVER** `None` 값이 남아있는 보고서를 완성으로 인정

## ✅ Mandatory (Must)

- **MUST** 모든 수치에 출처와 날짜 명기 — `"(CoinGecko, 2026-03)"`
- **MUST** IM 모든 섹션: 출처 없는 재무수치 → `"확인 필요"` 명기
- **MUST** 분석 마지막은 다날 비즈니스 함의로 마무리
- **MUST** 새 에이전트 추가 시 `agents/contracts.json`에도 등록

---

*Last Updated: 2026-03-06 | Based on Tech-Digest 2026-03-05 Standards*
