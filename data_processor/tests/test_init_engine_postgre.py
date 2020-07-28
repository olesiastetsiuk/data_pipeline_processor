import sys
sys.path.insert(0,'/home/olysavra/datasqueezer/data_pipeline/data_pipeline_processor/data_processor/')

import pytest

import testing.postgresql
import psycopg2

from data_workflow_api.init_engine_postgre import DbServiceConnect, TableStyles
from data_workflow_api.configs import POSTGRE_TABLE_NAME, CREATE_TABLE_QUERY, CVS_ROW_INSERT_QUERY



with testing.postgresql.Postgresql() as postgresql:
    db = DbServiceConnect(postgresql.dsn()) 
    
    with TableStyles(db) as table:
        table.create_table(CREATE_TABLE_QUERY, POSTGRE_TABLE_NAME)
        table.update_table_records(CVS_ROW_INSERT_QUERY, ('id','gender','masterCategory','subCategory','articleType','baseColour','season',2000,'usage','productDisplayName'))
        records = table.query_table_all("SELECT * FROM test;")
        assert (records==[('id', 'gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 2000, 'usage', 'productDisplayName', None, None)])



    
   
    

