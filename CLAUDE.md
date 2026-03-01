# danal — 운영 규칙

## 실행 명령
```bash
python main.py --brief              # 주간 브리핑
python main.py --im "Circle"        # IM 초안
python main.py --screen stablecoin  # 스크리닝
```

## 고정 원칙
- 출력은 반드시 `outputs/` 하위에만
- skills/ 파일은 수정하지 않음 (도메인 지식, 읽기 전용)
- src/ 파일 1개당 100줄 이하 유지

## API 키 (환경변수)
- `FRED_API_KEY` — 거시경제 지표
- `PERPLEXITY_API_KEY` — 뉴스·기업 리서치
