from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import csv
from tempfile import NamedTemporaryFile
import shutil

# initalize all delivery file to empty
for f in ["ubereat", "foodora", "inhouse", "pickup"]:
    if f == "foodora":
        with open("./data/{}.csv".format(f), 'w') as fw:
            csv_writer = csv.writer(fw)
            csv_writer.writerow(["ID","_delivery_no","_address","_order","_order_no"])
    else:
        with open("./data/{}.json".format(f), 'w') as fw:
            json.dump({}, fw)

with open("./data/pizza_information.json") as f:
    data = json.load(f)

lotto_seed = [10]
order_details = {}

app = Flask("Assignment 2")
api = Api(app)

# @app.route('/pizza')
# def welcome_pizza():
#     return 'Welcome to Pizza Planet!'


class Pizza(Resource):
    def get(self):
        return 'Welcome to Pizza Planet!'


class PizzaInfo(Resource):
    def get(self):
        return data, 200


class PizzaEachInfo(Resource):
    def get(self, info):
        return data[info], 200

class Order(Resource):
    def get(self):
        return order_details, 200

    def post(self):
        new_order = request.get_json()
        for k in new_order.keys():
            if k in order_details:
                return "Order number already existed", 404 
        order_details.update(new_order)
        return "Added new order",201

    def delete(self):
        delete_order_num = request.get_json()
        if delete_order_num in order_details:
            order_details.pop(delete_order_num)
            return "Order deleted", 201
        else:
            return "Order number does not existed", 404

class EachOrder(Resource):
    def get(self, order_num):
        if (str(order_num) not in order_details):
            return "Order number does not exist", 404
        else:
            return order_details[str(order_num)], 200

    def put(self, order_num):
        updated_order = request.get_json()
        if str(order_num) not in order_details:
            return "Order number does not existed", 404
        order_details[str(order_num)] = updated_order
        return "Updated order", 201


class Delivery(Resource):
    def load_file(self, method):
        if method == 'foodora':
            #return a list of dict
            with open("./data/{}.csv".format(method), 'r') as fr:
                csv_reader = csv.DictReader(fr)
                dict_list = {}
                for line in csv_reader:
                    key_num = line["ID"]
                    dict_list[key_num] = {}
                    for k, v in line.items():
                        if k != "ID":
                            if k == "_order":
                                dict_list[key_num].update({k: json.loads(v.replace("\'", "\""))})
                            else:
                                dict_list[key_num].update({k:v})
                return dict_list
        else:
            with open("./data/{}.json".format(method), 'r') as fr:
                return json.load(fr)

    def write_file(self, method, new_data):
        if method == 'foodora':
            with open("./data/{}.csv".format(method), 'a') as fa:
                csv_writer = csv.writer(fa)
                for k, v in new_data.items():
                    l_value = [k]
                    for val in v.values():
                        l_value.append(val)
                    csv_writer.writerow(l_value)
        else:
            with open("./data/{}.json".format(method), "w") as fw:
                json.dump(new_data, fw)

    def update_delete_csv(self,method, data, change_type):
        filename = "./data/{}.csv".format(method)
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        fields = ["ID", "_delivery_no","_address","_order","_order_no"]
        with open(filename, 'r') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            writer = csv.DictWriter(tempfile, fieldnames=fields)
            for row in reader:
                if row["ID"] in data.keys():
                    if change_type == "update":
                        row["_address"] = data[row["ID"]]["_address"]
                        row["_order"] = data[row["ID"]]["_order"]
                        row["_order_no"] = data[row["ID"]]["_order_no"]
                    else:
                        continue
                writer.writerow(row)
        shutil.move(tempfile.name, filename)

    def get(self, method):
        return self.load_file(method), 200

    def post(self, method):
        data = json.loads(request.get_json())
        current_data = self.load_file(method)
        #check if data exist in current_data
        for k in data.keys():
            if k in current_data:
                return "Order number already exist", 404
        if method == "foodora":
            self.write_file(method, data)
            return "added successfully", 201
        else:
            current_data.update(data)
            self.write_file(method, current_data)
            return "added successfully", 201

    def put(self, method):
        #check if the one we want to update does not exist
        data = json.loads(request.get_json())
        current_data = self.load_file(method)
        for k in data.keys():
            if k not in current_data:
                return "Order number does not exist", 404
        if method == "foodora":
            self.update_delete_csv(method, data, "update")
            return "update successfully", 201
        else:
            current_data.update(data)
            self.write_file(method, current_data)
            return "added successfully", 201

    def delete(self, method):
        #check if the order_num not exist in current data
        order_num = request.get_json()
        current_data = self.load_file(method)
       
        if str(order_num) not in current_data:
            return "Order number does not exist", 404
        if method == "foodora":
            self.update_delete_csv(method, {str(order_num): {}}, "delete")
            return "delete successfully", 201
        else:
            j_file = self.load_file(method)
            del j_file[str(order_num)]
            self.write_file(method, j_file)
            return "delete successfully", 201

class EachDelivery(Resource):
    def get(self, method, delivery_num):
        current_data = Delivery().load_file(method)
        if str(delivery_num) in current_data:
            return current_data[str(delivery_num)], 200
        else:
            return "Delivery Number does not exist", 404

class Lotto(Resource):
    def get(self):
        return lotto_seed[0]

    def put(self):
        new_seed = request.get_json()
        lotto_seed.clear()
        lotto_seed.append(new_seed)
        return 201

api.add_resource(Pizza, '/pizza')
api.add_resource(PizzaInfo, '/pizza/information')
api.add_resource(PizzaEachInfo, '/pizza/information/<string:info>')
api.add_resource(Order, '/pizza/order')
api.add_resource(EachOrder, '/pizza/order/<int:order_num>')
api.add_resource(Delivery, '/pizza/order/delivery/<string:method>')
api.add_resource(EachDelivery, '/pizza/order/delivery/<string:method>/<int:delivery_num>')
api.add_resource(Lotto, '/pizza/order/lotto')


if __name__ == "__main__":
    app.run(debug=True)
