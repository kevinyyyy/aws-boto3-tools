import boto3
import excel_writer

FILE_ROW = []
client = boto3.client('s3')


def all_cos():
    s3 = boto3.resource('s3')
    # bucket = s3.Bucket('aa-bj-hdmap-emrdata')
    # for attr in dir(bucket):
    #     print(attr + ' :'+ str(getattr(bucket,attr)))

    title = ['name', 'creation_date', 'region']
    bucket_name_list = []
    s3 = boto3.resource('s3')
    buckets = s3.buckets.all()
    for bucket in buckets:
        try:
            valid = False
            for obj in bucket.objects.all():
                valid = True
                break
            if not valid:
                bucket_name_list.append(bucket.name)
                print("invalid s3 bucket:" + bucket.name)
        except Exception as e:
            print('access denied:' + bucket.name)
            print(e)

    all_tags = {}
    for bucket in bucket_name_list:
        tag = s3_tags(bucket)
        if tag != None and tag.get(bucket) != None:
            all_tags[bucket] = tag[bucket]

    tags_set = set()
    for k in all_tags:
        tags_set.add(k['Key'])
    
    for k in tags_set:
        title.append('tag_' + k)

    for bucket in bucket_name_list:
        current_bucket = s3.Bucket(bucket)
        row = []
        #title = ['name', 'creation_date', 'region']
        row.append(current_bucket.name)
        row.append(current_bucket.create_date.strftime("%Y-%m-%d %H:%M:%S"))
        row.append('cn-north-1')
        tags = all_tags.get(current_bucket.name)
        if tags != None:
            tag_dict = {}
            for tag in tags:
                tag_dict[tag['Key']] = tag['Value']
            for key in tags_set:
                if tag_dict.get(key) != None:
                    row.append(tag_dict[key])
                else:
                    row.append('-')
        
def s3_tags(bucket_name):
    try:
        response = client.get_bucket_tagging(
            Bucket=bucket_name
        )
        tag = {}
        if response != None and response.get('TagSet') != None:
            tag[bucket_name] = response.get('TagSet')
            return tag
        return None
    except Exception as e:
            print('get tag error:' + bucket_name)
            print(e)


if __name__ == '__main__':
    all_cos()
    excel_writer.write_to_excel('E:\\file\\aws_s3.xlsx','S3',FILE_ROW)
    #s3_tags('elasticbeanstalk-cn-north-1-257625911310')
