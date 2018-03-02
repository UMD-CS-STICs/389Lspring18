import argparse
import json
from os import listdir
from os.path import isdir, isfile, join

import boto3
from config import SQS_QUEUE_NAME

sqs = boto3.resource('sqs')
sqs_client = boto3.client('sqs')


def send_messages(queue_name, bucket, keys, height, width):
    """Generates and sends a set of thumbnail requests as SQS messages.
    Args:
        queue_name (string): Name of queue to send messages to.
        bucket (string): Bucket containing image to thumbnail.
        keys (string list): List of key names of images to thumbnail.
        height (int): Height in pixels of thumbnail image produce.
        width (int): Width in pixels of thumbnail image produce.
    """
    # TODO(you)
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Upload SQS messages to generate thumbnails')

    parser.add_argument('--bucket', default='cmsc389l-public',
                        help='S3 bucket containing original images')
    parser.add_argument('--keys', nargs='+', default=['codelab-05/owl.jpg', 'codelab-05/dancing.jpg',
                                                      'codelab-05/canyon.jpg', 'codelab-05/skyline.jpg', 'codelab-05/street.jpg'], help='Setup all S3 buckets')
    parser.add_argument('--height', default=400, type=int,
                        help='Thumbnail height (px)')
    parser.add_argument('--width', default=400, type=int,
                        help='Thumbnail width (px)')

    args = parser.parse_args()

    send_messages(SQS_QUEUE_NAME, args.bucket,
                  args.keys, args.height, args.width)
