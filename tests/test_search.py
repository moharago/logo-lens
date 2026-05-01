"""API 통합 테스트 (실제 MongoDB/ES 없이 mock 사용)."""
import io
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from PIL import Image

from src.api.main import app


def make_png(color: tuple[int, int, int] = (255, 0, 0)) -> bytes:
    img = Image.new("RGB", (64, 64), color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture(autouse=True)
def mock_ensure_index():
    with patch("src.api.main.ensure_index", new_callable=AsyncMock):
        yield


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
@patch("src.api.main.ingest_logo", new_callable=AsyncMock, return_value="abc123")
async def test_upload_logo(mock_ingest):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/logos",
            files={"file": ("logo.png", make_png(), "image/png")},
            data={"brand_name": "TestBrand", "tags": "red, test"},
        )
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] == "abc123"
    assert body["tags"] == ["red", "test"]
    mock_ingest.assert_called_once()


@pytest.mark.asyncio
@patch("src.api.main.search_similar", new_callable=AsyncMock)
async def test_search_returns_results(mock_search):
    mock_search.return_value = [
        {"_id": "abc123", "brand_name": "TestBrand", "tags": ["red"], "score": 0.98}
    ]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/search",
            files={"file": ("query.png", make_png(), "image/png")},
            params={"top_k": 5},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 1
    assert body["results"][0]["brand_name"] == "TestBrand"


@pytest.mark.asyncio
@patch("src.api.main.search_similar", new_callable=AsyncMock, return_value=[])
async def test_search_top_k_clamped(mock_search):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/search",
            files={"file": ("query.png", make_png(), "image/png")},
            params={"top_k": 999},
        )
    assert resp.status_code == 200
    # top_k는 20으로 클램핑되어 search_similar에 전달돼야 함
    _, kwargs = mock_search.call_args
    assert kwargs["top_k"] == 20
