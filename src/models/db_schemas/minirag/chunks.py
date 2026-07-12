from .minirag_base import sqlalchemy_base
from sqlalchemy import Column, Integer,func, DateTime , String , ForeignKey
from sqlalchemy.dialects.postgresql import UUID , JSONB
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Index
from pydantic import BaseModel

class DataChunk(sqlalchemy_base):
    __tablename__ = "data_chunks"

    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 , unique=True, nullable=False)
    chunk_text = Column(String, nullable=False)
    chunk_metadata = Column(JSONB, nullable=False, default={})
    chunk_order = Column(Integer, nullable=False)
    chunk_project_id = Column(UUID(as_uuid=True), ForeignKey("projects.project_id"), nullable=False)
    chunk_file_id = Column(UUID(as_uuid=True), ForeignKey("files.file_uuid"), nullable=False)

    project = relationship("Project", back_populates="data_chunks")
    file = relationship("File", back_populates="data_chunks")

    created_at = Column(DateTime(timezone=True), server_default=func.now() , nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now() , nullable=True)

    __table_args__ = (
        Index('chunk_project_id_index', 'chunk_project_id'),
        Index('chunk_file_id_index', 'chunk_file_id'),
    )


class retrievedchunk(BaseModel):
    text : str
    score : float