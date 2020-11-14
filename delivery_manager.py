import requests
import json
import csv

class DeliveryManager:
    def __init__(self, r=requests):
        self._r = r
        self._URL = "http://localhost:5000/pizza/order/delivery"
        # d_method should be one of the["ubereat", "foodora", "inhouse", "pickup"]

    def get_delivery(self, d_method):
        """Return a json response get the current delivery dictionary by .json()/ (get_json for test)"""
        res = self._r.get(self._URL + "/{}".format(d_method))
        if isinstance(res, requests.models.Response):
            return res.json()
        return res.get_json()


    def get_each_delivery(self, d_method, delivery_num):
        """Return a json response get the specific delivery number's
         dictionary by .json()/ (get_json for test)"""
        res = self._r.get(self._URL + "/{}/{}".format(d_method, delivery_num))
        if res.status_code == 404:
            return 404
        else:
            if isinstance(res, requests.models.Response):
                return res.json()
            return res.get_json()

    def add_new_delivery(self, d_method, d_obj, delivery_num):
        """Add new delivery on the flask server, return 201 if success, 404 if failure."""
        delivery = {str(delivery_num): d_obj}
        res = self._r.post(self._URL + "/{}".format(d_method),
                          json=json.dumps(delivery,
                                          default=lambda o: o.__dict__,
                                          indent=4))
        if res.status_code == 404:
            return 404
        else:
            return 201

    def update_delivery(self, d_method, d_obj, delivery_num):
        """Update the flask server on delivery obj, return 201 if success, 404 if failure."""
        delivery = {str(delivery_num): d_obj}
        res = self._r.put(self._URL + "/{}".format(d_method),
                         json=json.dumps(delivery, default=lambda o: o.__dict__,
                                         indent=4))
        if res.status_code == 404:
            return 404
        else:
            return 201

    def delete_delivery(self, d_method, delivery_num):
        """Delete the delivery obj by delivery_num on the flask server, return 201 if success, 
        404 if failure."""
        res = self._r.delete(self._URL + "/{}".format(d_method),
                            json=delivery_num)
        if res.status_code == 404:
            return 404
        else:
            return 201

    def get_delivery_types(self):
        """Return a list of supporting delivery type."""
        return ["ubereat", "foodora", "inhouse", "pickup"]
