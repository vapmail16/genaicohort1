from vector_store import VectorStore
from qdrant_client import QdrantClient
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME


def inspect_paragraph(paragraph: str, top_k: int = 1):
    print("[DEBUG] Starting search for most similar chunk...")
    # Search for the most similar chunk using the VectorStore
    vs = VectorStore()
    results = vs.search(paragraph, limit=top_k)
    print(f"[DEBUG] Search complete. Number of results: {len(results)}")
    if not results:
        print("No similar chunk found.")
        return
    
    # Print the best matching chunk and its vector
    best = results[0]
    print("Most similar chunk found:")
    print("Text:", best['text'])
    print("Metadata:", best['metadata'])
    print("Score:", best['score'])
    print()
    
    print(f"[DEBUG] Fetching vector for chunk ID: {best['id']}")
    # Fetch the vector from Qdrant by point ID
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    scroll_result, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter={
            "must": [
                {"key": "_id", "match": {"value": best['id']}}
            ]
        },
        limit=1,
        with_vectors=True
    )
    print(f"[DEBUG] Scroll result length: {len(scroll_result)}")
    if scroll_result:
        vector = scroll_result[0].vector
        print(f"Vector embedding (first 10 dims): {vector[:10]}")
        print(f"Vector length: {len(vector)}")
    else:
        print("Vector not found for this chunk.")


if __name__ == "__main__":
    paragraph = input("Enter the paragraph to inspect:\n")
    print("[DEBUG] Input received. Proceeding to inspect paragraph...")
    inspect_paragraph(paragraph) 