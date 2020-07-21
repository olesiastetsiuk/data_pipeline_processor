#Postgre configs
POSTGRES_CONFIG = {
    'user' : 'Postgres',
    'password' : 'root',
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





