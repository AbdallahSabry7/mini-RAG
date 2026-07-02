from fastapi import Depends, FastAPI , APIRouter ,UploadFile , status , Request
from fastapi.responses import JSONResponse
import os
from models.enums import ResponseEnums
from models.projectModel import ProjectModel
from models.chunkModel import ChunkModel
from helpers.config import get_settings, Settings
from controllers import NLPController 
from .schemas import NLPRequest
from models.enums.ResponseEnums import ResponseStatus
nlp_router = APIRouter(
    prefix = "/api/v1/nlp",
    tags = ['api_v1','nlp']
)

@nlp_router.post("/index/push/{project_id}")
async def push_index(req: Request, project_id: str, push_request: NLPRequest):

    project_model = await ProjectModel.create_instance(
        db_conn=req.app.state.mongodb_database
    )

    project = await project_model.get_project_or_create(project_id=project_id)

    data_chunk_model = await ChunkModel.create_instance(
        db_conn=req.app.state.mongodb_database
    )

    nlp_controller = NLPController(
    vector_db_client=req.app.state.vector_db_client,
    generation_client=req.app.state.generation_client,
    embedding_client=req.app.state.embedding_client
    )

    has_records = True
    page_no = 1
    page_size = 50
    idx = 0
    inserted_count = 0
    while has_records:
        data_chunks = await data_chunk_model.get_data_chunks_by_project_id(project_id=project.id, page= page_no, page_size= page_size)
        
        if len(data_chunks):
            page_no += 1

        if len(data_chunks) == 0 or not data_chunks:
            has_records = False
            break

        chunks_ids = list(range(idx, idx + len(data_chunks)))
        idx += len(data_chunks)

        is_inserted = nlp_controller.index_into_vector_db(project=project, data_chunks=data_chunks, chunks_ids=chunks_ids,do_reset=push_request.do_reset)

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"signal": ResponseStatus.FAILED_TO_INSERT_CHUNKS.value}
            )
        
        inserted_count += len(data_chunks)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"signal": ResponseStatus.SUCCESSFULLY_INSERTED_CHUNKS.value, "inserted_count": inserted_count}
    )



