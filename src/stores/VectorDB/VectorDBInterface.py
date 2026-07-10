from abc import ABC, abstractmethod
from typing import List
from models.db_schemas import retrievedchunk

class VectorDBInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name:str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self):
        pass

    @abstractmethod
    def get_collection_info(self, collection_name:str) -> dict:
        pass

    @abstractmethod
    def create_collection(self, collection_name:str, embedding_size:int, do_reset:bool = False):
        pass

    @abstractmethod
    def delete_collection(self, collection_name:str):
        pass

    @abstractmethod
    def insert_collection(self, collection_name:str, text:str, vector:list, metadata:dict = None, record_id:str = None):
        pass

    @abstractmethod
    def insert_collection_batch(self, collection_name:str, texts:list, vectors:list, metadatas:list = None, record_ids:list = None, batch_size:int = 100):
        pass

    @abstractmethod
    def search_collection_by_vector(self, collection_name:str , vector:list , limit:int = 10) -> List[retrievedchunk]:
        pass

