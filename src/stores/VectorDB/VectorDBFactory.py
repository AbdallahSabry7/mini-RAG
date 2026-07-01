from VectorDBProviders import QDrantDB
from VectorDBEnums import VectorDBType, DistanceMetric
from controllers.BaseController import BaseController

class VectorDBFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    def create_vector_db(self, provider_name: str):
        if provider_name == VectorDBType.QDRANT.value:
            db_path = self.base_controller.get_database_path(self.config.VECTOR_DB_PATH)
            return QDrantDB(db_path, self.config.VECTOR_DB_DISTANCE_METRIC)
        else:
            return None