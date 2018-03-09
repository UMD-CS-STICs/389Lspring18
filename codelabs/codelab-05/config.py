# TODO: change me!
USERNAME = 'colink'

# SQS
SQS_QUEUE_NAME = 'cmsc389l-{}'.format(USERNAME)
DLQ_NAME = SQS_QUEUE_NAME + '-dlq'

# S3
S3_OUTPUT_BUCKET = 'cmsc389l-{}-codelab-05-thumbnails'.format(USERNAME)
S3_CODE_BUCKET = 'cmsc389l-{}-codelab-05-code'.format(USERNAME)

# EC2
SECURITY_GROUP = 'cmsc389l-{}-codelab-05'.format(USERNAME)
SSH_PORT = 22
S3_ROLE_NAME = 's3-codelab-04'
S3_INSTANCE_PROFILE_NAME = 's3-codelab-05-profile'
EC2_TAG_KEY = 'assignment'
EC2_TAG_VALUE = 'codelab-05'
CODE_FILES = ['image.py', 'config.py', 'utils.py']
