class Car:
    def __init__(self, car_id, model, make, year, license_plate, capacity, car_type):
        self.car_id = car_id
        self.model = model
        self.make = make
        self.year = year
        self.license_plate = license_plate
        self.capacity = capacity
        self.car_type = car_type  # e.g., 'economy', 'premium', 'suv'
        self.is_available = True
        self.current_location = None
        self.features = []

    def update_location(self, location):
        self.current_location = location

    def set_availability(self, is_available):
        self.is_available = is_available

    def add_feature(self, feature):
        self.features.append(feature)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - {self.license_plate}"