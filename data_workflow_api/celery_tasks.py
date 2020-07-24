import os
import json


import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from celery import Celery

from configs import AWS_BUCKET_NAME, AWS_TABLE_NAME, UPLOAD_PATH, DOWNLOAD_PATH, POSTGRES_CONFIG, TABLE_NAME, DATASET_PATH, META_DATA_HASH_KEY_UPDATE_QUERY, HASH_QUERY
from utils import utils


app = Celery('celery_tasks')
app.config_from_object('celeryconfig')

@app.task
def load_csv_to_postgre(path, in_bulk = False):
    """
    Load csv to existing postgre table.
        Note:
        Receives path to cvs, in_bulk option is False by default and uses cursor.copy_from method
    """
    try:
        db_service = DbServiceConnect(POSTGRES_CONFIG)
        with TableStyles(db_service) as table:
            if in_bulk: 
                table.bulk_cvs_update_table(DATASET_PATH['styles.csv'], TABLE_NAME) #hardcoded tablename, could be refactored to more general case
            else: 
                table.update_table_from_cvs_by_row(DATASET_PATH['styles.csv'], CVS_ROW_INSERT_QUERY) #hardcoded insert query, same
    except Exception as e:
        print("Exception '{}' happened during load cvs to postgre celery task".format(e))
    

@app.task
def load_meta_data_to_postgre(path):
    """
    Load meta data and hash keys to postgre columns META_DATA JSONB and HASH_KEY
        Note:
        Receives path to folder with meta files and images, iterates over row updates columns
    """

    meta_files_path = path['meta_files']
    imgs_files_path = path['images']

    try:
        db_service = DbServiceConnect(POSTGRES_CONFIG)
        with TableStyles(db_service) as table:
            records = query_table(META_DATA_HASH_KEY_UPDATE_QUERY)
            for record in records:
                image_id = record['id']
                meta_json_path = meta_files_path+image_id+'.json'
                image_path = imgs_files_path+image_id+'.jpg'
                with open(meta_json_path) as meta_file:
                    meta_data = json.load(meta_file)
                    with open(image_path, 'rb') as image_file:
                        hash_string = utils.md5(image_file)
                        table.update_table_records(META_DATA_HASH_KEY_UPDATE_QUERY, meta_data, hash_string, image_id)
    except Exception as e:
        print("Exception '{}' happened during updating meta and hash columns in postgre celery task".format(e))

# task to put single data on s3, get hash from postgre
@app.task
def put_data_s3_by_record_from_query(path):

    """Upload file into AWS S3 storage
    
        Note: 
            Receivespath, obtains md5 hash function of the image file from postgre table,
            saves file_key (hash) and file_name for image values in AWS DynamoDB,
            uploads file to AWS S3 storage for .
    
    """

    imgs_files_path = path['images']

    try:
        db_service = DbServiceConnect(POSTGRES_CONFIG)
        with TableStyles(db_service) as table:
            records = query_table(HASH_QUERY)
            for record in records:
                image_id = record['id']
                hash_string = record['hash_key']
                image_path = imgs_files_path+image_id+'.jpg'
                db = boto3.resource('dynamodb')
                table = db.Table(AWS_TABLE_NAME)
                table.put_item(
                        Item = {
                            'file_key': hash_string,
                            'image_file_name': image_file_name
                        })                
                s3 = boto3.client('s3')
                with open(image_path, 'rb') as f:
                    s3.upload_fileobj(f, AWS_BUCKET_NAME, hash_string)

    except ClientError as e:
        hash_string = None



#task to pit bulk on s3
#task to query


# task to get single fron s3

# task to get bulk from s3

#task to update json
# task to bulk update postgre






    #TODO put json to postgre, add search inside jsons in postgre, add creating index from hash column 
