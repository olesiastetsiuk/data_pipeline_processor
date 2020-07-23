import os

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from celery import Celery

from config import AWS_BUCKET_NAME, AWS_TABLE_NAME, UPLOAD_PATH, DOWNLOAD_PATH
from utils import utils

#from configs import DATASET_PATH


app = Celery('celery_tasks')
app.config_from_object('celeryconfig')


@app.task
def put_single_data_to_s3(path):
    """Upload file into AWS S3 storage
    
        Note: 
            Receivespath, obtains md5 hash function of the image file,
            saves file_key (hash) and file_name for image values in AWS DynamoDB,
            uploads file to AWS S3 storage.
    
    """

    hash_string = None
    try:
        db = boto3.resource('dynamodb')
        table = db.Table(AWS_TABLE_NAME)

        meta_files_path = path['meta_files']
        imgs_files_path = path['images']

        #iterate over rows get id, search for name in files, get paths
        
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
            
            #update column in styles table
        except ClientError as e:
            hash_string = None

    return hash_string

@app.task
def put_batch_data_to_s3(path):
    """Upload batch files into AWS S3 storage
    
        Note: 
            Receives path, obtains md5 hash function of the image file,
            saves file_key (hash) and file_name for image values in AWS DynamoDB,
            uploads file to AWS S3 storage.
    
    """

    hash_string = None
    try:
        db = boto3.resource('dynamodb')
        table = db.Table(AWS_TABLE_NAME)

        meta_files_path = path['meta_files']
        imgs_files_path = path['images']

        #iterate over rows get id, search for name in files, get paths
        
            with open(meta_file_path, 'rb') as f:
                hash_string = utils.md5(f)
        
            path, file_name = os.path.split(file_path)
            table.put_item(
                Item = {
                    'file_key': hash_string,
                    'meta_file_name': file_name)
        
            s3 = boto3.client('s3')
            with open(file_path, 'rb') as f:
                s3.upload_fileobj(f, AWS_BUCKET_NAME, hash_string)
            
            #update column in styles table
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

    #TODO put json to postgre, add search inside jsons in postgre, add creating index from hash column 
