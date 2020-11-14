# a2-starter

## Package required to install:

**Flask**: pip install Flask

**Flask_restful**: pip install flask-restful

**requests**: pip install requests

**pytest**: pip install pytest

**Tempfile**: pip install tempfile

**Shutil**: pip install shutil

## Instruction:

Run the flask module by running: python3 PizzaParlour.py

Start the CLI by running: python3 order_handler.py

Run pytest with by running: pytest --cov-report term --cov=. tests
 
## Pair Programming

We decided to do a lottery system and multiple toppings adding functionality into a pizza as our pair programming feature design.

We worked on the lottery system first. Leo was the driver for this feature and Walker was the navigator. During the pair programming, Walker directed Leo on how to handle user input and setting seeds for the lottery systems in the cli with the lottery() function. Then, Leo added a server call on the order manager and handled the flask side request on pizzaParlour. 

And then we switched roles when starting working on the multiple toppings feature: Walker became the driver and Leo became the navigator. Walker started by changing the attribute “topping” from type str to type list of str in class Order. And then Leo directed Walker to make a change in class OrderManager to make it accept the new attribute type in class Order. Next, Walker went back to the CLI side and discussed with Leo about how the new user interface should look like (e.g. what question to ask users, when to accept input). After that, we were basically done with this feature and what only left to do is writing tests for it.

**Reflection:**
Overall, the pair programming process went smoothly in our team. We both like and dislike the idea of the driver and navigator. Although it improves our correctness and cleaness of our code as the other person can point out errors right away, it also wastes a lot of time on debating on an idea.
 
## Design Patterns

**Data Access Object:**
We implemented class Order, Delivery, DataManager, PizzaManager, OrderManager, DeliveryManager,  OrderCreator, and DeliveryOrder with DAO to develop abstraction layers.

**Single Responsibility Principle:**
All of our classes do and only do one task. For example, PizzaManager is only responsible for sending information about pizza type, pizza topping, and etc. The task of class OrderHandler is complex, so its methods separate its task to many small tasks and each of these methods only performs specific functionality for class OrderHandler.

**Open/Close Principle:**
Our design allows us to easily add new functionality. For example, if we need to handle a new type of data, we can just add a new manager class and it would not affect other manager classes.

**Dependency Injection:**
When creating Order object and Delivery object, we should let class OrderCreator and DeliveryCreator do the work.

**Singleton:**
Class OrderCreator and DeliveryCreator are singleton classes since their only task is to create Order objects or Delivery objects.

## CODE CRAFTSMANSHIP
To keep our code clean and consistent we install pylint to check our syntax error or any inconsistent code. Also, we use visual studio as our IDE as we can easily debug our code, fix the bug, and even navigate between files smoothly.
