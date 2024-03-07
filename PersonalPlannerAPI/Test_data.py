# User

!!!register

{
    "username": "J7",
    "password": "your_password",
    "first_name": "YourFirstName",
    "last_name": "YourLastName",
    "email": "your.email@example.com",
    "city": "YourCity",
    "state": "YourState",
    "address": "YourAddress",
    "zipcode": 12346
}

!!!login

{
    "username": "J7",
    "password": "your_password"
}

# Category

{
    "label": "outdoor",
}

# Create Events

{
  "category": 1,
  "title": "punching Event",
  "description": "This is a sample event description.",
  "event_date": "2024-05-26",
  "event_time": "12:00:00",
  "city": "Sample City",
  "state": "Sample State",
  "address": "123 Sample St",
  "zipcode": 12345
}

# Update of Events

{
  "user": 1,
  "category": 3,
  "title": "1111",
  "description": "11111",
  "date": "2024-01-26",
  "start_datetime": "2024-01-26",
  "city": "Nashvegas",
  "state": "TN",
  "address": "1234 Sample St",
  "zipcode": 11111
}

# get all, get id of PPusers
# http://localhost:8000/ppusers
# http://localhost:8000/ppusers/3



# structure of PPusers for PUT
{
    "id": 1,
    "user": {
        "id": 1,
        "username": "user1",
        "first_name": "User123",
        "last_name": "One",
        "email": "user1@example.com"
    },
    "city": "City1",
    "state": "State1",
    "address": "Address1",
    "zipcode": 12345
}