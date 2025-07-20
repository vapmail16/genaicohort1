#!/usr/bin/env python3
"""
🚀 Launch Script for AI Stock Market Analyst

This script launches the Streamlit web application with proper configuration.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = [
        'streamlit', 'plotly', 'pandas', 'python-dotenv', 
        'langchain', 'langchain-openai', 'openai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required keys."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  No .env file found")
        print("💡 The app will work with limited functionality")
        print("   Add OPENAI_API_KEY to .env for full AI features")
        return False
    
    # Check if API keys are present
    with open(env_path, 'r') as f:
        content = f.read()
    
    has_openai = 'OPENAI_API_KEY=' in content and not content.split('OPENAI_API_KEY=')[1].split('\n')[0].strip() == 'your_openai_api_key_here'
    has_news = 'NEWS_API_KEY=' in content and not content.split('NEWS_API_KEY=')[1].split('\n')[0].strip() == 'your_news_api_key_here'
    
    if has_openai:
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  OpenAI API key not configured - limited functionality")
    
    if has_news:
        print("✅ News API key configured")
    else:
        print("ℹ️  News API key not configured - will use mock data")
    
    return True

def main():
    """Launch the Streamlit application."""
    print("🚀 AI Stock Market Analyst - Launch Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    check_env_file()
    
    # Launch Streamlit
    print("\n🌐 Launching web application...")
    print("💡 The app will open in your default browser")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        # Launch Streamlit with custom configuration
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.base", "light",
            "--theme.primaryColor", "#1f77b4"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("💡 Try running: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()