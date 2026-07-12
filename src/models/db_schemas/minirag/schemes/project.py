from .minirag_base import sqlalchemy_base
from sqlalchemy import Column, Integer,func, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Project(sqlalchemy_base):
    __tablename__ = "projects"

    project_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 , unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now() , nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now() , nullable=True)