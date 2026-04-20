"""FAISS IndexFlatIP vector store with metadata."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import faiss
import numpy as np

INDEX_FILE = "index.faiss"
METADATA_FILE = "metadata.jsonl"


@dataclass
class ChunkMetadata:
    """Metadata stored alongside each vector."""

    chunk_id: int
    page_number: int
    heading_path: list[str] = field(default_factory=list)
    content: str = ""


@dataclass
class SearchResult:
    """A single search result with score and metadata."""

    score: float
    metadata: ChunkMetadata


class VectorStore:
    """FAISS IndexFlatIP with L2-normalized vectors for cosine similarity."""

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self._metadata: list[ChunkMetadata] = []

    def add(self, vectors: np.ndarray, metadata: list[ChunkMetadata]) -> None:
        """Add L2-normalized vectors with metadata."""
        vectors = np.ascontiguousarray(vectors, dtype=np.float32)
        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self._metadata.extend(metadata)

    def search(self, query: np.ndarray, k: int = 10) -> list[SearchResult]:
        """Search for top-k similar vectors."""
        if self.index.ntotal == 0:
            return []
        query = np.ascontiguousarray(query, dtype=np.float32)
        faiss.normalize_L2(query)
        k = min(k, self.index.ntotal)
        scores, indices = self.index.search(query, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            results.append(SearchResult(score=float(score), metadata=self._metadata[idx]))
        return results

    def save(self, directory: str) -> None:
        """Persist index and metadata to disk."""
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / INDEX_FILE))
        with open(path / METADATA_FILE, "w") as f:
            for meta in self._metadata:
                f.write(json.dumps(asdict(meta)) + "\n")

    @classmethod
    def load(cls, directory: str) -> VectorStore:
        """Load index and metadata from disk."""
        path = Path(directory)
        index = faiss.read_index(str(path / INDEX_FILE))
        store = cls(dimension=index.d)
        store.index = index
        with open(path / METADATA_FILE) as f:
            for line in f:
                data = json.loads(line)
                store._metadata.append(ChunkMetadata(**data))
        return store
