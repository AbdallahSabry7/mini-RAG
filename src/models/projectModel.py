from .DataBaseModel import DataBaseModel
from .db_schemas import ProjectSchema
from .enums.DataBaseEnums import DataBaseEnums

class ProjectModel(DataBaseModel):
    def __init__(self,db_conn):
        super().__init__(db_conn)
        self.connection = self.db_conn[DataBaseEnums.Collection_project_name.value]

    async def create_project(self,project_data:ProjectSchema):
        result = await self.connection.insert_one(project_data.dict())
        return result.inserted_id
    
    async def get_project_or_create(self,project_id:str):

        record = await self.connection.find_one({"project_id": project_id})
        if record is None:
            new_project = ProjectSchema(project_id=project_id)
            new_project = await self.create_project(new_project)
            return new_project
        
        return ProjectSchema(**record)
    
    async def get_all_projects(self,page: int =1 , page_size: int = 10):
        total_records = await self.connection.count_documents({})
        total_pages = total_records // page_size
        if total_records % page_size > 0:
            total_pages += 1

        cursor = self.connection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for record in cursor:
            projects.append(ProjectSchema(**record))

        return projects, total_pages

