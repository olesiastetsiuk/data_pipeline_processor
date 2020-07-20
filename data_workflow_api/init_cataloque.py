#setting up Postgre for cataloque
import psycopg2

      

# Connect to the PostgreSQL database server

postgresConnection = psycopg2.connect("dbname=test user=test password='test'")

 

# Get cursor object from the database connection

cursor = postgresConnection.cursor()

 

name_Table = "news_stories"

 

# Create table statement

sqlCreateTable = "create table "+name_Table+" (id bigint, title varchar(128), summary varchar(256), story text);"

 

# Create a table in PostgreSQL database

cursor.execute(sqlCreateTable)

postgresConnection.commit()

 

# Get the updated list of tables

sqlGetTableList = "SELECT table_schema,table_name FROM information_schema.tables where table_schema='test' ORDER BY table_schema,table_name ;"

#sqlGetTableList = "\dt"

 

# Retrieve all the rows from the cursor

cursor.execute(sqlGetTableList)

tables = cursor.fetchall()