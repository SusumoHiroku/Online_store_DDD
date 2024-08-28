from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    RESERVED = 'reserved'
    CANCELLED = 'cancelled'
    SOLD = 'sold'

@dataclass
class Order:
    id: int
    product_id: int
    quantity: int
    status: OrderStatus = OrderStatus.RESERVED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def cancel(self):
        if self.status == OrderStatus.RESERVED:
            self.status = OrderStatus.CANCELLED
            self.updated_at = datetime.now()
        else:
            raise ValueError("Cannot cancel an order that is not reserved.")

    def complete_sale(self):
        if self.status == OrderStatus.RESERVED:
            self.status = OrderStatus.SOLD
            self.updated_at = datetime.now()
        else:
            raise ValueError("Cannot complete sale for an order that is not reserved.")