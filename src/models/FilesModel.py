from .DataBaseModel import DataBaseModel
from .db_schemas import FileSchema
from .enums.DataBaseEnums import DataBaseEnums
from bson.objectid import ObjectId

class FilesModel(DataBaseModel):
    def __init__(self, db_conn):
        super().__init__(db_conn)
        self.connection = self.db_conn[DataBaseEnums.collection_file_name.value]

    @classmethod
    async def create_instance(cls, db_conn):
        instance = cls(db_conn)
        await instance._init_collections()
        return instance

    async def _init_collections(self):
        all_collections = await self.db_conn.list_collection_names()
        if DataBaseEnums.collection_file_name.value not in all_collections:
            self.collection = self.db_conn[DataBaseEnums.collection_file_name.value]
            indexes = FileSchema.get_indexes()
            for index in indexes:
                await self.collection.create_index(index['key'], name=index['name'], unique=index['unique'])

    async def create_file(self, file_data: FileSchema):
        result = await self.connection.insert_one(file_data.dict(by_alias=True, exclude_unset=True))
        file_data.id = result.inserted_id
        return file_data
    
    async def get_all_project_files(self, file_project_id: str , file_type: str):
        records = await self.connection.find({"file_project_id": ObjectId(file_project_id) if file_project_id is str else file_project_id,
                                        "file_type": file_type
                                        }, ).to_list(length=None)
        
        return [FileSchema(**record) for record in records]
    
    async def get_file_by_filename(self, file_project_id: str , file_name: str):
        record = await self.connection.find_one({"file_project_id": ObjectId(file_project_id) if file_project_id is str else file_project_id,
                                        "file_name": file_name
                                        })
        
        if record is None:
            return None
        
        return FileSchema(**record)



