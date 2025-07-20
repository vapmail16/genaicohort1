#!/usr/bin/env python3
"""
Test script to verify LLM prompt and response
"""

import os
import openai
from vector_store import VectorStore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_llm_response():
    """Test the LLM response with the specific query and context"""
    
    # Initialize vector store and OpenAI client
    vs = VectorStore()
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Test query
    query = "proceedings against a controller or processor, the plaintiff should have the choice to bring the action before the courts?"
    
    print(f"🔍 Query: {query}")
    print("=" * 80)
    
    # Get search results
    results = vs.search(query, limit=5, score_threshold=0.3)
    
    if results:
        # Create context from results
        context = "\n\n".join([r['text'] for r in results])
        
        print(f"📄 Retrieved {len(results)} chunks:")
        for i, result in enumerate(results, 1):
            print(f"Chunk {i} (Score: {result['score']:.4f}): {result['text'][:100]}...")
        
        print("\n" + "=" * 80)
        print("📝 FULL CONTEXT:")
        print(context)
        print("=" * 80)
        
        # Create the same prompt as in the app
        prompt = (
            "Answer the following question using ONLY the context below. "
            "If the context does not contain enough information, say 'I don't know based on the provided context.'\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        )
        
        print("🤖 PROMPT SENT TO LLM:")
        print(prompt)
        print("=" * 80)
        
        # Get LLM response
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for answering questions about a document."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.2,
            )
            
            answer = response.choices[0].message.content
            print("🤖 LLM RESPONSE:")
            print(answer)
            
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
    else:
        print("❌ No search results found")

if __name__ == "__main__":
    test_llm_response() 