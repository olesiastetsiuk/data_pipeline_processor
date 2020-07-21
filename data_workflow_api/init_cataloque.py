import psycopg2

from data_pipeline_processor.configs.postgres_config import POSTGRES_CONFIG, TABLE_NAME, TABLE_QUERY


class DbServiceBase:

    def __init__(self):
        self.conn = psycopg2.connect(**postgres_config)
    

class TableBase:

    self __init__(self, conn):
        self._conn = conn
    
    @property
    def cursor(self):
        return self._conn.cursor()
    
    @property
    def table_name(self, name):
        return name
    
     def __enter__(self):
        self.startup()
        return self
    
    def __exit__(self):
        self.shutdown()
    
    def startup(self):
        print(self._conn.get_dsn_parameters(),"\n")
    
    def shutdown(self):
        self.cursor.close()
        self._conn.close()
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
    
    def create_table(self, table_query):

        try:
            cursor.execute(table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)


                    




 

