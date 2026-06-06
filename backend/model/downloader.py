from huggingface_hub import snapshot_download
from pathlib import Path
import os

MODEL_ID = "openai/clip-vit-base-patch32"
MODEL_DIR = Path(os.getenv("LOCALAPPDATA")) / "ImageBank" / "model"

def get_model_path() -> Path:
    """
    Retorna o caminho do modelo local.
    Se não existir, faz o download do Hugging Face.
    """
    if MODEL_DIR.exists() and any(MODEL_DIR.iterdir()):
        print(f"[model] Modelo já existe em: {MODEL_DIR}")
        return MODEL_DIR

    print(f"[model] Baixando modelo '{MODEL_ID}'...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=MODEL_DIR,
        ignore_patterns=["*.msgpack", "*.h5", "flax_model*"],
    )

    print(f"[model] Download concluído em: {MODEL_DIR}")
    return MODEL_DIR