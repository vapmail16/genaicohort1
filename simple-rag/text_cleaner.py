#!/usr/bin/env python3
"""
Text Cleaning and Preprocessing Module for RAG Application
"""

import re
import string
from typing import Optional, List
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextCleaner:
    """
    A comprehensive text cleaning class for preprocessing documents.
    
    Features:
    - HTML tag removal
    - Special character cleaning
    - Lowercase conversion
    - Optional stopword removal
    - Whitespace normalization
    - Number preservation (optional)
    """
    
    def __init__(self, 
                 remove_stopwords: bool = False,
                 remove_numbers: bool = False,
                 language: str = 'english'):
        """
        Initialize the text cleaner.
        
        Args:
            remove_stopwords: Whether to remove stopwords
            remove_numbers: Whether to remove numbers
            language: Language for stopwords (default: 'english')
        """
        self.remove_stopwords = remove_stopwords
        self.remove_numbers = remove_numbers
        self.language = language
        
        # Download required NLTK data if not already present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        if self.remove_stopwords:
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                logger.info("Downloading NLTK stopwords...")
                nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words(self.language))
        else:
            self.stop_words = set()
    
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
    
    def remove_stopwords_from_text(self, text: str) -> str:
        """
        Remove stopwords from text.
        
        Args:
            text: Input text
            
        Returns:
            Text with stopwords removed
        """
        if not self.remove_stopwords or not self.stop_words:
            return text
        
        # Tokenize the text
        words = word_tokenize(text.lower())
        
        # Remove stopwords
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        
        # Rejoin the text
        return ' '.join(filtered_words)
    
    def clean_text(self, text: str) -> str:
        """
        Apply all cleaning steps to the text.
        
        Args:
            text: Raw input text
            
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
        text = self.remove_stopwords_from_text(text)
        logger.debug(f"After stopword removal: {len(text)}")
        
        # Final whitespace normalization
        text = self.normalize_whitespace(text)
        
        logger.info(f"Text cleaning completed. Final length: {len(text)}")
        return text
    
    def clean_documents(self, documents: List[dict]) -> List[dict]:
        """
        Clean a list of documents.
        
        Args:
            documents: List of documents with 'text' key
            
        Returns:
            List of cleaned documents
        """
        cleaned_docs = []
        
        for i, doc in enumerate(documents):
            if 'text' in doc:
                cleaned_text = self.clean_text(doc['text'])
                cleaned_doc = doc.copy()
                cleaned_doc['text'] = cleaned_text
                cleaned_docs.append(cleaned_doc)
                logger.info(f"Cleaned document {i+1}/{len(documents)}")
            else:
                logger.warning(f"Document {i+1} missing 'text' key, skipping")
                cleaned_docs.append(doc)
        
        return cleaned_docs


def create_text_cleaner(remove_stopwords: bool = False, 
                       remove_numbers: bool = False,
                       language: str = 'english') -> TextCleaner:
    """
    Factory function to create a TextCleaner instance.
    
    Args:
        remove_stopwords: Whether to remove stopwords
        remove_numbers: Whether to remove numbers
        language: Language for stopwords
        
    Returns:
        Configured TextCleaner instance
    """
    return TextCleaner(
        remove_stopwords=remove_stopwords,
        remove_numbers=remove_numbers,
        language=language
    )


if __name__ == "__main__":
    # Example usage
    cleaner = TextCleaner(remove_stopwords=True, remove_numbers=False)
    
    sample_text = """
    <p>This is a <strong>sample</strong> text with HTML tags.</p>
    It contains numbers like 123 and 456.7, and special characters @#$%.
    The text has multiple    spaces and
    newlines.
    """
    
    cleaned = cleaner.clean_text(sample_text)
    print("Original:", repr(sample_text))
    print("Cleaned:", repr(cleaned)) 