import argparse
import boto3

parser = argparse.ArgumentParser(
    description='Send messages to an existing queue assuming you have write access.'
)
parser.add_argument(
    "message_body", nargs='?', default="MSG", help="message body to post to queue"
)
parser.add_argument(
    "-n", "--num-messages", type=int, default=1, help="number of messages to generate"
)
args = parser.parse_args()
stop = args.num_messages + 1
message = args.message_body

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(
    QueueName='cmsc389l-sp18-demo',
    QueueOwnerAWSAccountId='425288583600'
)
print("********************")
print(args.message_body)
print("********************")

#send message(s)
for i in range(1, args.num_messages + 1):
    response = queue.send_message(
        MessageBody=f"{message} {i} "
    )
    print(response)
    print(f"{message} {i} ")
