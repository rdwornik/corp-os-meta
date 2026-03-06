"""corp_os_meta — Shared metadata schema for corp-by-os agent ecosystem."""
from .models import (
    SCHEMA_VERSION,
    Authority,
    Confidentiality,
    DocumentType,
    DomainEnum,
    Layer,
    NoteFrontmatter,
    QualityLevel,
    SourceType,
)
from .normalize import load_taxonomy, normalize_frontmatter, normalize_terms
from .validate import ValidationResult, generate_links_line, get_output_path, validate_frontmatter

__all__ = [
    "NoteFrontmatter",
    "DocumentType",
    "SourceType",
    "Layer",
    "Confidentiality",
    "Authority",
    "DomainEnum",
    "QualityLevel",
    "SCHEMA_VERSION",
    "normalize_frontmatter",
    "load_taxonomy",
    "normalize_terms",
    "validate_frontmatter",
    "ValidationResult",
    "get_output_path",
    "generate_links_line",
]
