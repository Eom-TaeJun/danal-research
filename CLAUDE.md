# danal — 운영 규칙

> 세션 시작 시 `INTENT.md` → `AGENTS.md` → `spec.md` 순서로 읽을 것.  
> 이 파일은 빠른 참조용. 아키텍처 원칙은 `AGENTS.md`, 방법론은 `spec.md` 참조.

## 실행 명령
```bash
python main.py --brief              # 주간 브리핑
python main.py --im "Circle"        # IM 초안
python main.py --screen stablecoin  # 섹터 스크리닝 (레짐 분석 포함)
python main.py --analyze            # 레짐 판단만 단독 실행
```

## Agents
| 에이전트 | 모델 | 역할 |
|---------|------|------|
| `danal-lead` | sonnet | 요청 해석 + 결과 품질 검토 + 위임 |
| `research-agent` | sonnet | IM 리서치 + None 값 보완 |
| `collect-agent` | haiku | 시장 데이터 수집 (brief/screen) |
| `macro-analyst` | sonnet | 레짐 판단 + 다날 비즈니스 함의 |
| `sanity-checker` | haiku | 품질 게이트 (None값·출처·다날함의) |

에이전트 계약 상세: `agents/contracts.json`  
하니스 아키텍처: `AGENTS.md`  
방법론 원천: `spec.md`

## Skill Activation Mapping
| 작업 | 활성화 스킬 |
|------|-----------|
| IM 작성 | `im-draft` + `danal-context` |
| 주간 브리핑 | `weekly-brief` |
| 스크리닝 | `stablecoin-market` |
| 레짐·매크로 분석 | `danal-context` |

## 고정 원칙
- 출력은 반드시 `outputs/` 하위에만
- `skills/` 파일은 수정하지 않음 (읽기 전용 도메인 지식)
- `src/` 파일 1개당 100줄 이하 유지
- 수치는 반드시 출처와 날짜 명기 — `"(CoinGecko, 2026-03)"`
- `None` 값이 남은 리포트는 완성이 아님

## API 키 (환경변수)
- `FRED_API_KEY` — 거시경제 지표
- `PERPLEXITY_API_KEY` — 뉴스·기업 리서치
