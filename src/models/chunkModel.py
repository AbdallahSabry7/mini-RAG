from .DataBaseModel import DataBaseModel
from .db_schemas import DataChunk
from .enums.DataBaseEnums import DataBaseEnums
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(DataBaseModel):
    def __init__(self,db_conn):
        super().__init__(db_conn)
        self.connection = self.db_conn[DataBaseEnums.collection_data_chunk_name.value]

    @classmethod
    async def create_instance(cls, db_conn):
        instance = cls(db_conn)
        await instance._init_collections()
        return instance

    async def _init_collections(self):
        all_collections = await self.db_conn.list_collection_names()
        if DataBaseEnums.collection_data_chunk_name.value not in all_collections:
            self.collection =  self.db_conn[DataBaseEnums.collection_data_chunk_name.value]
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(index['key'], name=index['name'], unique=index['unique'])

    async def create_chunk(self,chunk_data:DataChunk):
        result = await self.connection.insert_one(chunk_data.dict(by_alias=True, exclude_unset=True))
        chunk_data._id = result.inserted_id
        return chunk_data
    
    async def get_chunk(self, chunk_id: str):
        record = await self.connection.find_one({"_id": ObjectId(chunk_id)})
        if record is None:
            return None
        return DataChunk(**record)
    
    async def create_chunks_bulk(self, chunks: list , batch_size: int =100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.dict(by_alias=True, exclude_unset=True)) for chunk in batch]
            await self.connection.bulk_write(operations)

        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        result = await self.connection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count
    
