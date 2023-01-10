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

# # Next we'll set a basic configuration for the static website.
website_payload = {
    'ErrorDocument': {
        'Key': '404.html'
    },
    'IndexDocument': {
        'Suffix': 'index.html'
    }
}

## Make our new S3 bucket a static website
bucket_website = s3_client.put_bucket_website(Bucket=bucket_name,
                                              WebsiteConfiguration=website_payload )
    

## Putting index.html and 404.html to our S3 bucket
filename = ['files/index.html', 'files/404.html']
for file in filename:
    data = open(file, 'r').read()
    print("Printing type of file-data", type(data))
    try:
        s3_client.put_object(Body=data,
                         Bucket=bucket_name,
                         Key=file,
                         ContentType='text/html') 
        print(f"{file} uploaded successfuly to S3 {bucket_name}")
    
    except ClientError as ce :
        print(f"Some error occured while uploading {file}")



## Enable Static Website Hosting on AWS S3 Bucket
try:
    response = s3_client.put_bucket_policy(Bucket=bucket_name,Policy=json.dumps(policy_payload))
    print("Static website hosting success !")
except ClientError as ce:
    print("Error creating static website :(")

## http://mystatic-website-bucket-hosting.s3-website.ap-south-1.amazonaws.com/files/