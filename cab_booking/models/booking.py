import datetime

class Booking:
    def __init__(self, booking_id, passenger, from_location, to_location):
        self.booking_id = booking_id
        self.passenger = passenger
        self.driver = None
        self.car = None
        self.from_location = from_location
        self.to_location = to_location
        self.status = "REQUESTED"  # REQUESTED, ACCEPTED, IN_PROGRESS, COMPLETED, CANCELLED
        self.request_time = datetime.datetime.now()
        self.pickup_time = None
        self.completion_time = None
        self.cancellation_time = None
        self.cancellation_reason = None
        self.estimated_distance_km = 0
        self.estimated_duration_minutes = 0
        self.actual_distance_km = 0
        self.actual_duration_minutes = 0
        self.fare = None

    def assign_driver(self, driver):
        self.driver = driver
        self.car = driver.assigned_car
        self.status = "ACCEPTED"
        return self

    def start_trip(self):
        self.status = "IN_PROGRESS"
        self.pickup_time = datetime.datetime.now()
        return self

    def complete_trip(self, actual_distance_km, actual_duration_minutes):
        self.status = "COMPLETED"
        self.completion_time = datetime.datetime.now()
        self.actual_distance_km = actual_distance_km
        self.actual_duration_minutes = actual_duration_minutes
        return self

    def cancel_trip(self, reason=None):
        self.status = "CANCELLED"
        self.cancellation_time = datetime.datetime.now()
        self.cancellation_reason = reason
        return self

    def set_estimated_trip_details(self, distance_km, duration_minutes):
        self.estimated_distance_km = distance_km
        self.estimated_duration_minutes = duration_minutes
        return self

    def calculate_fare(self, base_fare=50):
        from .fare import Fare
        if self.status == "COMPLETED" and self.fare is None:
            self.fare = Fare(
                self.booking_id,
                base_fare,
                self.actual_distance_km,
                self.actual_duration_minutes
            )
        return self.fare

    def get_trip_details(self):
        return {
            "booking_id": self.booking_id,
            "passenger": str(self.passenger) if self.passenger else None,
            "driver": str(self.driver) if self.driver else None,
            "car": str(self.car) if self.car else None,
            "from_location": self.from_location,
            "to_location": self.to_location,
            "status": self.status,
            "request_time": self.request_time,
            "pickup_time": self.pickup_time,
            "completion_time": self.completion_time,
            "estimated_distance_km": self.estimated_distance_km,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "actual_distance_km": self.actual_distance_km,
            "actual_duration_minutes": self.actual_duration_minutes,
            "fare": self.fare.generate_receipt() if self.fare else None
        }

    def __str__(self):
        return f"Booking {self.booking_id}: {self.from_location} -> {self.to_location} ({self.status})"
