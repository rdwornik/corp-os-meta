"""
Pydantic models defining the frontmatter contract for all corp-by-os notes.
Every tool imports NoteFrontmatter to validate output before writing.
"""
from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

SCHEMA_VERSION = 1


class DocumentType(str, Enum):
    PRESENTATION = "presentation"
    MEETING = "meeting"
    TRAINING = "training"
    DEMO = "demo"
    WORKSHOP = "workshop"
    RFP = "rfp"
    CONTRACT = "contract"
    EMAIL = "email"
    NOTES = "notes"
    DOCUMENT = "document"
    REPORT = "report"
    TUTORIAL = "tutorial"
    SECURITY_QUESTIONNAIRE = "security_questionnaire"


class QualityLevel(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    FRAGMENT = "fragment"


class NoteFrontmatter(BaseModel):
    """Required and optional frontmatter fields for all corp-by-os notes.

    This is the CONTRACT. Every tool must produce frontmatter that validates
    against this model. Tool-specific fields go in tool_meta.
    """

    # ── Required ──────────────────────────────────────────────────
    title: str
    date: date
    type: DocumentType
    topics: list[str] = Field(default_factory=list, max_length=8)
    schema_version: int = SCHEMA_VERSION
    source_tool: str  # "knowledge-extractor", "project-extractor", etc.
    source_file: str  # original file path or identifier

    # ── Optional but standardized ─────────────────────────────────
    products: list[str] = Field(default_factory=list, max_length=4)
    people: list[str] = Field(default_factory=list, max_length=3)
    language: str = "en"
    quality: QualityLevel = QualityLevel.FULL
    summary: str | None = None
    duration_min: int | None = None  # for video/meeting content
    model: str | None = None  # AI model used for extraction
    tokens_used: int | None = None
    confidence: float | None = None  # 0.0-1.0, for AI-extracted content
    project: str | None = None  # project ID for corp-project-extractor
    tags: list[str] = Field(default_factory=list)  # Obsidian convenience, non-authoritative

    # ── Tool-specific namespace ───────────────────────────────────
    tool_meta: dict[str, Any] = Field(default_factory=dict)

    # ── Validation metadata (set by validate, not by tool) ────────
    validation_warnings: list[str] = Field(default_factory=list, exclude=True)
