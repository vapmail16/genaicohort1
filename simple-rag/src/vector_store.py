from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
from typing import List, Dict, Any, Optional
import logging
from config import QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL, is_cloud_qdrant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        """Initialize the vector store with Qdrant client and embedding model."""
        if is_cloud_qdrant():
            # Use cloud connection (no :6333)
            self.client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY
            )
        else:
            # Use local connection
            self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.collection_name = COLLECTION_NAME
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create the collection if it doesn't exist."""
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_model.get_sentence_embedding_dimension(),
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents with 'text' and optional 'metadata' keys
            
        Returns:
            List of document IDs
        """
        if not documents:
            return []
        
        # Extract texts and create embeddings
        texts = [doc['text'] for doc in documents]
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Prepare points for insertion
        points = []
        doc_ids = []
        
        for i, doc in enumerate(documents):
            doc_id = str(uuid.uuid4())
            doc_ids.append(doc_id)
            
            point = PointStruct(
                id=doc_id,
                vector=embeddings[i],
                payload={
                    'text': doc['text'],
                    'metadata': doc.get('metadata', {}),
                    'source': doc.get('source', 'unknown')
                }
            )
            points.append(point)
        
        # Insert points into collection
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Successfully added {len(documents)} documents to vector store")
            return doc_ids
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def search(self, query: str, limit: int = 5, score_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query text
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score threshold
            
        Returns:
            List of similar documents with scores
        """
        # Create query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        try:
            # Search in collection
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    'id': result.id,
                    'score': result.score,
                    'text': result.payload['text'],
                    'metadata': result.payload.get('metadata', {}),
                    'source': result.payload.get('source', 'unknown')
                })
            
            logger.info(f"Found {len(results)} similar documents for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            raise
    
    def delete_collection(self):
        """Delete the collection (use with caution)."""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Collection {self.collection_name} deleted successfully")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            collection_info = self.client.get_collection(collection_name=self.collection_name)
            return {
                'name': self.collection_name,
                'vectors_count': collection_info.vectors_count,
                'points_count': collection_info.points_count,
                'status': collection_info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise 