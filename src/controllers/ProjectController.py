from .BaseController import BaseController
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_file_path(self, project_id: int):
        self.project_folder = os.path.join(self.folder_path, str(project_id))
        if not os.path.exists(self.project_folder):
            os.makedirs(self.project_folder)
        
        return self.project_folder