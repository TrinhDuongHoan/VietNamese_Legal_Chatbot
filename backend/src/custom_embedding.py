from functools import lru_cache
from sentence_transformers import SentenceTransformer

from src.configs import EMBEDDING_MODEL_NAME


@lru_cache
def get_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_embedding(text: str) -> list[float]:
    clean = text.replace("\n", " ").strip()
    return get_model().encode(clean, normalize_embeddings=True).tolist()
