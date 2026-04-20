"""Tests for heading-boundary chunker."""

from __future__ import annotations

from doc_memory.chunk.chunker import Chunk, chunk_document
from doc_memory.parser.base import Document, Page


class TestChunker:
    def test_chunks_by_heading(self) -> None:
        doc = Document(
            source="test.md",
            pages=[
                Page(number=1, content="# Intro\n\nHello\n\n## Methods\n\nExperiment"),
            ],
        )
        chunks = chunk_document(doc)
        assert len(chunks) >= 2
        assert all(isinstance(c, Chunk) for c in chunks)
        headings = [c.heading_path[-1] for c in chunks]
        assert "Intro" in headings
        assert "Methods" in headings

    def test_oversized_chunk_splits(self) -> None:
        long_text = "This is a sentence. " * 200
        doc = Document(
            source="test.md",
            pages=[Page(number=1, content=f"# Big\n\n{long_text}")],
        )
        chunks = chunk_document(doc, max_tokens=100)
        assert len(chunks) > 1
        for chunk in chunks:
            # Allow some tolerance for token counting
            assert len(chunk.content.split()) <= 150

    def test_chunk_has_metadata(self) -> None:
        doc = Document(
            source="test.md",
            pages=[Page(number=1, content="# Title\n\nContent here")],
        )
        chunks = chunk_document(doc)
        assert chunks[0].page_number == 1
        assert chunks[0].heading_path == ["Title"]

    def test_empty_document(self) -> None:
        doc = Document(source="empty.md", pages=[])
        chunks = chunk_document(doc)
        assert chunks == []
