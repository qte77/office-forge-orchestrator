"""Heading-boundary chunker with max-token fallback."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from doc_memory.parser.base import Document

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")

DEFAULT_MAX_TOKENS = 512
DEFAULT_OVERLAP_TOKENS = 64


@dataclass
class Chunk:
    """A chunk of document content with metadata."""

    content: str
    heading_path: list[str] = field(default_factory=list)
    page_number: int | None = None
    token_count: int = 0


def _word_count(text: str) -> int:
    """Approximate token count by word count."""
    return len(text.split())


def _split_oversized(
    text: str,
    heading_path: list[str],
    page_number: int | None,
    max_tokens: int,
    overlap_tokens: int,
) -> list[Chunk]:
    """Split oversized text at sentence boundaries with overlap."""
    sentences = SENTENCE_END.split(text)
    chunks: list[Chunk] = []
    current: list[str] = []
    current_count = 0

    for sentence in sentences:
        s_count = _word_count(sentence)
        if current_count + s_count > max_tokens and current:
            chunk_text = " ".join(current)
            chunks.append(
                Chunk(
                    content=chunk_text,
                    heading_path=list(heading_path),
                    page_number=page_number,
                    token_count=_word_count(chunk_text),
                )
            )
            # Keep overlap
            overlap: list[str] = []
            overlap_count = 0
            for s in reversed(current):
                wc = _word_count(s)
                if overlap_count + wc > overlap_tokens:
                    break
                overlap.insert(0, s)
                overlap_count += wc
            current = overlap + [sentence]
            current_count = overlap_count + s_count
        else:
            current.append(sentence)
            current_count += s_count

    if current:
        chunk_text = " ".join(current)
        chunks.append(
            Chunk(
                content=chunk_text,
                heading_path=list(heading_path),
                page_number=page_number,
                token_count=_word_count(chunk_text),
            )
        )

    return chunks


def chunk_document(
    doc: Document,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS,
) -> list[Chunk]:
    """Chunk a document by heading boundaries, splitting oversized sections."""
    chunks: list[Chunk] = []

    for page in doc.pages:
        text = page.content
        matches = list(HEADING_PATTERN.finditer(text))

        if not matches:
            if text.strip():
                wc = _word_count(text)
                if wc > max_tokens:
                    chunks.extend(
                        _split_oversized(
                            text, ["(untitled)"], page.number, max_tokens, overlap_tokens
                        )
                    )
                else:
                    chunks.append(
                        Chunk(
                            content=text.strip(),
                            heading_path=["(untitled)"],
                            page_number=page.number,
                            token_count=wc,
                        )
                    )
            continue

        heading_path: list[str] = []

        for i, match in enumerate(matches):
            level = len(match.group(1))
            heading = match.group(2).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content = text[start:end].strip()

            # Maintain heading path based on level
            heading_path = heading_path[: level - 1] + [heading]

            if not content:
                continue

            wc = _word_count(content)
            if wc > max_tokens:
                chunks.extend(
                    _split_oversized(
                        content, heading_path, page.number, max_tokens, overlap_tokens
                    )
                )
            else:
                chunks.append(
                    Chunk(
                        content=content,
                        heading_path=list(heading_path),
                        page_number=page.number,
                        token_count=wc,
                    )
                )

    return chunks
