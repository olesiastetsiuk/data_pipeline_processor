import psycopg2
import pandas as pd

from data_pipeline_processor.data_workflow_api.init_cataloque import DbServiceBase
from queries import sql_queries


class DbService(DbServiceBase):
    def __init__(self):
        super().__init__()

    _styles_query = sql_queries['_styles_query']    
    
    def styles(self):
        self.styles = pd.read_sql_query(self._styles_query, self.conn)
    
    