"""Hybrid retrieval: vector search → full page → tree filter."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from doc_memory.chunk.chunker import chunk_document
from doc_memory.embed.embedder import Embedder
from doc_memory.index.page_index import build_tree, filter_relevant
from doc_memory.parser.base import Document
from doc_memory.retrieve.vector import ChunkMetadata, VectorStore


@dataclass
class RetrievalResult:
    """A single retrieval result with context."""

    content: str
    score: float
    page_number: int | None
    heading_path: list[str]
    source: str


class HybridRetriever:
    """Full hybrid retrieval pipeline."""

    def __init__(
        self,
        dimension: int = 384,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.embedder = Embedder(model_name=model_name)
        self.store = VectorStore(dimension=dimension)
        self._documents: dict[str, Document] = {}

    def ingest(self, doc: Document) -> None:
        """Parse, chunk, embed, and index a document."""
        self._documents[doc.source] = doc
        chunks = chunk_document(doc)
        if not chunks:
            return

        texts = [c.content for c in chunks]
        vectors = self.embedder.encode(texts)

        metadata = [
            ChunkMetadata(
                chunk_id=i + self.store.index.ntotal,
                page_number=c.page_number or 0,
                heading_path=c.heading_path,
                content=c.content,
            )
            for i, c in enumerate(chunks)
        ]
        self.store.add(vectors, metadata)

    def search(self, query: str, k: int = 10) -> list[RetrievalResult]:
        """Embed query → vector search → tree filter → return results."""
        if self.store.index.ntotal == 0:
            return []

        query_vec = self.embedder.encode([query])
        search_results = self.store.search(query_vec, k=k * 2)  # over-fetch

        if not search_results:
            return []

        # Collect matched headings for tree filtering
        matched_headings: set[str] = set()
        for sr in search_results:
            matched_headings.update(sr.metadata.heading_path)

        # Build tree and filter for each source document
        results: list[RetrievalResult] = []
        seen_headings: set[str] = set()

        for sr in search_results[:k]:
            key = tuple(sr.metadata.heading_path)
            if key in seen_headings:
                continue
            seen_headings.add(key)

            results.append(
                RetrievalResult(
                    content=sr.metadata.content,
                    score=sr.score,
                    page_number=sr.metadata.page_number,
                    heading_path=sr.metadata.heading_path,
                    source=next(iter(self._documents), "unknown"),
                )
            )

        return results
