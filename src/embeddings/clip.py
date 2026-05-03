import torch
import torch.nn.functional as F
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from src.config import settings

_model: CLIPModel | None = None
_processor: CLIPProcessor | None = None


def _load() -> None:
    global _model, _processor
    if _model is None:
        _processor = CLIPProcessor.from_pretrained(settings.clip_model)
        _model = CLIPModel.from_pretrained(settings.clip_model)
        _model.eval()


def embed_image(image: Image.Image) -> list[float]:
    """이미지를 CLIP 임베딩 벡터(512차원, L2 정규화)로 변환."""
    _load()
    inputs = _processor(images=image, return_tensors="pt")
    with torch.no_grad():
        vision_outputs = _model.vision_model(pixel_values=inputs["pixel_values"])
        features = _model.visual_projection(vision_outputs.pooler_output)
        features = F.normalize(features, dim=-1)
    return features.squeeze().tolist()
