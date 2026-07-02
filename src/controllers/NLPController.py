from .BaseController import BaseController
from models.db_schemas import project , DataChunk 
from stores.LLM.LLMEnums import DocumentTypeEnums

class NLPController(BaseController):

    def __init__(self, vector_db_client, generation_client, embedding_client):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}"
    
    def reset_vector_db_collection(self, project : project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vector_db_client.delete_collection(collection_name = collection_name)
    
    def get_vector_db_collection(self, project : project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vector_db_client.get_collection_info(collection_name = collection_name)
        return collection_info
    def index_into_vector_db(self, project : project, data_chunks : list[DataChunk]):

        collection_name = self.create_collection_name(project_id=project.project_id)

        texts = [chunk.chunk_text for chunk in data_chunks]
        metadatas = [chunk.chunk_metadata for chunk in data_chunks]

        vectors = [
            self.generate_embedding(text = text , document_type = DocumentTypeEnums.DOCUMENT.value)
            for text in texts
        ]

        self.vector_db_client.create_collection(collection_name=collection_name, embedding_size=self.embedding_client.embedding_size, do_reset=False)

        self.vector_db_client.insert_collection_batch(collection_name=collection_name, vectors=vectors, texts=texts, metadata=metadatas, do_reset=False)

        return True
        

