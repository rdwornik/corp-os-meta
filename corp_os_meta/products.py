"""Canonical product key resolution and source reliability."""

import logging
import re
from difflib import SequenceMatcher
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).parent / "data"
_products_cache: list[dict] | None = None
_tiers_cache: dict | None = None

_FUZZY_THRESHOLD = 0.85


def _load_products() -> list[dict]:
    global _products_cache
    if _products_cache is None:
        with open(_DATA_DIR / "products.yaml") as f:
            _products_cache = yaml.safe_load(f)["products"]
    return _products_cache


def _load_tiers() -> dict:
    global _tiers_cache
    if _tiers_cache is None:
        with open(_DATA_DIR / "source_tiers.yaml") as f:
            _tiers_cache = yaml.safe_load(f)["reliability_tiers"]
    return _tiers_cache


def _build_name_index() -> dict[str, str]:
    """Build lowercase display_name -> key index, including variants."""
    index: dict[str, str] = {}
    for product in _load_products():
        for name in product["display_names"]:
            index[name.lower()] = product["key"]
        for variant in product.get("variants", []):
            for name in variant["display_names"]:
                index[name.lower()] = variant["key"]
    return index


def resolve_product_key(display_name: str) -> str | None:
    """Resolve display name to canonical key.

    Uses exact (case-insensitive) match first, then fuzzy match (>0.85 similarity).
    Checks variants too.
    """
    index = _build_name_index()
    lowered = display_name.lower()

    # Exact match
    if lowered in index:
        return index[lowered]

    # Fuzzy match
    best_score = 0.0
    best_key: str | None = None
    for name, key in index.items():
        score = SequenceMatcher(None, lowered, name).ratio()
        if score > best_score:
            best_score = score
            best_key = key
    if best_score >= _FUZZY_THRESHOLD:
        logger.debug(
            "Fuzzy matched '%s' -> '%s' (%.2f)", display_name, best_key, best_score
        )
        return best_key

    return None


def get_product_display_name(key: str) -> str | None:
    """Get primary display name for canonical key."""
    for product in _load_products():
        if product["key"] == key:
            return product["display_names"][0]
        for variant in product.get("variants", []):
            if variant["key"] == key:
                return variant["display_names"][0]
    return None


def is_platform_service(key: str) -> bool:
    """Check if product key is a platform service."""
    for product in _load_products():
        if product["key"] == key:
            return product.get("is_platform_service", False)
    return False


def get_source_reliability(tier_name: str) -> float:
    """Get reliability score for a source tier. Returns 0.1 for unknown tiers."""
    tiers = _load_tiers()
    tier = tiers.get(tier_name)
    if tier is None:
        logger.warning("Unknown source tier: %s", tier_name)
        return 0.1
    return tier["score"]


# Filename patterns for source classification, checked in order.
_TIER_PATTERNS: list[tuple[str, str]] = [
    (r"(?i)architect", "official_architecture_doc"),
    (r"(?i)service.description|sla", "service_description"),
    (r"(?i)implementation|deploy", "implementation_guide"),
    (r"(?i)release.note|changelog|migration", "release_notes"),
    (r"(?i)user.guide|api.ref|product.doc", "official_product_doc"),
    (r"(?i)training|enablement|module", "training_material"),
    (r"(?i)pitch|marketing|corporate.pres", "vendor_marketing"),
    (r"(?i)sales|customer.deck", "sales_deck"),
    (r"(?i)rfp|response", "historical_rfp"),
    (r"(?i)notes|meeting|summary", "user_notes"),
]

# source_type (from CKE) -> tier mapping
_SOURCE_TYPE_MAP: dict[str, str] = {
    "training": "training_material",
    "documentation": "official_product_doc",
    "release_note": "release_notes",
    "meeting": "user_notes",
    "research": "external_source",
}


def classify_source_tier(filename: str, source_type: str | None = None) -> str:
    """Heuristic classification of source into reliability tier.

    Uses filename patterns and optional source_type from CKE extraction.
    Falls back to source_type mapping if no filename pattern matches.
    """
    # Filename patterns take priority
    for pattern, tier in _TIER_PATTERNS:
        if re.search(pattern, filename):
            return tier

    # Fall back to source_type mapping
    if source_type and source_type in _SOURCE_TYPE_MAP:
        return _SOURCE_TYPE_MAP[source_type]

    # Heuristic: presentations without other signals -> sales_deck
    if re.search(r"(?i)\.(pptx?|key)$", filename):
        if source_type == "presentation":
            return "sales_deck"
        return "vendor_marketing"

    return "user_notes"
