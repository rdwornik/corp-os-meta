"""Tests for Pydantic frontmatter models."""
from datetime import date

import pytest

from corp_os_meta import DocumentType, NoteFrontmatter


def test_valid_note():
    note = NoteFrontmatter(
        title="Test Note",
        date=date(2026, 2, 21),
        type=DocumentType.PRESENTATION,
        topics=["Disaster Recovery", "SLA"],
        source_tool="knowledge-extractor",
        source_file="test.mkv",
    )
    assert note.title == "Test Note"
    assert note.schema_version == 1


def test_missing_required_field():
    with pytest.raises(Exception):
        NoteFrontmatter(title="No type")


def test_tool_meta_namespace():
    note = NoteFrontmatter(
        title="Test",
        date=date(2026, 1, 1),
        type=DocumentType.MEETING,
        source_tool="test",
        source_file="test.md",
        tool_meta={"knowledge_extractor": {"slide_index": 5}},
    )
    assert note.tool_meta["knowledge_extractor"]["slide_index"] == 5


def test_caps_not_exceeded():
    note = NoteFrontmatter(
        title="Test",
        date=date(2026, 1, 1),
        type=DocumentType.DOCUMENT,
        topics=["A", "B", "C", "D", "E", "F", "G", "H"],
        source_tool="test",
        source_file="test.md",
    )
    assert len(note.topics) == 8
