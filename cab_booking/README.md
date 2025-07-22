# Cab Booking API
This file provides documentation on how to use the Cab Booking REST API.

## API Endpoints

### Status Check
- `GET /api/status`: Check if the API is running

### Passenger Endpoints
- `POST /api/passengers`: Create a new passenger
- `GET /api/passengers/<passenger_id>`: Get passenger details

### Driver Endpoints
- `POST /api/drivers`: Create a new driver
- `GET /api/drivers/<driver_id>`: Get driver details

### Car Endpoints
- `POST /api/cars`: Register a new car
- `GET /api/cars/<car_id>`: Get car details

### Booking Endpoints
- `POST /api/bookings`: Create a new booking
- `GET /api/bookings/<booking_id>`: Get booking details
- `POST /api/bookings/<booking_id>/assign-driver`: Assign a driver to a booking
- `PUT /api/bookings/<booking_id>/start`: Start a trip
- `PUT /api/bookings/<booking_id>/complete`: Complete a trip
- `PUT /api/bookings/<booking_id>/cancel`: Cancel a trip

## Setup and Installation

1. Install required packages:
```bash
pip install -e .
```

2. Run the application:
```bash
python -m cab_booking.app
```

## Example Requests

### Create a Passenger
```
POST /api/passengers
{
  "name": "John Doe",
  "phone": "1234567890",
  "email": "john@example.com"
}
```

### Create a Booking
```
POST /api/bookings
{
  "passenger_id": "PASS-12345678",
  "from_location": "123 Main St",
  "to_location": "456 Park Ave",
  "estimated_distance_km": 10,
  "estimated_duration_minutes": 30
}
```
