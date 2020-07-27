import os
import json

import pandas as pd 

import sys
sys.path.insert(0,'data_pipeline_processor/data_workflow_api/')
sys.path.insert(0, '/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor')



import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from celery import Celery

from data_workflow_api import celeryconfig
from data_workflow_api.init_engine_postgre import DbServiceConnect, TableStyles
from data_workflow_api.configs import AWS_BUCKET_NAME, AWS_TABLE_NAME, DOWNLOAD_PATH, POSTGRES_CONFIG, TABLE_NAME


#from utils import utils


app = Celery('query_celery_tasks')
app.config_from_object('celeryconfig')

#16 MB of data, which can contain as many as 100 items

#singe query, batch/single get, statistcs, update meta


#@app.task
def get_queried_data_from_s3_by_one(query, batch_size_for_postgre_query, folder_path):
    """iterates over query by batch and downloads files from AWS S3 storage. 
    
        Note: 
            Receives file keys from query, obtains file names from AWS DynamoDB,
            downloads files from AWS S3 storage.
    
    """
    file_name = None
    db_service = DbServiceConnect(POSTGRES_CONFIG)
    with TableStyles(db_service) as postgre_table:
        with postgre_table.query_table_batch(query, batch_size_for_postgre_query) as records:            
            for batch in records:  
                for record in batch:
                    try:
                        db = boto3.resource("dynamodb")
                        table = db.Table(AWS_TABLE_NAME)
                        file_key = record[-1]                    
                        result = table.query(
                            KeyConditionExpression=Key('file_key').eq(file_key)
                        )                    
                        if result['Count']:
                            file_name = result["Items"][0]["file_name"]
                            query_folder = folder_path +'/'+ query.replace(' ', '_')
                            if not os.path.exists(query_folder):
                                os.mkdir(query_folder)                            
                            file_path = os.path.join(query_folder, file_name+'.jpg')                    
                            s3 = boto3.client('s3')
                            with open(file_path, 'wb') as f:
                                s3.download_fileobj(AWS_BUCKET_NAME, file_key, f)
                            print("{} downloaded".format(file_name))   

                    except ClientError as e:
                        file_name = None

#@app.task
    def update_meta_data_postgre(file_key, file_path):
        """Update file from AWS S3 storage
    
        Note: 
            Receives file key, obtains file name from AWS DynamoDB,
            update file from AWS S3 storage.
    
    """

def get_query_for_statistics(query, return_pandas_df=False):
    if return_pandas:
        query_stat_df = pd.DataFrame()
        db_service = DbServiceConnect(POSTGRES_CONFIG)
        with TableStyles(db_service) as postgre_table:
            with postgre_table.query_table_batch(query, batch_size_for_postgre_query) as records:
                query_stat_df = 







# @app.task
# def put_updated_images_on_s3():
#     pass

# @app.task
# def parse_json_column_postgre():
#     pass

#get_queried_data_from_s3_by_one("SELECT gender, season, year, meta_data, hash_key FROM test WHERE gender='Unisex' AND season='Summer';", 10, '/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/data/download')






    