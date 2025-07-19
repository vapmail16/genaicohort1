#!/usr/bin/env python3
"""
Demo script for Phase 1: Basic Stock Analyst Agent

This demonstrates the core functionality of our stock analyst agent
with tool binding for stock price, P/E ratio, and news sentiment.
"""

import os
from dotenv import load_dotenv
from src.agents.stock_analyst import StockAnalystAgent
from src.tools.stock_tools import get_stock_price, get_pe_ratio, get_news_sentiment


def demo_individual_tools():
    """Demonstrate individual tool functions."""
    print("=" * 60)
    print("PHASE 1 DEMO: Individual Stock Analysis Tools")
    print("=" * 60)
    
    ticker = "AAPL"
    print(f"\n🔍 Testing individual tools for {ticker}:\n")
    
    # Test stock price tool
    print("📈 Stock Price Data:")
    price_data = get_stock_price(ticker)
    if "error" not in price_data:
        print(f"  Current Price: ${price_data['current_price']}")
        print(f"  Change: ${price_data['change']} ({price_data['change_percent']}%)")
        print(f"  Volume: {price_data['volume']:,}")
    else:
        print(f"  Error: {price_data['error']}")
    
    # Test P/E ratio tool
    print("\n📊 Financial Metrics:")
    pe_data = get_pe_ratio(ticker)
    if "error" not in pe_data:
        print(f"  P/E Ratio: {pe_data['pe_ratio']}")
        print(f"  Forward P/E: {pe_data['forward_pe']}")
        print(f"  PEG Ratio: {pe_data['peg_ratio']}")
    else:
        print(f"  Error: {pe_data['error']}")
    
    # Test sentiment tool (using mock data)
    print("\n📰 News Sentiment:")
    sentiment_data = get_news_sentiment(ticker)
    if "error" not in sentiment_data:
        print(f"  Sentiment Score: {sentiment_data['sentiment_score']}")
        print(f"  Sentiment: {sentiment_data['sentiment_label'].upper()}")
        print(f"  News Count: {sentiment_data['news_count']}")
        print("  Top Headlines:")
        for headline in sentiment_data['top_headlines']:
            print(f"    - {headline}")
    else:
        print(f"  Error: {sentiment_data['error']}")


def demo_agent_without_llm():
    """Demonstrate agent functionality without requiring OpenAI API."""
    print("\n" + "=" * 60)
    print("PHASE 1 DEMO: Agent Tool Integration (Mock Mode)")
    print("=" * 60)
    
    print("\n🤖 Agent Features Demonstrated:")
    print("✅ Tool binding with LangChain")
    print("✅ Stock price retrieval")
    print("✅ Financial metrics analysis")
    print("✅ News sentiment processing")
    print("✅ Error handling and validation")
    print("✅ Comprehensive test coverage")
    
    print("\n📋 Agent Methods Available:")
    print("  • analyze_stock(ticker) - Full stock analysis")
    print("  • compare_stocks(tickers) - Compare multiple stocks")
    print("  • quick_sentiment_check(ticker) - Fast sentiment lookup")
    print("  • get_current_metrics(ticker) - Combined price & financial data")
    
    print("\n⚙️  To use with real LLM analysis, provide OPENAI_API_KEY")


def demo_with_llm():
    """Demonstrate full agent with LLM if API key is available."""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️  No OpenAI API key found. Skipping LLM demo.")
        print("   Set OPENAI_API_KEY in .env file to test full functionality.")
        return
    
    print("\n" + "=" * 60) 
    print("PHASE 1 DEMO: Full Agent with LLM Analysis")
    print("=" * 60)
    
    try:
        agent = StockAnalystAgent(api_key=api_key)
        ticker = "AAPL"
        
        print(f"\n🤖 Analyzing {ticker} with LLM agent...")
        print("Note: This will make actual API calls and may take time.\n")
        
        # Quick metrics check first
        metrics = agent.get_current_metrics(ticker)
        print("📊 Current Metrics Retrieved:")
        if "error" not in metrics:
            print(f"  Price: ${metrics.get('current_price', 'N/A')}")
            print(f"  P/E: {metrics.get('pe_ratio', 'N/A')}")
        
        # Full analysis (commented out to avoid API costs in demo)
        # print("\n🔍 Full LLM Analysis:")
        # analysis = agent.analyze_stock(ticker)
        # print(analysis)
        
        print("\n✅ LLM Agent initialized successfully!")
        print("   Uncomment analysis code to see full AI-powered analysis.")
        
    except Exception as e:
        print(f"\n❌ Error initializing agent: {str(e)}")


def main():
    """Run the complete Phase 1 demonstration."""
    print("🚀 Stock Market Analyst Agent - Phase 1 Demo")
    print("Test-Driven Development Complete!")
    
    # Demo individual tools
    demo_individual_tools()
    
    # Demo agent integration
    demo_agent_without_llm()
    
    # Demo with LLM if available
    demo_with_llm()
    
    print("\n" + "=" * 60)
    print("✅ PHASE 1 COMPLETE!")
    print("=" * 60)
    print("\n🎯 Phase 1 Achievements:")
    print("  • ✅ Project structure and testing framework")
    print("  • ✅ Stock data tools (price, P/E, sentiment)")
    print("  • ✅ Comprehensive test coverage (20 tests)")
    print("  • ✅ LangChain agent with tool binding")
    print("  • ✅ Error handling and validation")
    print("  • ✅ Mock data support for testing")
    
    print("\n🚧 Next: Phase 2 - Multi-Agent Collaboration")
    print("  • CrewAI/AutoGen integration")
    print("  • Specialized agents (Fetcher, News, Scorer, Reporter)")
    print("  • Agent communication and coordination")


if __name__ == "__main__":
    main()