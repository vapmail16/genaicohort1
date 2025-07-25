#!/usr/bin/env python3
"""
Test script to verify Qdrant Cloud connection
"""

from vector_store import VectorStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test the connection to Qdrant Cloud."""
    try:
        logger.info("Testing Qdrant Cloud connection...")
        
        # Initialize vector store
        vector_store = VectorStore()
        
        # Get collection info
        info = vector_store.get_collection_info()
        logger.info(f"✅ Connection successful!")
        logger.info(f"Collection: {info['name']}")
        logger.info(f"Status: {info['status']}")
        logger.info(f"Points count: {info['points_count']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n🎉 Your Qdrant Cloud connection is working!")
        print("You can now proceed with document ingestion.")
    else:
        print("\n💥 Connection failed. Please check your configuration.") 