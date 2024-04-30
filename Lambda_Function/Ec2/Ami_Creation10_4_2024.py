import boto3
import datetime

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Get current timestamp
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Name for the AMI
    ami_name = f"App_server_{timestamp}"
   
    # Create AMI
    response = ec2_client.create_image(
        InstanceId='i-08df51e64d489fb36',
        Name=ami_name,
        NoReboot=True
    )
    
    print("AMI creation initiated:", response['ImageId'])







