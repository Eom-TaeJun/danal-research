---
description: 핀테크 & 디지털자산 주간 브리핑 생성
argument-hint: ""
---

# /brief — 주간 브리핑 생성

**Use skill: `weekly-brief`** 를 로드하여 브리핑 구조와 작성 기준을 준비합니다.

## Step 1: 환경 확인

```bash
cd ~/projects/danal
echo "FRED: $([ -n \"$FRED_API_KEY\" ] && echo ✓ || echo ✗ MISSING)"
echo "PERPLEXITY: $([ -n \"$PERPLEXITY_API_KEY\" ] && echo ✓ || echo ✗ MISSING)"
```

FRED_API_KEY 없으면 거시경제 섹션 결측. PERPLEXITY_API_KEY 없으면 뉴스 섹션 결측.

## Step 2: 데이터 수집

```bash
python src/collect.py --mode brief
```

수집 후 확인:
- `outputs/context/snapshot_YYYYMMDD.json` 생성 여부
- `macro` 섹션: FEDFUNDS·DGS10·DEXKOUS 3개 필수
- `stablecoins` 섹션: USDT·USDC 최소 2개 이상

**Human-in-the-Loop Gate [1]**: 데이터 결측 여부 확인 후 진행

## Step 3: 보고서 작성

```bash
python src/report.py --type brief
```

`weekly-brief` 스킬의 브리핑 구조 4섹션을 따라 작성:
1. 거시경제 스냅샷 (지표 + WoW 변화)
2. 디지털자산 시장 (시총·도미넌스·BTC)
3. 이번 주 핵심 뉴스 3건 (함의 중심)
4. 투자 시사점 (다날 함의 포함)

**Human-in-the-Loop Gate [2]**: 다날 비즈니스 함의 단락 존재 확인

## Step 4: 품질 검증

`sanity-checker` 에이전트가 자동 활성화되어 3-Gate 검사 수행.
FAIL 항목 있으면 수정 후 재검사.

## 출력물

| 파일 | 경로 |
|------|------|
| 원본 데이터 | `outputs/context/snapshot_YYYYMMDD.json` |
| 브리핑 리포트 | `outputs/reports/brief_YYYYMMDD.md` |
