import boto3
import json

def all_snapshot():

    ec2 = boto3.resource('ec2')
    #snapshot = ec2.Snapshot('snap-01d2ce25a7e45e9aa')
    # for attr in dir(snapshot):
    #     print(attr + ' :'+ str(getattr(snapshot,attr)))
    for snap in ec2.snapshots.all():
        if snap.volume_id == None or snap.volume == None:
            print(snap.id)
        


if __name__ == '__main__':
    all_snapshot()