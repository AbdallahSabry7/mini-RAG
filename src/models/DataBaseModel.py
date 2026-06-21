from helpers.config import get_settings

class DataBaseModel:
    def __init__(self,db_conn):
        self.db_conn = db_conn
        self.settings = get_settings()