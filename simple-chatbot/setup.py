#!/usr/bin/env python3
"""
Setup script for the AI Chatbot Assistant.
This script helps users set up the chatbot for the first time.
"""

import os
import shutil
import sys

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('env_example.txt'):
        shutil.copy('env_example.txt', '.env')
        print("✅ Created .env file from template")
        print("📝 Please edit .env and add your OpenAI API key")
        return True
    else:
        print("❌ env_example.txt not found")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def main():
    """Main setup function."""
    print("🤖 AI Chatbot Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Get your API key from: https://platform.openai.com/api-keys")
    print("3. Run the application:")
    print("   python run.py")
    print("   or")
    print("   streamlit run app.py")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 