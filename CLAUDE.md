# logo-lens

로고 이미지 유사도 검색 시스템. 로고를 업로드하면 유사한 로고를 찾아주는 서비스.

## Stack

- **Python** — 메인 언어
- **MongoDB** — 로고 메타데이터 저장
- **Elasticsearch** — 벡터 유사도 검색 (kNN)
- **FastAPI** — API 서버 (예정)

## Project Structure (예정)

```
logo-lens/
├── CLAUDE.md
├── pyproject.toml
├── src/
│   ├── ingestion/      # 로고 수집 및 임베딩 파이프라인
│   ├── search/         # 유사도 검색 로직
│   ├── api/            # FastAPI 엔드포인트
│   └── db/             # MongoDB / ES 클라이언트
├── scripts/            # 데이터 적재 등 유틸 스크립트
└── tests/
```

## Git

- git 작업(commit, push, branch 생성 등)은 자동으로 하지 말고 항상 먼저 사용자에게 확인할 것

## Conventions

- Python 패키지 관리는 `uv` 사용
- 타입 힌트 필수, 가능하면 `pydantic` 모델 사용
- 환경변수는 `.env` 파일로 관리 (`.env.example` 유지)
- 테스트는 `pytest` 사용

## Key Concepts

- 로고 이미지 → 임베딩 벡터 추출 → Elasticsearch kNN 인덱스에 저장
- MongoDB에는 로고 원본 URL, 브랜드명, 태그 등 메타데이터 저장
- ES 문서의 `_id`와 MongoDB `_id`를 동일하게 유지하여 조인

## Environment Variables

```
MONGODB_URI=
ES_HOST=
ES_API_KEY=          # 또는 ES_USERNAME / ES_PASSWORD
```
