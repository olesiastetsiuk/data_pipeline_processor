import psycopg2
import csv

from data_pipeline_processor.configs.postgres_config import POSTGRES_CONFIG, TABLE_NAME, TABLE_QUERY, INSERT_QUERY


class DbServiceBase:

    def __init__(self):
        self.conn = psycopg2.connect(**postgres_config)    

class TableBase(DbServiceBase):
    def __init__(self):
        super().__init__()
    
    @property
    def cursor(self):
        return self.conn.cursor()
    
    @property
    def table_name(self, name):
        return name
    
     def __enter__(self):
        self.startup()
        return self
    
    def __exit__(self):
        self.shutdown()
    
    def startup(self):
        print(self.conn.get_dsn_parameters(),"\n")
    
    def shutdown(self):
        self.cursor.close()
        self.conn.close()
        print("PostgreSQL connection is closed")

    def create_table(self, table_query):
        pass 


class TableStyles(TableBase):

    def __init__(self):
        super().__init__()    

    @property
    def table_name(self, name):
        return name
    
    @property
    def cursor(self):
        return self._conn.cursor()
    
    def tables(self): #check if table name exists
        pass
    
    def create_table(self, table_query):

        try:
            self.cursor.execute(table_query)
            self.conn.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)
        
    def bulk_update(self, csv_path, insert_query):
        try:
            with open(csv_path, 'r') as data:
            reader = csv.reader(data)
            next(reader) 
            for row in reader:
                self.cursor.execute(
                insert_query,
                row
            )
            self.conn.commit()




                    




 

