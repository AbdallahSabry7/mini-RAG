from qdrant_client import models , QdrantClient
from ..VectorDBEnums import VectorDBType , DistanceMetric
from ..VectorDBInterface import VectorDBInterface
import logging
from typing import List

class QDrantDB(VectorDBInterface):
    def __init__(self, db_path : str , distance_metric : str):

        self.client = None
        self.db_path = db_path
        self.distance_metric = None

        if distance_metric.lower() == DistanceMetric.COSINE.value:
            self.distance_metric = models.Distance.COSINE
        elif distance_metric.lower() == DistanceMetric.EUCLIDEAN.value:
            self.distance_metric = models.Distance.EUCLIDEAN
        elif distance_metric.lower() == DistanceMetric.DOT.value:
            self.distance_metric = models.Distance.DOT
        else:
            raise ValueError(f"Invalid distance metric: {distance_metric}. Supported metrics are: {', '.join([metric.value for metric in DistanceMetric])}")

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        if self.client:
            self.client = None


    def is_collection_exists(self, collection_name:str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    
    def list_all_collections(self, collection_name: str) -> List:
        return self.client.get_collections(collection_name=collection_name)
    
    
    def delete_collection(self, collection_name:str):
        if self.is_collection_exists(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        else:
            self.logger.warning(f"Collection '{collection_name}' does not exist. Cannot delete.")


    def create_collection(self, collection_name:str, embedding_size:int, do_reset:bool = False):
        if do_reset and self.is_collection_exists(collection_name):
            _ = self.delete_collection(collection_name)
        if not self.is_collection_exists(collection_name):
            _ = self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=embedding_size,
                        distance=self.distance_metric
                    )
                )
            return True
        else:
            self.logger.warning(f"Collection '{collection_name}' already exists. Skipping creation.")
            return False
    