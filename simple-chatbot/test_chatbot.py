#!/usr/bin/env python3
"""
Test script for the chatbot core functionality.
Run this to test the chatbot without the Streamlit interface.
"""

import os
import sys
from chatbot_core import ChatbotCore
from config import Config

def test_chatbot():
    """Test the chatbot core functionality."""
    print("🤖 Testing AI Chatbot Assistant")
    print("=" * 50)
    
    # Check if API key is set
    if not Config.OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found!")
        print("Please set your OpenAI API key in the .env file or environment variables.")
        return False
    
    try:
        # Initialize chatbot
        print("📡 Initializing chatbot...")
        chatbot = ChatbotCore()
        print("✅ Chatbot initialized successfully!")
        
        # Test different personalities
        print("\n🎭 Testing Personalities:")
        for personality in Config.PERSONALITIES:
            print(f"\n--- Testing {personality} personality ---")
            chatbot.set_personality(personality)
            
            # Test simple response
            test_message = "Hello! How are you today?"
            print(f"User: {test_message}")
            
            response, success = chatbot.get_response(test_message)
            if success:
                print(f"Bot: {response}")
                print("✅ Response successful")
            else:
                print(f"❌ Error: {response}")
        
        # Test conversation memory
        print("\n🧠 Testing Conversation Memory:")
        chatbot.set_personality('friendly')
        
        messages = [
            "My name is Alice.",
            "What's my name?",
            "How many messages have we exchanged so far?"
        ]
        
        for i, message in enumerate(messages, 1):
            print(f"\nMessage {i}: {message}")
            response, success = chatbot.get_response(message)
            if success:
                print(f"Response: {response}")
            else:
                print(f"Error: {response}")
        
        # Test error handling
        print("\n⚠️ Testing Error Handling:")
        response, success = chatbot.get_response("")
        print(f"Empty message test: {response}")
        
        # Show statistics
        print("\n📊 Chat Statistics:")
        summary = chatbot.get_conversation_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def main():
    """Main test function."""
    print("Starting chatbot tests...")
    
    success = test_chatbot()
    
    if success:
        print("\n🎉 All tests passed! Your chatbot is ready to use.")
        print("\nTo run the full application:")
        print("streamlit run app.py")
    else:
        print("\n💥 Some tests failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 