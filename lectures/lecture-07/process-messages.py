import argparse
import time

import boto3
from playsound import playsound

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(
    QueueName='cmsc389l-s18-lecture-07',
    QueueOwnerAWSAccountId='800593953112'
)


def format_time(t):
    mins, secs = divmod(t, 60)
    return '{:02d}:{:02d}'.format(mins, secs)


def countdown_to_delete_message(body, t):
    total_time = format_time(t)
    print('')
    while t:
        print(
            f"\rMessage Received: \"{body}\" ({format_time(t)}/{total_time})", end='')
        time.sleep(1)
        t -= 1


def main(args):
    # Listen for messages indefinitely
    while True:
        # Returns either 0 or 1 SQS message.
        messages = queue.receive_messages(
            MaxNumberOfMessages=1, WaitTimeSeconds=2)
        if len(messages) == 0:
            print("\nNo messages found...")
        else:
            # Process message by printing out body
            message = messages[0]

            # Print timer to console until message is deleted
            countdown_to_delete_message(message.body, args.time_until_delete)

            if args.delete:
                message.delete()
                print(" [Deletion Request Sent]")
            else:
                print("")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process message from an existing queue assuming you have read access.')
    parser.add_argument(
        "-t", "--time-until-delete", type=int, default=2,
        help="time in seconds until a delete request for processed message is sent."
    )
    parser.add_argument(
        "-d", "--delete", default=False,
        help="whether to send delete request for received message from queue or not.", action='store_true'
    )
    parser.add_argument(
        "-p", "--play-sound", type=bool, default=False,
        help="whether to play audio or not. Only tested in Mac environment."
    )
    args = parser.parse_args()

    main(args)
