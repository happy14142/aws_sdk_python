# working with EC2
# https: // boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html

import sys
import boto3
from botocore.exceptions import ClientError


ec2 = boto3.client('ec2')
response = ec2.describe_instances()

print('describe_instances')
print(response)

InstanceId = response['Reservations'][0]['Instances'][0]['InstanceId']

print('monitor_instances')
response = ec2.monitor_instances(InstanceIds=[InstanceId])
print(response)

# Starts an Amazon EBS-backed instance that you've previously stopped.

try:
    response = ec2.start_instances(InstanceIds=['i-01aa6bb6eb45c7430'], DryRun=False)
except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

print("Starts an Amazon EBS-backed instance that you've previously stopped")
print(response)