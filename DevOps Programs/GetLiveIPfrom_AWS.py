import boto3

def get_live_servers_ips(asg_name):
    # Create an EC2 client using boto3
    ec2_client = boto3.client('ec2')
    
    # Create an AutoScaling client
    asg_client = boto3.client('autoscaling')
    
    # Describe the Auto Scaling group to get the instance IDs
    response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    
    # Check if the Auto Scaling group exists and is found
    if 'AutoScalingGroups' not in response or len(response['AutoScalingGroups']) == 0:
        print(f"Auto Scaling Group '{asg_name}' not found.")
        return []
    
    # Get the list of instances in the group
    instances = response['AutoScalingGroups'][0]['Instances']
    
    # Collect the instance IDs that are in the 'InService' state
    in_service_instances = [instance['InstanceId'] for instance in instances if instance['LifecycleState'] == 'InService']
    
    if not in_service_instances:
        print("No live instances found in the Auto Scaling group.")
        return []

    # Now, describe the instances to get their IP addresses
    instances_info = ec2_client.describe_instances(InstanceIds=in_service_instances)
    
    # Extract and return the private IPs of the live instances
    ip_addresses = []
    for reservation in instances_info['Reservations']:
        for instance in reservation['Instances']:
            ip_addresses.append(instance['PrivateIpAddress'])
    
    return ip_addresses

if __name__ == "__main__":
    # Name of your Auto Scaling group (replace with your actual ASG name)
    asg_name = "your-auto-scaling-group-name"
    
    # Fetch live server IPs
    ips = get_live_servers_ips(asg_name)
    
    if ips:
        print(f"Live server IPs in the Auto Scaling group '{asg_name}':")
        for ip in ips:
            print(ip)
    else:
        print(f"No live servers found in the Auto Scaling group '{asg_name}'.")



Explaination:
Explanation of the Script:
boto3.client:

This creates a connection to AWS EC2 and Auto Scaling services.
describe_auto_scaling_groups:

This call fetches details about the Auto Scaling group, including the instances associated with it.
Filter live instances:

The instances in an Auto Scaling group are checked for their lifecycle state (whether they are InService). Only those that are InService are considered as live servers.
describe_instances:

This retrieves detailed information about the EC2 instances, including their IP addresses.
Private IP Extraction:

The script extracts the private IP address (PrivateIpAddress) of each live instance and prints them.
Notes:
Replace "your-auto-scaling-group-name" with the name of your actual Auto Scaling group.
This script retrieves private IP addresses. If you need public IP addresses, you can modify the script to access PublicIpAddress instead of PrivateIpAddress.
Ensure that your AWS credentials are configured with the necessary permissions to access Auto Scaling and EC2 services.


Example Output:
Live server IPs in the Auto Scaling group 'your-auto-scaling-group-name':
10.0.1.15
10.0.1.16
10.0.1.17
