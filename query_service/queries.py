#AWS configs
# AWS S3 bucket name
AWS_BUCKET_NAME = 'S3'
# AWS DynamoDB table name
AWS_TABLE_NAME = 'test'
# Path for temporary storage
STORAGE_PATH = '/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/data/'
# Path for storage uploaded files
UPLOAD_PATH = STORAGE_PATH + '/upload/'
# Path for storage downloaded files
DOWNLOAD_PATH = STORAGE_PATH + '/download/'


#Postgre configs
POSTGRES_CONFIG = {
    'user' : 'postgres',
    'password' : '98052',
    'host' : 'localhost',
    'dbname' : 'im'
}

TABLE_NAME = 'test'


#queries
