import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from PersonalPlannerAPI.models import Category, Event, PPUser

class CategoryTests(APITestCase):
    fixtures = ['user', 'pp_user', 'token', 'categories_fixture', 'events_fixture']

    def setUp(self):
        self.user = User.objects.get(username='user1')  # Get the user from the fixture
        self.pp_user = PPUser.objects.get(user=self.user)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_category(self):
       
        url = "/categories"
        data = {
            'label': 'Marathon',
           
        }
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        json_response = response.json()
        # self.assertEqual(json_response["user"], self.pp_user.id)
        self.assertEqual(json_response["label"], "Marathon") 
    def test_get_categories(self):
        # Ensure we can retrieve an existing event
        url = "/categories"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_update_category(self):
        # Ensure we can update an existing event
        category_id = Category.objects.first().id
        url = f"/categories/{category_id}"
        data = {
            'label': 'Updated Category',
            
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Updated Category')

    def test_delete_event(self):
        # Ensure we can delete an existing event
        category_id = Category.objects.first().id  
        url = f"/categories/{category_id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
