from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    stock: int
    category: Optional[str] = None
    subcategory: Optional[str] = None
    discount: float = 0.0

    def apply_discount(self, discount: float):
        """Применяет скидку к товару."""
        self.discount = discount

    def is_available(self) -> bool:
        """Проверяет доступность товара."""
        return self.stock > 0