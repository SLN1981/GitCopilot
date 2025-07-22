from cab_booking.models import Car

class CarService:
    """Service class for handling car-related business logic"""
    
    def __init__(self):
        # In a real application, this would be a database connection
        self.cars = {}
    
    def create_car(self, car_data):
        """
        Create a new car
        
        Args:
            car_data (dict): Contains model, make, year, license_plate, capacity, car_type
            
        Returns:
            Car: The created car instance
        """
        car_id = f"CAR-{len(self.cars) + 1:08d}"
        
        car = Car(
            car_id=car_id,
            model=car_data.get('model'),
            make=car_data.get('make'),
            year=car_data.get('year'),
            license_plate=car_data.get('license_plate'),
            capacity=car_data.get('capacity'),
            car_type=car_data.get('car_type')
        )
        
        # Add features if provided
        if 'features' in car_data:
            for feature in car_data['features']:
                car.add_feature(feature)
        
        self.cars[car_id] = car
        return car
    
    def get_car(self, car_id):
        """
        Get a car by ID
        
        Args:
            car_id (str): The car ID
            
        Returns:
            Car: The car instance if found, None otherwise
        """
        return self.cars.get(car_id)
    
    def update_car(self, car_id, update_data):
        """
        Update a car's information
        
        Args:
            car_id (str): The car ID
            update_data (dict): The data to update
            
        Returns:
            Car: The updated car instance if found, None otherwise
        """
        car = self.get_car(car_id)
        if not car:
            return None
            
        # Update car attributes if provided
        if 'model' in update_data:
            car.model = update_data['model']
        if 'make' in update_data:
            car.make = update_data['make']
        if 'year' in update_data:
            car.year = update_data['year']
        if 'license_plate' in update_data:
            car.license_plate = update_data['license_plate']
        if 'capacity' in update_data:
            car.capacity = update_data['capacity']
        if 'car_type' in update_data:
            car.car_type = update_data['car_type']
            
        # Add new features if provided
        if 'features' in update_data:
            car.features = []  # Reset features
            for feature in update_data['features']:
                car.add_feature(feature)
            
        return car
    
    def delete_car(self, car_id):
        """
        Delete a car
        
        Args:
            car_id (str): The car ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        if car_id in self.cars:
            del self.cars[car_id]
            return True
        return False
    
    def update_availability(self, car_id, is_available):
        """
        Update a car's availability
        
        Args:
            car_id (str): The car ID
            is_available (bool): The availability status
            
        Returns:
            Car: The updated car instance if found, None otherwise
        """
        car = self.get_car(car_id)
        if not car:
            return None
            
        car.set_availability(is_available)
        return car
    
    def update_location(self, car_id, location):
        """
        Update a car's location
        
        Args:
            car_id (str): The car ID
            location (dict): The location data (e.g., latitude, longitude)
            
        Returns:
            Car: The updated car instance if found, None otherwise
        """
        car = self.get_car(car_id)
        if not car:
            return None
            
        car.update_location(location)
        return car
    
    def get_available_cars(self, car_type=None):
        """
        Get all available cars, optionally filtered by type
        
        Args:
            car_type (str, optional): The car type to filter by
            
        Returns:
            list: List of available car instances
        """
        available_cars = [car for car in self.cars.values() if car.is_available]
        
        if car_type:
            available_cars = [car for car in available_cars if car.car_type == car_type]
            
        return available_cars
