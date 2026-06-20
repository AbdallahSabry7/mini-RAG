from helpers.config import get_settings, Settings
import os


class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.folder_path = os.path.join(
            self.dir_path,
            'assets/data'
        )

        

