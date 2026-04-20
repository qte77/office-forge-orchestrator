"""Tests for TreeNode."""

from __future__ import annotations

from doc_memory.index.tree import TreeNode


class TestTreeNode:
    def test_create_node(self) -> None:
        node = TreeNode(heading="Root", level=0, content="", children=[])
        assert node.heading == "Root"
        assert node.level == 0
        assert node.children == []

    def test_filter_keeps_matching_node(self) -> None:
        node = TreeNode(heading="Match", level=1, content="data", children=[])
        result = node.filter(lambda n: n.heading == "Match")
        assert result is not None
        assert result.heading == "Match"
        assert result.content == "data"

    def test_filter_prunes_non_matching(self) -> None:
        node = TreeNode(heading="NoMatch", level=1, content="data", children=[])
        result = node.filter(lambda n: n.heading == "Other")
        assert result is None

    def test_filter_preserves_ancestor_of_matching_child(self) -> None:
        child = TreeNode(heading="Target", level=2, content="found", children=[])
        parent = TreeNode(heading="Parent", level=1, content="parent stuff", children=[child])
        result = parent.filter(lambda n: n.heading == "Target")
        assert result is not None
        assert result.heading == "Parent"
        assert result.content == ""  # parent content stripped
        assert len(result.children) == 1
        assert result.children[0].heading == "Target"

    def test_filter_prunes_non_matching_siblings(self) -> None:
        keep = TreeNode(heading="Keep", level=2, content="yes", children=[])
        drop = TreeNode(heading="Drop", level=2, content="no", children=[])
        root = TreeNode(heading="Root", level=0, content="", children=[keep, drop])
        result = root.filter(lambda n: n.heading == "Keep")
        assert result is not None
        assert len(result.children) == 1
        assert result.children[0].heading == "Keep"

    def test_to_text(self) -> None:
        child = TreeNode(heading="Sub", level=2, content="detail", children=[])
        root = TreeNode(heading="Doc", level=1, content="intro", children=[child])
        text = root.to_text()
        assert "Doc" in text
        assert "intro" in text
        assert "Sub" in text
        assert "detail" in text
