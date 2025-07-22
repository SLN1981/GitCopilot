from cab_booking.models import Driver

class DriverService:
    """Service class for handling driver-related business logic"""
    
    def __init__(self):
        # In a real application, this would be a database connection
        self.drivers = {}
    
    def create_driver(self, driver_data):
        """
        Create a new driver
        
        Args:
            driver_data (dict): Contains name, phone, email, license_number
            
        Returns:
            Driver: The created driver instance
        """
        driver_id = f"DRIV-{len(self.drivers) + 1:08d}"
        
        driver = Driver(
            driver_id=driver_id,
            name=driver_data.get('name'),
            phone=driver_data.get('phone'),
            email=driver_data.get('email'),
            license_number=driver_data.get('license_number')
        )
        
        self.drivers[driver_id] = driver
        return driver
    
    def get_driver(self, driver_id):
        """
        Get a driver by ID
        
        Args:
            driver_id (str): The driver ID
            
        Returns:
            Driver: The driver instance if found, None otherwise
        """
        return self.drivers.get(driver_id)
    
    def update_driver(self, driver_id, update_data):
        """
        Update a driver's information
        
        Args:
            driver_id (str): The driver ID
            update_data (dict): The data to update
            
        Returns:
            Driver: The updated driver instance if found, None otherwise
        """
        driver = self.get_driver(driver_id)
        if not driver:
            return None
            
        if 'name' in update_data:
            driver.name = update_data['name']
        if 'phone' in update_data:
            driver.phone = update_data['phone']
        if 'email' in update_data:
            driver.email = update_data['email']
        if 'license_number' in update_data:
            driver.license_number = update_data['license_number']
            
        return driver
    
    def delete_driver(self, driver_id):
        """
        Delete a driver
        
        Args:
            driver_id (str): The driver ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        if driver_id in self.drivers:
            del self.drivers[driver_id]
            return True
        return False
    
    def assign_car(self, driver_id, car):
        """
        Assign a car to a driver
        
        Args:
            driver_id (str): The driver ID
            car (Car): The car to assign
            
        Returns:
            Driver: The updated driver instance if found, None otherwise
        """
        driver = self.get_driver(driver_id)
        if not driver:
            return None
            
        driver.assign_car(car)
        return driver
    
    def update_availability(self, driver_id, is_available):
        """
        Update a driver's availability
        
        Args:
            driver_id (str): The driver ID
            is_available (bool): The availability status
            
        Returns:
            Driver: The updated driver instance if found, None otherwise
        """
        driver = self.get_driver(driver_id)
        if not driver:
            return None
            
        driver.set_availability(is_available)
        return driver
    
    def update_rating(self, driver_id, rating):
        """
        Update a driver's rating
        
        Args:
            driver_id (str): The driver ID
            rating (float): The rating value (1-5)
            
        Returns:
            Driver: The updated driver instance if found, None otherwise
        """
        driver = self.get_driver(driver_id)
        if not driver:
            return None
            
        driver.update_rating(rating)
        return driver
