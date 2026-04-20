"""Docling parser — fallback when Claude CLI unavailable."""

from __future__ import annotations

from doc_memory.parser.base import Document, Page

_AVAILABLE = True
try:
    from docling.document_converter import DocumentConverter
except ImportError:
    _AVAILABLE = False


class DoclingParser:
    """Parse documents via Docling library."""

    def __init__(self) -> None:
        if not _AVAILABLE:
            msg = "docling is not installed. Install with: pip install docling"
            raise ImportError(msg)
        self._converter = DocumentConverter()

    def parse(self, path: str) -> Document:
        result = self._converter.convert(path)
        content = result.document.export_to_markdown()
        pages = [Page(number=1, content=content)] if content else []
        return Document(source=path, pages=pages)
