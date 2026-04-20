"""Parser protocol and document models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass
class Page:
    """A single page of a document."""

    number: int
    content: str


@dataclass
class Document:
    """Parsed document with pages."""

    source: str
    pages: list[Page] = field(default_factory=list)


@runtime_checkable
class ParserProtocol(Protocol):
    """Interface for document parsers."""

    def parse(self, path: str) -> Document: ...
