import requests
import json
from order import Order

class Delivery:
    def __init__(self, _delivery_no: str, _address: str, _order: Order,
                 _order_no: str):
        self._delivery_no = _delivery_no
        self._address = _address
        self._order = _order
        self._order_no = _order_no

    def __eq__(self, other) -> bool:
        return (self.get_order_no() == other.get_order_no() and
            self.get_delivery_no() == other.get_delivery_no())

    def set_address(self, address: str) -> None:
        self._address = address

    def set_order(self, order: Order) -> None:
        self._order = order
        self._order_no = order.get_order_no()

    def get_delivery_no(self) -> str:
        return self._delivery_no

    def get_order_no(self) -> str:
        return self._order_no

    def get_address(self) -> str:
        return self._address

    def get_order(self) -> Order:
        return self._order

    @classmethod
    def from_json(cls, data):
        data["_order"] = Order.from_json(data["_order"])
        return cls(**data)