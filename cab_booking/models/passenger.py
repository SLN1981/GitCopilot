class Passenger:
    def __init__(self, passenger_id, name, phone, email):
        self.passenger_id = passenger_id
        self.name = name
        self.phone = phone
        self.email = email
        self.payment_methods = []
        self.booking_history = []
        self.favorite_locations = []

    def add_payment_method(self, payment_method):
        self.payment_methods.append(payment_method)

    def add_to_booking_history(self, booking):
        self.booking_history.append(booking)

    def add_favorite_location(self, location):
        self.favorite_locations.append(location)

    def get_recent_bookings(self, limit=5):
        return self.booking_history[-limit:] if len(self.booking_history) > 0 else []

    def __str__(self):
        return f"{self.name} ({self.passenger_id})"