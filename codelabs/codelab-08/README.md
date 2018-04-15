# Codelab 8: DynamoDB

### Overview

In this codelab will learn about DynamoDB, a [NoSQL](https://aws.amazon.com/nosql/) database service. You will also gain more experience using API Gateway and Lambda. At the end of this codelab, you will be able to read and right to your database simply by touching and endpoint.

![ArchitectureDiagram](../../../media/codelabs/codelab-08/archCL8.png) 

### Due Date

This code is due on *Thursday, April 26nd at 11:59:59PM*.

### Setup

Make sure to update your local repo with the remote by executing `git pull`. 
<!-- 
You won`t need to set up your pipenv environment for this codelab.
 -->

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

### IAM

In order to scale, we can't be relying on manual data entry. We want a lambda function to interact with DynamoDB on our behalf, which it will need permissions to do. Using the AWS Management Console, create a new role `Roles > Create role` and select `Lambda` as the service that will use this role.

![IAMlambda](../../../media/codelabs/codelab-08/IAMlambda.png)

For permissions, use AWSLambdaDynamoDBExecutionRole

![IAMpermissions](../../../media/codelabs/codelab-08/IAMpermissions.png)

<!-- 
might need to use the following instead

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

-->

Finally, give it a name

![IAMrolename](../../../media/codelabs/codelab-08/IAMrolename.png)

### Lambda

![functionFromScratch](../../../media/codelabs/codelab-08/functionFromScratch.png)

<!-- 

from __future__ import print_function

import boto3
import json

print(`Loading function`)


def handler(event, context):
    ```Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    ```
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

### API Gateway

As in codelab-07, we'll use the AWS Management Console to create a new API endpoint. 

![newAPIregional](../../../media/codelabs/codelab-08/newAPIregional.png)

![createResource](../../../media/codelabs/codelab-08/createResource.png)

This resource will be called `/items`

<!-- something with arguments? {#} -->

### Assignment

### Wrapping Up

If you're interested in being able to create tables using python, there's a tutorial available [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html). 

### Submission

You will be submitting a text file called `arn.txt` containing only the Amazon Resource Number (ARN) of your API Gateway.

Submit this assignment to `codelab8` on the submit server. Upload a zipped directory with the file:

```
<directory id>.zip
	arn.txt
```