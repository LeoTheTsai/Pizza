import unittest
from PizzaParlour import app
import json
import csv

class DeliveryTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DeliveryTest, self).__init__(*args, **kwargs)
        self.URL = "http://localhost:5000/pizza/order/delivery"
        self.server = app.test_client()
        self.test_not_exist_data = {"0": {"_delivery_no" : "0", "_address": "international", "_order": {"topping": "fish"}, "_order_no": "2"}}
        self.test_data = {"1": {"_delivery_no" : "1", "_address": "local", "_order": {"topping": "beef"}, "_order_no": "1"}}
        self.updated_data = {"1": {"_delivery_no" : "1", "_address": "local", "_order": {"topping": "chicken"}, "_order_no": "1"}}
        self.l = ["ubereat", "pickup", "inhouse", "foodora"]

        #reset the file
        self.reset_file()
        #initialize some value into the file

    def test_get_delivery(self):
        for s in self.l:
            r = self.server.get(self.URL + "/{}".format(s))
            assert r.status_code == 200
        self.reset_file()

    def test_add_delivery_post(self):
        for s in self.l:
            r = self.server.post(self.URL + "/{}".format(s), json = json.dumps(self.test_data))
            assert r.status_code == 201
        self.reset_file()

    def test_add_delivery_post_exist_delivery_no(self):
        for s in self.l:
            #add data first
            self.server.post(self.URL + "/{}".format(s), json = json.dumps(self.test_data))
            #test same data
            r = self.server.post(self.URL + "/{}".format(s), json = json.dumps(self.test_data))
            assert r.status_code == 404
        self.reset_file()

    def test_each_delivery_num_exist(self):
        for s in self.l:
            self.server.post(self.URL + "/{}".format(s), json = json.dumps(self.test_data))
            r = self.server.get(self.URL + "/{}/{}".format(s, 1))
            self.server.delete(self.URL + "/{}".format(s), json = "1")
            assert r.status_code == 200
        self.reset_file()
            

    def test_each_delivery_num_not_exist(self):
        for s in self.l:
            r = self.server.get(self.URL + "/{}/{}".format(s, 3))
            assert r.status_code == 404
        self.reset_file()

    def test_change_delivery_put(self):
        for s in self.l:
            #add unchange data first 
            self.server.post(self.URL + "/{}".format(s), json = json.dumps(self.test_data))
            r = self.server.put(self.URL + "/{}".format(s), json = json.dumps(self.updated_data))
            assert r.status_code == 201
        self.reset_file()

    def test_change_delivery_post_delivery_no_not_exist(self):
        for s in self.l:
            r = self.server.put(self.URL + "/{}".format(s), json = json.dumps(self.test_not_exist_data))
            assert r.status_code == 404
        self.reset_file()

    def test_delete_delivery(self):
        for s in self.l:
            # add sample data first
            self.server.post(self.URL + "/{}".format(s), json = json.dumps(self.test_data))
            r = self.server.delete(self.URL + "/{}".format(s), json = "1")
            assert r.status_code == 201
        self.reset_file()

    def test_delete_delivery_num_not_exist(self):
        for s in self.l:
            r = self.server.delete(self.URL + "/{}".format(s), json = "3")
            assert r.status_code == 404
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
                    