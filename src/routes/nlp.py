from fastapi import Depends, FastAPI , APIRouter ,UploadFile , status , Request
from fastapi.responses import JSONResponse
import os
from models.projectModel import ProjectModel
from models.chunkModel import ChunkModel
from helpers.config import get_settings, Settings
from controllers import NLPController 
nlp_router = APIRouter(
    prefix = "/api/v1/nlp",
    tags = ['api_v1','nlp']
)

@nlp_router.post("/index/push/{project_id}")
async def push_index(req: Request, project_id: str, project : ProjectModel):

    project_model = await ProjectModel.create_instance(
        db_conn=req.app.state.mongodb_database
    )

    project = await project_model.get_project_or_create(project_id=project_id)

    data_chunk_model = await ChunkModel.create_instance(
        db_conn=req.app.state.mongodb_database
    )
    data_chunks = await data_chunk_model.get_data_chunks_by_project_id(project_id=project_id , page=1, page_size=50)

    nlp_controller = NLPController(
        vector_db_client=req.app.state.vector_db_client,
        generation_client=req.app.state.generation_client,
        embedding_client=req.app.state.embedding_client
    )



