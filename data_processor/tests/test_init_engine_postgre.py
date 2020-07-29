import sys
sys.path.insert(0,'/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/data_processor/')

import pytest

import testing.postgresql
import psycopg2

from data_workflow_api.init_engine_postgre import DbServiceConnect, TableStyles
from data_workflow_api.configs import POSTGRE_TABLE_NAME, CREATE_TABLE_QUERY, CVS_ROW_INSERT_QUERY, TABLES_NAMES_LIST_QUERY



with testing.postgresql.Postgresql() as postgresql:
    db = DbServiceConnect(postgresql.dsn()) 
    
    with TableStyles(db) as table:
        tables = table.list_tables(TABLES_NAMES_LIST_QUERY)
        assert (tables == [])

        table.create_table(CREATE_TABLE_QUERY, POSTGRE_TABLE_NAME)
        updated_tables = table.list_tables(TABLES_NAMES_LIST_QUERY)
        assert (POSTGRE_TABLE_NAME in updated_tables[0])
        
        table.update_table_records(CVS_ROW_INSERT_QUERY, ('id','gender','masterCategory','subCategory','articleType','baseColour','season',2000,'usage','productDisplayName'))
        records = table.query_table_all("SELECT * FROM test;")
        assert (records==[('id', 'gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 2000, 'usage', 'productDisplayName', None, None)])

#TODO add test to all methods from TableStyles


    
   
    

