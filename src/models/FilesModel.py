from sqlalchemy.future import select

from .DataBaseModel import DataBaseModel
from .db_schemas import File
from .enums.DataBaseEnums import DataBaseEnums
from bson.objectid import ObjectId

class FilesModel(DataBaseModel):
    def __init__(self, db_conn):
        super().__init__(db_conn)
        self.connection = db_conn

    @classmethod
    async def create_instance(cls, db_conn):
        instance = cls(db_conn)
        return instance

    async def create_file(self, file_data: File):
        async with self.connection() as session:
            async with session.begin():
                session.add(file_data)
            await session.commit()
            await session.refresh(file_data)

        return file_data
    
    async def get_all_project_files(self, file_project_id: str , file_type: str):
        async with self.connection() as session:
            async with session.begin():
                query = select(File).where(File.file_project_id == file_project_id, File.file_type == file_type)
                result = await session.execute(query)
                file_records = result.scalars().all()
        return file_records
    async def get_file_by_filename(self, file_project_id: str , file_name: str):
        async with self.connection() as session:
            async with session.begin():
                query = select(File).where(File.file_project_id == file_project_id, File.file_name == file_name)
                result = await session.execute(query)
                record = result.scalar_one_or_none()

        return record




