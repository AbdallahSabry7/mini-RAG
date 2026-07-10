from .BaseController import BaseController
from models.db_schemas import project , DataChunk 
from stores.LLM.LLMEnums import DocumentTypeEnums

class NLPController(BaseController):

    def __init__(self, vector_db_client, generation_client, embedding_client, template_parser):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}"
    
    def reset_vector_db_collection(self, project : project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vector_db_client.delete_collection(collection_name = collection_name)
    
    def get_vector_db_collection(self, project : project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vector_db_client.get_collection_info(collection_name = collection_name)
        return collection_info
    
    def index_into_vector_db(self, project : project, data_chunks : list[DataChunk] , do_reset : bool = False , chunks_ids : list[int] = None):

        collection_name = self.create_collection_name(project_id=project.project_id)

        texts = [chunk.chunk_text for chunk in data_chunks]
        metadatas = [chunk.chunk_metadata for chunk in data_chunks]

        vectors = [
            self.embedding_client.generate_embedding(text = text , document_type = DocumentTypeEnums.RETRIEVAL_DOCUMENT.value)
            for text in texts
        ]

        self.vector_db_client.create_collection(collection_name=collection_name, embedding_size=self.embedding_client.embedding_size, do_reset=False)

        self.vector_db_client.insert_collection_batch(collection_name=collection_name, vectors=vectors, texts=texts, metadatas=metadatas, record_ids=chunks_ids)

        return True
        

    def search_vector_db(self, project : project, query_text : str, limit : int = 10):
        collection_name = self.create_collection_name(project_id=project.project_id)

        embedding_vector = self.embedding_client.generate_embedding(
            text=query_text,
            document_type=DocumentTypeEnums.RETRIEVAL_QUERY.value
        )

        if embedding_vector is None:
            self.logger.error("Failed to generate embedding for the query text.")
            return False

        search_results = self.vector_db_client.search_collection_by_vector(
            collection_name=collection_name,
            vector=embedding_vector,
            limit=limit
        )

        return search_results
    
    def generate_response(self, project : project , query : str , limit : int = 10):
        answer , full_prompt , chat_history = None , None , None
        search_results = self.search_vector_db(project=project, query_text=query, limit=limit)

        if not search_results or len(search_results) == 0:
            self.logger.error("No search results found.")
            return answer , full_prompt , chat_history

        system_prompt_template = self.template_parser.get(group="rag", key="system_prompt")
        system_prompt = system_prompt_template.substitute()

        document_prompt = "/n".join([
            self.template_parser.get(group="rag", key="document_template", vars={"index": idx, "content": result.text, "score": result.score})
            for idx, result in enumerate(search_results)
        ])

        footer_prompt = self.template_parser.get(group="rag", key="footer_template")
        footer_prompt = footer_prompt.substitute()

        chat_history = [self.generation_client.construct_prompt(prompt=system_prompt, role=self.generation_client.enums.SYSTEM.value)]

        full_prompt = "/n/n".join([
            document_prompt,
            footer_prompt
        ])

        answer = self.generation_client.generate_text(prompt=full_prompt, chat_history=chat_history)

        return answer , full_prompt , chat_history



