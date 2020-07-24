import psycopg2
import csv

from configs import POSTGRES_CONFIG, TABLE_NAME, TABLE_QUERY, DATASET_PATH, CVS_ROW_INSERT_QUERY


class DbServiceConnect:
    def __init__(self, postgres_config):
        self.conn = psycopg2.connect(**postgres_config)    

class TableBase:
    def __init__(self, dbservice):
        self.conn = dbservice.conn
    
    @property
    def cursor(self):
        return self.conn.cursor()
    
    def __enter__(self):
        self.startup()
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
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
    def __init__(self, db_service):
        super().__init__(db_service)
    
    def create_table(self, table_query, table_name):
        try:

            self.cursor.execute(table_query)
            self.conn.commit()            
            print("Table '{}'created successfully in PostgreSQL.".format(table_name))

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)
        
    def update_table_from_cvs_by_row(self, csv_path, insert_query):
        try:

            with open(csv_path, 'r') as data:
                reader = csv.reader(data)
                next(reader)
                count = 0
                for row in reader:
                    self.cursor.execute(
                    insert_query,
                    row
                )
                    self.conn.commit()
                    count += 1 

                print("'{}' records updated successfully ".format(count))

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while csv update by row PostgreSQL table", error)
        
    def bulk_cvs_update_table(self, csv_path, table_name):
        try:
            with open(csv_path, 'r') as data: 
                reader = csv.reader(data)
                next(reader)
                self.cursor.copy_from(data, table_name, sep=',', size=8192)
                self.conn.commit()            

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while csv bulk update PostgreSQL table", error)
    
    def query_table(self, query):
        records = None
        try:
            self.cursor.execute(query)
            records = self.cursor.fetchall() #fetchone(), fetchmany(SIZE) 
            print("Query '{}' successfully executed in PostgreSQL.".format(query))

        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while fetching data from PostgreSQL", error)
        return records
    
    def update_table_records(self, update_query, *args): #last arg image id
        try:
            self.cursor.execute(update_query, args)
            self.conn.commit()
            count = self.cursor.rowcount
            print("'{}'records updated successfully ".format(count))

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

if __name__ == "__main__":
    db_service = DbServiceConnect(POSTGRES_CONFIG)    
    with TableStyles(db_service) as table:
        table.create_table(TABLE_QUERY, TABLE_NAME)






                    




 

