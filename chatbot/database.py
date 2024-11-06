from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class VectorDatabase:
    def __init__(self):
        self.client = QdrantClient("qdrant", port=6333)
        self.collection_name = "chatbot_knowledge"
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
      collections = self.client.get_collections().collections
      if not any(collection.name == "chatbot_memory" for collection in collections):
          self.client.create_collection(
              collection_name="chatbot_memory",
              vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
          )

    def store_embedding(self, text, embedding):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[{"id": hash(text), "vector": embedding, "payload": {"text": text}}],
        )

    def search_similar(self, query_embedding, limit=5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
        )
        return [hit.payload["text"] for hit in results]
