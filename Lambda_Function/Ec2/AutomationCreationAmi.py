import boto3
import datetime

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Create new AMI
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    for reservation in ec2_client.describe_instances()['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            
            if instance_state not in ['running', 'stopping', 'stopped']:
                continue
            
            instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), '')
            
            # Ensure the instance ID is in a format that can be included in the AMI description
            if len(instance_id) > 10:
                instance_id_part = instance_id[-10:]  # Take the last 10 characters of the instance ID
            else:
                instance_id_part = instance_id
            
            ami_name = f"{instance_name}_{current_time}" if instance_name else f"Unnamed_Instance_{instance_id_part}_{current_time}"
            
            response = ec2_client.create_image(
                InstanceId=instance_id,
                Name=ami_name,
                Description=f"Instance_ID_{instance_id_part}",  # Add instance ID to description
                NoReboot=True
            )
            print(f"AMI creation initiated for instance {instance_id}: {response['ImageId']}")
    
    return {'statusCode': 200, 'body': 'AMIs creation initiated successfully.'}
