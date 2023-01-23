# create an Amazon S3 bucket
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html

import logging
import boto3
import os
import pathlib
from pathlib import Path 
from datetime import datetime

from botocore.exceptions import ClientError

list_flag = False
create_new_bucket_flag = False
upload_file_flag = False
upload_file_flag_2 = False
download_file_flag = False
get_bucket_lifecycle_configuration_flag = False
print_object_flag = False
delete_bucket_forced_flag = False
upload_photos_flag = True

base_folder = pathlib.Path(__file__).parent

#List all the existing buckets for the AWS account.

if list_flag:
# Retrieve the list of existing buckets
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    print(f'  {bucket}')

    # https: // docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_ListBuckets_section.html
    print('Existing buckets 2:')
    s3_resource = boto3.resource('s3')
    s3_resource.buckets.all()
    lists = list(s3_resource.buckets.all())
    print(lists)

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
if print_object_flag:
    bucket = 'bucket-sdk-python-123'
    s3_client = boto3.client('s3')
    response = s3_client.list_objects(
        Bucket=bucket
    )
    contents = response["Contents"]
    print(f'  {contents[0]}')


if create_new_bucket_flag:

    s3_client = boto3.client('s3')
    # create bucket 
    location = {'LocationConstraint': 'us-west-1'}
    # s3_client.create_bucket(Bucket='bucket-sdk-python-123',
    #                         CreateBucketConfiguration=location)
    # calling directly the standard create_bucket method 
    s3_client.create_bucket(Bucket='bucket-sdk-python-123')


if delete_bucket_forced_flag:
    # first delete the objects inside the bucket 
    s3 = boto3.resource('s3')
    bucket_name = "aws-cloudtrail-logs-821075683906-5695c6c7"
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.objects.delete()
        print("Emptied bucket '%s'.", bucket.name)
    except:
        print("Couldn't empty bucket '%s'.", bucket.name)
    
    # then delete the bucket itself
    client = boto3.client('s3')
    response = client.delete_bucket(
        Bucket=bucket_name
    )

    # finally print the remaining buckets
    response = client.list_buckets()
    print('Remaining buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    #print(f'  {bucket}')

# upload objects using the client's method
if upload_file_flag:
    file_name = "picture.png"
    file_full_name = pathlib.PurePath(base_folder, file_name)
    print(f"upload {file_name}")
    path = "c:/Py/Projects/Examples/AWS/aws_sdk/picture.png"
    s3 = boto3.client('s3')
    with open(file_full_name, "rb") as f:
        s3.upload_fileobj(f, "bucket-sdk-python-123", file_name)

if upload_photos_flag:
    # this function create the bucket, upload the files and download
    # eventually it can also delete the bucket 
    # define inputs 
    folder_file_base = "fotos"
    folder_file_input = "2020input"
    folder_file_output = "2020output"
    input_full_name = pathlib.Path(base_folder, folder_file_base, folder_file_input)
    output_full_name = pathlib.Path(base_folder, folder_file_base, folder_file_output)

    # create the bucket 
    s3 = boto3.resource('s3')
    bucket_name = f"bucket-sdk-{folder_file_input}"
    bucket = s3.Bucket(bucket_name)
    region = bucket.meta.client.meta.region_name
    try:
        bucket.create()
        bucket.wait_until_exists()
        print(
            f"Created bucket {bucket.name} in region={region}")
    except:
        print(f"Couldn't create bucket named {bucket.name} in region={region}",
              bucket.name, region)
    
    # upload the photos:
    upload_photos = True
    if upload_photos:
        for entry in input_full_name.iterdir():
            with open(entry, 'rb') as data:
                print(f"upload file {entry.name}")
                # insteead of entry.name or entry._str
                bucket.upload_fileobj(data, entry.name)

    delete_buckets = False
    if delete_buckets:
        s3 = boto3.resource('s3')
        try:
            bucket.objects.delete()
            print("Emptied bucket '%s'.", bucket.name)
        except:
            print("Couldn't empty bucket '%s'.", bucket.name)

        # then delete the bucket itself
        client = boto3.client('s3')
        response = client.delete_bucket(
            Bucket=bucket_name
        )

    download_photos = True
    client = boto3.client('s3')
    if download_photos:
        list = client.list_objects(Bucket=bucket_name)['Contents']
        for key in list:    
            # https://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket
            dest_pathname = os.path.join(output_full_name, key.get('Key'))
            client.download_file(bucket_name, key['Key'], dest_pathname)
            print(f"download file {key['Key']}")

# uploading objects using the Boto3 Bucket resource
if upload_file_flag_2:
    file_name = "picture.png"
    file_full_name = pathlib.PurePath(base_folder, file_name)
    print(f"upload {file_name}")
    path = "c:/Py/Projects/Examples/AWS/aws_sdk/picture.png"
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("bucket-sdk-python-123")
    with open(file_full_name, 'rb') as data:
        bucket.upload_fileobj(data, file_name)
    
if download_file_flag:
    file_name = "picture_out.png"
    s3 = boto3.client('s3')
    with open('FILE_NAME', 'wb') as f:
        s3.download_file("bucket-sdk-python-123", "picture.png", file_name)
        print(f"download file {file_name}")

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

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if get_bucket_lifecycle_configuration_flag:

    # Add a lifecycle configuration to an Amazon S3 bucket using an AWS SDK

    # You can direct Amazon S3 to change the storage class of objects by adding an S3 Lifecycle configuration to a bucket
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html

    client = boto3.client('s3')
    bucket = "bucket-sdk-python-123"
    response = client.put_bucket_lifecycle(
        Bucket=bucket,
        ChecksumAlgorithm='CRC32',
        LifecycleConfiguration={
            'Rules': [
                {
                    'Expiration': {
                        'Days': 123
                    },
                    'ID': 'string',
                    'Prefix': 'string',
                    'Status': 'Enabled',
                    'Transition':
                    {
                        'Days': 0,
                        'StorageClass': 'GLACIER',
                    },
                    'NoncurrentVersionTransition': {
                        'NoncurrentDays': 0,
                        'StorageClass': 'GLACIER'
                    },
                    'NoncurrentVersionExpiration': {
                        'NoncurrentDays': 1000
                    },
                    'AbortIncompleteMultipartUpload': {
                        'DaysAfterInitiation': 123
                    }
                },
            ]
        },
        ExpectedBucketOwner='821075683906'
    )


    response = client.get_bucket_lifecycle_configuration(
        Bucket=bucket
    )
    print(f"lifecycle_configuration:{response}")

    s3 = boto3.resource('s3')
    config = s3.BucketLifecycleConfiguration("bucket-sdk-python-123")
    print("lifecycle_configuration 2")
    print(
        "Got lifecycle rules %s for bucket '%s'.", config.rules)

    print(response)

    bucket = 'bucket-sdk-python-123'
    s3_client = boto3.client('s3')
    response = s3_client.list_objects(
        Bucket=bucket
    )

    contents = response["Contents"]
    print(f"content of bucket {bucket}")
    print(f'  {contents[0]}')


