"""Tests for MarkItDown parser fallback."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from doc_memory.parser.base import Document


class TestMarkItDownParser:
    def test_import_error_when_markitdown_missing(self) -> None:
        with patch.dict("sys.modules", {"markitdown": None}):
            import importlib

            from doc_memory.parser import markitdown

            importlib.reload(markitdown)
            with pytest.raises(ImportError):
                markitdown.MarkItDownParser()

    def test_parse_returns_document_when_available(self) -> None:
        mock_mit_cls = MagicMock()
        mock_result = MagicMock()
        mock_result.text_content = "# Title\n\nSome text"
        mock_mit_cls.return_value.convert.return_value = mock_result

        with patch.dict(
            "sys.modules",
            {"markitdown": MagicMock(MarkItDown=mock_mit_cls)},
        ):
            import importlib

            from doc_memory.parser import markitdown

            importlib.reload(markitdown)
            parser = markitdown.MarkItDownParser()
            doc = parser.parse("/tmp/test.pdf")

        assert isinstance(doc, Document)
        assert doc.source == "/tmp/test.pdf"
