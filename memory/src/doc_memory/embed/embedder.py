"""Sentence-transformers embedding wrapper."""

from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "all-MiniLM-L6-v2"


class Embedder:
    """Thin wrapper around SentenceTransformer for encoding text."""

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        """Encode texts to normalized embedding vectors."""
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return np.asarray(embeddings, dtype=np.float32)
