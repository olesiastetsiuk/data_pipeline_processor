#AWS configs
# AWS S3 bucket name
AWS_BUCKET_NAME = 'S3'
# AWS DynamoDB table name
AWS_TABLE_NAME = 'fashion_images'
# Path for temporary storage
STORAGE_PATH = './data/'
# Path for storage uploaded files
UPLOAD_PATH = STORAGE_PATH + '/upload/'
# Path for storage downloaded files
DOWNLOAD_PATH = STORAGE_PATH + '/download/'

DATASET_PATH = {
    'styles.csv': STORAGE_PATH + '/fashion_dataset/styles.csv', 
    'images': STORAGE_PATH+ '/fashion_dataset/images/',
    'meta_files': STORAGE_PATH+ '/fashion_dataset/styles/'
}

#Postgre configs
POSTGRES_CONFIG = {
    'user' : 'Postgres',
    'password' : '',
    'host' : 'localhost',
    'dbname' : 'postgres_db'
}

TABLE_NAME = 'styles'

TABLE_QUERY = '''CREATE TABLE styles
          (ID INT PRIMARY KEY     NOT NULL,
          GENDER           TEXT    NOT NULL,
          MASTERCATEGORY           TEXT    NOT NULL,
          SUBCATEGORY           TEXT    NOT NULL,
          ARTICLETYPE           TEXT    NOT NULL,
          SEASON           TEXT    NOT NULL,
          YEAR           INT    NOT NULL,
          USAGE           TEXT    NOT NULL,
          PRODUCTDISPLAYNAME           TEXT    NOT NULL,
          DYNAMO_KEY           TEXT FOREIGN KEY  NOT NULL DEFAULT 'hash'); '''

INSERT_QUERY = 'INSERT INTO styles VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

HASH_QUERY = 'SELECT id, dynamo_key FROM styles'







