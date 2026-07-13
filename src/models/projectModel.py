
from .DataBaseModel import DataBaseModel
from .db_schemas import Project
from .enums.DataBaseEnums import DataBaseEnums
from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(DataBaseModel):
    def __init__(self,db_conn):
        super().__init__(db_conn)
        self.connection = db_conn

    @classmethod
    async def create_instance(cls, db_conn):
        instance = cls(db_conn)
        return instance

    async def create_project(self,project_data:Project):
        async with self.connection() as session:
            async with session.begin():
                session.add(project_data)
            await session.commit()
            await session.refresh(project_data)

        return project_data
    
    async def get_project_or_create(self, project_id: str):
        async with self.connection() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project_record = result.scalar_one_or_none()

        if project_record is None:
            new_project = Project(project_id=project_id)
            return await self.create_project(new_project)
        

        return project_record

    async def get_all_projects(self,page: int =1 , page_size: int = 10):
        async with self.connection() as session:
            async with session.begin():
                total_records = await session.execute(select(func.count(Project.project_id)))

                total_records_count = total_records.scalar_one()
                total_pages = total_records_count // page_size
                if total_records_count % page_size > 0:
                    total_pages += 1

                query = select(Project).offset((page - 1) * page_size).limit(page_size)
                results = await session.execute(query).scalars().all()

            return results

