# create an Amazon S3 bucket
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html

import logging
import boto3

from botocore.exceptions import ClientError

create_new_bucket = True

#List all the existing buckets for the AWS account.

# Retrieve the list of existing buckets
s3_client = boto3.client('s3')
response = s3_client.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')


if create_new_bucket:
    # create bucket 
    location = {'LocationConstraint': 'us-west-1'}
    # s3_client.create_bucket(Bucket='bucket-sdk-python-123',
    #                         CreateBucketConfiguration=location)
    s3_client.create_bucket(Bucket='bucket-sdk-python-123')



def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


