from data_manager import DataManager
import requests
import json
from order import Order
from delivery import Delivery
import random
from order_creator import OrderCreator
from delivery_creator import DeliveryCreator

class OrderHandler:

    def __init__(self, server = requests):
        self.server = server
        self.data = DataManager(self.server)

    """
    Interface Methods
    """

    def start_interface(self) -> int:
        while True:
            print("\nCommand list:")
            print("submit_order")
            print("update_order")
            print("cancel_order")
            print("print_menu")
            print("quit")
            command = input("\nEnter your command: ")

            if command == "quit":
                break
            elif command == "submit_order":
                self.submit_order()
            elif command == "update_order":
                self.update_order()
            elif command == "cancel_order":
                self.cancel_order()
            elif command == "print_menu":
                self.print_menu()
            else:
                print("Error: Invalid command")

    def submit_order(self) -> None:
        pizza_size = ""
        pizza_type = ""
        toppings = []
        drink = ""
        delivery_type = ""

        while True:
            pizza_size = input("Select a size: ")
            if self.check_pizza_size(pizza_size):
                break
            print("Error: Invalid size")

        while True:
            pizza_type = input("Select a pizza type (or enter 'None'): ")
            if self.check_pizza_type(pizza_type):
                break
            print("Error: Invalid type")
            
        while True:
            topping = input("Add a pizza topping (or enter 'None'): ")
            if topping.lower() == 'none':
                break
            elif not self.check_topping(topping):
                print("Error: Invalid topping")
            else:
                toppings.append(topping)

        while True:
            drink = input("Select a drink: ")
            if self.check_drink(drink):
                break
            print("Error: Invalid drink")

        while True:
            delivery_type = input("Select a delivery type: ")
            if self.check_delivery_type(delivery_type):
                break
            print("Error: Invalid delivery type")

        address = input("Enter your address (enter anything if pick-up): ")

        order_no = self.submit_order_to_server(pizza_size, pizza_type, toppings,
            drink, delivery_type, address)

        print("Your order number is: " + str(order_no))
        print("Lottory Chance, Pull 777 to win for free food")
        lotto = input("Pull? (y/n): ")
        if lotto == "y" or lotto == "Y":
            pull_num = self.lottery()
            print("You pulled: " + str(pull_num))
            if pull_num == 777:
                print("You won!!!")
                print("Your total is 0 dollars.")
            else:
                print("Your total is {} dollars.".format(self.calculate_total(self.get_order_by_no(order_no))))
        else:
            print("Your total is {} dollars.".format(self.calculate_total(self.get_order_by_no(order_no))))

    def update_order(self) -> None:
        order_no = input("Enter order number: ")
        print("Select an item to update")
        item = input("size/type/topping/drink/delivery/address): ")
        add_topping = False
        if item.lower() == "topping":
            ans = input("Add or remove topping? (a/r): ")
            if ans == "a":
                add_topping = True
        new_value = input("Enter the item to update: ")
        n = self.update_order_in_server(order_no, item, new_value, add_topping)
        if n == 0:
            print("Updated successfully")
        elif n == 1:
            print("Nothing updated")
        else:
            print("Failed to update")

    def cancel_order(self) -> None:
        order_no = input("Enter order number: ")
        if self.cancel_order_in_server(order_no) == 0:
            print("Order " + order_no + " cancelled successfully")
        else:
            print("Error: Invalid order number")

    def print_menu(self) -> None:
        print("Pizza Types: ")
        types = self.data.get_pizza_manager().get_pizza_types()
        for i in range(len(types)):
            print(str(i + 1) + ". " + types[i]["Type"] + " $" +
                str(types[i]["Price"]))
        print()

        print("Pizza Toppings: ")
        toppings = self.data.get_pizza_manager().get_pizza_toppings()
        for i in range(len(toppings)):
            print(str(i + 1) + ". " + toppings[i]["Topping"] + " $" +
                str(toppings[i]["Price"]))
        print()

        print("Pizza Sizes: ")
        sizes = self.data.get_pizza_manager().get_pizza_sizes()
        for i in range(len(sizes)):
            print(str(i + 1) + ". " + sizes[i]["Size"] + " $" +
                str(sizes[i]["Price"]))
        print()

        print("Pizza Drinks: ")
        drinks = self.data.get_pizza_manager().get_drinks()
        for i in range(len(drinks)):
            print(str(i + 1) + ". " + drinks[i]["Drink"] + " $" +
                str(drinks[i]["Price"]))
        print()

        print("Delivery Types: ")
        delivery_types = self.data.get_delivery_manager().get_delivery_types()
        for delivery_type in delivery_types:
            print(delivery_type)
        print()


    """
    Processing Methods
    """

    def check_pizza_size(self, pizza_size: str) -> bool:
        size_dict = self.data.get_pizza_manager().get_pizza_sizes()
        for obj in size_dict:
            if obj["Size"].lower() == pizza_size.lower():
                return True
        return False

    def check_pizza_type(self, pizza_type: str) -> bool:
        if pizza_type.lower() == "none":
            return True
        type_dict = self.data.get_pizza_manager().get_pizza_types()
        for obj in type_dict:
            if obj["Type"].lower() == pizza_type.lower():
                return True
        return False

    def check_topping(self, topping: str) -> bool:
        topping_dict = self.data.get_pizza_manager().get_pizza_toppings()
        for obj in topping_dict:
            if obj["Topping"].lower() == topping.lower():
                return True
        return False

    def check_drink(self, drink: str) -> bool:
        drink_dict = self.data.get_pizza_manager().get_drinks()
        for obj in drink_dict:
            if obj["Drink"].lower() == drink.lower():
                return True
        return False

    def check_delivery_type(self, delivery_type: str) -> bool:
        type_list = self.data.get_delivery_manager().get_delivery_types()
        for t in type_list:
            if t == delivery_type.lower():
                return True
        return False

    def get_order_by_no(self, order_no: int) -> Order:
        raw_order = self.data.get_order_manager().get_order(order_no)
        if raw_order == 404:
            return None
        order = Order.from_json(json.loads(raw_order))
        return order

    def get_delivery_by_type_no(self, delivery_type: str,
                                delivery_no: int) -> Delivery:
        raw_delivery = self.data.get_delivery_manager().get_each_delivery(
            delivery_type, delivery_no
        )
        if raw_delivery == 404:
            return None
        delivery = Delivery.from_json(raw_delivery)
        return delivery

    def submit_order_to_server(self, pizza_size: str, pizza_type: str,
        toppings: [str], drink: str, delivery_type: str, address: str) -> int:
        if not pizza_type.lower() == "none":
            predefined = self.data.get_pizza_manager().get_predefined()
            predefined_toppings = []
            for d in predefined:
                if pizza_type in d:
                    predefined_toppings = d[pizza_type]
            for t in predefined_toppings:
                if t not in toppings:
                    toppings.append(t)

        order = OrderCreator.get_instance().create_order(pizza_size, pizza_type, toppings, drink,
            delivery_type)
        self.data.get_order_manager().add_new_order(order.get_order_no(), order)
        delivery = DeliveryCreator.get_instance().create_delivery(address, order, order.get_order_no())
        self.data.get_delivery_manager().add_new_delivery(order.get_delivery(),
                                                    delivery,
                                                    order.get_delivery_no())
        return order.get_order_no()

    def update_order_in_server(self, order_no: int, item: str,
        new_value: str, add_topping: bool) -> int:
        """
        Return 0 if updated successfully.
        Otherwise return -1.
        """
        order = self.get_order_by_no(order_no)
        delivery = self.get_delivery_by_type_no(order.get_delivery(), order_no)
        if item == "size":
            if not self.check_pizza_size(new_value):
                print("Error: Invalid size")
                return -1
            else:
                order.set_pizza_size(new_value)
                self.data.get_order_manager().update_order(order.get_order_no(),
                                                     order)
                delivery.set_order(order)
                self.data.get_delivery_manager().update_delivery(
                    order.get_delivery(),
                    delivery,
                    order.get_delivery_no()
                )
                return 0
        elif item == "type":
            if not self.check_pizza_type(new_value):
                print("Error: Invalid type")
                return -1
            else:
                order.set_pizza_type(new_value)
                self.data.get_order_manager().update_order(order.get_order_no(),
                                                     order)
                delivery.set_order(order)
                self.data.get_delivery_manager().update_delivery(
                    order.get_delivery(),
                    delivery,
                    order.get_delivery_no()
                )                                                     
                return 0
        elif item == "topping":
            if not self.check_topping(new_value):
                print("Error: Invalid topping")
                return -1
            else:
                if add_topping and new_value not in order.get_toppings():
                    order.add_topping(new_value)
                elif not add_topping and new_value in order.get_toppings():
                    order.remove_topping(new_value)
                else:
                    return 1
                self.data.get_order_manager().update_order(order.get_order_no(),
                                                     order)
                delivery.set_order(order)
                self.data.get_delivery_manager().update_delivery(
                    order.get_delivery(),
                    delivery,
                    order.get_delivery_no()
                )
                return 0
        elif item == "drink":
            if not self.check_drink(new_value):
                print("Error: Invalid drink")
                return -1
            else:
                order.set_drink(new_value)
                self.data.get_order_manager().update_order(order.get_order_no(),
                                                     order)
                delivery.set_order(order)
                self.data.get_delivery_manager().update_delivery(
                    order.get_delivery(),
                    delivery,
                    order.get_delivery_no()
                )
                return 0
        elif item == "delivery":
            if not self.check_delivery_type(new_value):
                print("Error: Invalid delivery type")
                return -1
            else:
                order.set_delivery(new_value)
                self.data.get_order_manager().update_order(order.get_order_no(),
                                                     order)
                delivery.set_order(order)
                self.data.get_delivery_manager().update_delivery(new_value,
                    delivery, delivery.get_delivery_no())
                return 0
        elif item == "address":
            delivery.set_address(new_value)
            self.data.get_delivery_manager().update_delivery(
                order.get_delivery(),
                delivery, delivery.get_delivery_no()
            )
            return 0
        else:
            print("Error: Invalid item to update")
            return -1

    def cancel_order_in_server(self, order_no) -> int:
        """
        Return 0 if order_no is valid and the order is deleted successfully.
        Otherwisw return -1.
        """
        order = self.get_order_by_no(order_no)
        if order is None:
            return -1
        status1 = self.data.get_delivery_manager().delete_delivery(
            order.get_delivery(), order.get_delivery_no())
        status2 = self.data.get_order_manager().delete_order(order_no)
        
        if status1 == 404 or status2 == 404:
            return -1
        return 0

    def check_json_type(self) -> bool:
        """
        Return True if server is of type requests
        Return False if server is of type flask.request
        """
        return isinstance(self.server, requests)

    def calculate_total(self, order: Order) -> float:
        if order is None:
            return 0

        size_price = 0
        sizes = self.data.get_pizza_manager().get_pizza_sizes()
        for size in sizes:
            if size["Size"].lower() == order.get_pizza_size().lower():
                size_price = size["Price"]
                break

        type_price = 0
        types = self.data.get_pizza_manager().get_pizza_types()
        for type in types:
            if type["Type"].lower() == order.get_pizza_type().lower():
                type_price = type["Price"]
                break

        topping_price = 0
        toppings = self.data.get_pizza_manager().get_pizza_toppings()
        for order_topping in order.get_toppings():
            for topping in toppings:
                if topping["Topping"].lower() == order_topping.lower():
                    topping_price += topping["Price"]
                    break

        drink_price = 0
        drinks = self.data.get_pizza_manager().get_drinks()
        for drink in drinks:
            if drink["Drink"].lower() == order.get_drink().lower():
                drink_price = drink["Price"]
                break

        return size_price + type_price + topping_price + drink_price

    def lottery(self):
        n = self.data.get_order_manager().get_seed_for_lotto()
        random.seed(n)
        n = int(random.random() * 1000)
        self.data.get_order_manager().set_seed_for_lotto(n)
        return n

if __name__ == "__main__":
    order_handler = OrderHandler()
    order_handler.start_interface()
