import psycopg2
import pandas as pd

from configs import postgres_config
from queries import sql_queries


class DbServiceBase:

    def __init__(self):
        self.conn = psycopg2.connect(**db_config)

class DbService(DbServiceBase):
    def __init__(self):
        super().__init__()

    _styles_query = sql_queries['_styles_query']    
    
    def styles(self):
        self.styles = pd.read_sql_query(self._styles_query, self.conn)
    
    