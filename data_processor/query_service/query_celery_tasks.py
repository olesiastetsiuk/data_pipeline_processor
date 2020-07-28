import os
import json
import glob

import pandas as pd 

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from celery import Celery
import psycopg2

from data_workflow_api.init_engine_postgre import DbServiceConnect, TableStyles
from data_workflow_api.configs import AWS_BUCKET_NAME, AWS_TABLE_NAME, DOWNLOAD_PATH, POSTGRES_CONFIG, POSTGRE_TABLE_NAME
from queries_config import META_DATA_UPDATE_QUERY


app = Celery('query_celery_tasks')
app.config_from_object('celeryconfig')


@app.task
def get_queried_data_from_s3_by_one(query, batch_size_for_postgre_query, folder_path):
    """iterates over query by batch and downloads files from AWS S3 storage. 
    
        Note: 
            Receives file keys from query, obtains file names from AWS DynamoDB,
            downloads files from AWS S3 storage. Returns query folder name. 
    
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
                            print("Image id {} downloaded".format(file_name))   

                    except ClientError as e:
                        file_name = None
    return query_folder


@app.task
def get_query_for_inspection(query, chunksize, folder_to_save_csv):
    """Gets queried results for calculation statistics.
        Note:
        Receives query, chunksize, return pandas datafarme merged from chunks saved as csv.
    """

    db_service = DbServiceConnect(POSTGRES_CONFIG)
    with TableStyles(db_service) as postgre_table:
        table = postgre_table.query_to_pandas_df(query, chunksize)
        query_df = pd.DataFrame()
        while True:
            try:
                query_df = query_df.append(next(table))
            except StopIteration:
                break
        query_df.reset_index(inplace=True)
        if not os.path.exists(folder_to_save_csv):
            os.mkdir(folder_to_save_csv)
        csv_full_path = folder_to_save_csv +'/'+ query.replace(' ', '_') + '.csv'
        query_df.to_csv(csv_full_path)
        return csv_full_path


@app.task
def append_meta_data_postgre(update_meta_query, meta_data_json_path):
    """Update meta data in Postgre column meta data.

    Note: 
        Receives qurty to concatenate meta data and path to jsons with new attribures named as image
""" 
    try:
        db_service = DbServiceConnect(POSTGRES_CONFIG)
        with TableStyles(db_service) as table:
            updates_to_meta_jsons = glob.glob(meta_data_json_path+"/*.json")
            for js in updates_to_meta_jsons:
                image_id = js.split('/')[-1].split('.')[0]           
                with open(js) as json_data:
                    meta_data = json.load(json_data)
                    table.update_table_records(update_meta_query, (json.dumps(meta_data), image_id))            
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while update meta to postgre", error)



#TODO 
## add getbatchitem for Dymamo (16 MB of data, which can contain as many as 100 items)
# check if we get all images, compare count by query
# checks for consistency 
# add batch update meta
# add parsing json column
# add profiling option/decorator
# add upload modified images to Dynamo to same hash keys but as a new attribute

    