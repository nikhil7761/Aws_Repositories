#Deletion logic for the all ami_images
import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Describe all images owned by the account
    images_response = ec2_client.describe_images(Owners=['self'])
    
    # Sort images by creation date in descending order (newest first)
    sorted_images = sorted(images_response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    
    # Define the maximum number of AMIs to retain
    max_retained_amis = 1
    
    # Check if the number of images exceeds the maximum
    if len(sorted_images) > max_retained_amis:
        # Get the IDs of older AMIs to delete
        amis_to_delete = [image['ImageId'] for image in sorted_images[max_retained_amis:]]
        
        # Deregister older AMIs
        for ami_id in amis_to_delete:
            ec2_client.deregister_image(ImageId=ami_id)
            print("Deleted older AMI:", ami_id)
            
            # Optionally, delete associated snapshots
            for snapshot in ec2_client.describe_snapshots(Filters=[{'Name': 'description', 'Values': ['*'+ami_id+'*']}])['Snapshots']:
                snapshot_id = snapshot['SnapshotId']
                ec2_client.delete_snapshot(SnapshotId=snapshot_id)
                print("Deleted associated snapshot:", snapshot_id)
    else:
        print("No need to delete old AMIs.")