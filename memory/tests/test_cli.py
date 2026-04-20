"""Tests for CLI entry point."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from doc_memory.cli import build_parser, main


class TestCLI:
    def test_build_parser_has_subcommands(self) -> None:
        parser = build_parser()
        # Should not raise
        args = parser.parse_args(["ingest", "/tmp/docs"])
        assert args.command == "ingest"
        assert args.path == "/tmp/docs"

    def test_build_parser_search(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["search", "find this"])
        assert args.command == "search"
        assert args.query == "find this"

    def test_main_no_args_exits(self) -> None:
        with patch("sys.argv", ["doc-memory"]):
            with pytest.raises(SystemExit):
                main()
