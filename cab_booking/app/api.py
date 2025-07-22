from flask import Flask, request, jsonify
import uuid
import sys
import os

# Add parent directory to path to allow relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from cab_booking.models import Booking, Car, Driver, Passenger, Fare

app = Flask(__name__)

# In-memory storage for demo purposes
cars = {}
drivers = {}
passengers = {}
bookings = {}

# Helper function to generate IDs
def generate_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

# Route to get API status
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'status': 'online',
        'message': 'Cab Booking API is running'
    })

# PASSENGER ENDPOINTS
@app.route('/api/passengers', methods=['POST'])
def create_passenger():
    data = request.json
    passenger_id = generate_id('PASS')
    
    passenger = Passenger(
        passenger_id=passenger_id,
        name=data.get('name'),
        phone=data.get('phone'),
        email=data.get('email')
    )
    
    passengers[passenger_id] = passenger
    
    return jsonify({
        'message': 'Passenger created successfully',
        'passenger_id': passenger_id
    }), 201

@app.route('/api/passengers/<passenger_id>', methods=['GET'])
def get_passenger(passenger_id):
    passenger = passengers.get(passenger_id)
    if not passenger:
        return jsonify({'error': 'Passenger not found'}), 404
    
    return jsonify({
        'passenger_id': passenger.passenger_id,
        'name': passenger.name,
        'phone': passenger.phone,
        'email': passenger.email
    })

# DRIVER ENDPOINTS
@app.route('/api/drivers', methods=['POST'])
def create_driver():
    data = request.json
    driver_id = generate_id('DRIV')
    
    driver = Driver(
        driver_id=driver_id,
        name=data.get('name'),
        phone=data.get('phone'),
        email=data.get('email'),
        license_number=data.get('license_number')
    )
    
    drivers[driver_id] = driver
    
    return jsonify({
        'message': 'Driver created successfully',
        'driver_id': driver_id
    }), 201

@app.route('/api/drivers/<driver_id>', methods=['GET'])
def get_driver(driver_id):
    driver = drivers.get(driver_id)
    if not driver:
        return jsonify({'error': 'Driver not found'}), 404
    
    return jsonify({
        'driver_id': driver.driver_id,
        'name': driver.name,
        'phone': driver.phone,
        'email': driver.email,
        'license_number': driver.license_number,
        'is_available': driver.is_available,
        'rating': driver.rating,
        'assigned_car': str(driver.assigned_car) if driver.assigned_car else None
    })

# CAR ENDPOINTS
@app.route('/api/cars', methods=['POST'])
def create_car():
    data = request.json
    car_id = generate_id('CAR')
    
    car = Car(
        car_id=car_id,
        model=data.get('model'),
        make=data.get('make'),
        year=data.get('year'),
        license_plate=data.get('license_plate'),
        capacity=data.get('capacity'),
        car_type=data.get('car_type')
    )
    
    cars[car_id] = car
    
    return jsonify({
        'message': 'Car created successfully',
        'car_id': car_id
    }), 201

@app.route('/api/cars/<car_id>', methods=['GET'])
def get_car(car_id):
    car = cars.get(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404
    
    return jsonify({
        'car_id': car.car_id,
        'model': car.model,
        'make': car.make,
        'year': car.year,
        'license_plate': car.license_plate,
        'capacity': car.capacity,
        'car_type': car.car_type,
        'is_available': car.is_available,
        'features': car.features
    })

# BOOKING ENDPOINTS
@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    booking_id = generate_id('BOOK')
    
    passenger_id = data.get('passenger_id')
    passenger = passengers.get(passenger_id)
    if not passenger:
        return jsonify({'error': 'Passenger not found'}), 404
    
    booking = Booking(
        booking_id=booking_id,
        passenger=passenger,
        from_location=data.get('from_location'),
        to_location=data.get('to_location')
    )
    
    # Set estimated trip details
    booking.set_estimated_trip_details(
        data.get('estimated_distance_km', 0),
        data.get('estimated_duration_minutes', 0)
    )
    
    bookings[booking_id] = booking
    passenger.add_to_booking_history(booking)
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking_id': booking_id
    }), 201

@app.route('/api/bookings/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    return jsonify(booking.get_trip_details())

@app.route('/api/bookings/<booking_id>/assign-driver', methods=['POST'])
def assign_driver_to_booking(booking_id):
    data = request.json
    driver_id = data.get('driver_id')
    
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    driver = drivers.get(driver_id)
    if not driver:
        return jsonify({'error': 'Driver not found'}), 404
    
    booking.assign_driver(driver)
    
    return jsonify({
        'message': 'Driver assigned to booking successfully',
        'booking_id': booking_id,
        'driver_id': driver_id
    })

@app.route('/api/bookings/<booking_id>/start', methods=['PUT'])
def start_trip(booking_id):
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if not booking.driver:
        return jsonify({'error': 'Cannot start trip without assigned driver'}), 400
    
    booking.start_trip()
    
    return jsonify({
        'message': 'Trip started successfully',
        'booking_id': booking_id,
        'status': booking.status
    })

@app.route('/api/bookings/<booking_id>/complete', methods=['PUT'])
def complete_trip(booking_id):
    data = request.json
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.status != 'IN_PROGRESS':
        return jsonify({'error': 'Only in-progress trips can be completed'}), 400
    
    booking.complete_trip(
        data.get('actual_distance_km', booking.estimated_distance_km),
        data.get('actual_duration_minutes', booking.estimated_duration_minutes)
    )
    
    # Calculate fare after trip completion
    fare = booking.calculate_fare()
    
    return jsonify({
        'message': 'Trip completed successfully',
        'booking_id': booking_id,
        'status': booking.status,
        'fare': fare.generate_receipt() if fare else None
    })

@app.route('/api/bookings/<booking_id>/cancel', methods=['PUT'])
def cancel_trip(booking_id):
    data = request.json
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.status in ['COMPLETED', 'CANCELLED']:
        return jsonify({'error': 'Cannot cancel a completed or already cancelled trip'}), 400
    
    booking.cancel_trip(data.get('reason'))
    
    return jsonify({
        'message': 'Trip cancelled successfully',
        'booking_id': booking_id,
        'status': booking.status
    })

if __name__ == '__main__':
    app.run(debug=True)
