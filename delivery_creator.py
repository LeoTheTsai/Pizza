from order import Order
from delivery import Delivery

"""
The class DeliveryCreator is only used for creating delivery object.
Design Pattern: Singleton
"""
class DeliveryCreator:
    __instance__ = None

    def __init__(self):
        if DeliveryCreator.__instance__ is None:
            DeliveryCreator.__instance__ = self
        else:
            raise Exception("You cannot create another DeliveryCreator object")

    @staticmethod
    def get_instance():
        """ Static method to fetch the current instance.
        """
        if not DeliveryCreator.__instance__:
            DeliveryCreator()
        return DeliveryCreator.__instance__

    def create_delivery(self, address: str, order: Order,
                        order_no: int) -> Delivery:
        delivery = Delivery(order.get_delivery_no(), address, order, order_no)
        return delivery
