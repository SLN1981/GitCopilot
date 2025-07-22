import datetime

class Fare:
    def __init__(self, booking_id, base_fare, distance_km, time_minutes):
        self.fare_id = f"FARE-{booking_id}"
        self.booking_id = booking_id
        self.base_fare = base_fare
        self.distance_km = distance_km
        self.time_minutes = time_minutes
        self.total_amount = 0
        self.discount = 0
        self.surge_multiplier = 1.0
        self.payment_status = "PENDING"  # PENDING, PAID, FAILED
        self.payment_method = None
        self.timestamp = datetime.datetime.now()
        self.calculate_fare()

    def calculate_fare(self):
        distance_cost = self.distance_km * 10  # Assume rate of $10 per km
        time_cost = self.time_minutes * 2  # Assume rate of $2 per minute
        subtotal = self.base_fare + distance_cost + time_cost
        surge_amount = subtotal * (self.surge_multiplier - 1)
        self.total_amount = (subtotal + surge_amount) * (1 - self.discount / 100)
        return self.total_amount

    def apply_discount(self, discount_percentage):
        self.discount = discount_percentage
        self.calculate_fare()

    def apply_surge_pricing(self, multiplier):
        self.surge_multiplier = multiplier
        self.calculate_fare()

    def mark_as_paid(self, payment_method):
        self.payment_status = "PAID"
        self.payment_method = payment_method

    def generate_receipt(self):
        return {
            "fare_id": self.fare_id,
            "booking_id": self.booking_id,
            "base_fare": self.base_fare,
            "distance_km": self.distance_km,
            "time_minutes": self.time_minutes,
            "discount": self.discount,
            "surge_multiplier": self.surge_multiplier,
            "total_amount": self.total_amount,
            "payment_status": self.payment_status,
            "payment_method": self.payment_method,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return f"Fare {self.fare_id}: ${self.total_amount:.2f} ({self.payment_status})"