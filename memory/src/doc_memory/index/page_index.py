"""Build and filter PageIndex trees from documents."""

from __future__ import annotations

import re

from doc_memory.index.tree import TreeNode
from doc_memory.parser.base import Document

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def _parse_sections(text: str) -> list[tuple[str, int, str]]:
    """Parse markdown text into (heading, level, content) tuples."""
    sections: list[tuple[str, int, str]] = []
    matches = list(HEADING_PATTERN.finditer(text))

    if not matches:
        if text.strip():
            sections.append(("(untitled)", 1, text.strip()))
        return sections

    # Content before first heading
    pre = text[: matches[0].start()].strip()
    if pre:
        sections.append(("(preamble)", 1, pre))

    for i, match in enumerate(matches):
        level = len(match.group(1))
        heading = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        sections.append((heading, level, content))

    return sections


def build_tree(doc: Document) -> TreeNode:
    """Build a heading tree from a Document."""
    root = TreeNode(heading="root", level=0, content="", children=[])
    stack: list[TreeNode] = [root]

    for page in doc.pages:
        for heading, level, content in _parse_sections(page.content):
            node = TreeNode(
                heading=heading, level=level, content=content, children=[]
            )
            while len(stack) > 1 and stack[-1].level >= level:
                stack.pop()
            stack[-1].children.append(node)
            stack.append(node)

    return root


def filter_relevant(
    tree: TreeNode, matched_headings: set[str]
) -> TreeNode | None:
    """Filter tree to branches containing matched headings."""
    return tree.filter(lambda n: n.heading in matched_headings)
