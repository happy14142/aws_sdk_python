# documentation can be found here 
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

import boto3
import sys

s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

# Upload a new file
data = open('picture.png', 'rb')
s3.Bucket('mynewbucket124324235').put_object(Key='picture.png', Body=data)





# working with EC2 instances
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
print(response)

ec2 = boto3.client('ec2')
if sys.argv[1] == 'ON':
    response = ec2.monitor_instances(InstanceIds=['INSTANCE_ID'])
else:
    response = ec2.unmonitor_instances(InstanceIds=['INSTANCE_ID'])
print(response)
