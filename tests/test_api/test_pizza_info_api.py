from PizzaParlour import app
import unittest
import json

class TestPizzaParlour(unittest.TestCase):
    def test_pizza(self):
        response = app.test_client().get('/pizza')

        assert response.status_code == 200
        assert response.data == b'"Welcome to Pizza Planet!"\n'

    def test_get_pizza_info(self):
        response = app.test_client().get('/pizza/information')
        
        with open("./data/pizza_information.json") as f:
            data = json.load(f)
        
        assert response.status_code == 200
        assert response.json == data

    def test_get_pizza_type_info(self):
        response = app.test_client().get('/pizza/information/Types')

        with open("./data/pizza_information.json") as f:
            data = json.load(f)

        assert response.status_code == 200
        assert response.json == data["Types"]

    def test_get_pizza_sizes_info(self):
        with open("./data/pizza_information.json") as f:
            data = json.load(f)

        response = app.test_client().get('/pizza/information/Sizes')

        assert response.status_code == 200
        assert response.json == data["Sizes"]
    
    def test_get_pizza_toppings_info(self):
        with open("./data/pizza_information.json") as f:
            data = json.load(f)

        response = app.test_client().get('/pizza/information/Toppings')

        assert response.status_code == 200
        assert response.json == data["Toppings"]
    
    def test_get_pizza_drinks_info(self):
        with open("./data/pizza_information.json") as f:
            data = json.load(f)

        response = app.test_client().get('/pizza/information/Drinks')

        assert response.status_code == 200
        assert response.json == data["Drinks"]

    def test_get_pizza_predefine(self):
        with open("./data/pizza_information.json") as f:
            data = json.load(f)

        response = app.test_client().get('/pizza/information/PreDefined')

        assert response.status_code == 200
        assert response.json == data["PreDefined"]

