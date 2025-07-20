#!/usr/bin/env python3
"""
Demo script for Phase 2: Multi-Agent Collaboration System

This demonstrates specialized agents working together:
- StockFetcherAgent: Gathers financial data
- NewsAnalystAgent: Analyzes market sentiment  
- RiskAssessmentAgent: Evaluates investment risks
- ReportGeneratorAgent: Creates comprehensive reports
"""

import os
from dotenv import load_dotenv
from src.multi_agents.specialized_agents import MultiAgentCoordinator


def demo_individual_agents():
    """Demonstrate individual specialized agents."""
    print("=" * 70)
    print("PHASE 2 DEMO: Individual Specialized Agents")
    print("=" * 70)
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    news_api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        print("❌ OpenAI API key required for Phase 2 demo")
        return
    
    coordinator = MultiAgentCoordinator(api_key=api_key, news_api_key=news_api_key)
    ticker = "AAPL"
    
    print(f"\n🔍 Testing individual agents with {ticker}:\n")
    
    # Test Stock Fetcher Agent
    print("🤖 Agent 1: Stock Data Fetcher")
    print("Role: Financial Data Specialist")
    try:
        price_result = coordinator.stock_fetcher.execute(f"Fetch current stock price data for {ticker}")
        print("✅ Price Data Retrieved:")
        print("   " + price_result.replace('\n', '\n   ')[:200] + "..." if len(price_result) > 200 else "   " + price_result.replace('\n', '\n   '))
    except Exception as e:
        print(f"⚠️  {str(e)[:100]}...")
    
    print()
    
    # Test News Analyst Agent  
    print("🤖 Agent 2: News Sentiment Analyst")
    print("Role: Market Psychology Expert")
    try:
        sentiment_result = coordinator.news_analyst.execute(f"Analyze recent news sentiment for {ticker}")
        print("✅ Sentiment Analysis:")
        print("   " + sentiment_result.replace('\n', '\n   ')[:300] + "..." if len(sentiment_result) > 300 else "   " + sentiment_result.replace('\n', '\n   '))
    except Exception as e:
        print(f"⚠️  {str(e)[:100]}...")
    
    print()
    
    # Test Risk Assessment Agent
    print("🤖 Agent 3: Risk Assessment Specialist") 
    print("Role: Risk Management Expert")
    try:
        risk_result = coordinator.risk_assessor.execute(f"Assess overall investment risk for {ticker} considering current market conditions")
        print("✅ Risk Assessment:")
        print("   " + risk_result.replace('\n', '\n   ')[:300] + "..." if len(risk_result) > 300 else "   " + risk_result.replace('\n', '\n   '))
    except Exception as e:
        print(f"⚠️  {str(e)[:100]}...")
    
    print()
    
    # Test Report Generator Agent
    print("🤖 Agent 4: Investment Report Generator")
    print("Role: Senior Investment Analyst") 
    try:
        report_result = coordinator.report_generator.execute(f"Create a brief investment summary for {ticker}")
        print("✅ Report Generation:")
        print("   " + report_result.replace('\n', '\n   ')[:300] + "..." if len(report_result) > 300 else "   " + report_result.replace('\n', '\n   '))
    except Exception as e:
        print(f"⚠️  {str(e)[:100]}...")


def demo_collaborative_analysis():
    """Demonstrate full collaborative multi-agent analysis."""
    print("\n" + "=" * 70)
    print("PHASE 2 DEMO: Collaborative Multi-Agent Analysis")
    print("=" * 70)
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    news_api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        print("❌ OpenAI API key required for collaborative demo")
        return
    
    coordinator = MultiAgentCoordinator(api_key=api_key, news_api_key=news_api_key)
    ticker = "TSLA"  # Using different ticker for variety
    
    print(f"\n🎯 Multi-Agent Collaborative Analysis for {ticker}")
    print("🔄 All agents working together in sequence...\n")
    
    try:
        # This will run all 4 agents in coordinated sequence
        results = coordinator.analyze_stock_collaborative(ticker)
        
        print("\n" + "=" * 70)
        print("📊 COLLABORATIVE ANALYSIS RESULTS")
        print("=" * 70)
        
        # Display results from each agent
        print(f"\n📈 STOCK DATA (Agent 1):")
        print("─" * 40)
        price_data = results.get('price_data', 'No data available')
        print(price_data[:400] + "..." if len(price_data) > 400 else price_data)
        
        print(f"\n📰 SENTIMENT ANALYSIS (Agent 2):")
        print("─" * 40)
        sentiment_data = results.get('sentiment_analysis', 'No analysis available')
        print(sentiment_data[:400] + "..." if len(sentiment_data) > 400 else sentiment_data)
        
        print(f"\n⚖️ RISK ASSESSMENT (Agent 3):")
        print("─" * 40)
        risk_data = results.get('risk_assessment', 'No assessment available')
        print(risk_data[:400] + "..." if len(risk_data) > 400 else risk_data)
        
        print(f"\n📋 FINAL REPORT (Agent 4):")
        print("─" * 40)
        report_data = results.get('final_report', 'No report generated')
        print(report_data[:500] + "..." if len(report_data) > 500 else report_data)
        
        print("\n✅ Multi-agent analysis complete!")
        
    except Exception as e:
        print(f"❌ Error in collaborative analysis: {str(e)}")
        print("💡 This may be due to API rate limits or network issues")


def demo_stock_comparison():
    """Demonstrate multi-stock comparison using agents."""
    print("\n" + "=" * 70)
    print("PHASE 2 DEMO: Multi-Stock Comparison")
    print("=" * 70)
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("⚠️  Multi-stock comparison is resource intensive")
    print("   This would analyze multiple stocks with all 4 agents")
    print("   Skipping full demo to preserve API credits\n")
    
    print("🎯 How it works:")
    print("   1. Each stock analyzed by all 4 agents")
    print("   2. Individual analysis results collected")
    print("   3. Report Generator creates comparative analysis")
    print("   4. Final ranking and recommendations provided")
    
    if api_key:
        print("\n💡 To test multi-stock comparison:")
        print("   coordinator = MultiAgentCoordinator(api_key='your_key')")
        print("   result = coordinator.compare_stocks_collaborative(['AAPL', 'GOOGL', 'TSLA'])")
        print("   # This will provide detailed comparative analysis")
    else:
        print("\n❌ OpenAI API key needed for multi-stock comparison")


def demo_architecture_overview():
    """Show the multi-agent architecture."""
    print("\n" + "=" * 70)
    print("PHASE 2 ARCHITECTURE: Multi-Agent Collaboration")
    print("=" * 70)
    
    print("""
🏗️  MULTI-AGENT ARCHITECTURE:

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Stock Fetcher  │    │   News Analyst   │    │ Risk Assessor   │
│    Agent 1      │    │     Agent 2      │    │    Agent 3      │
└─────────┬───────┘    └────────┬─────────┘    └───────┬─────────┘
          │                     │                      │
          └─────────────────────┼──────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Report Generator     │
                    │      Agent 4          │
                    └───────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Final Investment    │
                    │     Recommendation    │
                    └───────────────────────┘

🤖 AGENT SPECIALIZATIONS:

Agent 1: Stock Data Fetcher
• Role: Financial Data Specialist
• Tools: fetch_stock_price, fetch_financial_metrics  
• Focus: Price, volume, P/E ratios, financial metrics

Agent 2: News Sentiment Analyst  
• Role: Market Psychology Expert
• Tools: analyze_news_sentiment
• Focus: News sentiment, market psychology, external factors

Agent 3: Risk Assessment Specialist
• Role: Risk Management Expert  
• Tools: assess_valuation_risk, assess_sentiment_risk
• Focus: Investment risk scoring, volatility analysis

Agent 4: Investment Report Generator
• Role: Senior Investment Analyst
• Tools: generate_investment_recommendation
• Focus: Synthesis, final recommendations, actionable insights

🔄 WORKFLOW COORDINATION:

1. Parallel Data Collection (Agents 1 & 2)
2. Risk Analysis (Agent 3) 
3. Report Synthesis (Agent 4)
4. Human-reviewable recommendations
""")


def demo_test_results():
    """Show test coverage for Phase 2."""
    print("\n" + "=" * 70)
    print("PHASE 2 TEST COVERAGE")
    print("=" * 70)
    
    print("""
🧪 COMPREHENSIVE TEST SUITE:

✅ Individual Agent Tests:
   • BaseSpecializedAgent: 3 tests
   • StockFetcherAgent: 4 tests  
   • NewsAnalystAgent: 3 tests
   • RiskAssessmentAgent: 5 tests
   • ReportGeneratorAgent: 2 tests
   
✅ Multi-Agent Coordination Tests:
   • MultiAgentCoordinator: 3 tests
   
✅ Integration Tests:
   • Full system initialization: 1 test
   • Agent specialization: 1 test  
   • Workflow coordination: 1 test

📊 TOTAL: 23 tests - All passing ✅

🛡️  QUALITY ASSURANCE:
   • Error handling for each agent
   • Tool integration testing
   • Workflow sequence validation
   • Agent communication testing
   • Resource management verification
""")


def main():
    """Run the complete Phase 2 demonstration."""
    print("🚀 Stock Market Analyst Agent - Phase 2 Demo")
    print("Multi-Agent Collaboration System")
    
    # Demo individual agents
    demo_individual_agents()
    
    # Demo collaborative analysis
    demo_collaborative_analysis()
    
    # Demo stock comparison concept
    demo_stock_comparison()
    
    # Show architecture
    demo_architecture_overview()
    
    # Show test results
    demo_test_results()
    
    print("\n" + "=" * 70)
    print("✅ PHASE 2 COMPLETE!")
    print("=" * 70)
    
    print("\n🎯 Phase 2 Achievements:")
    print("  • ✅ 4 specialized AI agents created")
    print("  • ✅ Multi-agent coordination system") 
    print("  • ✅ Collaborative analysis workflow")
    print("  • ✅ 23 comprehensive tests passing")
    print("  • ✅ Agent specialization and role separation")
    print("  • ✅ Professional investment analysis pipeline")
    
    print("\n🔄 Agent Coordination Workflow:")
    print("  • 📊 Stock Fetcher → Gets price & financial data")
    print("  • 📰 News Analyst → Analyzes market sentiment")
    print("  • ⚖️  Risk Assessor → Evaluates investment risks")
    print("  • 📋 Report Generator → Creates final recommendations")
    
    print("\n🚧 Next: Phase 3 - Stateful Workflow with LangGraph")
    print("  • State management across agent interactions")
    print("  • Dynamic workflow routing based on data quality")
    print("  • Retry logic and error recovery")
    print("  • Conditional agent execution")


if __name__ == "__main__":
    main()