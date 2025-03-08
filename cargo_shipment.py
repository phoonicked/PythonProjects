'''
Problem Statement:
Design a system to track cargo shipments.
Create a Cargo class with the following attributes:
cargo_id: Unique identifier (string).
origin: Starting location (string).
destination: Ending location (string).
volume: Volume of the shipment (integer/float).
shipping_date: Date as a string (or datetime object).
Include a method to display cargo details.

Create a ShipmentTracker class that manages multiple Cargo objects. It should include:
A method add_cargo(cargo: Cargo) to add a shipment.
A method remove_cargo(cargo_id: str) to remove a shipment by its ID.
A method get_total_volume(shipping_date: str) -> float to return the total volume of shipments scheduled on that date.

Example:
cargo1 = Cargo("C001", "London", "Rotterdam", 1000, "2025-04-10")
cargo2 = Cargo("C002", "London", "Antwerp", 1500, "2025-04-10")

tracker = ShipmentTracker()
tracker.add_cargo(cargo1)
tracker.add_cargo(cargo2)
print(tracker.get_total_volume("2025-04-10"))  # Expected output: 2500
'''

class Cargo:
    def __init__(self, cargo_id, origin, destination, volume, shipping_data):
        self.cargo_id = cargo_id
        self.origin = origin
        self.destination = destination
        self.volume = volume
        self.shipping_data = shipping_data

class ShipmentTracker:
    def __init__(self):
        self.cargos = {}

    def add_cargo(self, cargo):
        self.cargos[cargo.cargo_id] = cargo
    
    def remove_cargo(self, cargo_id):
        if cargo_id in self.cargos:
            del self.cargos[cargo_id]
    
    def get_total_volume(self, shipping_date) -> float:
        return sum(cargo.volume for cargo in self.cargos.values() if cargo.shipping_data == shipping_date)
    
cargo1 = Cargo("C001", "London", "Rotterdam", 1000, "2025-04-10")
cargo2 = Cargo("C002", "London", "Antwerp", 1500, "2025-04-10")

tracker = ShipmentTracker()
tracker.add_cargo(cargo1)
tracker.add_cargo(cargo2)
print(tracker.get_total_volume("2025-04-10"))