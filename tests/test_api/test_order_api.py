from PizzaParlour import app
import unittest
import json

class OrderTest(unittest.TestCase):
    # note that all the add, delete carry over all methods.
    def __init__(self, *args, **kwargs):
        super(OrderTest, self).__init__(*args, **kwargs)
        self.URL = "http://localhost:5000/pizza/order"
        self.server = app.test_client()
        self.reset_order()

    def test_get_order(self):
        response = self.server.get(self.URL)
        assert response.status_code == 200

    def test_adding_new_order(self):
        # adding new data check return
        data1 = {"1": {"Types": "None", "Sizes": "small", "Toppins": "beef"}}
        data2 = {"2": {"Types": "Pep", "Sizes": "Medium", "Toppins": "Chicken"}}
        response = self.server.post(self.URL, json = data1)
        response2 = self.server.post(self.URL, json = data2)
        assert response.status_code == 201
        assert response.json == "Added new order"

        assert response2.status_code == 201
        assert response2.json == "Added new order"    

    def test_delete_not_exist_order(self):
        response = self.server.delete(self.URL, json = "3")

        assert response.status_code == 404
        assert response.json == "Order number does not existed"


    # def test_delete_exist_order(self):
    #     #check if delete's call is success
    #     response = self.server.delete(self.URL, json = "3")

    #     assert response.status_code == 201
    #     assert response.json == "Order deleted"

    def test_get_each_order_num_not_exist(self):
        response = self.server.get(self.URL + "/3")
        assert response.status_code == 404
        assert response.json == "Order number does not exist"

    # def test_get_each_order_num_exist(self):
    #     response = self.server.get(self.URL + "/1")
    #     assert response.status_code == 200

    # def test_update_specific_order_num_exist(self):
    #     order = {"1": {"Types": "Pep", "Sizes": "Medium", "Toppins": "Chicken"}}
    #     response = self.server.put(self.URL + "/1", json = order["1"])
    #     assert response.status_code == 201
    #     assert response.json == "Updated order"

    def test_update_specific_order_num_not_exist(self):
        order = {"2": {"Types": "Pep", "Sizes": "Medium", "Toppins": "Chicken"}}
        response = self.server.put(self.URL + "/2", json = order["2"])
        assert response.status_code == 404
        assert response.json == "Order number does not existed"


    def reset_order(self):
        res = self.server.get(self.URL).get_json()
        print(res)
        for k in res.keys():
            self.server.delete(self.URL, json = k)
