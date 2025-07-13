#!/usr/bin/env python3
"""
Launcher script for the AI Chatbot Assistant.
This script checks dependencies and starts the Streamlit application.
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'streamlit',
        'openai', 
        'pandas',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run:")
            print("pip install -r requirements.txt")
            return False
    
    return True

def check_api_key():
    """Check if OpenAI API key is configured."""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured!")
        print("\n📝 Please set up your API key:")
        print("1. Copy env_example.txt to .env")
        print("2. Edit .env and add your OpenAI API key")
        print("3. Get your API key from: https://platform.openai.com/api-keys")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("🤖 AI Chatbot Assistant Launcher")
    print("=" * 40)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check API key
    print("🔑 Checking API configuration...")
    if not check_api_key():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("🚀 Starting Streamlit application...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 40)
    
    # Start Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main() 