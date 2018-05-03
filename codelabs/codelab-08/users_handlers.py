""" User Manipulation Functions """
import os
import json

import boto3
import botocore
from boto3.dynamodb.conditions import Key

if 'DYNAMO_ENDPOINT' in os.environ:
    # Local endpoint for testing.
    dynamo = boto3.resource('dynamodb', endpoint_url=os.environ['DYNAMO_ENDPOINT'])
else:
    # Use default endpoint for production.
    dynamo = boto3.resource('dynamodb')

USERS_TABLE = 'user-profiles'
EMAIL_INDEX = 'email-index'

table = dynamo.Table(USERS_TABLE)

""" DynamoDB Table Helpers """

def getUser(id, table):
    user = table.get_item(
        Key={ 'id': id }
    )

    return user['Item']

def getUsers(table, email=None):
    if email:
        # TODO
        # NOTE: You need to query an index here. Don't just filter the results of a scan operation.
        pass

    return table.scan()['Items']

def insertUser(user, table):
    table.put_item(
        Item=user,
        ConditionExpression="attribute_not_exists(id)"
    )

    return user

def updateUser(id, user, table):
    user['id'] = id
    table.put_item(
        Item=user,
        ConditionExpression="attribute_exists(id)"
    )

    return user

def deleteUser(id, table):
    # TODO
    pass

def deleteUsers(table):
    for user in getUsers(table):
        deleteUser(user['id'], table)

""" API Helpers """

def getQueryStringParameter(event, key):
    if 'queryStringParameters' in event and event['queryStringParameters'] and key in event['queryStringParameters']:
        return event['queryStringParameters'][key]

    return None

def respond(err, res=None):
    """ Generates a response conforming to API Gateway's Lambda Proxy Integration. """

    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

""" Lambda Handlers """

def getUserHandler(event, context):
    """ GET /users/:id """
    id = event['pathParameters']['id']
    try:
        return respond(None, getUser(id, table))
    except Exception as e:
        return respond(e)

def getUsersHandler(event, context):
    """ GET /users """
    emailFilter = getQueryStringParameter(event, 'email')
    try:
        return respond(None, getUsers(table, email=emailFilter))
    except Exception as e:
        return respond(e)

def insertUserHandler(event, context):
    """ POST /users """
    user = json.loads(event['body'])
    try:
        return respond(None, insertUser(user, table))
    except Exception as e:
        return respond(e)

def updateUserHandler(event, context):
    """ PUT /users/:id """
    id = event['pathParameters']['id']
    user = json.loads(event['body'])
    try:
        return respond(None, updateUser(id, user, table))
    except Exception as e:
        return respond(e)

def deleteUserHandler(event, context):
    """ DELETE /users/:id """
    id = event['pathParameters']['id']
    try:
        return respond(None, deleteUser(id, table))
    except Exception as e:
        return respond(e)

def deleteUsersHandler(event, context):
    """ DELETE /users """
    try:
        return respond(None, deleteUsers(table))
    except Exception as e:
        return respond(e)
