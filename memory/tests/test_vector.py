"""Tests for FAISS vector store."""

from __future__ import annotations

import json

import numpy as np
import pytest

from doc_memory.retrieve.vector import ChunkMetadata, VectorStore


class TestVectorStore:
    def test_add_and_search(self) -> None:
        store = VectorStore(dimension=3)
        vectors = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32)
        metadata = [
            ChunkMetadata(chunk_id=0, page_number=1, heading_path=["A"], content="a"),
            ChunkMetadata(chunk_id=1, page_number=2, heading_path=["B"], content="b"),
        ]
        store.add(vectors, metadata)

        query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
        results = store.search(query, k=1)
        assert len(results) == 1
        assert results[0].metadata.content == "a"

    def test_search_returns_scores(self) -> None:
        store = VectorStore(dimension=3)
        vectors = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
        metadata = [
            ChunkMetadata(chunk_id=0, page_number=1, heading_path=["A"], content="a"),
        ]
        store.add(vectors, metadata)

        query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
        results = store.search(query, k=1)
        assert results[0].score > 0.9  # near-perfect match

    def test_save_and_load(self, tmp_path: pytest.TempPathFactory) -> None:
        store = VectorStore(dimension=3)
        vectors = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
        metadata = [
            ChunkMetadata(chunk_id=0, page_number=1, heading_path=["A"], content="a"),
        ]
        store.add(vectors, metadata)
        store.save(str(tmp_path))

        loaded = VectorStore.load(str(tmp_path))
        query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
        results = loaded.search(query, k=1)
        assert len(results) == 1
        assert results[0].metadata.content == "a"

    def test_empty_store_search(self) -> None:
        store = VectorStore(dimension=3)
        query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
        results = store.search(query, k=1)
        assert results == []
