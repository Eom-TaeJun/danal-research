---
description: 핀테크 / 디지털자산 섹터 스크리닝
argument-hint: "[stablecoin | fintech | defi | payments]"
---

# /screen [sector] — 섹터 스크리닝

**Use skill: `stablecoin-market`** (stablecoin 섹터) 또는 **`danal-context`** 를 로드하여 섹터 분석 기준을 준비합니다.

## Step 1: 환경 확인

```bash
cd ~/projects/danal
echo "FRED: $([ -n \"$FRED_API_KEY\" ] && echo ✓ || echo ✗ MISSING)"
echo "PERPLEXITY: $([ -n \"$PERPLEXITY_API_KEY\" ] && echo ✓ || echo ✗ MISSING)"
```

## Step 2: 섹터 데이터 수집

```bash
python src/collect.py --mode screen --sector "$ARGUMENTS"
```

수집 후 확인:
- `outputs/context/snapshot_YYYYMMDD.json` 생성 여부
- stablecoin 섹터: 시총 수치 + 도미넌스 있는지
- fintech 섹터: 규제 동향 뉴스 포함 여부

**Human-in-the-Loop Gate [1]**: 섹터 관련 데이터 충분한지 확인

## Step 3: 스크리닝 리포트 작성

```bash
python src/report.py --type screen --sector "$ARGUMENTS"
```

리포트 구조:
1. 섹터 현황 (시장 규모·성장률·경쟁 구도)
2. 주요 플레이어 (강점·약점 비교)
3. 규제 프레임워크 (확정/추진 중/미정 구분)
4. 투자 기회 (TAM 추정 + 진입 시나리오)
5. **다날 포지셔닝** — 이 섹터에서 다날의 차별화 포인트

**Human-in-the-Loop Gate [2]**: 다날 포지셔닝 단락의 구체성 확인  
→ 막연한 서술("기회가 있다")은 불합격 — 수치 기반 근거 필요

## Step 4: 품질 검증

`sanity-checker` 자동 활성화: None값·출처·다날 함의 3-Gate 검사.

## 출력물

| 파일 | 경로 |
|------|------|
| 섹터 데이터 | `outputs/context/snapshot_YYYYMMDD.json` |
| 스크리닝 리포트 | `outputs/reports/screen_[sector]_YYYYMMDD.md` |
