from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.configs import DEFAULT_COLLECTION_NAME, QDRANT_URL

client = QdrantClient(url=QDRANT_URL)


def create_collection(collection_name: str = DEFAULT_COLLECTION_NAME, vector_size: int = 384) -> None:
    names = [c.name for c in client.get_collections().collections]
    if collection_name not in names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def add_vector(collection_name: str, points: list[dict[str, Any]]) -> None:
    qpoints = [
        PointStruct(
            id=p["id"],
            vector=p["vector"],
            payload=p["payload"],
        )
        for p in points
    ]
    client.upsert(collection_name=collection_name, points=qpoints)


def search_vectors(query_vector: list[float], collection_name: str = DEFAULT_COLLECTION_NAME, limit: int = 5) -> list[dict]:
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
        with_payload=True,
    )
    output = []
    for i, item in enumerate(results, start=1):
        payload = item.payload or {}
        payload["similarity_score"] = item.score
        payload["search_rank"] = i
        output.append(payload)
    return output
