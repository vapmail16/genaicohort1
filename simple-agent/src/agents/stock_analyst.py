"""Stock Market Analyst Agent using LangChain with tool binding."""

import os
from typing import Dict, Any, List
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub

from src.tools.stock_tools import get_stock_price, get_pe_ratio, get_news_sentiment


class StockAnalystAgent:
    """A LangChain agent that analyzes stocks using bound tools."""
    
    def __init__(self, api_key: str = None, news_api_key: str = None):
        """
        Initialize the Stock Analyst Agent.
        
        Args:
            api_key: OpenAI API key
            news_api_key: News API key for sentiment analysis
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.news_api_key = news_api_key or os.getenv("NEWS_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model="gpt-3.5-turbo",
            temperature=0.1
        )
        
        # Create tools
        self.tools = self._create_tools()
        
        # Get react prompt from hub
        try:
            self.prompt = hub.pull("hwchase17/react")
        except:
            # Fallback prompt if hub is not available
            self.prompt = """You are a helpful assistant that can use tools to answer questions.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
        
        # Create agent
        agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def _create_tools(self) -> List[Tool]:
        """Create LangChain tools from our stock functions."""
        
        def stock_price_tool(ticker: str) -> str:
            """Get current stock price and basic information."""
            result = get_stock_price(ticker)
            if "error" in result:
                return f"Error: {result['error']}"
            return f"""Stock: {result['ticker']}
Current Price: ${result['current_price']}
Previous Close: ${result['previous_close']}
Change: ${result['change']} ({result['change_percent']}%)
Volume: {result['volume']:,}
Market Cap: ${result.get('market_cap', 'N/A'):,}"""
        
        def pe_ratio_tool(ticker: str) -> str:
            """Get P/E ratio and financial metrics."""
            result = get_pe_ratio(ticker)
            if "error" in result:
                return f"Error: {result['error']}"
            return f"""Stock: {result['ticker']}
P/E Ratio: {result['pe_ratio']}
Forward P/E: {result['forward_pe']}
PEG Ratio: {result['peg_ratio']}
Price-to-Book: {result['price_to_book']}
EPS: {result['eps']}
Revenue: ${result.get('revenue', 'N/A'):,}"""
        
        def news_sentiment_tool(ticker: str) -> str:
            """Get news sentiment analysis for a stock."""
            result = get_news_sentiment(ticker, self.news_api_key)
            if "error" in result:
                return f"Error: {result['error']}"
            return f"""Stock: {result['ticker']}
Sentiment Score: {result['sentiment_score']} (Range: -1 to 1)
Sentiment: {result['sentiment_label'].upper()}
News Articles: {result['news_count']}
Top Headlines:
""" + "\n".join([f"- {headline}" for headline in result['top_headlines']])
        
        return [
            Tool(
                name="get_stock_price",
                func=stock_price_tool,
                description="Get current stock price, change, volume, and market cap for a given ticker symbol"
            ),
            Tool(
                name="get_pe_ratio",
                func=pe_ratio_tool,
                description="Get P/E ratio, PEG ratio, price-to-book ratio and other financial metrics for a stock ticker"
            ),
            Tool(
                name="get_news_sentiment",
                func=news_sentiment_tool,
                description="Get recent news sentiment analysis for a stock ticker symbol"
            )
        ]
    
    def analyze_stock(self, ticker: str) -> str:
        """
        Perform comprehensive stock analysis.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Comprehensive analysis string
        """
        prompt = f"""
        You are a professional stock market analyst. Analyze the stock {ticker} by:
        
        1. Getting current stock price information
        2. Fetching P/E ratio and financial metrics  
        3. Analyzing recent news sentiment
        4. Providing a comprehensive analysis with:
           - Current market position
           - Valuation assessment (overvalued/undervalued/fairly valued)
           - Risk factors based on metrics and news
           - Investment recommendation (Buy/Hold/Sell) with reasoning
        
        Use the available tools to gather all necessary data, then provide a clear, professional analysis.
        """
        
        try:
            response = self.agent_executor.invoke({"input": prompt})
            return response.get("output", "No analysis generated")
        except Exception as e:
            return f"Error during analysis: {str(e)}"
    
    def compare_stocks(self, tickers: List[str]) -> str:
        """
        Compare multiple stocks.
        
        Args:
            tickers: List of stock ticker symbols
            
        Returns:
            Comparative analysis string
        """
        if len(tickers) < 2:
            return "At least 2 stocks are required for comparison"
        
        ticker_list = ", ".join(tickers)
        prompt = f"""
        You are a professional stock market analyst. Compare these stocks: {ticker_list}
        
        For each stock, gather:
        1. Current price and market performance
        2. P/E ratio and financial metrics
        3. Recent news sentiment
        
        Then provide a comparative analysis including:
        - Performance comparison
        - Valuation comparison 
        - Risk assessment comparison
        - Which stock(s) you would recommend and why
        - Ranking from most to least attractive for investment
        
        Use the available tools to gather data for all stocks.
        """
        
        try:
            response = self.agent_executor.invoke({"input": prompt})
            return response.get("output", "No comparison generated")
        except Exception as e:
            return f"Error during comparison: {str(e)}"
    
    def quick_sentiment_check(self, ticker: str) -> Dict[str, Any]:
        """
        Quick sentiment check without full analysis.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with sentiment data
        """
        try:
            return get_news_sentiment(ticker, self.news_api_key)
        except Exception as e:
            return {"error": f"Error getting sentiment for {ticker}: {str(e)}"}
    
    def get_current_metrics(self, ticker: str) -> Dict[str, Any]:
        """
        Get current stock metrics without analysis.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Combined price and financial metrics
        """
        try:
            price_data = get_stock_price(ticker)
            pe_data = get_pe_ratio(ticker)
            
            # Combine data
            combined = {}
            if "error" not in price_data:
                combined.update(price_data)
            if "error" not in pe_data:
                combined.update({k: v for k, v in pe_data.items() if k != "ticker"})
                
            return combined if combined else {"error": "Failed to get stock data"}
        except Exception as e:
            return {"error": f"Error getting metrics for {ticker}: {str(e)}"}