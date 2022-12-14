
import boto3
client = boto3.client('rds')

def get_all():
    response = client.describe_db_instances(
  
    )
    print(response)




if __name__ == '__main__':
    get_all()