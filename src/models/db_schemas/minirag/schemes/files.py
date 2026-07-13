from .minirag_base import sqlalchemy_base
from sqlalchemy import Column, Integer,func, DateTime , String , ForeignKey
from sqlalchemy.dialects.postgresql import UUID , JSONB
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Index

class File(sqlalchemy_base):
    __tablename__ = "files"

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4 , unique=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_config = Column(JSONB, nullable=True, default={})

    file_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    project = relationship("Project", back_populates="files")
    data_chunks = relationship("DataChunk", back_populates="file", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now() , nullable=False)

    __table_args__ = (
        Index('file_project_id_index', 'file_project_id'),
        Index('file_project_id_file_name_index', 'file_project_id', 'file_name', unique=True),
    )
