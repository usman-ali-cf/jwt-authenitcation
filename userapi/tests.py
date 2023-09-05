import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient


# Create your tests here.


class TestClass(TestCase):

    def get_token(self):
        self.register_test()
        client = APIClient()
        res = client.post("http://127.0.0.1:8000/user/login/",
                          data={'email': 'admin@gmail.com', 'password': '123'})
        return res.data['access']

    def login_test(self):
        self.register_test()
        client = APIClient()

        res = client.post("http://127.0.0.1:8000/user/login/",
                          data={'email': 'ali@gmail.com', 'password': '123'})
        print(res.data)
        self.assertEquals(res.status_code, 200)

    def register_test(self):
        client = APIClient()
        user_data = {
            "name": "admin",
            "email": "admin@gmail.com",
            "gender": "male",
            "city": "lahore",
            "is_admin": True,
            "password": "123",
            "last_login": None
        }
        response = client.post("http://127.0.0.1:8000/users/register", data=user_data, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['name'], "admin")

    def get_user_test(self):
        client = APIClient()
        token = self.get_token()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        user_data = {
            "name": "usman ali",
            "email": "ali@gmail.com",
            "gender": "male",
            "city": "lahore",
            "is_admin": True,
            "password": "123",
            "last_login": None
        }
        response = client.post("http://127.0.0.1:8000/users/register", data=user_data, format='json')

        response = client.get("http://127.0.0.1:8000/users/2/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['name'], "usman ali")
        self.assertEquals(response.data['gender'], "male")
        self.assertEquals(response.data["email"], "ali@gmail.com")

    def get_user_list_test(self):
        client = APIClient()
        token = self.get_token()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        user_data1 = {
            "name": "usman ali",
            "email": "ali@gmail.com",
            "gender": "male",
            "city": "lahore",
            "is_admin": True,
            "password": "123",
            "last_login": None
        }
        user_data2 = {
            "name": "babar azam",
            "email": "babar@gmail.com",
            "gender": "male",
            "city": "lahore",
            "is_admin": False,
            "password": "123",
            "last_login": None
        }
        response1 = client.post("http://127.0.0.1:8000/users/register", data=user_data1, format='json')
        response2 = client.post("http://127.0.0.1:8000/users/register", data=user_data2, format='json')
        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response2.status_code, 200)
        response = client.get("http://127.0.0.1:8000/users")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data[1]['name'], "usman ali")
        self.assertEquals(response.data[2]['name'], "babar azam")
        self.assertEquals(response.data[2]['gender'], "male")
        self.assertEquals(response.data[1]["email"], "ali@gmail.com")

    def edit_user_test(self):
        client = APIClient()
        token = self.get_token()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        user_data = {
            "name": "usman ali",
            "email": "ali@gmail.com",
            "gender": "male",
            "city": "lahore",
            "is_admin": True,
            "password": "123",
            "last_login": None
        }
        edited_data = {
            "name": "usman",
            "email": "usman@gmail.com",
            "city": "karachi",
            "password": "12"
        }
        response1 = client.post("http://127.0.0.1:8000/users/register", data=user_data, format='json')
        response = client.patch("http://127.0.0.1:8000/users/2/", data=edited_data, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['name'], "usman")
        self.assertEquals(response.data['email'], "usman@gmail.com")
        self.assertEquals(response.data['city'], "karachi")
        self.assertEquals(response.data['password'], "12")
