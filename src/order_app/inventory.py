class InventoryClient:
    def reserve(self, sku: str, quantity: int) -> None:
        """Reserve stock or raise a domain-specific error."""
        raise NotImplementedError
