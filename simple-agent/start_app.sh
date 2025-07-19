#!/bin/bash

# AI Stock Market Analyst - Startup Script
echo "🚀 Starting AI Stock Market Analyst..."
echo "=================================="

# Navigate to project directory
cd "$(dirname "$0")"

# Check Python and packages
echo "🔧 Checking requirements..."
python3 -c "import streamlit, plotly, pandas, dotenv; print('✅ All packages available')" || {
    echo "❌ Missing packages. Installing..."
    pip3 install streamlit plotly pandas python-dotenv
}

# Check API keys
if [ -f .env ]; then
    echo "✅ Environment file found"
else
    echo "⚠️  No .env file - app will work with limited functionality"
fi

# Set Python path and start Streamlit
export PYTHONPATH="."
echo ""
echo "🌐 Starting web application..."
echo "📱 App will open at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop"
echo ""

# Start Streamlit with proper configuration
python3 -m streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --theme.base light \
    --theme.primaryColor "#1f77b4"