#!/bin/bash
# Simple script to clear your AWS environment from codelab-05

export UMD_USERNAME='colink'

# SQS
# aws sqs delete-queue --queue-url "https://queue.amazonaws.com/800593953112/cmsc389l-${UMD_USERNAME}"
# aws sqs delete-queue --queue-url "https://queue.amazonaws.com/800593953112/cmsc389l-${UMD_USERNAME}-dlq"

# S3
aws s3 rb "s3://cmsc389l-${UMD_USERNAME}-codelab-05-code" --force
aws s3 rb "s3://cmsc389l-${UMD_USERNAME}-codelab-05-thumbnails" --force

# IAM
aws iam detach-role-policy --role-name s3-codelab-05 --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam detach-role-policy --role-name s3-codelab-05 --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess
aws iam remove-role-from-instance-profile --role-name s3-codelab-05 --instance-profile-name s3-codelab-05-profile
sleep 2 # Wait for remove-role-from-instance-profile to propagate
aws iam delete-role --role-name s3-codelab-05
aws iam delete-instance-profile --instance-profile-name s3-codelab-05-profile

# EC2
INSTANCES=`aws ec2 describe-tags | jq '.Tags[].ResourceId' | xargs`
echo $INSTANCES
aws ec2 terminate-instances --instance-ids $INSTANCES

echo "Waiting on instances to terminate..."
aws ec2 wait instance-terminated --instance-ids $INSTANCES
echo "All codelab-05 instances terminated"

# Security Group
aws ec2 delete-security-group --group-name "cmsc389l-${UMD_USERNAME}-codelab-05"
