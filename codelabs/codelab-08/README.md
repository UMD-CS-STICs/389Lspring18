# Codelab 8: DynamoDB

### Overview

In this codelab will learn about DynamoDB, a [NoSQL](https://aws.amazon.com/nosql/) database service. You will also gain more experience using API Gateway and Lambda. At the end of this codelab, you will be able to read and right to your database simply by touching and endpoint.

![ArchitectureDiagram](../../../media/codelabs/codelab-08/archCL8.png) 

<!-- 
### Due Date

This code is due on *Thursday, April 26nd at 11:59:59PM*.
 -->

### Setup

Make sure to update your local repo with the remote by executing `git pull`. 

You won't need to set up your pipenv environment for this codelab.


### DynamoDB

First, we want to create a place to store our data. Using the AWS Management Console, navigate to DynamoDB and `Create table`. Name it "codelab-08" and give it a String partition key called "studentID". Add a String sort key called "courseCode".

**Note**: For large datasets, AWS will use your partiton key to distribute your data across multiple servers.

![createTable](../../../media/codelabs/codelab-08/createTable.png)  

It'll take just a few moments to be created, then we can start loading data.

![tableBeingCreated](../../../media/codelabs/codelab-08/tableBeingCreated.png)

Now, we make a data object called an Item. Under the Items tab, select `Create item`. Enter in "Terpy" for studentID field, and "CMSC389L" for courseCode, then save. Do this a few times.

**Note**: The partition key, together with the sort key, uniquely identify an item.

![items](../../../media/codelabs/codelab-08/items.png)

From the drop-down menu, switch from `Scan` to `Query`.

![selectQuery](../../../media/codelabs/codelab-08/selectQuery.png)

Here, we can query on the student ID

![partition](../../../media/codelabs/codelab-08/partition.png)

... the studentID AND the courseCode

![partitionANDsort](../../../media/codelabs/codelab-08/partitionANDsort.png)

... but not the courseCode alone.

![noPartitionKey](../../../media/codelabs/codelab-08/noPartitionKey.png)

This is a limitation of NoSQL databases. Though there is a workaround using scan, this is part of the tradeoff we make for flexibility and scalability.


### API Gateway part1

In order to scale, we can't be relying on manual data entry. We want a lambda function to interact with DynamoDB on our behalf. But first, we want a way to route traffic. As in codelab-07, we'll use the AWS Management Console to create a new regional API. 

![newAPIregional](../../../media/codelabs/codelab-08/newAPIregional.png)

Create a new endpoint `Actions > Create Resource` called dynamodb.

![newResource](../../../media/codelabs/codelab-08/newResource.png)

Here we can expose various methods that will be available to request. For now, we'll add GET `Actions > Create Method` and use `Mock` as the integration type.

![GETmockIntegration](../../../media/codelabs/codelab-08/GETmockIntegration.png)

This will allow us to deploy the API `Actions > Deploy AOPI` and set up out Lambda functions. Do this now.

![deployAPI](../../../media/codelabs/codelab-08/deployAPI.png)

### Lambda

Head over to the Lambda service in the AWS Management Console. We'll create a new function using the _microservice-http-endpoint-python3_ blueprint.

![lambdaTemplate](../../../media/codelabs/codelab-08/lambdaTemplate.png)

Give the function a name, and select `Create a custom role` from the drop-down menu. This will open a new tab. Select `Create a new IAM Role`, name it, and view the policy document. We want to edit this and replace what's there with our own.

![newIAMrole](../../../media/codelabs/codelab-08/newIAMrole.png)

Here is what we are copying in *also included with the codelab as a json file*

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1428341300017",
      "Action": [
        "dynamodb:DeleteItem",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:UpdateItem"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "",
      "Resource": "*",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Effect": "Allow"
    }
  ]
}
```

After clicking allow and being redirected back to Lambda, we fill in our api-gateway information, and create the function.

![configureLambda](../../../media/codelabs/codelab-08/configureLambda.png)

```
<!-- 

from __future__ import print_function

import boto3
import json

print(`Loading function`)


def handler(event, context):
    
    #print("Received event: " + json.dumps(event, indent=2))

    operation = event[`operation`]

    if `tableName` in event:
        dynamo = boto3.resource(`dynamodb`).Table(event[`tableName`])

    operations = {
        `create`: lambda x: dynamo.put_item(**x),
        `read`: lambda x: dynamo.get_item(**x),
        `update`: lambda x: dynamo.update_item(**x),
        `delete`: lambda x: dynamo.delete_item(**x),
        `list`: lambda x: dynamo.scan(**x),
        `echo`: lambda x: x,
        `ping`: lambda x: `pong`
    }

    if operation in operations:
        return operations[operation](event.get(`payload`))
    else:
        raise ValueError(`Unrecognized operation "{}"`.format(operation))
-->
```

### API Gateway part2

Select _/dynamodb_ and again create a new resource. We can pass arguments by enclosing the name in braces.

![newChildResource](../../../media/codelabs/codelab-08/newChildResource.png)

And we can expose multiple methods.

![addMethods](../../../media/codelabs/codelab-08/addMethods.png)

Configure the PUT method with the lambda Function we just created and save.

![configureMethods](../../../media/codelabs/codelab-08/configureMethods.png)

You should see something like this. We can now test our function! Click the blue test thunderbolt.

![testBolt](../../../media/codelabs/codelab-08/testBolt.png)

The `{table}` field can be left blank, as we're not using arguments in the url. Instead, our function will be reading a JSON file. Use the one below to get our table.

```
{
	"httpMethod": "GET",
	"queryStringParameters": {
	"TableName": "codelab-08"
    }
}
```

![testResponse](../../../media/codelabs/codelab-08/testResponse.png)

### Further Reading

If you're interested in being able to create tables using python, there's a great tutorial in the  [docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html). 

Additionally, Colin King found a great end-to-end example of a serverless RESTful API available [here](https://github.com/serverless/examples/tree/master/aws-python-rest-api-with-dynamodb)

### Submission

There is no submission for this codelab.

<!-- 
You will be submitting a text file called `arn.txt` containing only the Amazon Resource Number (ARN) of your API Gateway.

Submit this assignment to `codelab8` on the submit server. Upload a zipped directory with the file:

```
<directory id>.zip
	arn.txt
```
 -->