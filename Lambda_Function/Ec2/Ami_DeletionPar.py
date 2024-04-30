import boto3

ddef lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    #Define the instance id
    InstanceId="i-03176b89fb7428443"

  # Described based upon the specified_instance_id
image_response=ec2_client.described_images(Filters=[{'Name':''}]) 




