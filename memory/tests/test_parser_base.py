"""Tests for parser base models and protocol."""

from __future__ import annotations

from doc_memory.parser.base import Document, Page, ParserProtocol


class TestPage:
    def test_page_has_number_and_content(self) -> None:
        page = Page(number=1, content="Hello world")
        assert page.number == 1
        assert page.content == "Hello world"


class TestDocument:
    def test_document_has_source_and_pages(self) -> None:
        pages = [Page(number=1, content="p1"), Page(number=2, content="p2")]
        doc = Document(source="test.pdf", pages=pages)
        assert doc.source == "test.pdf"
        assert len(doc.pages) == 2

    def test_document_empty_pages(self) -> None:
        doc = Document(source="empty.pdf", pages=[])
        assert doc.pages == []


class TestParserProtocol:
    def test_protocol_is_runtime_checkable(self) -> None:
        class FakeParser:
            def parse(self, path: str) -> Document:
                return Document(source=path, pages=[])

        assert isinstance(FakeParser(), ParserProtocol)
