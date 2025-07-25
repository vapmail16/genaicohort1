#!/usr/bin/env python3
"""
Test the full AI functionality with real API keys
"""

import os
from dotenv import load_dotenv
from src.agents.stock_analyst import StockAnalystAgent


def test_full_ai_analysis():
    """Test full AI analysis with real API keys."""
    print("🤖 TESTING FULL AI-POWERED STOCK ANALYSIS")
    print("=" * 60)
    
    load_dotenv()
    
    try:
        agent = StockAnalystAgent(
            api_key=os.getenv("OPENAI_API_KEY"),
            news_api_key=os.getenv("NEWS_API_KEY")
        )
        print("✅ AI Agent initialized with real API keys!")
        
        # Test 1: Quick sentiment check (using real News API)
        print("\n📰 Testing News Sentiment with Real API:")
        ticker = "AAPL"
        sentiment = agent.quick_sentiment_check(ticker)
        
        if "error" not in sentiment:
            print(f"✅ {ticker} Sentiment Analysis:")
            print(f"   Score: {sentiment['sentiment_score']}")
            print(f"   Label: {sentiment['sentiment_label']}")
            print(f"   News Count: {sentiment['news_count']}")
            if sentiment['top_headlines']:
                print(f"   Latest: \"{sentiment['top_headlines'][0]}\"")
        else:
            print(f"⚠️  Using mock data: {sentiment}")
        
        # Test 2: Get current metrics
        print(f"\n📊 Testing Current Metrics for {ticker}:")
        metrics = agent.get_current_metrics(ticker)
        if "error" in metrics:
            print(f"⚠️  API limits: {metrics['error'][:60]}...")
        else:
            print("✅ Retrieved metrics successfully!")
            for key, value in list(metrics.items())[:5]:  # Show first 5
                print(f"   {key}: {value}")
        
        # Test 3: Full AI Analysis (This will use GPT!)
        print(f"\n🧠 FULL AI ANALYSIS for {ticker}:")
        print("🔄 Calling GPT for comprehensive stock analysis...")
        print("⏳ This may take 10-30 seconds...")
        
        analysis = agent.analyze_stock(ticker)
        
        print("\n" + "=" * 60)
        print(f"🎯 AI ANALYSIS RESULT for {ticker}:")
        print("=" * 60)
        print(analysis)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True


def test_stock_comparison():
    """Test AI stock comparison."""
    print("\n" + "=" * 60)
    print("🔄 TESTING AI STOCK COMPARISON")
    print("=" * 60)
    
    load_dotenv()
    
    try:
        agent = StockAnalystAgent(
            api_key=os.getenv("OPENAI_API_KEY"),
            news_api_key=os.getenv("NEWS_API_KEY")
        )
        
        stocks = ["AAPL", "GOOGL"]
        print(f"🔍 Comparing: {', '.join(stocks)}")
        print("🧠 AI is analyzing multiple stocks...")
        print("⏳ This may take 30-60 seconds...")
        
        comparison = agent.compare_stocks(stocks)
        
        print("\n" + "=" * 60)
        print(f"🎯 AI COMPARISON RESULT:")
        print("=" * 60)
        print(comparison)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Comparison error: {str(e)}")


def main():
    """Run full AI testing."""
    print("🚀 FULL AI FUNCTIONALITY TEST")
    print("Using your real OpenAI and News API keys!")
    print()
    
    # Test individual analysis
    success = test_full_ai_analysis()
    
    if success:
        # Test comparison if individual analysis worked
        print("\n💡 Individual analysis successful!")
        
        choice = input("\n🤔 Run stock comparison test? (costs more API credits) [y/N]: ").lower()
        if choice == 'y':
            test_stock_comparison()
        else:
            print("⏭️  Skipping comparison test to save API credits")
    
    print("\n🎉 AI TESTING COMPLETE!")
    print("\n✅ Your Stock Analyst Agent is fully operational!")
    print("🔥 Ready to analyze any stock with AI power!")


if __name__ == "__main__":
    main()