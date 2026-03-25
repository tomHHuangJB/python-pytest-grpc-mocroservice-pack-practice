import pytest

from order_app.pricing import calculate_total


@pytest.mark.unit
@pytest.mark.parametrize(
    ("unit_price", "quantity", "expected_total"),
    [
        (10.0, 1, 10.0),
        (19.99, 2, 39.98),
        (2.5, 4, 10.0),
    ],
)
def test_calculate_total_returns_expected_amount(unit_price: float, quantity: int, expected_total: float) -> None:
    assert calculate_total(unit_price, quantity) == expected_total


@pytest.mark.unit
@pytest.mark.parametrize(
    ("unit_price", "quantity"),
    [
        (0, 1),
        (-1, 1),
        (10, 0),
        (10, -2),
    ],
)
def test_calculate_total_rejects_invalid_values(unit_price: float, quantity: int) -> None:
    with pytest.raises(ValueError):
        calculate_total(unit_price, quantity)
