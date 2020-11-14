import requests
import json

class PizzaManager:
    def __init__(self, r = requests):
        self._r = r
        self._URL = "http://localhost:5000/pizza/information"

    def get_pizza_types(self):
        """Return a json response object that contain list of pizza types and their prices,
         access through .json() (get_json if test)."""
        param = "Types"
        full_URL = self._URL + "/{}".format(param)
        res = self._r.get(full_URL)
        #res.json()

        if isinstance(res, requests.models.Response):
            return res.json()
        return res.get_json()

    def get_pizza_toppings(self):
        """Return a json response object that contain list of pizza toppings and their prices,
         access through .json()."""
        param = "Toppings"
        full_URL = self._URL + "/{}".format(param)
        res = self._r.get(full_URL)

        if isinstance(res, requests.models.Response):
            return res.json()
        return res.get_json()

    def get_pizza_sizes(self):
        """Return a json response object that contain list of pizza sizes and their prices,
         access through .json()."""
        param = "Sizes"
        full_URL = self._URL + "/{}".format(param)
        res = self._r.get(full_URL)

        if isinstance(res, requests.models.Response):
            return res.json()
        return res.get_json()

    def get_drinks(self):
        """Return a json response object that contain list of pizza drinks and their prices,
         access through .json()."""
        param = "Drinks"
        full_URL = self._URL + "/{}".format(param)
        res = self._r.get(full_URL)

        if isinstance(res, requests.models.Response):
            return res.json()
        return res.get_json()

    def get_predefined(self):
        param = "PreDefined"
        full_URL = self._URL + "/{}".format(param)
        res = self._r.get(full_URL)

        if isinstance(res, requests.models.Response):
            return res.json()
        return res.get_json()
