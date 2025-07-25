import re
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class HybridSearch:
    def __init__(self, documents: List[Dict[str, Any]]):
        """
        Initialize hybrid search with documents.
        
        Args:
            documents: List of documents with 'text' and optional 'metadata' keys
        """
        self.documents = documents
        self.texts = [doc['text'] for doc in documents]
        
        # Initialize TF-IDF vectorizer for keyword search
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),  # Include unigrams and bigrams
            min_df=1,
            max_df=0.95
        )
        
        # Fit TF-IDF vectorizer
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.texts)
        self.feature_names = self.tfidf_vectorizer.get_feature_names_out()
        
        logger.info(f"Initialized hybrid search with {len(documents)} documents")
    
    def keyword_search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Perform keyword-based search using TF-IDF.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of (document_index, score) tuples
        """
        # Transform query to TF-IDF vector
        query_vector = self.tfidf_vectorizer.transform([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = [(idx, similarities[idx]) for idx in top_indices if similarities[idx] > 0]
        return results
    
    def extract_keywords(self, query: str) -> List[str]:
        """
        Extract important keywords from query.
        
        Args:
            query: Search query
            
        Returns:
            List of extracted keywords
        """
        # Simple keyword extraction - can be enhanced with NLP libraries
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
    
    def keyword_boost_search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Perform keyword-boosted search that gives extra weight to exact keyword matches.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of (document_index, score) tuples
        """
        # Get base TF-IDF scores
        base_results = self.keyword_search(query, top_k * 2)
        
        # Extract keywords from query
        keywords = self.extract_keywords(query)
        
        # Boost scores for documents with exact keyword matches
        boosted_results = []
        for doc_idx, base_score in base_results:
            boost_factor = 1.0
            
            # Check for exact keyword matches
            doc_text = self.texts[doc_idx].lower()
            for keyword in keywords:
                if keyword in doc_text:
                    # Boost score based on keyword frequency
                    keyword_count = doc_text.count(keyword)
                    boost_factor += min(keyword_count * 0.1, 0.5)  # Cap boost at 0.5
            
            boosted_score = base_score * boost_factor
            boosted_results.append((doc_idx, boosted_score))
        
        # Sort by boosted scores and return top-k
        boosted_results.sort(key=lambda x: x[1], reverse=True)
        return boosted_results[:top_k]
    
    def hybrid_search(self, query: str, top_k: int = 10, 
                     vector_weight: float = 0.7, keyword_weight: float = 0.3) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining vector and keyword search.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            vector_weight: Weight for vector similarity scores (0.0-1.0)
            keyword_weight: Weight for keyword search scores (0.0-1.0)
            
        Returns:
            List of search results with combined scores
        """
        # Get keyword search results
        keyword_results = self.keyword_boost_search(query, top_k * 2)
        
        # Create a mapping of document indices to keyword scores
        keyword_scores = {idx: score for idx, score in keyword_results}
        
        # Normalize keyword scores
        if keyword_scores:
            max_keyword_score = max(keyword_scores.values())
            if max_keyword_score > 0:
                keyword_scores = {idx: score / max_keyword_score for idx, score in keyword_scores.items()}
        
        # Combine scores (assuming vector scores are already normalized)
        combined_scores = {}
        for doc_idx in keyword_scores:
            keyword_score = keyword_scores[doc_idx]
            # For hybrid search, we'll use the keyword score as a proxy for vector score
            # In a real implementation, you'd get actual vector scores from your vector store
            vector_score = keyword_score  # Placeholder - replace with actual vector scores
            
            combined_score = (vector_weight * vector_score) + (keyword_weight * keyword_score)
            combined_scores[doc_idx] = combined_score
        
        # Sort by combined scores
        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Format results
        results = []
        for doc_idx, score in sorted_results[:top_k]:
            results.append({
                'id': doc_idx,
                'score': score,
                'text': self.documents[doc_idx]['text'],
                'metadata': self.documents[doc_idx].get('metadata', {}),
                'source': self.documents[doc_idx].get('source', 'unknown'),
                'keyword_score': keyword_scores.get(doc_idx, 0),
                'vector_score': score  # Placeholder
            })
        
        return results
    
    def semantic_keyword_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Perform semantic keyword search that considers both meaning and exact matches.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of search results
        """
        # Extract keywords
        keywords = self.extract_keywords(query)
        
        # Get TF-IDF scores
        tfidf_results = self.keyword_search(query, top_k * 2)
        
        # Calculate semantic relevance based on keyword overlap
        semantic_results = []
        for doc_idx, tfidf_score in tfidf_results:
            doc_text = self.texts[doc_idx].lower()
            
            # Calculate keyword overlap
            matched_keywords = [kw for kw in keywords if kw in doc_text]
            keyword_overlap = len(matched_keywords) / len(keywords) if keywords else 0
            
            # Calculate semantic score (combination of TF-IDF and keyword overlap)
            semantic_score = (0.6 * tfidf_score) + (0.4 * keyword_overlap)
            
            semantic_results.append({
                'id': doc_idx,
                'score': semantic_score,
                'text': self.documents[doc_idx]['text'],
                'metadata': self.documents[doc_idx].get('metadata', {}),
                'source': self.documents[doc_idx].get('source', 'unknown'),
                'tfidf_score': tfidf_score,
                'keyword_overlap': keyword_overlap,
                'matched_keywords': matched_keywords
            })
        
        # Sort by semantic score
        semantic_results.sort(key=lambda x: x['score'], reverse=True)
        return semantic_results[:top_k] 