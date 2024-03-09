import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from PersonalPlannerAPI.models import Category, Event, PPUser

class EventTests(APITestCase):
    fixtures = ['user', 'pp_user', 'token', 'categories_fixture', 'events_fixture']
    
        
    def setUp(self):
        self.user = User.objects.get(username='user1')  # Get the user from the fixture
        self.pp_user = PPUser.objects.get(user=self.user)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_event(self):
       
        url = "/events"
        data = {
            'title': 'New Event',
            'event_date': '2024-03-16',
            'event_time': '13:00',
            'description': 'New Description',
            'category': 1,
            'city': 'New City',
            'state': 'NC',
            'address': '456 New St',
            'zipcode': 67890,
        }
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        json_response = response.json()
        # self.assertEqual(json_response["user"], self.pp_user.id)
        self.assertEqual(json_response["category"]["id"], 1) 
        self.assertEqual(json_response["title"], "New Event")
        self.assertEqual(json_response["description"], "New Description")
        self.assertEqual(json_response["event_date"], "2024-03-16")
        self.assertEqual(json_response["event_time"], "13:00")
        self.assertEqual(json_response["city"], "New City")
        self.assertEqual(json_response["state"], "NC")
        self.assertEqual(json_response["address"], "456 New St")
        self.assertEqual(json_response["zipcode"], 67890) 

    def test_retrieve_event(self):
        # Ensure we can retrieve an existing event
        url = "/events"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_event(self):
        # Ensure we can update an existing event
        event_id = Event.objects.first().id  
        url = f"/events/{event_id}"
        data = {
            'title': 'Updated Event',
            'description': 'Updated Description',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Event')
        self.assertEqual(response.data['description'], 'Updated Description')

    def test_delete_event(self):
        # Ensure we can delete an existing event
        event_id = Event.objects.first().id  
        url = f"/events/{event_id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
