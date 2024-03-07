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


# structure of Update of PPusers -pending
{
    "id": 3,
    "user": {
        "id": 3,
        # only include username if updating to new value
        "username": "michelle", 
        "first_name": "Chelle",
        "last_name": "Totherow",
        "email": "michelle@email.com"
    },
    "city": "Madison",
    "state": "TN",
    "address": "2134 this address",
    "zipcode": 37115
}