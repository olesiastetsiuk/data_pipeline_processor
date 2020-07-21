import psycopg2
import csv

from configs import POSTGRES_CONFIG, TABLE_NAME, TABLE_QUERY


class DbServiceBase:
    def __init__(self, postgres_config):
        self.conn = psycopg2.connect(**postgres_config)    

class TableBase:
    def __init__(self, dbservice):
        self.conn = dbservice.conn
    
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
    
    # def tables(self): #check if table name exists
    #     pass
    
    def create_table(self, table_query):
        try:

            self.cursor.execute(table_query)
            self.conn.commit()            
            print("Table '{}'created successfully in PostgreSQL.".format(self.table_name))

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

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error bulk update PostgreSQL table", error)
    
    def table_query(self, query):
        self.conn.execute(query)
        pass

    # def table_update(self,):
    #     pass

if __name__ == "__main__":
    db_service = DbServiceBase(POSTGRES_CONFIG)
    with TableStyles(db_service) as table:
        tabel_name = table.table_name(TABLE_NAME)
        table.create_table(TABLE_QUERY)






                    




 

