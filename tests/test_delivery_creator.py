import unittest
from order import Order
from delivery import Delivery
from order_creator import OrderCreator
from delivery_creator import DeliveryCreator
import csv
import json

class TestDeliveryCreator(unittest.TestCase):
    def test_create_order(self):
        pizza_size = "small"
        pizza_type = "none"
        toppings = []
        drink = "coke"
        delivery_type = "pickup"
        address = "17 Wall Street"
        order = OrderCreator.get_instance().create_order(
                    pizza_size,
                    pizza_type,
                    toppings,
                    drink,
                    delivery_type,
                )

        self.assertEqual(
            DeliveryCreator.get_instance().create_delivery(
                address,
                order,
                order.get_order_no()
            ),
            Delivery(
                OrderCreator._delivery_no - 1,
                address,
                order,
                order.get_order_no()
            )
        )