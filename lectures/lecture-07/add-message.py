import argparse

import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
# Andrej/Colin have write access; everyone else has just read access
queue = sqs.get_queue_by_name(
    QueueName='cmsc389l-s18-lecture-07',
    QueueOwnerAWSAccountId='800593953112'
)


def main(args):
    # send message(s)
    for i in range(1, args.num_messages + 1):
        response = queue.send_message(
            MessageBody=f"{args.message} {i}"
        )
        print(
            f"Message sent: \"{args.message} {i}\" ({response['MessageId']})")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Send messages to an existing queue assuming you have write access.'
    )
    parser.add_argument(
        "message", nargs='?', default="MSG", help="message body to post to queue"
    )
    parser.add_argument(
        "-n", "--num-messages", type=int, default=1, help="number of messages to generate"
    )
    args = parser.parse_args()

    main(args)
