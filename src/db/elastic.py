from elasticsearch import AsyncElasticsearch, BadRequestError
from src.config import settings

_client: AsyncElasticsearch | None = None

# CLIP ViT-B/32 임베딩 차원
EMBEDDING_DIM = 512

INDEX_MAPPINGS = {
    "properties": {
        "mongo_id": {"type": "keyword"},
        "brand_name": {"type": "text"},
        "tags": {"type": "keyword"},
        "embedding": {
            "type": "dense_vector",
            "dims": EMBEDDING_DIM,
            "index": True,
            "similarity": "cosine",
        },
    }
}

INDEX_SETTINGS = {
    "number_of_shards": 1,
    "number_of_replicas": 0,
}


def get_client() -> AsyncElasticsearch:
    global _client
    if _client is None:
        _client = AsyncElasticsearch(settings.es_host)
    return _client


async def ensure_index() -> None:
    client = get_client()
    try:
        await client.indices.create(
            index=settings.es_index,
            mappings=INDEX_MAPPINGS,
            settings=INDEX_SETTINGS,
        )
    except BadRequestError as e:
        if e.error != "resource_already_exists_exception":
            raise
