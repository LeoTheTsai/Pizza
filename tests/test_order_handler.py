import unittest

from order_handler import OrderHandler
from order import Order
from delivery import Delivery
from data_manager import DataManager
import csv
import json
from PizzaParlour import app
from order_creator import OrderCreator
from delivery_creator import DeliveryCreator

class TestOrderHandler(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOrderHandler, self).__init__(*args, **kwargs)
        self.server = app.test_client()
        self.order_handler = OrderHandler(self.server)
        self.l = ["ubereat", "pickup", "inhouse", "foodora"]
        self.reset_file()

    def test_check_pizza_size_valid_input_1(self):
        s = "Medium"
        self.assertEqual(self.order_handler.check_pizza_size(s), True)

    def test_check_pizza_size_valid_input_2(self):
        s = "large"
        self.assertEqual(self.order_handler.check_pizza_size(s), True)

    def test_check_pizza_size_invalid_input(self):
        s = "34"
        self.assertEqual(self.order_handler.check_pizza_size(s), False)

    def test_check_pizza_size_invalid_input_empty_string(self):
        s = ""
        self.assertEqual(self.order_handler.check_pizza_size(s), False)

    def test_check_pizza_type_valid_input_1(self):
        s = "none"
        self.assertEqual(self.order_handler.check_pizza_type(s), True)

    def test_check_pizza_type_valid_input_2(self):
        s = "VEGETARIAN"
        self.assertEqual(self.order_handler.check_pizza_type(s), True)

    def test_check_pizza_type_invalid_input(self):        
        s = ""
        self.assertEqual(self.order_handler.check_pizza_type(s), False)

    def test_check_pizza_type_invalid_input_empty_string(self):
        s = ""
        self.assertEqual(self.order_handler.check_pizza_type(s), False)

    def test_check_topping_valid_input(self):
        s = "chicken"
        self.assertEqual(self.order_handler.check_topping(s), True)

    def test_check_topping_invalid_input(self):
        s = "VEGETARIAN"
        self.assertEqual(self.order_handler.check_topping(s), False)

    def test_check_topping_invalid_input_empty_string(self):
        s = ""
        self.assertEqual(self.order_handler.check_topping(s), False)

    def test_check_drink_valid_input(self):
        s = "coke"
        self.assertEqual(self.order_handler.check_drink(s), True)

    def test_check_drink_invalid_input(self):
        s = "sofa"
        self.assertEqual(self.order_handler.check_drink(s), False)

    def test_check_pizza_size_invalid_input_empty_string(self):
        s = ""
        self.assertEqual(self.order_handler.check_drink(s), False)

    def test_check_delivery_type_valid_input(self):
        s = "ubereats"
        self.assertEqual(self.order_handler.check_delivery_type(s), False)

    def test_check_delivery_type_invalid_input(self):
        s = "sofa"
        self.assertEqual(self.order_handler.check_delivery_type(s), False)

    def test_check_delivery_type_invalid_input_empty_string(self):
        s = ""
        self.assertEqual(self.order_handler.check_delivery_type(s), False)

    def test_get_order_by_no_valid_input(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )

        self.assertEqual(
            self.order_handler.get_order_by_no(order1.get_order_no()),
            order1
        )
        self.reset_file()

    def test_get_order_by_no_invalid_input(self):
        self.assertEqual(
            self.order_handler.get_order_by_no(94),
            None
        )

    def test_get_delivery_by_no_valid_input(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "foodora")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        self.assertEqual(
            self.order_handler.get_delivery_by_type_no(
                order1.get_delivery(),
                order1.get_delivery_no()
            ).get_delivery_no(),
            str(order1.get_delivery_no())
        )
        self.reset_file()

    def test_submit_order_to_server_none_type_pickup(self):
        pizza_size = "small"
        pizza_type = "none"
        toppings = ["beef", "chicken"]
        drink = "coke"
        delivery_type = "pickup"
        address = "none"

        self.assertEqual(
            self.order_handler.submit_order_to_server(
                pizza_size,
                pizza_type,
                toppings,
                drink,
                delivery_type,
                address
            ),
            OrderCreator._order_no - 1
        )
        self.reset_file()

    def test_submit_order_to_server_valid_type_pickup(self):
        pizza_size = "small"
        pizza_type = "Pepperoni"
        toppings = ["beef", "chicken"]
        drink = "coke"
        delivery_type = "pickup"
        address = "none"

        self.assertEqual(
            self.order_handler.submit_order_to_server(
                pizza_size,
                pizza_type,
                toppings,
                drink,
                delivery_type,
                address
            ),
            OrderCreator._order_no - 1
        )
        self.reset_file()

    def test_submit_order_to_server_valid_type_ubereats(self):
        pizza_size = "small"
        pizza_type = "Pepperoni"
        toppings = ["beef", "chicken"]
        drink = "coke"
        delivery_type = "ubereats"
        address = "none"

        self.assertEqual(
            self.order_handler.submit_order_to_server(
                pizza_size,
                pizza_type,
                toppings,
                drink,
                delivery_type,
                address
            ),
            OrderCreator._order_no - 1
        )
        self.reset_file()

    def test_submit_order_to_server_none_type_inhouse(self):
        pizza_size = "small"
        pizza_type = "none"
        toppings = ["beef", "chicken"]
        drink = "coke"
        delivery_type = "inhouse"
        address = "none"

        self.assertEqual(
            self.order_handler.submit_order_to_server(
                pizza_size,
                pizza_type,
                toppings,
                drink,
                delivery_type,
                address
            ),
            OrderCreator._order_no - 1
        )
        self.reset_file()

    def test_submit_order_to_server_none_type_topping_pickup(self):
        pizza_size = "small"
        pizza_type = "none"
        toppings = []
        drink = "coke"
        delivery_type = "pickup"
        address = "none"

        self.assertEqual(
            self.order_handler.submit_order_to_server(
                pizza_size,
                pizza_type,
                toppings,
                drink,
                delivery_type,
                address
            ),
            OrderCreator._order_no - 1
        )
        self.reset_file()

    def test_update_order_handler_valid_size_foodora(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "foodora")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "size"
        new_value = "large"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            0
        )
        self.reset_file()

    def test_update_order_handler_invalid_size_pickup(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "size"
        new_value = "huge"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            -1
        )
        self.reset_file()

    def test_update_order_handler_valid_type_pickup(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "type"
        new_value = "Pepperoni"
        add_topping = True

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            0
        )
        self.reset_file()

    def test_update_order_handler_valid_add_topping_pickup(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "topping"
        new_value = "chicken"
        add_topping = True

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            0
        )
        self.reset_file()

    def test_update_order_handler_valid_remove_topping_pickup(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef", "chicken"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "topping"
        new_value = "chicken"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            0
        )
        self.reset_file()

    def test_update_order_handler_invalid_remove_topping_pickup(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "topping"
        new_value = "chicken"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            1
        )
        self.reset_file()

    def test_update_order_handler_valid_drink_pickup(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "drink"
        new_value = "coke"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            0
        )
        self.reset_file()

    def test_update_order_handler_invalid_drink_pickup(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "drink"
        new_value = "melon juice"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            -1
        )
        self.reset_file()

    def test_update_order_handler_valid_delivery(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "delivery"
        new_value = "ubereat"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            0
        )
        self.reset_file()

    def test_update_order_handler_invalid_delivery(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "delivery"
        new_value = "subway"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            -1
        )
        self.reset_file()

    def test_update_order_handler_address(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "address"
        new_value = "17 Wall Street"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            0
        )
        self.reset_file()

    def test_update_order_handler_invalid_item(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        item = "mood"
        new_value = "happy"
        add_topping = False

        self.assertEqual(
            self.order_handler.update_order_in_server(
                order1.get_order_no(),
                item,
                new_value,
                add_topping
            ),
            -1
        )
        self.reset_file()   

    def test_cancel_order_in_server_valid_order_no(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        self.assertEqual(
            self.order_handler.cancel_order_in_server(order1.get_order_no()),
            0
        )
        self.reset_file()

    def test_cancel_order_in_server_invalid_order_no(self):
        self.assertEqual(
            self.order_handler.cancel_order_in_server(10000),
            -1
        )

    def test_calculate_total_order_none(self):
        self.assertEqual(
            self.order_handler.calculate_total(None),
            0
        )

    def test_calculate_total_valid_order(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        self.assertEqual(
            self.order_handler.calculate_total(order1),
            6
        )
        self.reset_file()

    def test_calculate_total_invalid_order_1(self):
        order1 = OrderCreator.get_instance().create_order("small", "none", ["beef"], "coke", 
                                            "spaceship")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        self.assertEqual(
            self.order_handler.calculate_total(order1),
            6
        )
        self.reset_file()

    def test_calculate_total_invalid_order_2(self):
        order1 = OrderCreator.get_instance().create_order("huge", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        self.assertEqual(
            self.order_handler.calculate_total(order1),
            4
        )
        self.reset_file()

    def test_calculate_total_invalid_order_3(self):
        order1 = OrderCreator.get_instance().create_order("", "none", ["beef"], "coke", 
                                            "pickup")
        self.order_handler.data.get_order_manager().add_new_order(
            order1.get_order_no(), order1
        )
        delivery1 = DeliveryCreator.get_instance().create_delivery(
            "1998 Washington Street",
            order1,
            order1.get_order_no()
        )
        self.order_handler.data.get_delivery_manager().add_new_delivery(
            order1.get_delivery(),
            delivery1,
            order1.get_delivery_no()
        )

        self.assertEqual(
            self.order_handler.calculate_total(order1),
            4
        )
        self.reset_file()

    def reset_file(self):
        for f in self.l:
            if f == "foodora":
                with open("./data/{}.csv".format(f), 'w') as fw:
                    csv_writer = csv.writer(fw)
                    csv_writer.writerow(["ID","_delivery_no","_address","_order","_order_no"])
            else:
                with open("./data/{}.json".format(f), 'w') as fw:
                    json.dump({}, fw)

    def reset_order(self):
        res = self.server.get("http://localhost:5000/pizza/order").get_json()
        for k in res.keys():
            self.server.delete("http://localhost:5000/pizza/order", json = k)

if __name__ == "__main__":
    unittest.main()
