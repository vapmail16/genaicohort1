import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

class Config:
    """Configuration class for the chatbot application."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1000))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    
    # OpenAI Pricing (per 1K tokens) - Updated as of 2024
    MODEL_PRICING = {
        'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},  # $0.0015/1K input, $0.002/1K output
        'gpt-4': {'input': 0.03, 'output': 0.06},  # $0.03/1K input, $0.06/1K output
        'gpt-4-turbo': {'input': 0.01, 'output': 0.03},  # $0.01/1K input, $0.03/1K output
        'gpt-4o': {'input': 0.005, 'output': 0.015},  # $0.005/1K input, $0.015/1K output
        'gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},  # $0.00015/1K input, $0.0006/1K output
    }
    
    # Chatbot Personalities
    PERSONALITIES = {
        'friendly': {
            'name': 'Friendly Assistant',
            'system_message': 'You are a friendly, helpful assistant. Be warm, encouraging, and supportive in your responses.',
            'emoji': '😊'
        },
        'professional': {
            'name': 'Professional Assistant',
            'system_message': 'You are a professional, formal assistant. Provide clear, concise, and accurate information.',
            'emoji': '💼'
        },
        'funny': {
            'name': 'Funny Assistant',
            'system_message': 'You are a witty and humorous assistant. Make jokes, use puns, and keep conversations entertaining.',
            'emoji': '😂'
        },
        'creative': {
            'name': 'Creative Assistant',
            'system_message': 'You are a creative and imaginative assistant. Think outside the box and provide innovative solutions.',
            'emoji': '🎨'
        },
        'savage': {
            'name': 'Savage Assistant',
            'system_message': 'You are a savage, witty assistant who responds to rude or abusive language with clever comebacks and witty retorts. When users are disrespectful, respond with humor and clever responses that match their energy but in a more intelligent way. Be creative with your responses and use wordplay, sarcasm, and clever observations.',
            'emoji': '😈'
        }
    }
    
    # File Paths
    CHAT_LOG_FILE = 'chat_history.csv'
    LOG_FILE = 'chatbot.log'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'chatbot.log')
    
    # UI Configuration
    MAX_MESSAGES_DISPLAY = 50
    SIDEBAR_WIDTH = 300 