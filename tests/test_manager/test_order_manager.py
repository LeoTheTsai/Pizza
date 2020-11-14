from PizzaParlour import app
from order_manager import OrderManager
import unittest
import json
import requests

class TestOrderManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOrderManager, self).__init__(*args, **kwargs)
        self.server = app.test_client()
        self.order_manager = OrderManager(self.server)
        self.test_data_key = "1"
        self.test_data = {"Toppings": "beef", "Sizes": "Large"}
        self.test_data_key2 = "2"
        self.test_data2 = {"Toppings": "Chicken", "Sizes": "Small"}
        self.test_data_key3 = "3"
        self.test_data3 = {"Toppings": "Fish", "Sizes": "Medium"}

        #reset what is on the test_client first due to other test
        r = self.server.get(self.order_manager._URL).get_json()
        for k in r.keys():
            self.server.delete(self.order_manager._URL, json = k)

        #initialize the server and push the test_data first
        #use dumps because it is more consistent with the ordermanager adding method
        self.server.post(self.order_manager._URL, json = {self.test_data_key: json.dumps(self.test_data)})
        self.server.post(self.order_manager._URL, json = {self.test_data_key2: json.dumps(self.test_data2)})


    def test_get_all_order(self):
        #data is a dict where key is string and value is json.dumps dict
        actual = self.order_manager.get_all_orders()
        expected = {self.test_data_key: json.dumps(self.test_data), self.test_data_key2: json.dumps(self.test_data2)}
        assert actual == expected

    def test_get_order_num_exist(self):
        actual =  json.loads(self.order_manager.get_order(1))
        expected = self.test_data
        assert actual == expected

    def test_get_order_num_not_exist(self):
        actual = self.order_manager.get_order(4)
        expected = 404
        assert actual == expected

    def test_add_new_order_num_exist(self):
        actual = self.order_manager.add_new_order(self.test_data_key, self.test_data)
        expected = 404
        assert actual == expected
    
    def test_add_new_order_num_not_exist(self):
        actual = self.order_manager.add_new_order(self.test_data_key3, self.test_data3)
        expected = 201
        #after adding need to delete, otherwise test_get_all will record one more
        self.server.delete(self.order_manager._URL, json = 2)
        assert actual == expected

    def test_delete_order_num_exist(self):
        actual = self.order_manager.delete_order(self.test_data_key)
        expected = 201
        assert actual == expected

    def test_delete_order_num_not_exist(self):
        actual = self.order_manager.delete_order(4)
        expected = 404
        assert actual == expected

    def test_update_order_num_exist(self):
        updated_data2 = {"Toppings": "Pork", "Sizes": "Small"}
        actual = self.order_manager.update_order(self.test_data_key2, updated_data2)
        expected = 201
        assert actual == expected

    def test_update_order_num_not_exist(self):
        actual = self.order_manager.update_order(4, None)
        expected = 404
        assert actual == expected

    def test_get_seed(self):
        actual = self.order_manager.get_seed_for_lotto()
        expected = 10
        assert actual == expected

    def test_set_seed(self):
        self.order_manager.set_seed_for_lotto(100)
        actual = self.order_manager.get_seed_for_lotto()
        expected = 100
        assert actual == expected

        # back to original
        self.order_manager.set_seed_for_lotto(10)
        actual = self.order_manager.get_seed_for_lotto()
        expected = 10
        assert actual == expected