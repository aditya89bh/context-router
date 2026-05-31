"""Semantic relevance scoring."""
from __future__ import annotations

import hashlib
import re
from typing import Iterable, Protocol

import numpy as np


class EmbeddingModel(Protocol):
    def encode(self, texts: str | list[str]) -> np.ndarray: ...


class HashingEmbeddingModel:
    """Deterministic local fallback embedding model.

    It avoids network/model downloads in tests while preserving SemanticRouter behavior.
    Production users can pass a sentence-transformers model instead.
    """

    def __init__(self, dimensions: int = 256) -> None:
        self.dimensions = dimensions

    def encode(self, texts: str | list[str]) -> np.ndarray:
        single = isinstance(texts, str)
        values = [texts] if single else texts
        vectors = [self._embed(text) for text in values]
        arr = np.vstack(vectors)
        return arr[0] if single else arr

    def _embed(self, text: str) -> np.ndarray:
        vec = np.zeros(self.dimensions, dtype=np.float32)
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        for token in tokens:
            digest = hashlib.blake2b(token.encode(), digest_size=4).digest()
            idx = int.from_bytes(digest, "little") % self.dimensions
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        return vec if norm == 0 else vec / norm


def load_sentence_transformer(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingModel:
    """Load a sentence-transformers model.

    Kept separate so applications can opt into heavyweight semantic embeddings.
    """
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def cosine_similarity(query_embedding: np.ndarray, candidate_embeddings: np.ndarray) -> np.ndarray:
    query = np.asarray(query_embedding, dtype=np.float32)
    candidates = np.asarray(candidate_embeddings, dtype=np.float32)
    if candidates.ndim == 1:
        candidates = candidates.reshape(1, -1)
    query_norm = np.linalg.norm(query) or 1.0
    candidate_norms = np.linalg.norm(candidates, axis=1)
    candidate_norms[candidate_norms == 0] = 1.0
    return (candidates @ query) / (candidate_norms * query_norm)


def relevance_scores(query: str, texts: Iterable[str], model: EmbeddingModel | None = None) -> list[float]:
    model = model or HashingEmbeddingModel()
    text_list = list(texts)
    if not text_list:
        return []
    query_embedding = model.encode(query)
    candidate_embeddings = model.encode(text_list)
    scores = cosine_similarity(query_embedding, candidate_embeddings)
    return [float(max(0.0, min(1.0, score))) for score in scores]
