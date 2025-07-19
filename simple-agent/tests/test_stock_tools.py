"""Tests for stock market data tools."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import datetime

from src.tools.stock_tools import get_stock_price, get_pe_ratio, get_news_sentiment


class TestGetStockPrice:
    """Tests for get_stock_price function."""
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_get_stock_price_success(self, mock_ticker):
        """Test successful stock price retrieval."""
        # Mock yfinance response
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        
        # Create mock price history
        mock_history = pd.DataFrame({
            'Close': [150.0, 155.0],
            'Volume': [1000000, 1100000]
        })
        mock_stock.history.return_value = mock_history
        mock_stock.info = {'marketCap': 2500000000}
        
        result = get_stock_price('AAPL')
        
        assert result['ticker'] == 'AAPL'
        assert result['current_price'] == 155.0
        assert result['previous_close'] == 150.0
        assert result['change'] == 5.0
        assert result['change_percent'] == 3.33
        assert result['volume'] == 1100000
        assert result['market_cap'] == 2500000000
        assert 'timestamp' in result
        assert 'error' not in result
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_get_stock_price_empty_data(self, mock_ticker):
        """Test handling of empty stock data."""
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        mock_stock.history.return_value = pd.DataFrame()  # Empty DataFrame
        
        result = get_stock_price('INVALID')
        
        assert 'error' in result
        assert 'INVALID' in result['error']
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_get_stock_price_single_day_data(self, mock_ticker):
        """Test with single day of data (no previous close)."""
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        
        mock_history = pd.DataFrame({
            'Close': [150.0],
            'Volume': [1000000]
        })
        mock_stock.history.return_value = mock_history
        mock_stock.info = {}
        
        result = get_stock_price('AAPL')
        
        assert result['current_price'] == 150.0
        assert result['previous_close'] == 150.0
        assert result['change'] == 0.0
        assert result['change_percent'] == 0.0
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_get_stock_price_exception(self, mock_ticker):
        """Test exception handling."""
        mock_ticker.side_effect = Exception("Network error")
        
        result = get_stock_price('AAPL')
        
        assert 'error' in result
        assert 'AAPL' in result['error']
        assert 'Network error' in result['error']


class TestGetPeRatio:
    """Tests for get_pe_ratio function."""
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_get_pe_ratio_success(self, mock_ticker):
        """Test successful P/E ratio retrieval."""
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        mock_stock.info = {
            'trailingPE': 25.5,
            'forwardPE': 22.3,
            'pegRatio': 1.2,
            'priceToBook': 3.1,
            'trailingEps': 6.11,
            'totalRevenue': 365000000000
        }
        
        result = get_pe_ratio('AAPL')
        
        assert result['ticker'] == 'AAPL'
        assert result['pe_ratio'] == 25.5
        assert result['forward_pe'] == 22.3
        assert result['peg_ratio'] == 1.2
        assert result['price_to_book'] == 3.1
        assert result['eps'] == 6.11
        assert result['revenue'] == 365000000000
        assert 'timestamp' in result
        assert 'error' not in result
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_get_pe_ratio_missing_data(self, mock_ticker):
        """Test with missing P/E data."""
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        mock_stock.info = {}  # Empty info
        
        result = get_pe_ratio('STARTUP')
        
        assert result['ticker'] == 'STARTUP'
        assert result['pe_ratio'] is None
        assert result['forward_pe'] is None
        assert 'timestamp' in result
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_get_pe_ratio_exception(self, mock_ticker):
        """Test exception handling."""
        mock_ticker.side_effect = Exception("API error")
        
        result = get_pe_ratio('AAPL')
        
        assert 'error' in result
        assert 'API error' in result['error']


class TestGetNewsSentiment:
    """Tests for get_news_sentiment function."""
    
    def test_get_news_sentiment_mock_data(self):
        """Test with mock data (no API key)."""
        result = get_news_sentiment('AAPL')
        
        assert result['ticker'] == 'AAPL'
        assert -1 <= result['sentiment_score'] <= 1
        assert result['sentiment_label'] in ['positive', 'negative', 'neutral']
        assert result['news_count'] == 5
        assert len(result['top_headlines']) == 3
        assert 'timestamp' in result
        assert 'error' not in result
    
    @patch('src.tools.stock_tools.requests.get')
    def test_get_news_sentiment_with_api(self, mock_get):
        """Test with real API call."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Apple reports strong quarterly growth'},
                {'title': 'Analysts upgrade Apple stock rating'},
                {'title': 'Apple announces new iPhone launch'},
                {'title': 'Apple stock hits new high'},
                {'title': 'Apple beats earnings expectations'}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_news_sentiment('AAPL', api_key='test_key')
        
        assert result['ticker'] == 'AAPL'
        assert result['sentiment_score'] > 0  # Should be positive due to keywords
        assert result['sentiment_label'] == 'positive'
        assert result['news_count'] == 5
        assert len(result['top_headlines']) == 5
        
        # Verify API was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'newsapi.org' in args[0]
        assert 'apiKey' in kwargs['params']
        assert kwargs['params']['apiKey'] == 'test_key'
    
    @patch('src.tools.stock_tools.requests.get')
    def test_get_news_sentiment_negative(self, mock_get):
        """Test negative sentiment calculation."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Apple stock downgraded by analysts'},
                {'title': 'Apple reports weak quarterly results'},
                {'title': 'Apple stock decline continues'},
                {'title': 'Apple misses earnings expectations'},
                {'title': 'Analysts recommend sell on Apple'}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_news_sentiment('AAPL', api_key='test_key')
        
        assert result['sentiment_score'] < 0
        assert result['sentiment_label'] == 'negative'
    
    @patch('src.tools.stock_tools.requests.get')
    def test_get_news_sentiment_neutral(self, mock_get):
        """Test neutral sentiment calculation."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Apple announces quarterly results'},
                {'title': 'Apple holds investor meeting'},
                {'title': 'Apple stock trading sideways'},
                {'title': 'Apple maintains market position'},
                {'title': 'Apple reports standard earnings'}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_news_sentiment('AAPL', api_key='test_key')
        
        assert -0.1 <= result['sentiment_score'] <= 0.1
        assert result['sentiment_label'] == 'neutral'
    
    @patch('src.tools.stock_tools.requests.get')
    def test_get_news_sentiment_api_error(self, mock_get):
        """Test API error handling."""
        mock_get.side_effect = Exception("API timeout")
        
        result = get_news_sentiment('AAPL', api_key='test_key')
        
        assert 'error' in result
        assert 'API timeout' in result['error']
    
    @patch('src.tools.stock_tools.requests.get')
    def test_get_news_sentiment_no_articles(self, mock_get):
        """Test handling of no articles returned."""
        mock_response = Mock()
        mock_response.json.return_value = {'articles': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_news_sentiment('UNKNOWN', api_key='test_key')
        
        assert result['sentiment_score'] == 0
        assert result['sentiment_label'] == 'neutral'
        assert result['news_count'] == 0
        assert result['top_headlines'] == []


class TestIntegration:
    """Integration tests combining multiple tools."""
    
    @patch('src.tools.stock_tools.yf.Ticker')
    def test_multiple_tools_same_ticker(self, mock_ticker):
        """Test using multiple tools on the same ticker."""
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        
        # Mock stock price data
        mock_history = pd.DataFrame({
            'Close': [150.0, 155.0],
            'Volume': [1000000, 1100000]
        })
        mock_stock.history.return_value = mock_history
        mock_stock.info = {
            'marketCap': 2500000000,
            'trailingPE': 25.5,
            'forwardPE': 22.3
        }
        
        # Get all data
        price_data = get_stock_price('AAPL')
        pe_data = get_pe_ratio('AAPL')
        sentiment_data = get_news_sentiment('AAPL')
        
        # Verify all successful
        assert 'error' not in price_data
        assert 'error' not in pe_data
        assert 'error' not in sentiment_data
        
        # Verify consistent ticker
        assert price_data['ticker'] == pe_data['ticker'] == sentiment_data['ticker'] == 'AAPL'