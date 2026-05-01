import asyncio
import io
from datetime import UTC, datetime

from bson.binary import Binary
from PIL import Image

from src.config import settings
from src.db.elastic import get_client as get_es
from src.db.mongo import get_collection
from src.embeddings.clip import embed_image


async def ingest_logo(
    image: Image.Image,
    brand_name: str,
    tags: list[str] | None = None,
) -> str:
    """로고를 MongoDB(원본)와 Elasticsearch(벡터)에 저장하고 MongoDB _id를 반환."""
    # 1. 임베딩 (CPU-bound → 스레드풀)
    embedding = await asyncio.to_thread(embed_image, image)

    # 2. 이미지 원본을 PNG bytes로 직렬화
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    image_bytes = Binary(buf.getvalue())

    # 3. MongoDB 저장
    col = get_collection()
    doc = {
        "brand_name": brand_name,
        "tags": tags or [],
        "image": image_bytes,
        "created_at": datetime.now(UTC),
    }
    result = await col.insert_one(doc)
    mongo_id = str(result.inserted_id)

    # 4. Elasticsearch 색인 (MongoDB _id를 ES doc id로 동일하게 사용)
    es = get_es()
    await es.index(
        index=settings.es_index,
        id=mongo_id,
        document={
            "mongo_id": mongo_id,
            "brand_name": brand_name,
            "tags": tags or [],
            "embedding": embedding,
        },
    )

    return mongo_id
