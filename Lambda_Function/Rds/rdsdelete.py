import boto3
import time

def create_db_snapshot(db_instance_identifier):
  rds = boto3.client('rds')
  try:
    # Create a new snapshot
    response = rds.create_db_snapshot(
        DBSnapshotIdentifier='snapshot-' + db_instance_identifier + '-' + str(int(time.time())),
        DBInstanceIdentifier=db_instance_identifier
    )
    print("Snapshot created:", response['DBSnapshot']['DBSnapshotIdentifier'])
  except Exception as e:
    print("Error creating snapshot:", str(e))

def delete_old_snapshots(db_instance_identifier, num_to_keep):
  rds = boto3.client('rds')
  try:
    # List existing snapshots
    snapshots = rds.describe_db_snapshots(DBInstanceIdentifier=db_instance_identifier)['DBSnapshots']

    # Filter out snapshots without 'SnapshotCreateTime'
    snapshots_with_time = [snap for snap in snapshots if 'SnapshotCreateTime' in snap]

    # Sort filtered list by creation time (descending order)
    snapshots_with_time.sort(key=lambda snap: snap['SnapshotCreateTime'], reverse=True)

    # Delete all except the most recent num_to_keep
    for snapshot in snapshots_with_time[num_to_keep:]:
      rds.delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])
      print("Snapshot deleted:", snapshot['DBSnapshotIdentifier'])
  except Exception as e:
    print("Error:", str(e))

def lambda_handler(event, context):
  db_instance_identifier = 'database-1'  # Replace with your RDS instance identifier
  num_to_keep = 2

  # Call your functions for snapshot management
  create_db_snapshot(db_instance_identifier)
  delete_old_snapshots(db_instance_identifier, num_to_keep)

  return "Database snapshots managed successfully!"  # You can customize the return value

# Save this code in a file named lambda_function.py (or your preferred extension)
