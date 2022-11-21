import boto3
import excel_io
FILE_NAME = "aws_eip.xlsx"
RESOURCE_SHEET = "EIP"
FILE_ROWS = []

def all_eip():
    ec2 = boto3.client('ec2')
    filters = [
        {'Name': 'domain', 'Values': ['vpc']}
    ]
    response = ec2.describe_addresses(Filters=filters)

    data = response['Addresses']
    return data


def get_eip_list_bind_instance():
    data = all_eip()
    result = set()
    for item in data:
        if item.get('InstanceId') != None:
            result.add(item['InstanceId'])
    return result

def calc_invalid_eip():
    data = all_eip()
    # title = ['PublicIp','AllocationId','AssociationId','NetworkInterfaceId','NetworkInterfaceOwnerId','NetworkBorderGroup','PublicIpv4Pool']
    title = ['PublicIp','AllocationId','NetworkBorderGroup','PublicIpv4Pool']
    FILE_ROWS.append(title)
    for item in data:
        if item.get('InstanceId') == None and item.get('PrivateIpAddress') == None:
            row = []
            row.append(item.get('PublicIp'))
            row.append(item.get('AllocationId'))
            # row.append(item.get('AssociationId'))
            # row.append(item.get('NetworkInterfaceId'))
            # row.append(item.get('NetworkInterfaceOwnerId'))
            row.append(item.get('NetworkBorderGroup'))
            row.append(item.get('PublicIpv4Pool'))
            if item.get('Tags') != None:
                for tag in item.get('Tags'):
                    row.append('key_' + tag['Key'])
                    row.append('value_' + tag['Value'])
            FILE_ROWS.append(row)

if __name__ == '__main__':
    calc_invalid_eip()
    excel_io.write_to_excel(FILE_NAME,RESOURCE_SHEET,FILE_ROWS)

