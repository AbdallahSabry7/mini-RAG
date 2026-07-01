from helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.dir_path = os.path.dirname(os.path.dirname(__file__))
        self.folder_path = os.path.join(
            self.dir_path,
            'assets/data'
        )

        self.database_path = os.path.join(
            self.dir_path,
            'assets/database'
        )

    def generate_random_string(self, length: int = 8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def get_database_path(self, db_name: str = None):
        database_path = os.path.join(
            self.database_path, db_name
        )
        if not os.path.exists(database_path):
            os.makedirs(database_path, exist_ok=True)
            
        return database_path


