"""MarkItDown parser — last-resort fallback."""

from __future__ import annotations

from doc_memory.parser.base import Document, Page

_AVAILABLE = True
try:
    from markitdown import MarkItDown
except ImportError:
    _AVAILABLE = False


class MarkItDownParser:
    """Parse documents via MarkItDown library."""

    def __init__(self) -> None:
        if not _AVAILABLE:
            msg = "markitdown is not installed. Install with: pip install markitdown"
            raise ImportError(msg)
        self._converter = MarkItDown()

    def parse(self, path: str) -> Document:
        result = self._converter.convert(path)
        content = result.text_content
        pages = [Page(number=1, content=content)] if content else []
        return Document(source=path, pages=pages)
