"""Stock market data tools for the analyst agent."""

import yfinance as yf
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


def get_stock_price(ticker: str) -> Dict[str, Any]:
    """
    Get current stock price and basic info.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
        Dict containing price info or error message
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")
        
        if hist.empty:
            return {"error": f"No data found for ticker {ticker}"}
            
        current_price = hist['Close'].iloc[-1]
        previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close else 0
        
        return {
            "ticker": ticker,
            "current_price": round(float(current_price), 2),
            "previous_close": round(float(previous_close), 2),
            "change": round(float(change), 2),
            "change_percent": round(float(change_percent), 2),
            "volume": int(hist['Volume'].iloc[-1]),
            "market_cap": info.get('marketCap'),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"Error fetching data for {ticker}: {str(e)}"}


def get_pe_ratio(ticker: str) -> Dict[str, Any]:
    """
    Get P/E ratio and related financial metrics.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Dict containing P/E ratio and financial metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        pe_ratio = info.get('trailingPE')
        forward_pe = info.get('forwardPE')
        peg_ratio = info.get('pegRatio')
        price_to_book = info.get('priceToBook')
        
        return {
            "ticker": ticker,
            "pe_ratio": pe_ratio,
            "forward_pe": forward_pe,
            "peg_ratio": peg_ratio,
            "price_to_book": price_to_book,
            "eps": info.get('trailingEps'),
            "revenue": info.get('totalRevenue'),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"Error fetching P/E data for {ticker}: {str(e)}"}


def get_news_sentiment(ticker: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Get news sentiment for a stock ticker.
    
    Args:
        ticker: Stock ticker symbol
        api_key: News API key (optional, will use mock data if not provided)
    
    Returns:
        Dict containing news sentiment analysis
    """
    try:
        if not api_key:
            # Mock sentiment data for testing
            return {
                "ticker": ticker,
                "sentiment_score": 0.2,  # Scale: -1 (very negative) to 1 (very positive)
                "sentiment_label": "neutral",
                "news_count": 5,
                "top_headlines": [
                    f"{ticker} reports quarterly earnings",
                    f"Analysts upgrade {ticker} rating",
                    f"{ticker} announces new product launch"
                ],
                "timestamp": datetime.now().isoformat()
            }
        
        # Real API implementation (placeholder)
        company_name = ticker  # In real implementation, map ticker to company name
        url = f"https://newsapi.org/v2/everything"
        params = {
            'q': company_name,
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': api_key,
            'from': (datetime.now() - timedelta(days=7)).date().isoformat()
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])
        headlines = [article['title'] for article in articles[:5]]
        
        # Simple sentiment calculation (in real implementation, use NLP model)
        positive_keywords = ['upgrade', 'buy', 'strong', 'growth', 'profit', 'beat']
        negative_keywords = ['downgrade', 'sell', 'weak', 'loss', 'miss', 'decline']
        
        sentiment_score = 0
        for headline in headlines:
            headline_lower = headline.lower()
            sentiment_score += sum(0.2 for word in positive_keywords if word in headline_lower)
            sentiment_score -= sum(0.2 for word in negative_keywords if word in headline_lower)
        
        sentiment_score = max(-1, min(1, sentiment_score / len(headlines) if headlines else 0))
        
        if sentiment_score > 0.1:
            sentiment_label = "positive"
        elif sentiment_score < -0.1:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        return {
            "ticker": ticker,
            "sentiment_score": round(sentiment_score, 2),
            "sentiment_label": sentiment_label,
            "news_count": len(articles),
            "top_headlines": headlines,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Error fetching news sentiment for {ticker}: {str(e)}"}