#AWS configs
# AWS S3 bucket name
AWS_BUCKET_NAME = 'fashionstyles'
# AWS DynamoDB table name
AWS_TABLE_NAME = 'fashionstyles'
# Path for temporary storage
STORAGE_PATH = '/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/data/'
# Path for storage uploaded files
UPLOAD_PATH = STORAGE_PATH + '/upload/'
# Path for storage downloaded files
DOWNLOAD_PATH = STORAGE_PATH + '/download/'

# DATASET_PATH = {
#     'styles.csv': STORAGE_PATH + 'fashion_dataset/styles_sample.csv', 
#     'images': STORAGE_PATH+ 'fashion_dataset/images/',
#     'meta_files': STORAGE_PATH+ 'fashion_dataset/styles/'
# }

DATASET_PATH = {
    'styles': STORAGE_PATH + 'fashion_dataset/styles_sample.csv', 
    'images': '/home/olysavra/datasqueezer/IM/139630_329006_bundle_archive/'+ 'fashion_dataset/images/',
    'meta_files': '/home/olysavra/datasqueezer/IM/139630_329006_bundle_archive/' + 'fashion_dataset/styles/'
}

#Postgre configs
POSTGRES_CONFIG = {
    'user' : 'postgres',
    'password' : 98052,
    'host' : 'localhost',
    'dbname' : 'im',
    'port': 5432
}

POSTGRE_TABLE_NAME = 'test'

#id,gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName

CREATE_TABLE_QUERY = '''CREATE TABLE test
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

TABLES_NAMES_LIST_QUERY = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""

CVS_ROW_INSERT_QUERY = "INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(POSTGRE_TABLE_NAME)

BULK_CVS_UPDATE = "COPY {} (id,gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName) FROM %s DELIMITER ','CSV HEADER;".format(POSTGRE_TABLE_NAME)

SELECT_META_HASH_ID_QUERY = "select id, meta_data, hash_key from {}".format(POSTGRE_TABLE_NAME)

META_DATA_HASH_KEY_UPDATE_QUERY = "Update {} set meta_data = %s, hash_key = %s where id = %s".format(POSTGRE_TABLE_NAME)

CREATE_HASH_INDEX_QUERY = "CREATE INDEX dynamo_hash_key ON {} USING hash (HASH_KEY);".format(POSTGRE_TABLE_NAME)

HASH_QUERY = "SELECT id, HASH_KEY FROM {}".format(POSTGRE_TABLE_NAME)










