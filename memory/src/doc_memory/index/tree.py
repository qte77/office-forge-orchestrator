"""TreeNode for hierarchical document structure."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class TreeNode:
    """A node in the document heading tree."""

    heading: str
    level: int
    content: str
    children: list[TreeNode] = field(default_factory=list)

    def filter(self, predicate: Callable[[TreeNode], bool]) -> TreeNode | None:
        """Return subtree where predicate matches, preserving ancestors."""
        filtered_children = [
            c
            for child in self.children
            if (c := child.filter(predicate)) is not None
        ]
        if predicate(self) or filtered_children:
            return TreeNode(
                heading=self.heading,
                level=self.level,
                content=self.content if predicate(self) else "",
                children=filtered_children,
            )
        return None

    def to_text(self, _depth: int = 0) -> str:
        """Render tree as readable text with heading hierarchy."""
        prefix = "#" * max(self.level, 1)
        parts = [f"{prefix} {self.heading}"]
        if self.content:
            parts.append(self.content)
        for child in self.children:
            parts.append(child.to_text(_depth + 1))
        return "\n\n".join(parts)
