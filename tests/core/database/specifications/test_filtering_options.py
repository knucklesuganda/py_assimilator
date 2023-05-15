from typing import Callable, Any
from assimilator.core.database.specifications.filtering_options import FilteringOptions


class MockFilteringOptions(FilteringOptions):
    @staticmethod
    def _eq(field: str, value: Any) -> Callable[[], Any]:
        return lambda: f"eq({field}, {value})"

    @staticmethod
    def _gt(field: str, value: Any) -> Callable[[], Any]:
        return lambda: f"gt({field}, {value})"


def test_parse_field_single_option():
    options = MockFilteringOptions()
    result = options.parse_field("field", "value")
    assert callable(result)
    assert result() == "eq(field, value)"


def test_parse_field_foreign_key():
    options = MockFilteringOptions()
    result = options.parse_field("foreign_field__gt", 10)
    assert callable(result)
    assert result() == "gt(foreign_field, 10)"


def test_get_default_filter():
    options = MockFilteringOptions()
    default_filter = options.get_default_filter()
    assert callable(default_filter)
    assert default_filter("field", "value")() == "eq(field, value)"

