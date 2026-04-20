"""CLI entry point: doc-memory ingest <path>, doc-memory search <query>."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from doc_memory.parser.base import Document, Page
from doc_memory.parser.claude import ClaudeParser
from doc_memory.retrieve.hybrid import HybridRetriever

INDEX_DIR = ".doc_memory_index"


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="doc-memory",
        description="Document RAG: ingest and search documents",
    )
    sub = parser.add_subparsers(dest="command")

    ingest = sub.add_parser("ingest", help="Ingest documents from a directory")
    ingest.add_argument("path", help="Directory or file to ingest")

    search = sub.add_parser("search", help="Search ingested documents")
    search.add_argument("query", help="Search query")
    search.add_argument("-k", type=int, default=5, help="Number of results")

    return parser


def _parse_file(path: Path) -> Document:
    """Parse a single file using fallback chain."""
    errors: list[str] = []

    # Try Claude CLI
    try:
        return ClaudeParser().parse(str(path))
    except (RuntimeError, FileNotFoundError) as e:
        errors.append(f"Claude CLI: {e}")

    # Try Docling
    try:
        from doc_memory.parser.docling import DoclingParser

        return DoclingParser().parse(str(path))
    except (ImportError, Exception) as e:
        errors.append(f"Docling: {e}")

    # Try MarkItDown
    try:
        from doc_memory.parser.markitdown import MarkItDownParser

        return MarkItDownParser().parse(str(path))
    except (ImportError, Exception) as e:
        errors.append(f"MarkItDown: {e}")

    # Plain text fallback for .md/.txt
    if path.suffix in (".md", ".txt"):
        content = path.read_text(encoding="utf-8")
        return Document(source=str(path), pages=[Page(number=1, content=content)])

    msg = f"All parsers failed for {path}: {'; '.join(errors)}"
    raise RuntimeError(msg)


def _cmd_ingest(args: argparse.Namespace) -> None:
    """Ingest documents from path."""
    target = Path(args.path)
    retriever = HybridRetriever()

    files: list[Path] = []
    if target.is_dir():
        for ext in ("*.pdf", "*.docx", "*.md", "*.txt"):
            files.extend(target.glob(ext))
    elif target.is_file():
        files = [target]
    else:
        print(f"Error: {target} not found", file=sys.stderr)
        sys.exit(1)

    for f in sorted(files):
        print(f"Ingesting: {f}")
        doc = _parse_file(f)
        retriever.ingest(doc)

    retriever.store.save(INDEX_DIR)
    print(f"Indexed {len(files)} document(s) → {INDEX_DIR}/")


def _cmd_search(args: argparse.Namespace) -> None:
    """Search indexed documents."""
    index_path = Path(INDEX_DIR)
    if not index_path.exists():
        print("Error: No index found. Run 'doc-memory ingest' first.", file=sys.stderr)
        sys.exit(1)

    retriever = HybridRetriever()
    retriever.store = retriever.store.load(str(index_path))

    results = retriever.search(args.query, k=args.k)
    if not results:
        print("No results found.")
        return

    for i, r in enumerate(results, 1):
        heading = " > ".join(r.heading_path) if r.heading_path else "(no heading)"
        print(f"\n--- Result {i} (score: {r.score:.3f}) ---")
        print(f"Source: {r.source} | Page: {r.page_number} | {heading}")
        print(r.content[:500])


def main() -> None:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "ingest":
        _cmd_ingest(args)
    elif args.command == "search":
        _cmd_search(args)
