import boto3


def all_eip():
    ec2 = boto3.client('ec2')
    filters = [
        {'Name': 'domain', 'Values': ['vpc']}
    ]
    response = ec2.describe_addresses(Filters=filters)

    data = response['Addresses']
    result = set()
    for item in data:
        if item.get('InstanceId') != None:
            result.add(item['InstanceId'])
    return result

