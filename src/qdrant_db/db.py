import logging

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

logger = logging.getLogger(__name__)

class Qdrant:
    QDRANT_PATH = "./qdrant_data"
    COLLECTION_NAME = "medical_texts_local"

    def __init__(self):
        #self.client = QdrantClient(path=self.QDRANT_PATH) локально
        self.client = QdrantClient(host="qdrant", port=6333, prefer_grpc=True)
        self.get_client()
        logging.info("Qdrant client connected")

    def get_client(self):
        try:
            self.client.get_collection(self.COLLECTION_NAME)
        except Exception:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=768,  # BioBERT размерность
                    distance=Distance.COSINE
                ),
                optimizers_config={"memmap_threshold": 10000}  # Оптимизация памяти
            )

    def validate(self):
        if not isinstance(self.client, QdrantClient):
            raise TypeError('Qdrant client is not initialized')

        if not hasattr(self.client, 'upsert'):
            raise AttributeError('Qdrant not have upsert')

        logging.info("Qdrant client is initialized and validated")
