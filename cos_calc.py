import boto3

def all_cos():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('aa-bj-hdmap-emrdata')
    bucket_request_payment = s3.BucketRequestPayment('aa-bj-hdmap-emrdata')
    # for attr in dir(bucket):
    #     print(attr + ' :'+ str(getattr(bucket,attr)))
    for attr in dir(bucket_request_payment):
        print(attr + ' :'+ str(getattr(bucket_request_payment,attr)))

if __name__ == '__main__':
    all_cos()