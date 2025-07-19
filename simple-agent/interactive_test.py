#!/usr/bin/env python3
"""
Interactive test script for the Stock Analyst Agent

This script allows you to test the agent functionality interactively,
with and without API keys, and see how it handles different scenarios.
"""

import os
from dotenv import load_dotenv
from src.agents.stock_analyst import StockAnalystAgent
from src.tools.stock_tools import get_stock_price, get_pe_ratio, get_news_sentiment


def test_individual_tools():
    """Test individual stock tools with different tickers."""
    print("=" * 60)
    print("🧪 INDIVIDUAL TOOLS TESTING")
    print("=" * 60)
    
    test_tickers = ["AAPL", "GOOGL", "TSLA", "MSFT", "INVALID_TICKER"]
    
    for ticker in test_tickers:
        print(f"\n📊 Testing tools for: {ticker}")
        print("-" * 30)
        
        # Test stock price
        print("1. Stock Price:")
        price_data = get_stock_price(ticker)
        if "error" in price_data:
            print(f"   ❌ {price_data['error']}")
        else:
            print(f"   ✅ Price: ${price_data['current_price']}, Change: {price_data['change_percent']}%")
        
        # Test P/E ratio
        print("2. P/E Ratio:")
        pe_data = get_pe_ratio(ticker)
        if "error" in pe_data:
            print(f"   ❌ {pe_data['error']}")
        else:
            print(f"   ✅ P/E: {pe_data['pe_ratio']}, Forward P/E: {pe_data['forward_pe']}")
        
        # Test sentiment (always works with mock data)
        print("3. News Sentiment:")
        sentiment_data = get_news_sentiment(ticker)
        if "error" in sentiment_data:
            print(f"   ❌ {sentiment_data['error']}")
        else:
            print(f"   ✅ Sentiment: {sentiment_data['sentiment_label']} ({sentiment_data['sentiment_score']})")
            print(f"      Headlines: {len(sentiment_data['top_headlines'])} articles")


def test_agent_methods():
    """Test agent methods with mock data."""
    print("\n" + "=" * 60)
    print("🤖 AGENT TESTING (Mock Mode)")
    print("=" * 60)
    
    # Note: We'll test without OpenAI API key first
    print("Testing agent functionality without OpenAI API key...")
    print("(This demonstrates error handling and non-LLM methods)\n")
    
    try:
        # This will fail due to no API key, showing error handling
        agent = StockAnalystAgent(api_key="fake_key_for_testing")
        print("❌ This shouldn't happen - agent created with fake key")
    except Exception as e:
        print(f"✅ Proper error handling: {str(e)[:50]}...")
    
    # Test individual methods that don't require LLM
    print("\n📊 Testing non-LLM methods:")
    
    # We can create a "fake" agent just to test the data methods
    class MockAgent:
        def __init__(self):
            self.news_api_key = None
            
        def quick_sentiment_check(self, ticker):
            return get_news_sentiment(ticker, self.news_api_key)
            
        def get_current_metrics(self, ticker):
            try:
                price_data = get_stock_price(ticker)
                pe_data = get_pe_ratio(ticker)
                combined = {}
                if "error" not in price_data:
                    combined.update(price_data)
                if "error" not in pe_data:
                    combined.update({k: v for k, v in pe_data.items() if k != "ticker"})
                return combined if combined else {"error": "Failed to get stock data"}
            except Exception as e:
                return {"error": f"Error getting metrics for {ticker}: {str(e)}"}
    
    mock_agent = MockAgent()
    
    # Test sentiment check (works with mock data)
    print("1. Quick Sentiment Check:")
    sentiment = mock_agent.quick_sentiment_check("AAPL")
    print(f"   ✅ AAPL Sentiment: {sentiment['sentiment_label']} ({sentiment['sentiment_score']})")
    
    # Test metrics (may fail due to API limits)
    print("2. Current Metrics:")
    metrics = mock_agent.get_current_metrics("AAPL")
    if "error" in metrics:
        print(f"   ⚠️  API Limit: {metrics['error'][:50]}...")
    else:
        print(f"   ✅ Got metrics: Price ${metrics.get('current_price', 'N/A')}")


def test_with_real_api():
    """Test with real API keys if available."""
    print("\n" + "=" * 60)
    print("🔑 REAL API TESTING")
    print("=" * 60)
    
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    news_key = os.getenv("NEWS_API_KEY")
    
    print("API Key Status:")
    print(f"  OpenAI API Key: {'✅ Found' if openai_key else '❌ Not found'}")
    print(f"  News API Key: {'✅ Found' if news_key else '❌ Not found (optional)'}")
    
    if openai_key:
        print("\n🤖 Testing with real OpenAI API...")
        try:
            agent = StockAnalystAgent(api_key=openai_key, news_api_key=news_key)
            print("✅ Agent created successfully!")
            
            # Test quick methods first
            print("\n📊 Testing quick methods:")
            sentiment = agent.quick_sentiment_check("AAPL")
            print(f"  Sentiment: {sentiment.get('sentiment_label', 'Error')}")
            
            # Uncomment these for full testing (costs API credits):
            # print("\n🔍 Full Analysis (costs API credits):")
            # analysis = agent.analyze_stock("AAPL")
            # print(analysis[:200] + "..." if len(analysis) > 200 else analysis)
            
            print("\n💡 To test full analysis, uncomment the analysis code above")
            print("   (This will use OpenAI API credits)")
            
        except Exception as e:
            print(f"❌ Error with real API: {str(e)}")
    else:
        print("\n💡 To test with real APIs:")
        print("   1. Create .env file in project root")
        print("   2. Add: OPENAI_API_KEY=your_key_here")
        print("   3. Add: NEWS_API_KEY=your_news_key_here (optional)")
        print("   4. Run this script again")


def simulate_stock_recommendations():
    """Show how the system would work with mock data."""
    print("\n" + "=" * 60)
    print("📈 SIMULATED STOCK RECOMMENDATIONS")
    print("=" * 60)
    
    print("🎯 This shows how the system works with mock data:")
    print("   (In real usage, this data comes from Yahoo Finance + News APIs)\n")
    
    # Simulate different stock scenarios
    stocks = {
        "AAPL": {
            "scenario": "Strong Tech Stock",
            "mock_price": 175.50,
            "mock_pe": 28.5,
            "mock_sentiment": "positive",
            "mock_sentiment_score": 0.4
        },
        "TSLA": {
            "scenario": "Volatile Growth Stock", 
            "mock_price": 245.80,
            "mock_pe": 65.2,
            "mock_sentiment": "neutral",
            "mock_sentiment_score": 0.1
        },
        "VALUE": {
            "scenario": "Undervalued Stock",
            "mock_price": 45.20,
            "mock_pe": 12.8,
            "mock_sentiment": "negative",
            "mock_sentiment_score": -0.3
        }
    }
    
    for ticker, data in stocks.items():
        print(f"📊 {ticker} - {data['scenario']}:")
        print(f"  💰 Price: ${data['mock_price']}")
        print(f"  📈 P/E Ratio: {data['mock_pe']}")
        print(f"  📰 Sentiment: {data['mock_sentiment']} ({data['mock_sentiment_score']})")
        
        # Simple recommendation logic
        if data['mock_pe'] < 20 and data['mock_sentiment_score'] > 0:
            recommendation = "🟢 STRONG BUY"
        elif data['mock_pe'] < 30 and data['mock_sentiment_score'] >= 0:
            recommendation = "🟢 BUY"
        elif data['mock_pe'] < 40 and data['mock_sentiment_score'] >= -0.2:
            recommendation = "🟡 HOLD"
        else:
            recommendation = "🔴 SELL"
        
        print(f"  🎯 Recommendation: {recommendation}")
        print()
    
    print("💡 With real APIs and AI analysis, the agent would:")
    print("   • Fetch live stock data from Yahoo Finance")
    print("   • Get recent news and analyze sentiment")
    print("   • Use GPT to provide detailed analysis and reasoning")
    print("   • Consider market trends, company fundamentals, and risk factors")


def main():
    """Run interactive testing."""
    print("🧪 Interactive Stock Analyst Agent Testing")
    print("This shows you exactly how everything works!\n")
    
    while True:
        print("\n" + "=" * 60)
        print("Choose a test to run:")
        print("1. Test Individual Tools (price, P/E, sentiment)")
        print("2. Test Agent Methods (mock mode)")
        print("3. Test with Real APIs (if you have keys)")
        print("4. Show Simulated Stock Recommendations")
        print("5. Run All Tests")
        print("0. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (0-5): ").strip()
        
        if choice == "0":
            print("\n👋 Thanks for testing!")
            break
        elif choice == "1":
            test_individual_tools()
        elif choice == "2":
            test_agent_methods()
        elif choice == "3":
            test_with_real_api()
        elif choice == "4":
            simulate_stock_recommendations()
        elif choice == "5":
            test_individual_tools()
            test_agent_methods()
            test_with_real_api()
            simulate_stock_recommendations()
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()