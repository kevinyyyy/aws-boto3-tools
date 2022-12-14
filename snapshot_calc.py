import boto3
import excel_writer

EMPTY = '-'
FILE_ROW = []

def print_attr(snapshot):
    for attr in dir(snapshot):
        if type(getattr(snapshot,attr)) == str:
            print(attr + ' :' + str(type(getattr(snapshot,attr))) +':'+ str(getattr(snapshot,attr)))
        else:
            print_attr(getattr(snapshot,attr))
def all_snapshot():

    ec2 = boto3.resource('ec2')
    snapshot = ec2.Snapshot('snap-0c7b8efd')
    for attr in dir(snapshot):
        print(attr + ' :' + str(type(getattr(snapshot,attr))) +':'+ str(getattr(snapshot,attr)))

    # title = ['id','kms_key_id','owner_id','progress','start_time','state','state_message','storage_tier','volume_id','volume_size']
    # volume_dict = {}
    # result = []
    # tags_set = set()
    # volumes = ec2.volumes.all()
    # for v in volumes:
    #     volume_dict[v.id] = 1
    # i = 0
    # for item in ec2.snapshots.all():
    #     i+=1
    #     if volume_dict.get(item.volume_id) == None:
    #         if item.tags != None:
    #             for tag in item.tags:
    #                 key = tag['Key']
    #                 tags_set.add(key)
    # print(i)
    # for tag in tags_set:
    #     title.append('tag_' + tag)
    # FILE_ROW.append(title)

    # for snap in ec2.snapshots.all():
    # # title = ['id','kms_key_id','owner_id','progress','start_time','state','state_message','storage_tier','volume_id','volume_size']
    #     if volume_dict.get(snap.volume_id) == None:
    #         row = []
    #         row.append(snap.id);
    #         row.append(snap.kms_key_id);
    #         row.append(snap.owner_id);
    #         row.append(snap.progress);
    #         row.append(snap.start_time.strftime("%Y-%m-%d %H:%M:%S"));
    #         row.append(snap.state);
    #         row.append(snap.state_message);
    #         row.append(snap.storage_tier);
    #         row.append(snap.volume_id);
    #         row.append(snap.volume_size);
    #         if snap.tags != None:
    #             tag_list = snap.tags
    #             tag_dict = {}
    #             for t in tag_list:
    #                 tag_dict[t['Key']] = t['Value']
    #             for tag in tags_set:
    #                 if tag_dict.get(tag) != None:
    #                     row.append(tag_dict[tag])
    #                 else:
    #                     row.append(EMPTY)
    #         FILE_ROW.append(row)

if __name__ == '__main__':
    all_snapshot()
    #excel_writer.write_to_excel("E:\\file\\aws_snapshot.xlsx",'snapshot',FILE_ROW)