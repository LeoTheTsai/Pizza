import json
from flask import jsonify
import requests
#from order import Order

class OrderManager:
    def __init__(self, r = requests):
        self._r = r
        self._URL = "http://localhost:5000/pizza/order"

    def get_all_orders(self):
        """Return a json response containing a dictionary of all the orders' details. 
        (.json for request, get_json for test)"""
        res = self._r.get(self._URL)
        if isinstance(res, requests.models.Response):
            return res.json()
        return res.get_json()

    def get_order(self, order_num):
        """Return a json response object of a specific order by order_num.
        (deserialze by json_loads and then can be coverted to object
        by using Order.from_json())"""
        res = self._r.get(self._URL + "/{}".format(order_num))

        if res.status_code == 200:
            if isinstance(res, requests.models.Response):
                return res.json()
            return res.get_json()
        else:
            return 404

    def add_new_order(self, order_num, order_obj):
        """Add a new order. (Serialize order_obj to a json). Return 201 if success, 404 if failure."""
        order = {str(order_num): json.dumps(order_obj, default=lambda o: o.__dict__, indent=4)}
        res = self._r.post(self._URL, json=order)
        if res.status_code == 404:
            return 404
        else:
            return 201

    def delete_order(self, order_num):
        """Delete an order on flask server. Return 201 if success, 404 if failure."""
        res = self._r.delete(self._URL, json=str(order_num))
        if res.status_code == 404:
            return 404
        else:
            return 201

    def update_order(self, order_num : int, order_obj):
        """Update an existing order on flask server. Return 201 if success, 404 if failure."""
        res = self._r.put(self._URL + "/{}".format(order_num),
            json=json.dumps(order_obj, default=lambda o: o.__dict__, indent=4))
        if res.status_code == 404:
            return 404
        else:
            return 201

    def get_seed_for_lotto(self):
        """Return the seed for lottery store on the flask side."""
        res = self._r.get(self._URL + "/lotto")
        if isinstance(res, requests.models.Response):
            return int(res.json())
        return int(res.get_json())
    
    def set_seed_for_lotto(self, num):
        """Setting the seed to num for lottery on the server."""
        res = self._r.put(self._URL + "/lotto", json = num)
        if res.status_code == 404:
            return 404
        else:
            return 201 
