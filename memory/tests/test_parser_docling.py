"""Tests for Docling parser fallback."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from doc_memory.parser.base import Document


class TestDoclingParser:
    def test_import_error_when_docling_missing(self) -> None:
        with patch.dict("sys.modules", {"docling": None, "docling.document_converter": None}):
            # Re-import to trigger ImportError path
            import importlib

            from doc_memory.parser import docling

            importlib.reload(docling)
            with pytest.raises(ImportError):
                docling.DoclingParser()

    def test_parse_returns_document_when_available(self) -> None:
        mock_converter_cls = MagicMock()
        mock_result = MagicMock()
        mock_result.document.export_to_markdown.return_value = (
            "# Doc Title\n\nContent here"
        )
        mock_converter_cls.return_value.convert.return_value = mock_result

        with patch.dict(
            "sys.modules",
            {
                "docling": MagicMock(),
                "docling.document_converter": MagicMock(
                    DocumentConverter=mock_converter_cls
                ),
            },
        ):
            import importlib

            from doc_memory.parser import docling

            importlib.reload(docling)
            parser = docling.DoclingParser()
            doc = parser.parse("/tmp/test.pdf")

        assert isinstance(doc, Document)
        assert doc.source == "/tmp/test.pdf"
