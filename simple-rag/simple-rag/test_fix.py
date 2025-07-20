#!/usr/bin/env python3
"""
Test script to verify the fix works
"""

import os
import openai
from vector_store import VectorStore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_fix():
    """Test the improved prompt and deduplication"""
    
    # Initialize vector store and OpenAI client
    vs = VectorStore()
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Test query
    query = "proceedings against a controller or processor, the plaintiff should have the choice to bring the action before the courts?"
    
    print(f"🔍 Testing fix for query: {query}")
    print("=" * 80)
    
    # Get search results
    results = vs.search(query, limit=5, score_threshold=0.3)
    
    if results:
        # Apply the same deduplication logic as in the app
        unique_chunks = []
        seen_texts = set()
        for r in results:
            # Normalize text for comparison (remove extra spaces, newlines)
            normalized_text = ' '.join(r['text'].split())
            if normalized_text not in seen_texts:
                unique_chunks.append(r)
                seen_texts.add(normalized_text)
        
        print(f"📄 Original chunks: {len(results)}")
        print(f"📄 Unique chunks after deduplication: {len(unique_chunks)}")
        
        # Create context from unique chunks
        context = "\n\n".join([r['text'] for r in unique_chunks])
        
        print("\n📝 DEDUPLICATED CONTEXT:")
        print(context)
        print("=" * 80)
        
        # Use the improved prompt
        prompt = f"""Based on the following text, answer this question:

Text: {context}

Question: {query}

Answer:"""
        
        print("🤖 IMPROVED PROMPT:")
        print(prompt)
        print("=" * 80)
        
        # Get LLM response
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.1,
            )
            
            answer = response.choices[0].message.content
            print("🤖 LLM RESPONSE:")
            print(answer)
            
            # Check if the answer is correct
            if "courts of the Member States" in answer or "establishment" in answer or "data subject" in answer:
                print("✅ SUCCESS: The LLM found the correct answer!")
            else:
                print("❌ The answer doesn't seem to contain the expected information")
            
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
    else:
        print("❌ No search results found")

if __name__ == "__main__":
    test_fix() 