from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'phone': '1234567890',
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt to register the same user again
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_user_login(self):
        self.client.post(self.register_url, self.user_data)  # Register the user
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        # First, register and log in the user to get the access and refresh tokens
        self.client.post(self.register_url, self.user_data)
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        refresh_token = login_response.data['refresh']  # Get the refresh token from login response

        # Now attempt to log out using the refresh token
        response = self.client.post(self.logout_url, {
            'refresh_token': refresh_token  # Send the refresh token
        })

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)



class InventoryItemAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register') 
        self.login_url = reverse('login')          
        self.item_url = reverse('items')      
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'phone': '1234567890',
        }
        
        # Register the user
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "User registration failed")
        
        # Log in to get the access token
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        
        self.assertIn('access', login_response.data, "Access token not found in login response")
        self.access_token = login_response.data['access']

    def test_create_item(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        print("Authorization Header:", headers)
        
        response = self.client.post(self.item_url, {
            'name': 'Test Item',
            'description': 'This is a test item.',
            'quantity': 20,
            'price': 34.56
        }, **headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Item creation failed")
        self.assertIn('id', response.data, "ID not found in response")


    def test_get_items(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        self.client.post(self.item_url, {
            'name': 'Test Item',
            'description': 'This is a test item.',
            'quantity': 20,
            'price': 34.56,
        }, **headers)

        response = self.client.get(self.item_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item_by_id(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        create_response = self.client.post(self.item_url, {
            'name': 'Test Item',
            'description': 'This is a test item.',
            'quantity': 20,
            'price': 34.56,
        }, **headers)
        item_id = create_response.data['id']
        response = self.client.get(reverse('item-detail', args=[item_id]), **headers)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_item_without_auth(self):
        response = self.client.post(self.item_url, {
            'name': 'Test Item',
            'description': 'This is a test item.',
            'quantity': 20,
            'price': 34.56,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        create_response = self.client.post(self.item_url, {
            'name': 'Test Item',
            'description': 'This is a test item.',
            'quantity': 20,
            'price': 34.56,
        }, **headers)
        item_id = create_response.data['id']

        update_response = self.client.put(reverse('item-detail', args=[item_id]), {
            'name': 'Updated Item',
            'quantity': 30,
        }, **headers)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], 'Updated Item')
        self.assertEqual(update_response.data['quantity'], 30)

    def test_delete_item(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        create_response = self.client.post(self.item_url, {
            'name': 'Test Item',
            'description': 'This is a test item.',
            'quantity': 20,
            'price': 34.56,
        }, **headers)
        item_id = create_response.data['id']

        delete_response = self.client.delete(reverse('item-detail', args=[item_id]), **headers)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        retrieve_response = self.client.get(reverse('item-detail', args=[item_id]), **headers)
        self.assertEqual(retrieve_response.status_code, status.HTTP_404_NOT_FOUND)
