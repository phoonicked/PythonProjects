'''
Problem Statement:
Implement a simplified order book for commodity trading.

Create an Order class with the following attributes:

order_id: Unique identifier (string).
commodity: E.g., "Oil" or "Gas".
quantity: Amount of commodity.
price: Price per unit.
order_type: Either "buy" or "sell".
Create an OrderBook class that can:

Add orders (add_order).
Cancel orders (cancel_order).
Match orders: Implement a method match_orders(commodity: str) that 
finds one buy order and one sell order for the same commodity such that 
the buy price is greater than or equal to the sell price, and then 
removes them from the book (simulating a trade).

Example:
order1 = Order("O001", "Oil", 100, 50, "buy")
order2 = Order("O002", "Oil", 100, 45, "sell")
order_book = OrderBook()
order_book.add_order(order1)
order_book.add_order(order2)
matched = order_book.match_orders("Oil")
if matched:
    print(f"Matched: {matched[0].order_id} with {matched[1].order_id}")
else:
    print("No match found")
# Expected: Matched orders because 50 >= 45.
'''

class Order:
    def __init__(self, order_id, commodity, quantity, price, order_type):
        self.order_id = order_id
        self.commodity = commodity
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
    
class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.order_type == "buy":
            self.buy_orders.append(order)
        elif order.order_type == "sell":
            self.sell_orders.append(order)

    def cancel_order(self, order_id):
        self.buy_orders = [order for order in self.buy_orders if order.oder_id != order_id]
        self.sell_orders = [order for order in self.sell_orders if order.oder_id != order_id]

    def match_orders(self, commodity: str):
        buy_orders = [order for order in self.buy_orders if order.commodity == commodity]
        sell_orders = [order for order in self.sell_orders if order.commodity == commodity]

        buy_orders.sort(key=lambda o: o.price, reverse=True)
        sell_orders.sort(key=lambda o: o.price)
        
        for buy in buy_orders:
            for sell in sell_orders:
                if buy.price >= sell.price:
                    self.buy_orders.remove(buy)
                    self.sell_orders.remove(sell)
                    return (buy, sell)

        return None
    
if __name__ == "__main__":
    order1 = Order("O001", "Oil", 10, 50, "buy")
    order2 = Order("O002", "Oil", 100, 45, "sell")
    order3 = Order("O003", "Oil", 600, 50, "buy")
    order4 = Order("O004", "Oil", 300, 35, "sell")
    order_book = OrderBook()
    order_book.add_order(order1)
    order_book.add_order(order2)
    order_book.add_order(order3)
    order_book.add_order(order4)
    match = order_book.match_orders("Oil")
    if match:
        print(f"Matched: {match[0].order_id} with {match[1].order_id}")
    else:
        print("No match found")
