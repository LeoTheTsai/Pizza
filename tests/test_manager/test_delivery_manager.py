from PizzaParlour import app
from delivery_manager import DeliveryManager
import unittest
import json
import csv

class TestDeliveryManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDeliveryManager, self).__init__(*args, **kwargs)
        self.server = app.test_client()
        self.delivery_manager = DeliveryManager(self.server)
        self.fields = self.delivery_manager.get_delivery_types()
        #initialize test data, insert into each file some data
        self.data_key = "1"
        self.data = {"_delivery_no": "1", 
                        "_address": "local", 
                        "_order": {"topping": "beef"}, 
                        "_order_no": "2"
                    }
        #clear all the data in the file first
        self.reset_file()


    def test_get_delivery(self):
        self.add_data()
        for f in self.fields:
            actual = self.delivery_manager.get_delivery(f)
            expected = {self.data_key: self.data}
            assert actual == expected
        self.reset_file()

    def test_get_each_delivery(self):
        self.add_data()
        for f in self.fields:
            actual = self.delivery_manager.get_each_delivery(f, self.data_key)
            expected = self.data
            assert actual == expected
        self.reset_file()

    def test_add_delivery_num_not_exist(self):
        for f in self.fields:
            actual = self.delivery_manager.add_new_delivery(f, self.data, self.data_key)
            expected = 201
            assert actual == expected
        self.reset_file()

    def test_add_delivery_num_exist(self):
        self.add_data()
        for f in self.fields:
            actual = self.delivery_manager.add_new_delivery(f, self.data, self.data_key)
            expected = 404
            assert actual == expected
        self.reset_file()

    def test_update_delivery_num_exist(self):
        self.add_data()
        new_key = "1"
        new_data = {"_delivery_no": "1", 
                        "_address": "fishmarket", 
                        "_order": {"topping": "chicken"}, 
                        "_order_no": "2"
                    }
        for f in self.fields:
            actual = self.delivery_manager.update_delivery(f, new_data, new_key)
            expected = 201
            assert actual == expected
        self.reset_file()
    
    def test_update_delivery_num_not_exist(self):
        self.add_data()
        for f in self.fields:
            actual = self.delivery_manager.update_delivery(f, None, "2")
            expected = 404
            assert actual == expected
        self.reset_file()

    def test_delete_delivery_num_exist(self):
        self.add_data()
        for f in self.fields:
            actual = self.delivery_manager.delete_delivery(f, self.data_key)
            expected = 201
            assert actual == expected
        self.reset_file()

    def test_delete_delivery_num_not_exist(self):
        self.add_data()
        for f in self.fields:
            actual = self.delivery_manager.delete_delivery(f, "2")
            expected = 404
            assert actual == expected
        self.reset_file()

    def reset_file(self):
        for f in self.fields:
            if f == "foodora":
                with open("./data/{}.csv".format(f), 'w') as fw:
                    csv_writer = csv.writer(fw)
                    csv_writer.writerow(["ID","_delivery_no","_address","_order","_order_no"])
            else:
                with open("./data/{}.json".format(f), 'w') as fw:
                    json.dump({}, fw)

    def add_data(self):
        for f in self.fields:
            self.server.post(self.delivery_manager._URL + "/{}".format(f), 
                json = json.dumps({self.data_key: self.data}))
        
    
