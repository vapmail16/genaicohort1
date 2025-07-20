from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
from typing import List, Dict, Any, Optional
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from config import QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, QDRANT_URL, COLLECTION_NAME, is_cloud_qdrant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleVectorStore:
    def __init__(self):
        """Initialize the vector store with Qdrant client and simple TF-IDF embedding."""
        if is_cloud_qdrant():
            # Use cloud connection (no :6333)
            self.client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY
            )
        else:
            # Use local connection
            self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        
        self.collection_name = COLLECTION_NAME
        self.vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
        self.documents = []
        self.embeddings = None
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
                        size=384,  # Fixed size for TF-IDF vectors to match existing collection
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    def _text_to_vector(self, text: str) -> List[float]:
        """Convert text to vector using TF-IDF."""
        try:
            # Fit vectorizer if not already fitted
            if not hasattr(self.vectorizer, 'vocabulary_'):
                self.vectorizer.fit([text])
            
            # Transform text to vector
            vector = self.vectorizer.transform([text]).toarray()[0]
            
            # Pad or truncate to 384 dimensions
            if len(vector) < 384:
                vector = np.pad(vector, (0, 384 - len(vector)), 'constant')
            elif len(vector) > 384:
                vector = vector[:384]
            
            return vector.tolist()
        except Exception as e:
            logger.error(f"Error converting text to vector: {e}")
            # Return zero vector as fallback
            return [0.0] * 384
    
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
        embeddings = [self._text_to_vector(text) for text in texts]
        
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
    
    def search(self, query: str, limit: int = 5, score_threshold: float = 0.1) -> List[Dict[str, Any]]:
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
        query_embedding = self._text_to_vector(query)
        
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
            # Return basic info without the problematic fields
            return {
                'name': self.collection_name,
                'status': 'active',
                'note': 'Collection info retrieval failed due to version compatibility'
            } 