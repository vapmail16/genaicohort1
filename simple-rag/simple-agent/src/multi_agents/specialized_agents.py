"""
Phase 2: Multi-Agent Collaboration System

This module implements specialized agents that work together:
- StockFetcherAgent: Gathers stock price and financial data
- NewsAnalystAgent: Analyzes news sentiment and market news
- RiskAssessmentAgent: Evaluates risk factors and scoring
- ReportGeneratorAgent: Creates comprehensive reports
"""

import os
from typing import Dict, Any, List, Optional
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from src.tools.stock_tools import get_stock_price, get_pe_ratio, get_news_sentiment


class BaseSpecializedAgent:
    """Base class for specialized agents."""
    
    def __init__(self, name: str, role: str, goal: str, api_key: str, model: str = "gpt-3.5-turbo"):
        self.name = name
        self.role = role
        self.goal = goal
        self.api_key = api_key
        self.llm = ChatOpenAI(api_key=api_key, model=model, temperature=0.1)
        self.tools = self._create_tools()
        self._setup_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Override in subclasses to define specific tools."""
        return []
    
    def _setup_agent(self):
        """Setup the agent with prompt and tools."""
        prompt_template = f"""
You are {self.name}, a {self.role}.

Your goal: {self.goal}

You have access to the following tools:
{{tools}}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{input}}
Thought:{{agent_scratchpad}}
"""
        
        prompt = PromptTemplate.from_template(prompt_template)
        agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def execute(self, task: str) -> str:
        """Execute a task and return the result."""
        try:
            response = self.agent_executor.invoke({"input": task})
            return response.get("output", "No output generated")
        except Exception as e:
            return f"Error in {self.name}: {str(e)}"


class StockFetcherAgent(BaseSpecializedAgent):
    """Agent specialized in fetching stock price and financial data."""
    
    def __init__(self, api_key: str):
        super().__init__(
            name="Stock Data Fetcher",
            role="Financial Data Specialist",
            goal="Retrieve accurate and up-to-date stock prices, P/E ratios, and financial metrics",
            api_key=api_key
        )
    
    def _create_tools(self) -> List[Tool]:
        def fetch_stock_price(ticker: str) -> str:
            """Fetch current stock price and trading data."""
            result = get_stock_price(ticker)
            if "error" in result:
                return f"Unable to fetch price for {ticker}: {result['error']}"
            
            return f"""Stock Price Data for {ticker}:
• Current Price: ${result['current_price']}
• Previous Close: ${result['previous_close']}  
• Change: ${result['change']} ({result['change_percent']}%)
• Volume: {result['volume']:,}
• Market Cap: {result.get('market_cap', 'N/A')}
• Timestamp: {result['timestamp']}"""
        
        def fetch_financial_metrics(ticker: str) -> str:
            """Fetch P/E ratios and financial metrics."""
            result = get_pe_ratio(ticker)
            if "error" in result:
                return f"Unable to fetch financial metrics for {ticker}: {result['error']}"
            
            return f"""Financial Metrics for {ticker}:
• P/E Ratio: {result['pe_ratio']}
• Forward P/E: {result['forward_pe']}
• PEG Ratio: {result['peg_ratio']}
• Price-to-Book: {result['price_to_book']}
• EPS: {result['eps']}
• Revenue: {result.get('revenue', 'N/A')}
• Timestamp: {result['timestamp']}"""
        
        return [
            Tool(
                name="fetch_stock_price",
                func=fetch_stock_price,
                description="Fetch current stock price, volume, and market data for a ticker symbol"
            ),
            Tool(
                name="fetch_financial_metrics", 
                func=fetch_financial_metrics,
                description="Fetch P/E ratio, EPS, revenue and other financial metrics for a ticker symbol"
            )
        ]


class NewsAnalystAgent(BaseSpecializedAgent):
    """Agent specialized in analyzing news sentiment and market psychology."""
    
    def __init__(self, api_key: str, news_api_key: Optional[str] = None):
        self.news_api_key = news_api_key
        super().__init__(
            name="News Sentiment Analyst",
            role="Market Psychology Expert", 
            goal="Analyze news sentiment, market psychology, and external factors affecting stock performance",
            api_key=api_key
        )
    
    def _create_tools(self) -> List[Tool]:
        def analyze_news_sentiment(ticker: str) -> str:
            """Analyze news sentiment for a stock."""
            result = get_news_sentiment(ticker, self.news_api_key)
            if "error" in result:
                return f"Unable to analyze sentiment for {ticker}: {result['error']}"
            
            sentiment_emoji = {
                'positive': '📈',
                'negative': '📉', 
                'neutral': '➡️'
            }
            
            return f"""News Sentiment Analysis for {ticker}:
• Sentiment: {sentiment_emoji.get(result['sentiment_label'], '')} {result['sentiment_label'].upper()}
• Score: {result['sentiment_score']} (Range: -1 to +1)
• News Articles Analyzed: {result['news_count']}
• Recent Headlines:
{chr(10).join([f"  - {headline}" for headline in result['top_headlines']])}
• Analysis Timestamp: {result['timestamp']}

Market Psychology Insight: 
{self._interpret_sentiment(result['sentiment_score'], result['sentiment_label'])}"""
        
        return [
            Tool(
                name="analyze_news_sentiment",
                func=analyze_news_sentiment,
                description="Analyze recent news sentiment and market psychology for a stock ticker"
            )
        ]
    
    def _interpret_sentiment(self, score: float, label: str) -> str:
        """Provide psychological interpretation of sentiment."""
        if score > 0.3:
            return "Strong positive momentum - market confidence is high"
        elif score > 0.1:
            return "Cautiously optimistic - moderate positive sentiment"
        elif score > -0.1:
            return "Market neutrality - mixed signals from news flow"
        elif score > -0.3:
            return "Moderate concern - some negative sentiment present"
        else:
            return "Significant negative sentiment - market caution advised"


class RiskAssessmentAgent(BaseSpecializedAgent):
    """Agent specialized in risk assessment and scoring."""
    
    def __init__(self, api_key: str):
        super().__init__(
            name="Risk Assessment Specialist",
            role="Risk Management Expert",
            goal="Evaluate investment risk factors, volatility, and provide risk scores with detailed analysis",
            api_key=api_key
        )
    
    def _create_tools(self) -> List[Tool]:
        def assess_valuation_risk(metrics_string: str) -> str:
            """Assess valuation risk based on financial metrics."""
            try:
                # Parse input string format: "pe_ratio,forward_pe,peg_ratio"
                parts = metrics_string.split(',')
                pe_ratio = parts[0] if len(parts) > 0 else None
                forward_pe = parts[1] if len(parts) > 1 else None
                peg_ratio = parts[2] if len(parts) > 2 else None
                
                pe = float(pe_ratio) if pe_ratio and pe_ratio != 'None' else None
                fpe = float(forward_pe) if forward_pe and forward_pe != 'None' else None
                peg = float(peg_ratio) if peg_ratio and peg_ratio != 'None' else None
                
                risk_factors = []
                risk_score = 0  # 0-10 scale
                
                # P/E Risk Assessment
                if pe:
                    if pe < 15:
                        risk_factors.append("✅ Low P/E suggests undervaluation or value opportunity")
                        risk_score += 1
                    elif pe < 25:
                        risk_factors.append("⚠️ Moderate P/E - fair valuation range")
                        risk_score += 3
                    elif pe < 40:
                        risk_factors.append("🔴 High P/E - overvaluation risk")
                        risk_score += 6
                    else:
                        risk_factors.append("🚨 Very high P/E - significant overvaluation risk")
                        risk_score += 8
                
                # PEG Risk Assessment  
                if peg:
                    if peg < 1.0:
                        risk_factors.append("✅ PEG < 1.0 suggests growth at reasonable price")
                    elif peg < 1.5:
                        risk_factors.append("⚠️ PEG moderately elevated - monitor growth sustainability")
                        risk_score += 2
                    else:
                        risk_factors.append("🔴 High PEG - growth expectations may be unrealistic")
                        risk_score += 4
                
                # Forward P/E comparison
                if pe and fpe:
                    pe_trend = "improving" if fpe < pe else "declining"
                    risk_factors.append(f"📊 Forward P/E trend: {pe_trend}")
                
                risk_level = "LOW" if risk_score <= 3 else "MODERATE" if risk_score <= 6 else "HIGH"
                
                return f"""Valuation Risk Assessment:
• Overall Risk Level: {risk_level} ({risk_score}/10)
• Key Risk Factors:
{chr(10).join([f"  {factor}" for factor in risk_factors])}
• Recommendation: {"Suitable for conservative investors" if risk_score <= 3 else "Requires careful monitoring" if risk_score <= 6 else "High-risk investment - caution advised"}"""
                
            except Exception as e:
                return f"Error in valuation risk assessment: {str(e)}"
        
        def assess_sentiment_risk(sentiment_string: str) -> str:
            """Assess risk based on market sentiment."""
            try:
                # Parse input string format: "sentiment_score,sentiment_label"
                parts = sentiment_string.split(',')
                sentiment_score = parts[0] if len(parts) > 0 else "0"
                sentiment_label = parts[1] if len(parts) > 1 else "neutral"
                
                score = float(sentiment_score)
                
                if score >= 0.2:
                    risk_level = "LOW"
                    risk_desc = "Positive market sentiment reduces short-term volatility risk"
                elif score >= -0.2:
                    risk_level = "MODERATE" 
                    risk_desc = "Neutral sentiment suggests balanced risk-reward"
                else:
                    risk_level = "HIGH"
                    risk_desc = "Negative sentiment increases volatility and downside risk"
                
                return f"""Sentiment Risk Assessment:
• Risk Level: {risk_level}
• Analysis: {risk_desc}
• Score Impact: {score} indicates {sentiment_label} market psychology
• Short-term Volatility: {"Expected" if abs(score) > 0.3 else "Moderate" if abs(score) > 0.1 else "Low"}"""
                
            except Exception as e:
                return f"Error in sentiment risk assessment: {str(e)}"
        
        return [
            Tool(
                name="assess_valuation_risk",
                func=assess_valuation_risk,
                description="Assess valuation risk using P/E ratio, Forward P/E, and PEG ratio. Input format: 'pe_ratio,forward_pe,peg_ratio'"
            ),
            Tool(
                name="assess_sentiment_risk", 
                func=assess_sentiment_risk,
                description="Assess risk based on sentiment score and label. Input format: 'sentiment_score,sentiment_label'"
            )
        ]


class ReportGeneratorAgent(BaseSpecializedAgent):
    """Agent specialized in creating comprehensive investment reports."""
    
    def __init__(self, api_key: str):
        super().__init__(
            name="Investment Report Generator",
            role="Senior Investment Analyst",
            goal="Synthesize all analysis into clear, actionable investment reports with recommendations",
            api_key=api_key
        )
    
    def _create_tools(self) -> List[Tool]:
        def generate_investment_recommendation(analysis_data: str) -> str:
            """Generate final investment recommendation based on all analysis."""
            # This tool processes the combined analysis from other agents
            return f"""Processing combined analysis to generate investment recommendation...

Analysis Data Received:
{analysis_data}

Generating comprehensive report with:
• Executive Summary
• Risk-Reward Analysis  
• Investment Recommendation
• Price Targets and Timeline
• Key Monitoring Points"""
        
        return [
            Tool(
                name="generate_investment_recommendation",
                func=generate_investment_recommendation,
                description="Generate final investment recommendation based on combined analysis from all agents"
            )
        ]


class MultiAgentCoordinator:
    """Coordinates multiple specialized agents to work together."""
    
    def __init__(self, api_key: str, news_api_key: Optional[str] = None):
        self.api_key = api_key
        self.news_api_key = news_api_key
        
        # Initialize specialized agents
        self.stock_fetcher = StockFetcherAgent(api_key)
        self.news_analyst = NewsAnalystAgent(api_key, news_api_key)
        self.risk_assessor = RiskAssessmentAgent(api_key)
        self.report_generator = ReportGeneratorAgent(api_key)
    
    def analyze_stock_collaborative(self, ticker: str) -> Dict[str, Any]:
        """Perform collaborative stock analysis using multiple agents."""
        print(f"🚀 Starting multi-agent analysis for {ticker}...")
        results = {}
        
        # Step 1: Stock Data Fetcher Agent
        print("📊 Agent 1: Fetching stock data...")
        price_task = f"Fetch current stock price and trading data for {ticker}"
        results['price_data'] = self.stock_fetcher.execute(price_task)
        
        metrics_task = f"Fetch financial metrics including P/E ratios for {ticker}" 
        results['financial_metrics'] = self.stock_fetcher.execute(metrics_task)
        
        # Step 2: News Analyst Agent
        print("📰 Agent 2: Analyzing news sentiment...")
        sentiment_task = f"Analyze recent news sentiment and market psychology for {ticker}"
        results['sentiment_analysis'] = self.news_analyst.execute(sentiment_task)
        
        # Step 3: Risk Assessment Agent
        print("⚖️ Agent 3: Assessing investment risks...")
        # Extract metrics for risk assessment (simplified for demo)
        risk_task = f"Based on the analysis of {ticker}, assess overall investment risk considering both valuation metrics and market sentiment"
        results['risk_assessment'] = self.risk_assessor.execute(risk_task)
        
        # Step 4: Report Generator Agent
        print("📄 Agent 4: Generating comprehensive report...")
        combined_analysis = f"""
STOCK: {ticker}

PRICE DATA:
{results.get('price_data', 'Data unavailable')}

FINANCIAL METRICS:
{results.get('financial_metrics', 'Data unavailable')}

SENTIMENT ANALYSIS:
{results.get('sentiment_analysis', 'Analysis unavailable')}

RISK ASSESSMENT:
{results.get('risk_assessment', 'Assessment unavailable')}
"""
        
        report_task = f"Create a comprehensive investment report for {ticker} based on the following multi-agent analysis: {combined_analysis}"
        results['final_report'] = self.report_generator.execute(report_task)
        
        print("✅ Multi-agent analysis complete!")
        return results
    
    def compare_stocks_collaborative(self, tickers: List[str]) -> Dict[str, Any]:
        """Compare multiple stocks using collaborative agent analysis."""
        print(f"🔄 Starting multi-agent comparison of {', '.join(tickers)}...")
        
        # Analyze each stock with all agents
        stock_analyses = {}
        for ticker in tickers:
            print(f"\n📈 Analyzing {ticker}...")
            stock_analyses[ticker] = self.analyze_stock_collaborative(ticker)
        
        # Generate comparative report
        print("\n📊 Generating comparative analysis...")
        comparison_data = ""
        for ticker, analysis in stock_analyses.items():
            comparison_data += f"\n{ticker} ANALYSIS:\n{analysis.get('final_report', 'No report generated')}\n" + "="*50
        
        comparison_task = f"Compare and rank the following stocks based on their analysis: {comparison_data}"
        comparative_report = self.report_generator.execute(comparison_task)
        
        return {
            'individual_analyses': stock_analyses,
            'comparative_report': comparative_report
        }