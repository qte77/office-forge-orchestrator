"""Tests for hybrid retrieval pipeline."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

from doc_memory.parser.base import Document, Page
from doc_memory.retrieve.hybrid import HybridRetriever, RetrievalResult
from doc_memory.retrieve.vector import ChunkMetadata, SearchResult


class TestHybridRetriever:
    def test_ingest_creates_index(self) -> None:
        mock_embedder = MagicMock()
        mock_embedder.encode.return_value = np.array(
            [[0.1, 0.2, 0.3]], dtype=np.float32
        )

        with patch("doc_memory.retrieve.hybrid.Embedder", return_value=mock_embedder):
            retriever = HybridRetriever(dimension=3)
            doc = Document(
                source="test.md",
                pages=[Page(number=1, content="# Title\n\nContent")],
            )
            retriever.ingest(doc)

        assert retriever.store.index.ntotal >= 1

    def test_search_returns_results(self) -> None:
        mock_embedder = MagicMock()
        mock_embedder.encode.return_value = np.array(
            [[0.5, 0.5, 0.0]], dtype=np.float32
        )

        with patch("doc_memory.retrieve.hybrid.Embedder", return_value=mock_embedder):
            retriever = HybridRetriever(dimension=3)
            doc = Document(
                source="test.md",
                pages=[Page(number=1, content="# Intro\n\nHello world")],
            )
            retriever.ingest(doc)
            results = retriever.search("hello", k=5)

        assert isinstance(results, list)
        assert all(isinstance(r, RetrievalResult) for r in results)

    def test_search_empty_index(self) -> None:
        mock_embedder = MagicMock()
        mock_embedder.encode.return_value = np.array(
            [[0.1, 0.2, 0.3]], dtype=np.float32
        )

        with patch("doc_memory.retrieve.hybrid.Embedder", return_value=mock_embedder):
            retriever = HybridRetriever(dimension=3)
            results = retriever.search("anything", k=5)

        assert results == []
