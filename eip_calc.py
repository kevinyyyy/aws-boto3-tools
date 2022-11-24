import boto3
import excel_writer
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
    title = ['Name','PublicIp','AllocationId','AssociationId','NetworkInterfaceId','NetworkInterfaceOwnerId','NetworkBorderGroup','PublicIpv4Pool']
    #title = ['Name','PublicIp','AllocationId','NetworkBorderGroup','PublicIpv4Pool']
    FILE_ROWS.append(title)
    name_dict = {}
    tags_set = set()
    for item in data:
        if item.get('InstanceId') == None and item.get('PrivateIpAddress') == None:
            if item.get('Tags') != None:
                for tag in item.get('Tags'):
                    key = tag['Key']
                    if key == 'Name':
                        name_dict[item.get('PublicIp')] = tag['Value']
                        continue
                    tags_set.add(key)
    for k in tags_set:
        title.append('key_' + k)
    
    for item in data:
        if item.get('InstanceId') == None and item.get('PrivateIpAddress') == None:
            row = []
            if name_dict.get('PublicIp') != None:
                row.append(name_dict[item.get('PublicIp')])
            else:
                row.append('-')
            row.append(item.get('PublicIp'))
            row.append(item.get('AllocationId'))
            row.append(item.get('AssociationId'))
            row.append(item.get('NetworkInterfaceId'))
            row.append(item.get('NetworkInterfaceOwnerId'))
            row.append(item.get('NetworkBorderGroup'))
            row.append(item.get('PublicIpv4Pool'))
            if item.get('Tags') != None:
                tag_list = item.get('Tags')
                tag_dict = {}
                for t in tag_list:
                    tag_dict[t['Key']] = t['Value']
                for tag in tags_set:
                    if tag_dict.get(tag) != None:
                        row.append(tag_dict[tag])
                    else:
                        row.append('-')
            FILE_ROWS.append(row)

if __name__ == '__main__':
    calc_invalid_eip()
    excel_writer.write_to_excel(FILE_NAME,RESOURCE_SHEET,FILE_ROWS)

