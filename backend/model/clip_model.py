from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from pathlib import Path
import torch
import numpy as np
from backend.model.downloader import get_model_path

_model = None
_processor = None

def _load_model():
    """Carrega o modelo CLIP na memória (apenas uma vez)."""
    global _model, _processor

    if _model is not None:
        return

    model_path = get_model_path()
    print("[model] Carregando modelo CLIP...")

    _processor = CLIPProcessor.from_pretrained(model_path)
    _model = CLIPModel.from_pretrained(model_path)
    _model.eval()

    print("[model] Modelo carregado.")


def get_text_embedding(text: str) -> list[float]:
    """Gera embedding vetorial a partir de um texto."""
    _load_model()

    inputs = _processor(text=[text], return_tensors="pt", padding=True)

    with torch.no_grad():
        embedding = _model.get_text_features(**inputs)

    embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding[0].numpy().tolist()


def get_image_embedding(image_path: Path) -> list[float]:
    """Gera embedding vetorial a partir de uma imagem."""
    _load_model()

    image = Image.open(image_path).convert("RGB")
    inputs = _processor(images=image, return_tensors="pt")

    with torch.no_grad():
        embedding = _model.get_image_features(**inputs)

    embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding[0].numpy().tolist()