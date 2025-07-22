from cab_booking.models import Booking, Fare

class BookingService:
    """Service class for handling booking-related business logic"""
    
    def __init__(self, passenger_service=None, driver_service=None, car_service=None):
        # In a real application, this would be a database connection
        self.bookings = {}
        self.passenger_service = passenger_service
        self.driver_service = driver_service
        self.car_service = car_service
    
    def create_booking(self, booking_data):
        """
        Create a new booking
        
        Args:
            booking_data (dict): Contains passenger_id, from_location, to_location,
                                estimated_distance_km, estimated_duration_minutes
                                
        Returns:
            Booking: The created booking instance
        """
        booking_id = f"BOOK-{len(self.bookings) + 1:08d}"
        
        # Get the passenger
        passenger_id = booking_data.get('passenger_id')
        passenger = None
        if self.passenger_service:
            passenger = self.passenger_service.get_passenger(passenger_id)
        
        if not passenger:
            raise ValueError(f"Passenger with ID {passenger_id} not found")
        
        # Create the booking
        booking = Booking(
            booking_id=booking_id,
            passenger=passenger,
            from_location=booking_data.get('from_location'),
            to_location=booking_data.get('to_location')
        )
        
        # Set estimated trip details
        booking.set_estimated_trip_details(
            booking_data.get('estimated_distance_km', 0),
            booking_data.get('estimated_duration_minutes', 0)
        )
        
        # Add the booking to the passenger's history
        passenger.add_to_booking_history(booking)
        
        # Store the booking
        self.bookings[booking_id] = booking
        
        return booking
    
    def get_booking(self, booking_id):
        """
        Get a booking by ID
        
        Args:
            booking_id (str): The booking ID
            
        Returns:
            Booking: The booking instance if found, None otherwise
        """
        return self.bookings.get(booking_id)
    
    def assign_driver(self, booking_id, driver_id):
        """
        Assign a driver to a booking
        
        Args:
            booking_id (str): The booking ID
            driver_id (str): The driver ID
            
        Returns:
            Booking: The updated booking instance
        """
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found")
        
        driver = None
        if self.driver_service:
            driver = self.driver_service.get_driver(driver_id)
        
        if not driver:
            raise ValueError(f"Driver with ID {driver_id} not found")
        
        # Assign the driver
        booking.assign_driver(driver)
        
        # Update driver and car availability
        if driver.assigned_car and self.car_service:
            self.car_service.update_availability(driver.assigned_car.car_id, False)
        if self.driver_service:
            self.driver_service.update_availability(driver_id, False)
        
        return booking
    
    def start_trip(self, booking_id):
        """
        Start a trip
        
        Args:
            booking_id (str): The booking ID
            
        Returns:
            Booking: The updated booking instance
        """
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found")
        
        if not booking.driver:
            raise ValueError(f"Booking {booking_id} does not have an assigned driver")
        
        booking.start_trip()
        return booking
    
    def complete_trip(self, booking_id, trip_data):
        """
        Complete a trip
        
        Args:
            booking_id (str): The booking ID
            trip_data (dict): Contains actual_distance_km, actual_duration_minutes
            
        Returns:
            Booking: The updated booking instance
        """
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found")
        
        if booking.status != 'IN_PROGRESS':
            raise ValueError(f"Booking {booking_id} is not in progress")
        
        # Complete the trip with actual metrics
        booking.complete_trip(
            trip_data.get('actual_distance_km', booking.estimated_distance_km),
            trip_data.get('actual_duration_minutes', booking.estimated_duration_minutes)
        )
        
        # Calculate the fare
        fare = booking.calculate_fare(trip_data.get('base_fare', 50))
        
        # Apply surge pricing if provided
        if 'surge_multiplier' in trip_data:
            fare.apply_surge_pricing(trip_data['surge_multiplier'])
        
        # Apply discount if provided
        if 'discount' in trip_data:
            fare.apply_discount(trip_data['discount'])
        
        # Update driver and car availability
        if booking.driver and self.driver_service:
            self.driver_service.update_availability(booking.driver.driver_id, True)
            
        if booking.car and self.car_service:
            self.car_service.update_availability(booking.car.car_id, True)
        
        return booking
    
    def cancel_trip(self, booking_id, reason=None):
        """
        Cancel a trip
        
        Args:
            booking_id (str): The booking ID
            reason (str, optional): The cancellation reason
            
        Returns:
            Booking: The updated booking instance
        """
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found")
        
        if booking.status in ['COMPLETED', 'CANCELLED']:
            raise ValueError(f"Booking {booking_id} cannot be cancelled")
        
        booking.cancel_trip(reason)
        
        # Update driver and car availability if a driver was assigned
        if booking.driver and self.driver_service:
            self.driver_service.update_availability(booking.driver.driver_id, True)
            
        if booking.car and self.car_service:
            self.car_service.update_availability(booking.car.car_id, True)
        
        return booking
    
    def get_trip_details(self, booking_id):
        """
        Get detailed information about a trip
        
        Args:
            booking_id (str): The booking ID
            
        Returns:
            dict: The trip details
        """
        booking = self.get_booking(booking_id)
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found")
        
        return booking.get_trip_details()
    
    def get_passenger_bookings(self, passenger_id):
        """
        Get all bookings for a passenger
        
        Args:
            passenger_id (str): The passenger ID
            
        Returns:
            list: List of booking instances
        """
        passenger_bookings = []
        for booking in self.bookings.values():
            if booking.passenger and booking.passenger.passenger_id == passenger_id:
                passenger_bookings.append(booking)
                
        return passenger_bookings
    
    def get_driver_bookings(self, driver_id):
        """
        Get all bookings for a driver
        
        Args:
            driver_id (str): The driver ID
            
        Returns:
            list: List of booking instances
        """
        driver_bookings = []
        for booking in self.bookings.values():
            if booking.driver and booking.driver.driver_id == driver_id:
                driver_bookings.append(booking)
                
        return driver_bookings
