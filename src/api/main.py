import io
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from bson import ObjectId
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image

from fastapi.middleware.cors import CORSMiddleware

from src.db.elastic import ensure_index
from src.db.mongo import get_collection
from src.ingestion.pipeline import ingest_logo
from src.search.similarity import search_similar


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await ensure_index()
    yield


app = FastAPI(title="Logo Lens", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _open_image(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data)).convert("RGB")


# ── 업로드 ────────────────────────────────────────────────────────────────────

@app.post("/logos", status_code=201)
async def upload_logo(
    file: UploadFile = File(...),
    brand_name: str = Form(...),
    tags: str = Form(""),
) -> dict[str, Any]:
    """로고 이미지를 업로드해 MongoDB + Elasticsearch에 저장."""
    image = _open_image(await file.read())
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    mongo_id = await ingest_logo(image, brand_name, tag_list)
    return {"id": mongo_id, "brand_name": brand_name, "tags": tag_list}


# ── 조회 ─────────────────────────────────────────────────────────────────────

@app.get("/logos/{logo_id}")
async def get_logo(logo_id: str) -> dict[str, Any]:
    """로고 메타데이터 조회."""
    if not ObjectId.is_valid(logo_id):
        raise HTTPException(status_code=404, detail="Logo not found")
    col = get_collection()
    doc = await col.find_one(
        {"_id": ObjectId(logo_id)},
        projection={"image": 0},
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Logo not found")
    doc["_id"] = logo_id
    return doc


@app.get("/logos/{logo_id}/image")
async def get_logo_image(logo_id: str) -> Response:
    """로고 원본 이미지(PNG) 반환."""
    if not ObjectId.is_valid(logo_id):
        raise HTTPException(status_code=404, detail="Logo not found")
    col = get_collection()
    doc = await col.find_one({"_id": ObjectId(logo_id)}, projection={"image": 1})
    if not doc or "image" not in doc:
        raise HTTPException(status_code=404, detail="Logo not found")
    return Response(content=bytes(doc["image"]), media_type="image/png")


# ── 검색 ─────────────────────────────────────────────────────────────────────

@app.post("/search")
async def search(
    file: UploadFile = File(...),
    top_k: int = 5,
) -> dict[str, Any]:
    """업로드한 이미지와 유사한 로고 top_k개 반환."""
    top_k = min(max(top_k, 1), 20)
    image = _open_image(await file.read())
    results = await search_similar(image, top_k=top_k)
    return {"count": len(results), "results": results}


# ── 헬스체크 ──────────────────────────────────────────────────────────────────

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
