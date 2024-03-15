import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from PersonalPlannerAPI.models import Category, Event, PPUser

class UserTests(APITestCase):
    fixtures = ['user', 'token', 'pp_user']

    def test_create_registration(self):
        url = "/register"
        data = {
            "username": "newuser3",
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "city": "New City",  # Example PPUser field
            "state": "New State",  # Example PPUser field
            "address": "123 Street",  # Example PPUser field
            "zipcode": "12345", 
            "profile_picture": None # Example PPUser field
            # Optionally, include other fields needed for PPUser
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')
        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_keys = {'valid', 'token', 'id', 'first_name', 'username', 'city','email','state','profile_picture','zipcode','last_name','address'}
        self.assertEqual(set(response.data.keys()), expected_keys)
        
        # Optionally, you can also check the content of the response
        user = User.objects.get(username='newuser3')
        self.assertEqual(user.email, "newuser@example.com")

        # Check the rare_user properties in database
        pp_user = PPUser.objects.get(user=user)
        self.assertEqual(pp_user.user_id, user.id)

    def test_create_login(self):
        """
        Ensure we can login a user
        """

        # Define the endpoint in the API to which
        # the request will be sent
        url = "/login"

        # Define the request body
        data = {
            "username": "user1",
            "password": "totherow"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response body contains the expected keys
        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response['token'], "1600073627c3344754172dd997452440b1ddba7a")

    def test_retrieve_user(self):
        # Assuming there's an existing user with ID 1 in the database
        user_id = 1
        url = f"/ppusers/{user_id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Optionally, you can also check the content of the response
        json_response = response.json()
        self.assertEqual(json_response["id"], user_id)
        # Add more assertions based on your User model fields
    def test_update_user(self):
        # Assuming there's an existing PPUser with ID 1 in the database
        pp_user_id = 1
        url = f"/ppusers/{pp_user_id}"
        data = {
            "city": "Updated City",
            "state": "Updated State",
            "address": "Updated Address",
            "zipcode": "54321",
            # Include other fields needed for update
        }

        # Initiate request and store response
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Optionally, you can check the content of the response
        pp_user = PPUser.objects.get(id=pp_user_id)
        self.assertEqual(pp_user.city, "Updated City")
        self.assertEqual(pp_user.state, "Updated State")
        self.assertEqual(pp_user.address, "Updated Address")
        self.assertEqual(pp_user.zipcode, 54321)
    def test_delete_user(self):
        # Assuming there's an existing PPUser with ID 1 in the database
        pp_user_id = 1
        url = f"/ppusers/{pp_user_id}"

        # Initiate request and store response
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the PPUser has been deleted
        with self.assertRaises(PPUser.DoesNotExist):
            PPUser.objects.get(id=pp_user_id)