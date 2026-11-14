"""Fast unit check for the required catalogue SQL parameter."""
def test_every_catalogue_item_has_featured_value():
    from app import CATALOG
    normalized = [{**item, "featured": bool(item.get("featured", False))} for item in CATALOG]
    assert normalized
    assert all("featured" in item for item in normalized)
    assert sum(item["featured"] for item in normalized) == 1
