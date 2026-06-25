from .DataBaseModel import DataBaseModel
from .db_schemas import project
from .enums.DataBaseEnums import DataBaseEnums

class ProjectModel(DataBaseModel):
    def __init__(self,db_conn):
        super().__init__(db_conn)
        self.connection = self.db_conn[DataBaseEnums.Collection_project_name.value]

    @classmethod
    async def create_instance(cls, db_conn):
        instance = cls(db_conn)
        await instance._init_collections()
        return instance
    
    async def _init_collections(self):
        all_collections = await self.db_conn.list_collection_names()
        if DataBaseEnums.Collection_project_name.value not in all_collections:
            self.collection = self.db_conn[DataBaseEnums.Collection_project_name.value]
            indexes = project.get_indexes()
            for index in indexes:
                await self.collection.create_index(index['key'], name=index['name'], unique=index['unique'])

    async def create_project(self,project_data:project):
        result = await self.connection.insert_one(project_data.dict(by_alias=True, exclude_unset=True))
        project_data.id = result.inserted_id
        return project_data
    
    async def get_project_or_create(self, project_id: str):
        record = await self.connection.find_one({"project_id": project_id})

        if record is None:
            new_project = project(project_id=project_id)

            result = await self.connection.insert_one(
                new_project.model_dump(by_alias=True, exclude_unset=True)
            )

            new_project.id = result.inserted_id
            return new_project

        return project(**record)
    
    async def get_all_projects(self,page: int =1 , page_size: int = 10):
        total_records = await self.connection.count_documents({})
        total_pages = total_records // page_size
        if total_records % page_size > 0:
            total_pages += 1

        cursor = self.connection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for record in cursor:
            projects.append(project(**record))

        return projects, total_pages

