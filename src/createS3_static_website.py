# Load aws boto3 module
import boto3
import json
import logging

from botocore.client import ClientError


# Create S3 client
s3_client = boto3.client('s3')
location = {'LocationConstraint': 'ap-south-1'}

# Set a bucket name which will be our domain name.
bucket_name = "mystatic-website-bucket-hosting"

# Check if bucket exists or not
try:
    s3_client.head_bucket(Bucket=bucket_name)
    bucket_exists = 'Yes'
except ClientError:
    bucket_exists = 'No'
    print(f"{bucket_name} bucket doesnot exists")

##Create a new S3 bucket only if it do not exists
if bucket_exists == 'Yes':
    print(f" {bucket_name} bucket already exists !")
else:
    try:
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration= location)
    except ClientError as ce:
        print(f"Error occured while creating S3 bucket- {bucket_name}", ce)

# We need to set an S3 policy for our bucket to
# allow anyone read access to our bucket and files.
# If we do not set this policy, people will not be
# able to view our S3 static web site.
policy_payload = {
  "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mystatic-website-bucket-hosting/*"
  }
  ]
}

# # Add the policy to the bucket
response = s3_client.put_bucket_policy(Bucket=bucket_name,Policy=json.dumps(policy_payload))

# # Next we'll set a basic configuration for the static
# # website.
# website_payload = {
#     'ErrorDocument': {
#         'Key': '404.html'
#     },
#     'IndexDocument': {
#         'Suffix': 'index.html'
#     }
# }

# # Make our new S3 bucket a static website
# bucket_website = s3_client.BucketWebsite(bucket_name)

# # And configure the static website with our desired index.html
# # and 404.html configuration.
# bucket_website.put(WebsiteConfiguration=website_payload)