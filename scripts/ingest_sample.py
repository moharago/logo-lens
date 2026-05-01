#!/usr/bin/env python3
"""샘플 로고를 생성해 MongoDB + Elasticsearch에 적재하는 스크립트."""
import asyncio
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.elastic import ensure_index, get_client as get_es
from src.db.mongo import get_client as get_mongo
from src.ingestion.pipeline import ingest_logo

SAMPLES = [
    {"brand_name": "RedCircle",      "tags": ["red", "circle"],    "color": (220, 50, 50),   "shape": "circle"},
    {"brand_name": "BlueSquare",     "tags": ["blue", "square"],   "color": (50, 100, 220),  "shape": "square"},
    {"brand_name": "GreenTriangle",  "tags": ["green", "triangle"],"color": (50, 180, 80),   "shape": "triangle"},
    {"brand_name": "OrangeCircle",   "tags": ["orange", "circle"], "color": (230, 140, 30),  "shape": "circle"},
    {"brand_name": "PurpleSquare",   "tags": ["purple", "square"], "color": (130, 60, 200),  "shape": "square"},
    {"brand_name": "CyanDiamond",    "tags": ["cyan", "diamond"],  "color": (0, 190, 200),   "shape": "diamond"},
]


def make_logo(color: tuple[int, int, int], shape: str, size: int = 224) -> Image.Image:
    img = Image.new("RGB", (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    pad = size // 7

    if shape == "circle":
        draw.ellipse([pad, pad, size - pad, size - pad], fill=color)
    elif shape == "square":
        draw.rectangle([pad, pad, size - pad, size - pad], fill=color)
    elif shape == "triangle":
        draw.polygon([(size // 2, pad), (size - pad, size - pad), (pad, size - pad)], fill=color)
    elif shape == "diamond":
        cx, cy = size // 2, size // 2
        draw.polygon([(cx, pad), (size - pad, cy), (cx, size - pad), (pad, cy)], fill=color)

    return img


async def main() -> None:
    print("ES 인덱스 초기화...")
    await ensure_index()

    for sample in SAMPLES:
        image = make_logo(sample["color"], sample["shape"])
        mongo_id = await ingest_logo(image, sample["brand_name"], sample["tags"])
        print(f"  [{sample['shape']:10s}] {sample['brand_name']:20s} -> {mongo_id}")

    print(f"\n{len(SAMPLES)}개 샘플 로고 적재 완료.")

    await get_es().close()
    get_mongo().close()


if __name__ == "__main__":
    asyncio.run(main())
