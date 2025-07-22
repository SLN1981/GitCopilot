"""
This module contains initialization for the services package.
"""

from .passenger_service import PassengerService
from .driver_service import DriverService
from .car_service import CarService
from .booking_service import BookingService

# Initialize services
passenger_service = PassengerService()
driver_service = DriverService()
car_service = CarService()
booking_service = BookingService(
    passenger_service=passenger_service,
    driver_service=driver_service,
    car_service=car_service
)
