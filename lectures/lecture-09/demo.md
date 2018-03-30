# Lambda Thumbnailer Demo

In this demo, we will take the thumbnailer from the SQS codelab and replace the EC2 instance with a Lambda function to *significantly* reduce the system's complexity.

With this change, we will set up the Lambda function to trigger every time an image is uploaded to the S3 bucket.

Because we are using Lambda, we don't need to worry about load balancing the thumbnail requests with SQS! So we won't need the SQS queue anymore.

We will upload instructions on following this codelab after class.
