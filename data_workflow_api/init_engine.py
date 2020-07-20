import boto3
from botocore.exceptions import ClientError

#from configs.aws import AWS_BUCKET_NAME, AWS_TABLE_NAME

# AWS S3 bucket name
AWS_BUCKET_NAME = 'fashionimages'
# AWS DynamoDB table name
AWS_TABLE_NAME = 'fashion_images'
# Path for temporary storage
STORAGE_PATH = './data/'
# Path for temporary storage uploaded files
UPLOAD_PATH = STORAGE_PATH + '/upload/'
# Path for temporary storage downloaded files
DOWNLOAD_PATH = STORAGE_PATH + '/download/'


def init():
    """Initialize AWS services for the backend.
    
        Note:
            S3 is used to store files.
            DynamoDB is used to bind a key-value between a hash and a file name.
    """

    def bucket_exists(bucket):
        s3 = boto3.resource('s3')
        return s3.Bucket(bucket) in s3.buckets.all()

    try:
        s3 = boto3.client('s3')

        if bucket_exists(AWS_BUCKET_NAME):
            print("Bucket '{}' already exists.".format(AWS_BUCKET_NAME))
        else: 
            store = s3.create_bucket(Bucket=AWS_BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
    
        db = boto3.resource('dynamodb')

        table = db.create_table(
            AttributeDefinitions=[
                {'AttributeName': 'file_key', 'AttributeType': 'S'}

            ],
            TableName=AWS_TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'file_key', 'KeyType': 'HASH'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5 
        })

        print("Table '{}' was created.".format(AWS_TABLE_NAME))

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table '{}' already exists.".format(AWS_TABLE_NAME))
        else:
            print("Unexpected error: {}".format(e))



if __name__ == '__main__':
    init()