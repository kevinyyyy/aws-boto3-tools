import boto3
import excel_writer
import excel_reader

'''
ec2.instance:
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
'_id', 'ami_launch_index', 'architecture', 'attach_classic_link_vpc', 'attach_volume', 'block_device_mappings', 'boot_mode', 'capacity_reservation_id', 'capacity_reservation_specification', 'classic_address', 'client_token', 'console_output', 'cpu_options', 'create_image', 'create_tags', 'delete_tags', 'describe_attribute', 'detach_classic_link_vpc', 'detach_volume', 'ebs_optimized', 'elastic_gpu_associations', 'elastic_inference_accelerator_associations', 'ena_support', 'enclave_options', 'get_available_subresources', 'hibernation_options', 'hypervisor', 'iam_instance_profile', 'id', 'image', 'image_id', 'instance_id', 'instance_lifecycle', 'instance_type', 'ipv6_address', 'kernel_id', 'key_name', 'key_pair', 'launch_time', 'licenses', 'load', 'maintenance_options', 'meta', 'metadata_options', 'modify_attribute', 'monitor', 'monitoring', 'network_interfaces', 'network_interfaces_attribute', 'outpost_arn', 'password_data', 'placement', 'placement_group', 'platform', 'platform_details', 'private_dns_name', 'private_dns_name_options', 'private_ip_address', 'product_codes', 'public_dns_name', 'public_ip_address', 'ramdisk_id', 'reboot', 'reload', 'report_status', 'reset_attribute', 'reset_kernel', 'reset_ramdisk', 'reset_source_dest_check', 'root_device_name', 'root_device_type', 'security_groups', 'source_dest_check', 'spot_instance_request_id', 'sriov_net_support', 'start', 'state', 'state_reason', 'state_transition_reason', 'stop', 'subnet', 'subnet_id', 'tags', 'terminate', 'tpm_support', 'unmonitor', 'usage_operation', 'usage_operation_update_time', 'virtualization_type', 'volumes', 'vpc', 'vpc_addresses', 'vpc_id', 'wait_until_exists', 'wait_until_running', 'wait_until_stopped', 'wait_until_terminated']


volume:
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
'_id', 'attach_to_instance', 'attachments', 'availability_zone', 'create_snapshot', 'create_tags', 'create_time', 'delete', 'describe_attribute', 'describe_status', 'detach_from_instance', 'enable_io', 'encrypted', 'fast_restored', 'get_available_subresources', 'id', 'iops', 
'kms_key_id', 'load', 'meta', 'modify_attribute', 'multi_attach_enabled', 'outpost_arn', 'reload', 'size', 'snapshot_id', 'snapshots', 'state', 'tags', 'throughput', 'volume_id', 'volume_type']
'''


# this is for invalid ec2

# result rows
FILE_ROWS = []
RESOURCE_SHEET = 'ec2'
FILE_NAME = 'aws_ec2.xlsx'
instanceIds = set()
EMPTY = '-'

def ec2_price():
    old_table = excel_reader.read_excel('aws_ec22.xlsx',0)
    price_dict = {}
    for row in old_table:
        price_dict[row[0].value] = row[13].value
    return price_dict

# calc ec2 invalid data
def calc_data():
    ec2 = boto3.resource('ec2')
    title = ['Name','id','type','volume','vpc_id','launch_time','network','private_dns','private_ip','public_dnc','public_ip','status','节约成本（月）','节约成本（年）']
    FILE_ROWS.append(title)
    price_dict = ec2_price()
    instanceAll = ec2.instances.all()
    name_dict = {}
    tags_set = set()
    for instance in instanceAll:
        if instance.state['Name'] != 'running':
            if len(instance.tags) > 0:
                    for tag in instance.tags:
                        key = tag['Key']
                        if key == 'Name':
                            name_dict[instance.id] = tag['Value']
                            continue
                        tags_set.add(key)

    for tag in tags_set:
        title.append('tag_' + tag)
        
    for instance in instanceAll:
        # inctance is not running 
        if instance.state['Name'] != 'running':
            instanceIds.add(instance.id)
            row = []
            if name_dict.get(instance.id) != None:
                row.append(name_dict[instance.id])
            else:
                row.append(EMPTY)
            row.append(instance.id)
            row.append(instance.instance_type)
            volumeStr = ''
            for volume in instance.volumes.all():
                volumeStr += volume.volume_type +' '+str(volume.size) + '\n'
            row.append(volumeStr)
            row.append(instance.vpc_id)
            row.append(instance.launch_time.strftime("%Y-%m-%d, %H:%M:%S"))
            if len(instance.network_interfaces) >= 1:
                row.append(instance.network_interfaces[0].id)
            else:
                row.append(EMPTY)
            row.append(instance.private_dns_name)
            row.append(instance.private_ip_address)

            if instance.public_dns_name != None:
                row.append(instance.public_dns_name)
            else:
                row.append(EMPTY)

            if instance.public_ip_address != None:
                row.append(instance.public_ip_address)
            else:
                row.append(EMPTY)
            row.append(instance.state['Name'])
            if price_dict.get(instance.id) != None:
                row.append(price_dict.get(instance.id))
                row.append(price_dict.get(instance.id) * 12)
            else:
                row.append(EMPTY)
                row.append(EMPTY)
            if len(instance.tags) > 0:
                tag_list = instance.tags
                tag_dict = {}
                for t in tag_list:
                    tag_dict[t['Key']] = t['Value']
                for tag in tags_set:
                    if tag_dict.get(tag) != None:
                        row.append(tag_dict[tag])
                    else:
                        row.append(EMPTY)
                
            FILE_ROWS.append(row)


if __name__ == '__main__':

    calc_data()
    excel_writer.write_to_excel(FILE_NAME,RESOURCE_SHEET,FILE_ROWS)

    # for row in FILE_ROWS:
    #    print(row)

    # print('size of invalid ec2:' + str(len(instanceIds)))
    # for id in instanceIds:
    #     print(id)