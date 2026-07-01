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

    def generate_random_string(self, length: int = 8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        

