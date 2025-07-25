#!/usr/bin/env python3
"""
Simple test to see if LLM can find the answer
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def simple_test():
    """Simple test with the exact answer in context"""
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # The exact context that contains the answer
    context = """(145) For proceedings against a controller or processor, the plaintiff should have the choice to bring the action before the courts of the Member States where the controller or processor has an establishment or where the data subject resides, unless the controller is a public authority of a Member State acting in the exercise of its public powers."""
    
    query = "proceedings against a controller or processor, the plaintiff should have the choice to bring the action before the courts?"
    
    print("🔍 Simple Test")
    print("=" * 50)
    print(f"Query: {query}")
    print(f"Context: {context}")
    print("=" * 50)
    
    # Try a simpler prompt
    prompt = f"""Based on the following text, answer this question:

Text: {context}

Question: {query}

Answer:"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.1,
        )
        
        answer = response.choices[0].message.content
        print("🤖 LLM Response:")
        print(answer)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_test() 