from enum import Enum

class VectorDBType(str, Enum):
    QDrant = "QDrant"

class DistanceMetric(str, Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"