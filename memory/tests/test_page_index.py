"""Tests for PageIndex builder."""

from __future__ import annotations

from doc_memory.index.page_index import build_tree, filter_relevant
from doc_memory.parser.base import Document, Page


class TestBuildTree:
    def test_build_from_single_page(self) -> None:
        doc = Document(
            source="test.md",
            pages=[Page(number=1, content="# Title\n\nIntro\n\n## Section\n\nBody")],
        )
        tree = build_tree(doc)
        assert tree.heading == "root"
        assert len(tree.children) >= 1

    def test_build_from_multiple_pages(self) -> None:
        doc = Document(
            source="test.md",
            pages=[
                Page(number=1, content="# Chapter 1\n\nFirst"),
                Page(number=2, content="# Chapter 2\n\nSecond"),
            ],
        )
        tree = build_tree(doc)
        assert len(tree.children) == 2

    def test_nested_headings(self) -> None:
        doc = Document(
            source="test.md",
            pages=[
                Page(number=1, content="# H1\n\nText\n\n## H2\n\nSub\n\n### H3\n\nDeep"),
            ],
        )
        tree = build_tree(doc)
        h1 = tree.children[0]
        assert h1.heading == "H1"
        assert len(h1.children) == 1
        h2 = h1.children[0]
        assert h2.heading == "H2"
        assert len(h2.children) == 1


class TestFilterRelevant:
    def test_filter_by_heading(self) -> None:
        doc = Document(
            source="test.md",
            pages=[
                Page(
                    number=1,
                    content="# Intro\n\nHello\n\n## Methods\n\nExperiment\n\n## Results\n\nData",
                ),
            ],
        )
        tree = build_tree(doc)
        filtered = filter_relevant(tree, matched_headings={"Methods"})
        assert filtered is not None
        text = filtered.to_text()
        assert "Methods" in text
        assert "Results" not in text
