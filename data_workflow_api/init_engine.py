import boto3
from botocore.exceptions import ClientError

from configs.aws import AWS_BUCKET_NAME, AWS_TABLE_NAME


def init():
    """Initialize AWS services for the backend.
    
        Note:
            S3 is used to store files.
            DynamoDB is used to bind a key-value between a hash and a file name.
    """

    try:
        s3 = boto3.client('s3')
        store = s3.create_bucket(Bucket=AWS_BUCKET_NAME)
    
        db = boto3.resource('dynamodb')
        table = db.create_table(
            AttributeDefinitions=[
                {'AttributeName': 'file_key', 'AttributeType': 'S'},
                {'AttributeName': 'image_file_name', 'AttributeType': 'S'},
                {'AttributeName': 'meta_file_name', 'AttributeType': 'S'}
            ],
            TableName=AWS_TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'file_key', 'KeyType': 'HASH'},
                {'AttributeName': 'image_file_name','KeyType': 'RANGE'},
                {'AttributeName': 'meta_file_name','KeyType': 'RANGE'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5 #hardcoded for Free Usage Tier
        })
    except ClientError as e:
            print("Unexpected error: {}".format(e))


if __name__ == '__main__':
    init()


#TODO update to load data to existing table, look for possible errors, check db schema