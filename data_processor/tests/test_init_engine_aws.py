
import sys
sys.path.insert(0,'/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/')

import pytest
import boto3
from moto import mock_s3
from moto import mock_dynamodb2

from data_processor.data_workflow_api.init_engine_aws import init
from data_processor.data_workflow_api.init_engine_postgre import DbServiceConnect, TableStyles
from data_processor.data_workflow_api.celery_tasks import put_data_s3_by_record_from_query

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client('s3', region_name='us-east-1')



@mock_dynamodb2
def test_init():   
    
    table_name = 'test'
    dynamodb = boto3.resource('dynamodb', 'us-east-1')

    table = dynamodb.create_table(
        TableName=table_name,
            AttributeDefinitions=[
                {'AttributeName': 'file_key', 'AttributeType': 'S'},
                {'AttributeName': 'file_name', 'AttributeType': 'S'},

            ],
            KeySchema=[
                {'AttributeName': 'file_key', 'KeyType': 'HASH'},
                {'AttributeName': 'file_name','KeyType': 'RANGE'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5 
        })

    item = {'file_key': 'hash_string', 'file_name': 'image_id'}

    table.put_item(Item = item)

    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
            'file_key': 'hash_string',
            'file_name': 'image_id'
        }
    )
    if 'Item' in response:
        item = response['Item']

    assert ("file_key" in item)    
    assert (item["file_key"] == "hash_string")
    assert ("file_name" in item)    
    assert (item["file_name"] == "image_id")





