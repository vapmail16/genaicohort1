#!/usr/bin/env python3
"""
Debug script to test search functionality and see what chunks are retrieved
"""

import os
from vector_store import VectorStore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_search():
    """Test search functionality with the specific query"""
    
    # Initialize vector store
    print("Initializing vector store...")
    vs = VectorStore()
    
    # Test query
    query = "proceedings against a controller or processor, the plaintiff should have the choice to bring the action before the courts?"
    
    print(f"\n🔍 Testing query: {query}")
    print("=" * 80)
    
    # Test with different score thresholds
    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    for threshold in thresholds:
        print(f"\n📊 Testing with score threshold: {threshold}")
        print("-" * 50)
        
        try:
            results = vs.search(query, limit=5, score_threshold=threshold)
            
            if results:
                print(f"✅ Found {len(results)} results")
                for i, result in enumerate(results, 1):
                    print(f"\n📄 Chunk {i} (Score: {result['score']:.4f})")
                    print(f"Source: {result.get('source', 'unknown')}")
                    print(f"Text preview: {result['text'][:200]}...")
                    print("-" * 30)
            else:
                print("❌ No results found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test with no score threshold to see all possible results
    print(f"\n🔍 Testing with NO score threshold (limit=10)")
    print("-" * 50)
    
    try:
        results = vs.search(query, limit=10, score_threshold=0.0)
        
        if results:
            print(f"✅ Found {len(results)} results")
            for i, result in enumerate(results, 1):
                print(f"\n📄 Chunk {i} (Score: {result['score']:.4f})")
                print(f"Source: {result.get('source', 'unknown')}")
                print(f"Text: {result['text']}")
                print("-" * 30)
        else:
            print("❌ No results found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_search() 