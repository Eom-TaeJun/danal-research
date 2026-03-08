# SQLite / PostgreSQL 최신 동향 — 2026-02-15 이후

> 조사일: 2026-03-07 | 출처: sqlite.org, postgresql.org, GitHub, SitePoint

---

## SQLite 3.52.0 — 2026-03-11 릴리즈

### 핵심 변경

| 카테고리 | 내용 |
|---------|------|
| **ALTER TABLE 확장** | `NOT NULL`, `CHECK` 제약 조건 추가/제거 가능 (기존 불가) |
| **신규 JSON 함수** | `json_array_insert()`, `jsonb_array_insert()` 추가 |
| **QRF 라이브러리** | 인터랙티브 CLI 기본 출력이 유니코드 박스 문자 기반 표 형식으로 변경 |
| **집합 연산 최적화** | `EXCEPT`, `INTERSECT`, `UNION` 전체를 sort-and-merge 알고리즘 통일 |
| **JOIN 최적화** | star schema 대형 다방향 조인에서 조인 순서 선택 개선 |
| **API 추가** | `SQLITE_PREPARE_FROM_DDL` — 가상 테이블이 스키마에서 SQL 구문 안전하게 준비 가능 |
| **CLI** | `--timeout S` 옵션 추가, `.sql`/`.txt` 파일 인수 직접 실행 지원 |

### 직전 릴리즈 — 3.51.2 (2026-01-09)

- `jsonb_each()`, `jsonb_tree()` 추가 — 중첩 object/array 값을 JSONB로 반환

---

## PostgreSQL 18 — 2025-09-25 릴리즈 (18.1 → 18.2 패치 진행 중)

### 주요 신기능

| 카테고리 | 내용 |
|---------|------|
| **Virtual Generated Columns** | 읽기 시점 계산 — 저장 공간 절약, 이제 기본값 |
| **OR 조건 인덱스 최적화** | WHERE의 OR 조건에 인덱스 활용 가능 |
| **Temporal 제약 조건** | 범위 기반 PRIMARY KEY, UNIQUE, FK 제약 지원 |
| **OAuth 2.0 인증** | SSO 시스템 통합 간소화 |
| **RETURNING 확장** | INSERT/UPDATE/DELETE/MERGE에서 OLD, NEW 참조 가능 |
| **GIN 인덱스 병렬 빌드** | B-tree, BRIN에 이어 GIN도 병렬 구축 지원 |
| **버전 업그레이드 통계 유지** | 메이저 업그레이드 후 플래너 통계 보존 |

---

## 트렌드 — SQLite의 Edge 프로덕션 진입 (2026)

| 플랫폼 | 상태 |
|--------|------|
| **Cloudflare D1** | 글로벌 읽기 복제 GA |
| **Turso** | 임베디드 복제본 자동 동기화 |
| **LiteFS** | 안정화 완료 |

---

## 출처

- [SQLite Release 3.52.0](https://sqlite.org/draft/releaselog/3_52_0.html)
- [SQLite Release 3.51.2](https://www.sqlite.org/releaselog/3_51_2.html)
- [SQLite Release History](https://sqlite.org/changes.html)
- [PostgreSQL 18 Released](https://www.postgresql.org/about/news/postgresql-18-released-3142/)
- [PostgreSQL 18.2 Release Notes](https://www.postgresql.org/docs/release/18.2/)
- [Post-PostgreSQL: Is SQLite on the Edge Production Ready? (2026)](https://www.sitepoint.com/sqlite-edge-production-readiness-2026/)
- [sqlite/sqlite GitHub Releases](https://github.com/sqlite/sqlite/releases)
