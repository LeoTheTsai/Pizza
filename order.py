import requests
import json

class Order:
    def __init__(self, _order_no: int, _pizza_size: str, _pizza_type: str,
                 _toppings: [str], _drink: str, _delivery: str, _delivery_no: int):
        self._pizza_type = _pizza_type
        self._toppings = _toppings
        self._pizza_size = _pizza_size
        self._drink = _drink
        self._order_no = _order_no
        self._delivery = _delivery
        self._delivery_no = _delivery_no

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        return self.get_order_no() == other.get_order_no()

    def set_pizza_type(self, pizza_type: str) -> None:
        self._pizza_type = pizza_type

    def add_topping(self, topping: str) -> None:
        self._toppings.append(topping)

    def remove_topping(self, topping: str) -> None:
        if topping in self._toppings:
            self._toppings.remove(topping)

    def set_pizza_size(self, pizza_size: str) -> None:
        self._pizza_size = pizza_size

    def set_drink(self, drink: str) -> None:
        self._drink = drink

    def set_delivery(self, delivery_type) -> None:
        self._delivery = delivery_type

    def get_order_no(self) -> int:
        return self._order_no

    def get_pizza_type(self) -> str:
        return self._pizza_type

    def get_toppings(self) -> [str]:
        return self._toppings

    def get_pizza_size(self) -> str:
        return self._pizza_size

    def get_drink(self) -> str:
        return self._drink

    def get_delivery(self) -> str:
        return self._delivery

    def get_delivery_no(self) -> int:
        return self._delivery_no

    @classmethod
    def from_json(cls, data):
        return cls(**data)