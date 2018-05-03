"""End-to-end tests for the User Profile API."""
import unittest
import sys
import os
import json

import boto3

DYNAMO_ENDPOINT = 'http://localhost:8000'

os.environ['DYNAMO_ENDPOINT'] = DYNAMO_ENDPOINT

# Import after overwriting environment variables
import users_handlers

dynamo = boto3.resource('dynamodb', endpoint_url=DYNAMO_ENDPOINT)

def makeEvent(body=None, params=None, query=None):
    """ Generates an event object conforming to API Gateway's Lambda Proxy Integration. """
    event = {
        'body': json.dumps(body)
    }
    if params:
        event['pathParameters'] = params
    if query:
        event['queryStringParameters'] = query

    return event

class TestUserProfileHandlers(unittest.TestCase):
    def setUp(self):
        table = dynamo.create_table(
            AttributeDefinitions=[
                { 'AttributeName': 'id', 'AttributeType': 'S' },
                { 'AttributeName': 'email', 'AttributeType': 'S' }
            ],
            TableName=users_handlers.USERS_TABLE,
            KeySchema=[ { 'AttributeName': 'id', 'KeyType': 'HASH' } ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            },
            GlobalSecondaryIndexes=[
                {
                    'IndexName': users_handlers.EMAIL_INDEX,
                    'KeySchema': [ { 'AttributeName': 'email', 'KeyType': 'HASH' } ],
                    'Projection': { 'ProjectionType': 'ALL' },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                }
            ]
        )
        table.wait_until_exists()

    def tearDown(self):
        table = dynamo.Table(users_handlers.USERS_TABLE)
        table.delete()
        table.wait_until_not_exists()

    def test_users_are_initially_empty(self):
        resp = users_handlers.getUsersHandler({}, {})
        self.assertEqual(json.loads(resp['body']), [])

    def test_insert_single_user(self):
        user = { 'id': "1", 'name': "John Smith" }

        resp = users_handlers.insertUserHandler(makeEvent(user), {})
        self.assertEqual(json.loads(resp['body']), user)

        resp = users_handlers.getUserHandler(makeEvent(params={'id': '1'}), {})
        self.assertEqual(json.loads(resp['body']), user)

    def test_error_on_insert_existing_user(self):
        user = { 'id': "1", 'name': "John Smith" }

        resp = users_handlers.insertUserHandler(makeEvent(user), {})
        self.assertEqual(resp['statusCode'], '200')

        resp = users_handlers.insertUserHandler(makeEvent(user), {})
        self.assertEqual(resp['statusCode'], '400')

    def test_update_user(self):
        user1 = { 'id': "1", 'name': "John Smith" }
        user2 = { 'id': "2", 'name': "Jane Doe" }

        users_handlers.insertUserHandler(makeEvent(user1), {})
        users_handlers.insertUserHandler(makeEvent(user2), {})

        updated_user = { 'id': "1", 'name': "Joe Shmoe" }
        users_handlers.updateUserHandler(makeEvent(updated_user, params={'id': '1'}), {})

        resp = users_handlers.getUsersHandler({}, {})
        self.assertCountEqual(json.loads(resp['body']), [user2, updated_user])

    def test_update_user_without_id(self):
        user = { 'id': "1", 'name': "John Smith" }

        users_handlers.insertUserHandler(makeEvent(user), {})

        updated_user = { 'name': "Joe Shmoe" }
        users_handlers.updateUserHandler(makeEvent(updated_user, params={'id': '1'}), {})

        updated_user['id'] = '1'
        resp = users_handlers.getUsersHandler({}, {})
        self.assertCountEqual(json.loads(resp['body']), [updated_user])

    def test_error_on_update_nonexistent_user(self):
        user = { 'id': "1", 'name': "John Smith" }

        resp = users_handlers.updateUserHandler(makeEvent(user, params={'id': '1'}), {})
        self.assertEqual(resp['statusCode'], '400')

    def test_delete_user(self):
        user1 = { 'id': "1", 'name': "John Smith" }
        user2 = { 'id': "2", 'name': "Jane Doe" }

        users_handlers.insertUserHandler(makeEvent(user1), {})
        users_handlers.insertUserHandler(makeEvent(user2), {})

        resp = users_handlers.deleteUserHandler(makeEvent(params={'id': '1'}), {})
        self.assertEqual(json.loads(resp['body']), user1)

        resp = users_handlers.getUsersHandler({}, {})
        self.assertCountEqual(json.loads(resp['body']), [user2])

    def test_delete_nonexistent_user(self):
        resp = users_handlers.deleteUserHandler(makeEvent(params={'id': '1'}), {})
        self.assertEqual(resp['statusCode'], '400')

    def test_delete_empty_users(self):
        resp = users_handlers.deleteUsersHandler({}, {})
        self.assertEqual(resp['statusCode'], '200')

        resp = users_handlers.getUsersHandler({}, {})
        self.assertCountEqual(json.loads(resp['body']), [])

    def test_delete_users(self):
        user1 = { 'id': "1", 'name': "John Smith" }
        user2 = { 'id': "2", 'name': "Jane Doe" }

        users_handlers.insertUserHandler(makeEvent(user1), {})
        users_handlers.insertUserHandler(makeEvent(user2), {})

        resp = users_handlers.deleteUsersHandler({}, {})
        self.assertEqual(resp['statusCode'], '200')

        resp = users_handlers.getUsersHandler({}, {})
        self.assertCountEqual(json.loads(resp['body']), [])

    def test_get_user_by_email(self):
        user1 = { 'id': "1", 'name': "John Smith", 'email': 'john@example.com' }
        user2 = { 'id': "2", 'name': "Jane Doe", 'email': 'jane@example.com' }

        users_handlers.insertUserHandler(makeEvent(user1), {})
        users_handlers.insertUserHandler(makeEvent(user2), {})

        resp = users_handlers.getUsersHandler(makeEvent(query={ 'email': 'jane@example.com' }), {})
        self.assertCountEqual(json.loads(resp['body']), [user2])

    def test_get_user_by_nonexistent_email(self):
        resp = users_handlers.getUsersHandler(makeEvent(query={ 'email': 'none@example.com' }), {})
        self.assertEqual(resp['statusCode'], '200')
        self.assertCountEqual(json.loads(resp['body']), [])


if __name__ == '__main__':
    unittest.main()
