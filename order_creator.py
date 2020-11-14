from order import Order

"""
The class OrderCreator is only used for creating order object.
Design Pattern: Singleton
"""
class OrderCreator:
    _order_no = 0
    _delivery_no = 0
    __instance__ = None

    def __init__(self):
        if OrderCreator.__instance__ is None:
            OrderCreator.__instance__ = self
        else:
            raise Exception("You cannot create another DeliveryCreator object")

    @staticmethod
    def get_instance():
        """ Static method to fetch the current instance.
        """
        if not OrderCreator.__instance__:
            OrderCreator()
        return OrderCreator.__instance__

    def create_order(self, pizza_size: str, pizza_type: str, toppings: [str],
                        drink: str, delivery_type: str) -> Order:
        order = Order(
            OrderCreator._order_no,
            pizza_size,
            pizza_type,
            toppings,
            drink,
            delivery_type,
            OrderCreator._delivery_no
        )
        OrderCreator._order_no += 1
        OrderCreator._delivery_no += 1
        return order