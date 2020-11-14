import unittest
from order import Order
from order_creator import OrderCreator
import csv
import json

class TestOrderCreator(unittest.TestCase):
    def test_create_order(self):
        pizza_size = "small"
        pizza_type = "none"
        toppings = []
        drink = "coke"
        delivery_type = "pickup"

        self.assertEqual(
            OrderCreator.get_instance().create_order(
                pizza_size,
                pizza_type,
                toppings,
                drink,
                delivery_type,
            ),
            Order(
                OrderCreator._order_no - 1,
                pizza_size,
                pizza_type,
                toppings,
                drink,
                delivery_type,
                OrderCreator._delivery_no - 1
            )
        )