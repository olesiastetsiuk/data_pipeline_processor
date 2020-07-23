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

DATASET_PATH = {
    'styles.csv': STORAGE_PATH + 'fashion_dataset/styles_sample.csv', 
    'images': STORAGE_PATH+ 'fashion_dataset/images/',
    'meta_files': STORAGE_PATH+ 'fashion_dataset/styles/'
}

#Postgre configs
POSTGRES_CONFIG = {
    'user' : 'postgres',
    'password' : '98052',
    'host' : 'localhost',
    'dbname' : 'im'
}

TABLE_NAME = 'test'

#id,gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName

TABLE_QUERY = '''CREATE TABLE test
          (ID TEXT NOT NULL,
          GENDER           TEXT    NOT NULL,
          MASTERCATEGORY           TEXT    NOT NULL,
          SUBCATEGORY           TEXT    NOT NULL,
          ARTICLETYPE           TEXT    NOT NULL,
          BASECOLOUR TEXT NOT NULL,
          SEASON           TEXT    NOT NULL,
          YEAR           INT    NOT NULL,
          USAGE           TEXT    NOT NULL,
          PRODUCTDISPLAYNAME           TEXT    NOT NULL,
          META_DATA JSONB,
          HASH_KEY TEXT); '''

CVS_ROW_INSERT_QUERY = 'INSERT INTO test VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

#BULK_CVS_UPDATE = 'COPY test (id,gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName) FROM %s DELIMITER ','CSV HEADER;

META_DATA_HASH_KEY_UPDATE_QUERY = 'UPDATE test set META_DATA = %s, HASH_KEY = %s where ID = %s'

META_DATA_UPDATE_QUERY = 'UPDATE test set META_DATA = %s where ID = %s'



HASH_QUERY = 'SELECT id, dynamo_key FROM test'










