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
def put_data_to_s3(file_path):
    """Upload file into AWS S3 storage
    
        Note: 
            Receives file path, obtains md5 hash function of the file,
            saves file_key (hash) and file_name values in AWS DynamoDB,
            uploads file to AWS S3 storage.
    
    """

@app.task
def get_data_from_s3(file_key):
    """Download file from AWS S3 storage
    
        Note: 
            Receives file key, obtains file name from AWS DynamoDB,
            downloads file from AWS S3 storage.
    
    """