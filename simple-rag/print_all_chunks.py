from vector_store import VectorStore
from qdrant_client import QdrantClient
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

vs = VectorStore()
results = vs.search("", limit=1, score_threshold=0.0)  # Get only 1 chunk

print(f"Found {len(results)} chunk in the vector database\n")

if results:
    chunk = results[0]
    print(f"Chunk 1:")
    print("Text:", chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'])
    print("Metadata:", chunk['metadata'])
    print("Score:", chunk['score'])
    print("ID:", chunk['id'])
    
    # Try to get the actual vector using scroll without filter
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    try:
        # Get all points and find the one with matching ID
        scroll_result, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=1000,  # Get all points
            with_vectors=True
        )
        
        # Find the point with matching ID
        target_point = None
        for point in scroll_result:
            if point.id == chunk['id']:
                target_point = point
                break
        
        if target_point and target_point.vector:
            vector = target_point.vector
            print(f"\nVector embedding (first 10 dimensions): {vector[:10]}")
            print(f"Vector length: {len(vector)}")
            print(f"Vector type: {type(vector)}")
            print(f"Vector min value: {min(vector)}")
            print(f"Vector max value: {max(vector)}")
            print(f"Vector mean: {sum(vector)/len(vector):.6f}")
        else:
            print("\nVector not found for this chunk.")
            
    except Exception as e:
        print(f"\nError fetching vector: {e}")
    
    print("-" * 40) 