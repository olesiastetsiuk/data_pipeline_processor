import os
import json

import hashlib

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from celery import Celery

from psycopg2.extras import Json

from .init_engine_postgre import DbServiceConnect, TableStyles

from .configs import AWS_BUCKET_NAME, AWS_TABLE_NAME, POSTGRES_CONFIG, DATASET_PATH, POSTGRE_TABLE_NAME
from .configs import CVS_ROW_INSERT_QUERY, META_DATA_HASH_KEY_UPDATE_QUERY, HASH_QUERY, CREATE_HASH_INDEX_QUERY, SELECT_META_HASH_ID_QUERY 

app = Celery('celery_tasks')
app.config_from_object('celeryconfig')

def md5(f):
    """
    Obtains md5 hash function of file-like object
    
    """

    h = hashlib.md5(f)    
    return h.hexdigest()


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
                table.bulk_cvs_update_table(DATASET_PATH['styles'], POSTGRE_TABLE_NAME, size=8192) #hardcoded tablename, could be refactored to more general case
            else: 
                table.update_table_from_cvs_by_row(path, CVS_ROW_INSERT_QUERY) #hardcoded insert query
                #TODO fix for nonexisting values in columns
    except Exception as e:
        print("Exception '{}' happened during load cvs to postgre celery task".format(e))
    return path
    

@app.task
def load_meta_data_to_postgre(path):
    """
    Load meta data and hash keys to postgre columns META_DATA JSONB and HASH_KEY
        Note:
        Receives path to folder with meta files and images, iterates over row updates columns
    """

    meta_files_path = path +'/styles/'
    imgs_files_path = path +'/images/'

    try:
        db_service = DbServiceConnect(POSTGRES_CONFIG)
        with TableStyles(db_service) as table:
            records = table.query_table(SELECT_META_HASH_ID_QUERY)
            for record in records:
                image_id = record[0]
                meta_json_path = meta_files_path+image_id+'.json'
                image_path = imgs_files_path+image_id+'.jpg'
                with open(meta_json_path) as json_data:
                    meta_data = json.load(json_data)
                    image_file = open(image_path, 'rb').read()
                    hash_string = md5(image_file)
                    table.update_table_records(META_DATA_HASH_KEY_UPDATE_QUERY, (json.dumps(meta_data), hash_string, image_id))
            table.create_index_from_column(CREATE_HASH_INDEX_QUERY, 'HASH_KEY')
    except Exception as e:
        print("Exception '{}' happened during updating meta and hash columns in postgre celery task".format(e))
    return path


@app.task
def put_data_s3_by_record_from_query(path):

    """Upload file into AWS S3 storage
    
        Note: 
            Receivespath, obtains md5 hash function of the image file from postgre table,
            saves file_key (hash) and file_name for image values in AWS DynamoDB,
            uploads file to AWS S3 storage for .
    
    """

    imgs_files_path = path +'/images/'

    try:
        db_service = DbServiceConnect(POSTGRES_CONFIG)
        with TableStyles(db_service) as table:
            records = table.query_table(HASH_QUERY)
            if records: 
                for record in records:
                    image_id = record[0]
                    hash_string = record[-1]
                    image_path = imgs_files_path+image_id+'.jpg'
                    db = boto3.resource('dynamodb')
                    table = db.Table(AWS_TABLE_NAME)
                    table.put_item(
                            Item = {
                                'file_key': hash_string,
                                'file_name': image_id
                            })                
                    s3 = boto3.client('s3')
                    with open(image_path, 'rb') as f:
                        s3.upload_fileobj(f, AWS_BUCKET_NAME, hash_string)
                        print("Image {} uploaded to S3".format(image_id))

    except ClientError as e:
        print("Error {} while put data to S3".format(e))
    return path



#TODO
# folder with jsons to table with id and JSONB column to bulk load
# folder with images to table with id and hash value to bulk load
# how to BatchWriteItem + batch load on s3? 
# update dynamo only by images + hash without postgre query - how to preserve consistency?
# csv to dummy vars
