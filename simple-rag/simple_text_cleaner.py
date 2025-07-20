#!/usr/bin/env python3
"""
Simplified Text Cleaning Module for RAG Application
"""

import re
import string
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTextCleaner:
    """
    A simplified text cleaning class for preprocessing documents.
    
    Features:
    - HTML tag removal
    - Special character cleaning
    - Lowercase conversion
    - Whitespace normalization
    - Number preservation (optional)
    """
    
    def __init__(self, remove_numbers: bool = False):
        """
        Initialize the text cleaner.
        
        Args:
            remove_numbers: Whether to remove numbers
        """
        self.remove_numbers = remove_numbers
        
        # Basic English stopwords (common words that don't add semantic value)
        self.basic_stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
            'had', 'what', 'said', 'each', 'which', 'she', 'do', 'how', 'their',
            'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some',
            'her', 'would', 'make', 'like', 'into', 'him', 'time', 'two', 'more',
            'go', 'no', 'way', 'could', 'my', 'than', 'first', 'been', 'call',
            'who', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get',
            'come', 'made', 'may', 'part'
        }
    
    def remove_html_tags(self, text: str) -> str:
        """
        Remove HTML tags from text.
        
        Args:
            text: Input text that may contain HTML tags
            
        Returns:
            Text with HTML tags removed
        """
        # Remove HTML tags using regex
        clean_text = re.sub(r'<[^>]+>', '', text)
        # Remove HTML entities
        clean_text = re.sub(r'&[a-zA-Z]+;', '', clean_text)
        clean_text = re.sub(r'&#\d+;', '', clean_text)
        return clean_text
    
    def clean_special_characters(self, text: str) -> str:
        """
        Clean special characters while preserving important punctuation.
        
        Args:
            text: Input text with special characters
            
        Returns:
            Text with cleaned special characters
        """
        # Keep important punctuation for legal documents
        important_punct = r'[.,;:!?()[\]{}"\'-]'
        
        # Remove special characters but keep important punctuation
        clean_text = re.sub(r'[^\w\s' + important_punct + ']', ' ', text)
        
        # Clean up multiple spaces
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        return clean_text.strip()
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Input text with irregular whitespace
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Replace multiple newlines with single newline
        text = re.sub(r'\n+', '\n', text)
        # Replace multiple tabs with single space
        text = re.sub(r'\t+', ' ', text)
        
        return text.strip()
    
    def remove_numbers(self, text: str) -> str:
        """
        Remove numbers from text.
        
        Args:
            text: Input text that may contain numbers
            
        Returns:
            Text with numbers removed
        """
        # Remove standalone numbers
        text = re.sub(r'\b\d+\b', '', text)
        # Remove numbers with decimals
        text = re.sub(r'\b\d+\.\d+\b', '', text)
        # Remove numbers with commas (like 1,000)
        text = re.sub(r'\b\d{1,3}(,\d{3})*\b', '', text)
        
        return text
    
    def remove_basic_stopwords(self, text: str) -> str:
        """
        Remove basic stopwords from text.
        
        Args:
            text: Input text
            
        Returns:
            Text with stopwords removed
        """
        # Split into words
        words = text.split()
        
        # Remove stopwords
        filtered_words = [word for word in words if word.lower() not in self.basic_stopwords]
        
        # Rejoin the text
        return ' '.join(filtered_words)
    
    def clean_text(self, text: str, remove_stopwords: bool = False) -> str:
        """
        Apply all cleaning steps to the text.
        
        Args:
            text: Raw input text
            remove_stopwords: Whether to remove stopwords
            
        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        logger.debug(f"Original text length: {len(text)}")
        
        # Step 1: Remove HTML tags
        text = self.remove_html_tags(text)
        logger.debug(f"After HTML removal: {len(text)}")
        
        # Step 2: Clean special characters
        text = self.clean_special_characters(text)
        logger.debug(f"After special char cleaning: {len(text)}")
        
        # Step 3: Normalize whitespace
        text = self.normalize_whitespace(text)
        logger.debug(f"After whitespace normalization: {len(text)}")
        
        # Step 4: Convert to lowercase
        text = text.lower()
        logger.debug(f"After lowercase conversion: {len(text)}")
        
        # Step 5: Remove numbers (if enabled)
        if self.remove_numbers:
            text = self.remove_numbers(text)
            logger.debug(f"After number removal: {len(text)}")
        
        # Step 6: Remove stopwords (if enabled)
        if remove_stopwords:
            text = self.remove_basic_stopwords(text)
            logger.debug(f"After stopword removal: {len(text)}")
        
        # Final whitespace normalization
        text = self.normalize_whitespace(text)
        
        logger.info(f"Text cleaning completed. Final length: {len(text)}")
        return text
    
    def clean_documents(self, documents: List[dict], remove_stopwords: bool = False) -> List[dict]:
        """
        Clean a list of documents.
        
        Args:
            documents: List of documents with 'text' key
            remove_stopwords: Whether to remove stopwords
            
        Returns:
            List of cleaned documents
        """
        cleaned_docs = []
        
        for i, doc in enumerate(documents):
            if 'text' in doc:
                cleaned_text = self.clean_text(doc['text'], remove_stopwords)
                cleaned_doc = doc.copy()
                cleaned_doc['text'] = cleaned_text
                cleaned_docs.append(cleaned_doc)
                logger.info(f"Cleaned document {i+1}/{len(documents)}")
            else:
                logger.warning(f"Document {i+1} missing 'text' key, skipping")
                cleaned_docs.append(doc)
        
        return cleaned_docs


def create_simple_text_cleaner(remove_numbers: bool = False) -> SimpleTextCleaner:
    """
    Factory function to create a SimpleTextCleaner instance.
    
    Args:
        remove_numbers: Whether to remove numbers
        
    Returns:
        Configured SimpleTextCleaner instance
    """
    return SimpleTextCleaner(remove_numbers=remove_numbers)


if __name__ == "__main__":
    # Example usage
    cleaner = SimpleTextCleaner(remove_numbers=False)
    
    sample_text = """
    <p>This is a <strong>sample</strong> text with HTML tags.</p>
    It contains numbers like 123 and 456.7, and special characters @#$%.
    The text has multiple    spaces and
    newlines.
    """
    
    print("=== Text Cleaning Demo ===")
    print("Original:", repr(sample_text))
    print()
    
    # Test without stopword removal
    cleaned = cleaner.clean_text(sample_text, remove_stopwords=False)
    print("Cleaned (no stopwords):", repr(cleaned))
    print()
    
    # Test with stopword removal
    cleaned_with_stopwords = cleaner.clean_text(sample_text, remove_stopwords=True)
    print("Cleaned (with stopwords):", repr(cleaned_with_stopwords)) 