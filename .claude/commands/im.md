---
description: 투자 검토 보고서(IM) 초안 작성
argument-hint: "[기업명]"
---

# /im [기업명] — Investment Memorandum 초안

**Use skill: `im-draft`** 와 **`danal-context`** 를 로드하여 IM 구조와 다날 투자 맥락을 준비합니다.

## Step 1: 환경 확인

```bash
cd ~/projects/danal
echo "PERPLEXITY: $([ -n \"$PERPLEXITY_API_KEY\" ] && echo ✓ || echo ✗ MISSING)"
```

PERPLEXITY_API_KEY 없으면 리서치 불가 — 수동 입력으로 대체해야 함.

## Step 2: 기업 리서치

```bash
python src/research.py --company "$ARGUMENTS"
```

수집 후 확인:
- `outputs/context/research_[기업명]_YYYYMMDD.json` 생성 여부
- 재무 섹션: 매출·영업이익·밸류에이션 수치 존재 여부
- 경영진 섹션: 창업팀 2인 이상 정보

**Human-in-the-Loop Gate [1]**: 재무 수치 결측 여부 확인  
→ 결측 시 research-agent가 추가 웹 리서치로 보완

## Step 3: IM 초안 작성

```bash
python src/report.py --type im --company "$ARGUMENTS"
```

`im-draft` 스킬의 6섹션 구조를 따름:
1. Executive Summary + 투자 의견
2. Company Overview
3. Market Opportunity (TAM/SAM/SOM)
4. Investment Thesis (Bull 3개 / Bear 3개)
5. Key Risks & Mitigants
6. 다음 단계

**Human-in-the-Loop Gate [2]**: Bull/Bear 균형·재무 수치 출처 확인

## Step 4: None 값 보완

```bash
grep -n "None" outputs/reports/im_*.md | wc -l
```

`None` 이 남아있으면 research-agent를 재호출해 보완.
0이 될 때까지 반복.

## Step 5: 품질 검증

`sanity-checker` 에이전트가 3-Gate 자동 검사.
`danal-context` 스킬 기준으로 다날 비즈니스 함의 마지막 단락 확인.

## 출력물

| 파일 | 경로 |
|------|------|
| 리서치 데이터 | `outputs/context/research_[기업명]_YYYYMMDD.json` |
| IM 초안 | `outputs/reports/im_[기업명]_YYYYMMDD.md` |
