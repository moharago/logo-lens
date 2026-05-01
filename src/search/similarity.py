import asyncio

from bson import ObjectId
from PIL import Image

from src.config import settings
from src.db.elastic import get_client as get_es
from src.db.mongo import get_collection
from src.embeddings.clip import embed_image


async def search_similar(image: Image.Image, top_k: int = 5) -> list[dict]:
    """이미지와 유사한 로고 top_k개를 반환."""
    embedding = await asyncio.to_thread(embed_image, image)

    es = get_es()
    resp = await es.search(
        index=settings.es_index,
        knn={
            "field": "embedding",
            "query_vector": embedding,
            "k": top_k,
            "num_candidates": top_k * 10,
        },
        size=top_k,
    )

    results = []
    col = get_collection()

    for hit in resp["hits"]["hits"]:
        mongo_id = hit["_id"]
        doc = await col.find_one(
            {"_id": ObjectId(mongo_id)},
            projection={"image": 0},  # 이미지 바이너리는 제외
        )
        if doc:
            doc["_id"] = mongo_id
            results.append({**doc, "score": round(hit["_score"], 4)})

    return results
