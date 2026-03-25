def calculate_total(unit_price: float, quantity: int) -> float:
    if unit_price <= 0:
        raise ValueError("unit_price must be positive")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    return round(unit_price * quantity, 2)
