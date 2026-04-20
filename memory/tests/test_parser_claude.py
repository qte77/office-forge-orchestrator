"""Tests for Claude CLI parser."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from doc_memory.parser.base import Document
from doc_memory.parser.claude import ClaudeParser


class TestClaudeParser:
    def test_parse_returns_document(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "# Title\n\nSome content\n\n## Section 2\n\nMore content"

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            parser = ClaudeParser()
            doc = parser.parse("/tmp/test.pdf")

        assert isinstance(doc, Document)
        assert doc.source == "/tmp/test.pdf"
        assert len(doc.pages) >= 1
        mock_run.assert_called_once()

    def test_parse_raises_on_failure(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "error"

        with patch("subprocess.run", return_value=mock_result):
            parser = ClaudeParser()
            with pytest.raises(RuntimeError):
                parser.parse("/tmp/bad.pdf")
