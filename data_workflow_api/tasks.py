import os

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from celery import Celery

from config import AWS_BUCKET_NAME, AWS_TABLE_NAME, UPLOAD_PATH, DOWNLOAD_PATH
from utils import utils


app = Celery('tasks')
app.config_from_object('celeryconfig')


@app.task
def put_data_to_s3(path):
    """Upload file into AWS S3 storage
    
        Note: 
            Receives path, obtains md5 hash function of the meta-file,
            saves file_key (hash) and file_names for image and meta-file values in AWS DynamoDB,
            uploads files to AWS S3 storage.
    
    """

    hash_string = None
    try:
        db = boto3.resource('dynamodb')
        table = db.Table(AWS_TABLE_NAME)

        utils.
    
        with open(meta_file_path, 'rb') as f:
            hash_string = utils.md5(f)
    
        path, file_name = os.path.split(file_path)
        table.put_item(
            Item = {
                'file_key': hash_string,
                'meta_file_name': meta_file_name,
                'image_file_name': image_file_name
            })
    
        s3 = boto3.client('s3')
        with open(file_path, 'rb') as f:
            s3.upload_fileobj(f, AWS_BUCKET_NAME, hash_string)
            #add seconf file
    except ClientError as e:
        hash_string = None

    return hash_string

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

    @app.task
    def update_file(file_key, file_path):
        """Update file from AWS S3 storage
    
        Note: 
            Receives file key, obtains file name from AWS DynamoDB,
            update file from AWS S3 storage.
    
    """

    #TODO put 1K to postgre, read line, create hash, add hash to new column in postgre, get pathes to file by name, add to Dynamo, save to s3 

