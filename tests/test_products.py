"""Tests for product key resolution and source reliability."""

from corp_os_meta.products import (
    classify_source_tier,
    get_product_display_name,
    get_source_reliability,
    is_platform_service,
    resolve_product_key,
)


# ── Product resolution ──────────────────────────────────────────


def test_resolve_exact_match():
    assert resolve_product_key("Blue Yonder WMS") == "wms"


def test_resolve_case_insensitive():
    assert resolve_product_key("blue yonder wms") == "wms"


def test_resolve_variant():
    assert resolve_product_key("WMS Classic") == "wms_classic"


def test_resolve_variant_native():
    assert resolve_product_key("Platform Native Warehouse Management") == "wms_native"


def test_resolve_platform_service():
    assert resolve_product_key("Analytics") == "analytics"


def test_resolve_bare_wms():
    assert resolve_product_key("WMS") == "wms"


def test_resolve_bare_platform():
    assert resolve_product_key("Platform") == "platform"


def test_resolve_bare_control_tower():
    assert resolve_product_key("Control Tower") == "control_tower"


def test_resolve_unknown():
    assert resolve_product_key("Nonexistent Product") is None


def test_resolve_fuzzy():
    """Close match still resolves."""
    assert resolve_product_key("BY WMS") == "wms"


# ── Display names ───────────────────────────────────────────────


def test_display_name():
    assert get_product_display_name("wms") == "Blue Yonder WMS"


def test_display_name_variant():
    assert get_product_display_name("wms_classic") == "WMS Classic"


def test_display_name_unknown():
    assert get_product_display_name("nonexistent") is None


# ── Platform service ────────────────────────────────────────────


def test_is_platform_service_true():
    assert is_platform_service("analytics") is True


def test_is_platform_service_false():
    assert is_platform_service("wms") is False


def test_is_platform_service_unknown():
    assert is_platform_service("nonexistent") is False


# ── Source reliability ──────────────────────────────────────────


def test_reliability_official():
    assert get_source_reliability("official_architecture_doc") == 1.0


def test_reliability_sales():
    assert get_source_reliability("sales_deck") == 0.4


def test_reliability_unknown():
    assert get_source_reliability("unknown_tier") == 0.1


# ── Source classification ───────────────────────────────────────


def test_classify_architecture_doc():
    assert (
        classify_source_tier("BYPlatform-Architecture.pdf")
        == "official_architecture_doc"
    )


def test_classify_training():
    assert (
        classify_source_tier("Module_1.pptx", source_type="training")
        == "training_material"
    )


def test_classify_release_notes():
    assert classify_source_tier("Release_Notes_v3.pdf") == "release_notes"


def test_classify_sales_deck():
    assert (
        classify_source_tier("Q4_Sales_Deck.pptx", source_type="presentation")
        == "sales_deck"
    )


def test_classify_fallback_source_type():
    """source_type mapping used when no filename pattern matches."""
    assert (
        classify_source_tier("random_file.pdf", source_type="training")
        == "training_material"
    )
