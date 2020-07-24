import os
import json


import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from celery import Celery

from configs import AWS_BUCKET_NAME, AWS_TABLE_NAME, UPLOAD_PATH, DOWNLOAD_PATH, POSTGRES_CONFIG, TABLE_NAME, DATASET_PATH, META_DATA_HASH_KEY_UPDATE_QUERY, HASH_QUERY
from utils import utils


app = Celery('query_celery_tasks')
app.config_from_object('celeryconfig')



@app.task
    def update_file(file_key, file_path):
        """Update file from AWS S3 storage
    
        Note: 
            Receives file key, obtains file name from AWS DynamoDB,
            update file from AWS S3 storage.
    
    """


@app.task
def get_data_from_s3(file_key):
    """Download file from AWS S3 storage
    
        Note: 
            Receives file key, obtains file name from AWS DynamoDB,
            downloads file from AWS S3 storage.
    
    """

    file_name = None
    try:
        db = boto3.resource("dynamodb")
        table = db.Table(AWS_TABLE_NAME)
        
        result = table.query(
            KeyConditionExpression=Key('file_key').eq(file_key)
        )
        
        if result['Count']:
            file_name = result["Items"][0]["file_name"]
            file_path = os.path.join(DOWNLOAD_PATH, file_name)
        
            s3 = boto3.client('s3')
            with open(file_path, 'wb') as f:
                s3.download_fileobj(AWS_BUCKET_NAME, file_key, f)    

    except ClientError as e:
        file_name = None

    return file_name

    