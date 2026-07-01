from .BaseController import BaseController
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_file_path(self, project_id: str):
        self.project_folder = os.path.join(self.folder_path, project_id)
        if not os.path.exists(self.project_folder):
            os.makedirs(self.project_folder)
        
        return self.project_folder