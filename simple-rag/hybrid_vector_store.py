from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
from typing import List, Dict, Any, Optional
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from config import QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, QDRANT_URL, COLLECTION_NAME, is_cloud_qdrant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridVectorStore:
    def __init__(self):
        """Initialize the hybrid vector store with Qdrant client and TF-IDF for keyword search."""
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
        self.tfidf_matrix = None
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
                        size=384,  # Fixed size for TF-IDF vectors
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
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query."""
        words = re.findall(r'\b\w+\b', query.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    def _keyword_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Perform keyword-based search using TF-IDF."""
        if not self.documents:
            return []
        
        # Extract keywords
        keywords = self._extract_keywords(query)
        
        # Calculate keyword-based scores
        keyword_scores = []
        for i, doc in enumerate(self.documents):
            doc_text = doc['text'].lower()
            
            # Calculate keyword overlap
            matched_keywords = [kw for kw in keywords if kw in doc_text]
            keyword_overlap = len(matched_keywords) / len(keywords) if keywords else 0
            
            # Calculate keyword frequency score
            keyword_freq_score = 0
            for keyword in keywords:
                keyword_freq_score += doc_text.count(keyword)
            
            # Normalize keyword frequency
            if keyword_freq_score > 0:
                keyword_freq_score = min(keyword_freq_score / 10, 1.0)  # Cap at 1.0
            
            # Combined keyword score
            keyword_score = (0.7 * keyword_overlap) + (0.3 * keyword_freq_score)
            
            if keyword_score > 0:
                keyword_scores.append({
                    'id': i,
                    'score': keyword_score,
                    'text': doc['text'],
                    'metadata': doc.get('metadata', {}),
                    'source': doc.get('source', 'unknown'),
                    'matched_keywords': matched_keywords
                })
        
        # Sort by keyword score
        keyword_scores.sort(key=lambda x: x['score'], reverse=True)
        return keyword_scores[:limit]
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Add documents to the vector store."""
        if not documents:
            return []
        
        # Store documents for keyword search
        self.documents = documents
        
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
                    'source': doc.get('source', 'unknown'),
                    'doc_index': i  # Store document index for hybrid search
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
        """Perform vector search (original functionality)."""
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
    
    def hybrid_search(self, query: str, limit: int = 5, 
                     vector_weight: float = 0.6, keyword_weight: float = 0.4) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining vector and keyword search.
        
        Args:
            query: Search query
            limit: Number of results to return
            vector_weight: Weight for vector similarity scores (0.0-1.0)
            keyword_weight: Weight for keyword search scores (0.0-1.0)
        """
        # Get vector search results
        vector_results = self.search(query, limit * 2, score_threshold=0.05)
        
        # Get keyword search results
        keyword_results = self._keyword_search(query, limit * 2)
        
        # Create mappings for easy lookup
        vector_scores = {result['id']: result['score'] for result in vector_results}
        keyword_scores = {result['id']: result['score'] for result in keyword_results}
        
        # Normalize scores
        if vector_scores:
            max_vector_score = max(vector_scores.values())
            if max_vector_score > 0:
                vector_scores = {k: v / max_vector_score for k, v in vector_scores.items()}
        
        if keyword_scores:
            max_keyword_score = max(keyword_scores.values())
            if max_keyword_score > 0:
                keyword_scores = {k: v / max_keyword_score for k, v in keyword_scores.items()}
        
        # Combine scores
        combined_scores = {}
        all_docs = set(vector_scores.keys()) | set(keyword_scores.keys())
        
        for doc_id in all_docs:
            vector_score = vector_scores.get(doc_id, 0)
            keyword_score = keyword_scores.get(doc_id, 0)
            
            combined_score = (vector_weight * vector_score) + (keyword_weight * keyword_score)
            combined_scores[doc_id] = combined_score
        
        # Sort by combined scores
        sorted_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Format results
        results = []
        for doc_id, combined_score in sorted_docs[:limit]:
            # Find the original result data
            vector_result = next((r for r in vector_results if r['id'] == doc_id), None)
            keyword_result = next((r for r in keyword_results if r['id'] == doc_id), None)
            
            if vector_result:
                result = vector_result.copy()
                result['score'] = combined_score
                result['vector_score'] = vector_scores.get(doc_id, 0)
                result['keyword_score'] = keyword_scores.get(doc_id, 0)
                if keyword_result:
                    result['matched_keywords'] = keyword_result.get('matched_keywords', [])
                results.append(result)
        
        logger.info(f"Hybrid search found {len(results)} documents for query: {query}")
        return results
    
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
            return {
                'name': self.collection_name,
                'status': 'active',
                'note': 'Collection info retrieval failed due to version compatibility'
            } 