class Driver:
    def __init__(self, driver_id, name, phone, email, license_number):
        self.driver_id = driver_id
        self.name = name
        self.phone = phone
        self.email = email
        self.license_number = license_number
        self.is_available = True
        self.rating = 0.0
        self.total_ratings = 0
        self.assigned_car = None

    def assign_car(self, car):
        self.assigned_car = car

    def set_availability(self, is_available):
        self.is_available = is_available

    def update_rating(self, new_rating):
        total = self.rating * self.total_ratings
        self.total_ratings += 1
        self.rating = (total + new_rating) / self.total_ratings

    def __str__(self):
        return f"{self.name} ({self.driver_id}) - Rating: {self.rating:.1f}"