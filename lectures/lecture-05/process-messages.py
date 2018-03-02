import argparse
import boto3
import time
# For Colin!!!!
from playsound import playsound

def countdown_to_delete_message(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1


parser = argparse.ArgumentParser(description='Process message from an existing queue assuming you have read access.')
parser.add_argument(
    "-t", "--time-until-delete", type=int, default=2,
    help="time in seconds until a delete request for processed message is sent."
)
parser.add_argument(
    "-d", "--delete", type=bool, default=False,
    help="whether to send delete request for received message from queue or not."
)
parser.add_argument(
    "-p", "--play-sound", type=bool, default=False,
    help="whether to play audio or not. Only tested in Mac environment."
)
args = parser.parse_args()

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(
    QueueName='cmsc389l-sp18-demo',
    QueueOwnerAWSAccountId='425288583600'
)

# Process message by printing out body
# Note: receive_messages retuns a list and by default grabs a single message
message = queue.receive_messages()[0]

# Print message body to console
print("The message received has the following body:")
print(message.body)
if args.play_sound:
    playsound("ferraris.mp3")
# This sound can be muted by your terminal setting even though it is playing    
else:
    print('\a')
print("\n*********************************")

# Print timer to console until message is deleted
countdown_to_delete_message(args.time_until_delete)

if args.delete:
   message.delete()
   print("sent request to delete message")
   if args.play_sound:
       playsound("deleted.mp3")
else:
    print("No request to delete message")



    # Let the queue know that the message is processed
   # message.delete()