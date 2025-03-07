import re
from datetime import datetime



def valid_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


class OnlineShoppingSystem:
    def __init__(self):
        self.customers = {}
        self.products = {}
        self.orders = []

    def register_customer(self, customer):
        if customer.id in self.customers:
            raise ValueError(f"Customer with ID {customer.id} already exists.")
        self.customers[customer.id] = customer
        print(f"Customer '{customer.name}' registered successfully!")

    def add_product(self, product):
        if product.id in self.products:
            raise ValueError(f"Product with ID {product.id} already exists.")
        self.products[product.id] = product
        print(f"Product '{product.name}' added successfully!")

    def view_products(self):
        if not self.products:
            print("No available products.")
        else:
            print("Available Products:")
            for product in self.products.values():
                print(product)

    def process_order(self, customer_id, payment_method):
        if customer_id not in self.customers:
            raise ValueError(f"No customer found with ID {customer_id}.")
        customer = self.customers[customer_id]
        if not customer.shopping_cart.products:
            raise ValueError("Shopping cart is empty.")

        
        order = Order()
        for product in customer.shopping_cart.products.values():
            order.add_product(product)
        order.process_payment(payment_method)

        
        customer.shopping_cart.clear_cart()
        customer.orders[order.id] = order
        self.orders.append(order)
        print(f"Order processed successfully for customer '{customer.name}'!")


class Customer:
    customer_id_counter = 0

    def __init__(self, name, email):
        self.id = Customer.customer_id_counter
        Customer.customer_id_counter += 1
        self.name = name
        self.email = email
        self.shopping_cart = ShoppingCart()
        self.orders = {}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not valid_email(value):
            raise ValueError("Invalid email address.")
        self.__email = value

    def add_to_cart(self, product):
        self.shopping_cart.add_product(product)

    def remove_from_cart(self, product):
        self.shopping_cart.remove_product(product)

    def view_cart(self):
        self.shopping_cart.view_cart()

    def view_orders(self):
        if not self.orders:
            print("No orders placed yet.")
        else:
            for order in self.orders.values():
                order.view_order_details()


class Product:
    product_id_counter = 0

    def __init__(self, name, price, description, availability=True):
        self.id = Product.product_id_counter
        Product.product_id_counter += 1
        self.name = name
        self.price = price
        self.description = description
        self.availability = availability

    def __str__(self):
        return (f"Product ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Price: {self.price}\n"
                f"Description: {self.description}\n"
                f"Availability: {'In Stock' if self.availability else 'Out of Stock'}")


class ShoppingCart:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Invalid product type.")
        self.products[product.id] = product

    def remove_product(self, product):
        if product.id not in self.products:
            print(f"Product with ID {product.id} not found in the cart.")
        else:
            del self.products[product.id]
            print(f"Product '{product.name}' removed from the cart.")

    def view_cart(self):
        if not self.products:
            print("Shopping cart is empty.")
        else:
            print("Shopping Cart:")
            for product in self.products.values():
                print(product)

    def clear_cart(self):
        self.products.clear()
        print("Shopping cart cleared.")


class Order:
    order_id_counter = 0

    def __init__(self):
        self.id = Order.order_id_counter
        Order.order_id_counter += 1
        self.products = []
        self.status = "Pending"
        self.payment = None

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Invalid product type.")
        self.products.append(product)

    def process_payment(self, payment_method):
        total_amount = sum(product.price for product in self.products)
        self.payment = Payment(total_amount, payment_method)
        self.status = "Completed"

    def view_order_details(self):
        print(f"Order ID: {self.id}")
        print(f"Status: {self.status}")
        print("Products:")
        for product in self.products:
            print(f"- {product.name} (${product.price})")
        print(self.payment)


class Payment:
    payment_id_counter = 0

    def __init__(self, amount, payment_method):
        self.id = Payment.payment_id_counter
        Payment.payment_id_counter += 1
        self.amount = amount
        self.payment_method = payment_method
        self.payment_date = datetime.now()

    def __str__(self):
        return (f"Payment ID: {self.id}\n"
                f"Amount: ${self.amount}\n"
                f"Method: {self.payment_method}\n"
                f"Date: {self.payment_date}")




system = OnlineShoppingSystem()

customer1 = Customer("Anna", "anna@mail.com")
customer2 = Customer("Karen", "karen@mail.com")
system.register_customer(customer1)
system.register_customer(customer2)

phone = Product("Smartphone", 120000.0, "High-end smartphone with great camera.")
headphones = Product("Headphones", 15000.0, "Wireless headphones with noise cancellation.")
book = Product("Programming Book", 8000.0, "Learn Python with real-world examples.")
system.add_product(phone)
system.add_product(headphones)
system.add_product(book)

print("\nAvailable Products:")
system.view_products()

customer1.add_to_cart(phone)
customer1.add_to_cart(book)
customer2.add_to_cart(headphones)

print("\nAnna's Cart:")
customer1.view_cart()

print("\nKaren's Cart:")
customer2.view_cart()

print("\nAnna is placing an order:")
system.process_order(customer1.id, "Bank Transfer")

print("\nKaren is placing an order:")
system.process_order(customer2.id, "Credit Card")

print("\nAnna's Orders:")
customer1.view_orders()

print("\nKaren's Orders:")
customer2.view_orders()
