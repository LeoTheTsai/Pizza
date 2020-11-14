import requests
import json

from pizza_manager import PizzaManager
from order_manager import OrderManager
from delivery_manager import DeliveryManager


class DataManager:
    def __init__(self, server = requests):
        self._server = server
        self._pizza_manager = PizzaManager(self._server)
        self._order_manager = OrderManager(self._server)
        self._delivery_manager = DeliveryManager(self._server)

    def get_pizza_manager(self):
        return self._pizza_manager

    def get_order_manager(self):
        return self._order_manager

    def get_delivery_manager(self):
        return self._delivery_manager