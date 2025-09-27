import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Replace with your tag key and value
    tag_key = 'Environment'
    tag_value = 'Dev'
    
    # Find instances with the tag
    response = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    # Collect instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    if instance_ids:
        print(f"Stopping instances: {instance_ids}")
        ec2.stop_instances(InstanceIds=instance_ids)
    else:
        print("No running instances found with the specified tag.")