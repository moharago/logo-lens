# Logo Lens

> 로고 이미지를 업로드하면 유사한 로고를 찾아주는 시각적 유사도 검색 시스템

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-005571?style=flat-square&logo=elasticsearch&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248?style=flat-square&logo=mongodb&logoColor=white)

---

## Overview

```
로고 이미지 업로드
      │
      ▼
 CLIP 임베딩 (512차원 벡터)
      │
      ├──► MongoDB  — 원본 이미지 + 메타데이터 저장
      │
      └──► Elasticsearch kNN — 벡터 유사도 인덱싱
                │
                ▼
         유사 로고 TOP 5 반환
```

---

## Tech Stack

| 레이어 | 기술 |
|--------|------|
| 임베딩 | CLIP `openai/clip-vit-base-patch32` (512차원, L2 정규화) |
| 벡터 검색 | Elasticsearch 8.x kNN (cosine similarity) |
| 메타데이터 | MongoDB 7 (이미지 원본 BSON Binary 저장) |
| API | FastAPI + Uvicorn |
| 프론트엔드 | React 18 + Vite |
| 패키지 관리 | uv |

---

## Project Structure

```
logo-lens/
├── src/
│   ├── config.py                  # 환경변수 설정 (pydantic-settings)
│   ├── api/
│   │   └── main.py                # FastAPI 엔드포인트
│   ├── db/
│   │   ├── mongo.py               # AsyncIOMotorClient
│   │   └── elastic.py             # AsyncElasticsearch + kNN 인덱스
│   ├── embeddings/
│   │   └── clip.py                # CLIP 임베딩 추출
│   ├── ingestion/
│   │   └── pipeline.py            # 로고 적재 파이프라인
│   └── search/
│       └── similarity.py          # kNN 유사도 검색
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── Header.jsx
│   │       ├── UploadSection.jsx   # 드래그앤드롭 업로드
│   │       ├── ResultsGrid.jsx     # 검색 결과 그리드
│   │       ├── LogoCard.jsx        # 유사도 카드
│   │       └── DetailsModal.jsx    # 메타데이터 팝업
│   └── vite.config.js             # /api/* → :8000 프록시
├── scripts/
│   └── ingest_sample.py           # 샘플 로고 6개 적재
├── tests/
│   └── test_search.py             # API 단위 테스트 (mock)
├── docker-compose.yml             # MongoDB + Elasticsearch
├── Dockerfile
├── pyproject.toml
└── .env.example
```

---

## Getting Started

### 1. 환경변수 설정

```bash
cp .env.example .env
```

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=logo_lens
ES_HOST=http://localhost:9200
ES_INDEX=logos
CLIP_MODEL=openai/clip-vit-base-patch32
```

### 2. 인프라 실행 (MongoDB + Elasticsearch)

```bash
docker compose up mongodb elasticsearch -d
```

### 3. 백엔드 실행

```bash
uv sync --dev
uvicorn src.api.main:app --reload
# → http://127.0.0.1:8000
```

### 4. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### 5. 샘플 데이터 적재 (선택)

```bash
python scripts/ingest_sample.py
```

6가지 도형 로고(원, 사각형, 삼각형, 마름모)를 자동 생성해 적재합니다.

---

## Docker (전체 스택)

```bash
docker compose up --build
# API  → http://localhost:8000
```

---

## API Endpoints

| Method | Path | 설명 |
|--------|------|------|
| `POST` | `/logos` | 로고 업로드 (MongoDB + ES 저장) |
| `GET` | `/logos/{id}` | 로고 메타데이터 조회 |
| `GET` | `/logos/{id}/image` | 로고 원본 이미지 반환 |
| `POST` | `/search` | 유사 로고 검색 (top_k 지정 가능) |
| `GET` | `/health` | 헬스체크 |

**검색 예시**

```bash
curl -X POST http://localhost:8000/search \
  -F "file=@logo.png" \
  -F "top_k=5"
```

```json
{
  "count": 5,
  "results": [
    {
      "_id": "664abc...",
      "brand_name": "Nike",
      "tags": ["swoosh", "sportswear"],
      "score": 0.9651
    }
  ]
}
```

---

## Architecture Notes

- **MongoDB `_id` = Elasticsearch doc `_id`** — 별도 조인 키 없이 동일 ID 사용
- 이미지 원본은 MongoDB에 BSON Binary(PNG bytes)로 저장, ES에는 벡터만 저장
- CLIP 임베딩은 L2 정규화 후 cosine similarity로 kNN 검색
- CPU-bound 임베딩 연산은 `asyncio.to_thread`로 스레드풀에서 실행

---

## Testing

```bash
pytest
```

mock 기반 단위 테스트 (MongoDB/ES 없이 실행 가능)

---

## License

MIT
