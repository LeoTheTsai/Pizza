from PizzaParlour import app
from pizza_manager import PizzaManager
import unittest
import json

class TestPizzaManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPizzaManager, self).__init__(*args, **kwargs)
        self.pizza_manager = PizzaManager(app.test_client())
        self.pizza_file = open("./data/pizza_information.json", 'r')

    def test_get_pizza_type(self):
        actual = self.pizza_manager.get_pizza_types() #list of type
        expected = json.load(self.pizza_file)
        assert actual == expected["Types"]

    def test_get_pizza_topping(self):
        actual = self.pizza_manager.get_pizza_toppings()
        expected = json.load(self.pizza_file)
        assert actual == expected["Toppings"]

    def test_get_pizza_drink(self):
        actual = self.pizza_manager.get_drinks()
        expected = json.load(self.pizza_file)
        assert actual == expected["Drinks"]
    
    def test_get_pizza_size(self):
        actual = self.pizza_manager.get_pizza_sizes()
        expected = json.load(self.pizza_file)
        assert actual == expected["Sizes"]

    def test_get_predefined(self):
        actual = self.pizza_manager.get_predefined()
        expected = json.load(self.pizza_file)
        assert actual == expected["PreDefined"]
    


