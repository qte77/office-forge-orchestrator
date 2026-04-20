"""Claude CLI parser — primary parser using subprocess."""

from __future__ import annotations

import subprocess

from doc_memory.parser.base import Document, Page


class ClaudeParser:
    """Parse documents via Claude CLI subprocess."""

    def parse(self, path: str) -> Document:
        result = subprocess.run(
            ["claude", "-p", f"Read and convert this document to markdown: {path}"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            msg = f"Claude CLI failed for {path}: {result.stderr}"
            raise RuntimeError(msg)

        content = result.stdout.strip()
        pages = [Page(number=1, content=content)] if content else []
        return Document(source=path, pages=pages)
