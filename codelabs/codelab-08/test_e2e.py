"""End-to-end tests for the User Profile API."""
import unittest
import sys
import os
import urllib

import requests

API_ENDPOINT = 'https://aiy1dzl472.execute-api.us-east-1.amazonaws.com/test'

class TestUserProfileAPI(unittest.TestCase):
    def submitRequest(self, method, path, expected_code=200, body=None, query=None):
        url = '/'.join([API_ENDPOINT, path])
        if query:
            url += '?' + urllib.parse.urlencode(query)

        kwargs = {}
        if body:
            kwargs['json'] = body

        resp = requests.request(method, url, **kwargs)
        self.assertEqual(resp.status_code, expected_code, resp.text)

        return resp

    def setUp(self):
        # Clear the users table
        self.submitRequest('DELETE', 'users')
        users = self.submitRequest('GET', 'users').json()
        self.assertCountEqual(users, [])

    def test_api_end_to_end(self):
        # Validate that requesting a nonexistent user returns an error code.
        self.submitRequest('GET', 'users/1', expected_code=400)

        # Insert a user and validate they can be fetched.
        user1 = { 'id': '1', 'name': 'John Smith', 'email': 'john@example.com' }
        self.submitRequest('POST', 'users', body=user1)
        returned_user = self.submitRequest('GET', 'users/1').json()
        self.assertEqual(returned_user, user1)

        # Insert a second user and validate that all users are returned on getUsers call.
        user2 = { 'id': '2', 'name': 'Jane Doe', 'email': 'jane@example.com' }
        self.submitRequest('POST', 'users', body=user2)
        users = self.submitRequest('GET', 'users').json()
        self.assertCountEqual(users, [user1, user2])

        # Update a user and validate the update propogates.
        new_user1 = { 'name': 'John', 'email': 'john@example.com' }
        self.submitRequest('PUT', 'users/1', body=new_user1)
        users = self.submitRequest('GET', 'users').json()
        new_user1['id'] = '1'
        self.assertCountEqual(users, [new_user1, user2])

        # Validate that users can be fetched by email.
        users = self.submitRequest('GET', 'users', query={ 'email': 'john@example.com' }).json()
        self.assertCountEqual(users, [new_user1])

        # Validate that DELETE /users/:id removes the specific user
        self.submitRequest('DELETE', 'users/1')
        users = self.submitRequest('GET', 'users').json()
        self.assertCountEqual(users, [user2])

        # Validate that DELETE /users properly removes users.
        self.submitRequest('DELETE', 'users')
        users = self.submitRequest('GET', 'users').json()
        self.assertCountEqual(users, [])

if __name__ == '__main__':
    unittest.main()
