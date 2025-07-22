from cab_booking.models import Passenger

class PassengerService:
    """Service class for handling passenger-related business logic"""
    
    def __init__(self):
        # In a real application, this would be a database connection
        self.passengers = {}
    
    def create_passenger(self, passenger_data):
        """
        Create a new passenger
        
        Args:
            passenger_data (dict): Contains name, phone, email
            
        Returns:
            Passenger: The created passenger instance
        """
        passenger_id = f"PASS-{len(self.passengers) + 1:08d}"
        
        passenger = Passenger(
            passenger_id=passenger_id,
            name=passenger_data.get('name'),
            phone=passenger_data.get('phone'),
            email=passenger_data.get('email')
        )
        
        self.passengers[passenger_id] = passenger
        return passenger
    
    def get_passenger(self, passenger_id):
        """
        Get a passenger by ID
        
        Args:
            passenger_id (str): The passenger ID
            
        Returns:
            Passenger: The passenger instance if found, None otherwise
        """
        return self.passengers.get(passenger_id)
    
    def update_passenger(self, passenger_id, update_data):
        """
        Update a passenger's information
        
        Args:
            passenger_id (str): The passenger ID
            update_data (dict): The data to update
            
        Returns:
            Passenger: The updated passenger instance if found, None otherwise
        """
        passenger = self.get_passenger(passenger_id)
        if not passenger:
            return None
            
        if 'name' in update_data:
            passenger.name = update_data['name']
        if 'phone' in update_data:
            passenger.phone = update_data['phone']
        if 'email' in update_data:
            passenger.email = update_data['email']
            
        return passenger
    
    def delete_passenger(self, passenger_id):
        """
        Delete a passenger
        
        Args:
            passenger_id (str): The passenger ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        if passenger_id in self.passengers:
            del self.passengers[passenger_id]
            return True
        return False
