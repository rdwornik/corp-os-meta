"""
Pydantic models defining the frontmatter contract for all corporate-os notes.
Schema version 2: adds knowledge dimensions (domains, layers, confidentiality, authority, temporal validity).
"""
from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

SCHEMA_VERSION = 2


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


class SourceType(str, Enum):
    OPPORTUNITY = "opportunity"
    RFP = "rfp"
    MEETING = "meeting"
    TRAINING = "training"
    DOCUMENTATION = "documentation"
    RELEASE_NOTE = "release_note"
    RESEARCH = "research"
    INTERNAL_UPDATE = "internal_update"


class Layer(str, Enum):
    OPERATIONAL = "operational"
    LEARNING = "learning"
    REFERENCE = "reference"


class Confidentiality(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class Authority(str, Enum):
    AUTHORITATIVE = "authoritative"
    APPROVED = "approved"
    TRIBAL = "tribal"


class QualityLevel(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    FRAGMENT = "fragment"


class DomainEnum(str, Enum):
    PRODUCT = "Product"
    PLATFORM_ARCHITECTURE = "Platform & Architecture"
    DELIVERY_IMPLEMENTATION = "Delivery & Implementation"
    CUSTOMER_SUCCESS = "Customer Success"
    GO_TO_MARKET = "Go-to-Market"
    COMMERCIALS = "Commercials"
    COMPETITIVE = "Competitive"
    INDUSTRY_SUPPLY_CHAIN = "Industry & Supply Chain"


class NoteFrontmatter(BaseModel):
    """Required and optional frontmatter fields for all corporate-os notes.

    Schema v2: Knowledge dimensions for personal business mastery.
    Every tool must produce frontmatter that validates against this model.
    Tool-specific fields go in tool_meta.
    """

    # ── Required ──────────────────────────────────────────────────
    title: str
    date: date
    type: DocumentType
    topics: list[str] = Field(default_factory=list, max_length=8)
    schema_version: int = SCHEMA_VERSION
    source_tool: str
    source_file: str

    # ── Knowledge Dimensions (v2) ─────────────────────────────────
    source_type: SourceType = SourceType.DOCUMENTATION
    layer: Layer = Layer.LEARNING
    domains: list[str] = Field(default_factory=list, max_length=3)
    confidentiality: Confidentiality = Confidentiality.INTERNAL
    authority: Authority = Authority.TRIBAL

    # ── Temporal Validity (v2) ────────────────────────────────────
    valid_to: date | None = None
    last_verified: date | None = None

    # ── Context ───────────────────────────────────────────────────
    products: list[str] = Field(default_factory=list, max_length=4)
    people: list[str] = Field(default_factory=list, max_length=3)
    client: str | None = None
    project: str | None = None

    # ── Standard Optional ─────────────────────────────────────────
    language: str = "en"
    quality: QualityLevel = QualityLevel.FULL
    summary: str | None = None
    duration_min: int | None = None
    model: str | None = None
    tokens_used: int | None = None
    confidence: float | None = None
    tags: list[str] = Field(default_factory=list)

    # ── Tool-specific namespace ───────────────────────────────────
    tool_meta: dict[str, Any] = Field(default_factory=dict)

    # ── Validation metadata ───────────────────────────────────────
    validation_warnings: list[str] = Field(default_factory=list, exclude=True)
