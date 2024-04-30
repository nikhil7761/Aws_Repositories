import boto3
import datetime

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Get current timestamp
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Name for the AMI
    ami_name = f"App_server_{timestamp}"
   
    # Create AMI for the first instance
    response = ec2_client.create_image(
        InstanceId='i-03176b89fb7428443',  # Instance ID for the first instance
        Name=ami_name,
        NoReboot=True
    )
    
    print("AMI creation initiated for first instance:", response['ImageId'])
    
    # Create AMI for the second instance
    second_instance_response = ec2_client.create_image(
        InstanceId='i-0b4cbb5add45c8d20',  # Instance ID for the second instance
        Name=f"Test_server_2_{timestamp}",  # Modify name if needed
        NoReboot=True
    )
    
    print("AMI creation initiated for second instance:", second_instance_response['ImageId'])


