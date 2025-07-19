"""Tests for Stock Analyst Agent."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os

from src.agents.stock_analyst import StockAnalystAgent


class TestStockAnalystAgent:
    """Tests for StockAnalystAgent class."""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_init_with_env_var(self):
        """Test initialization with environment variable."""
        agent = StockAnalystAgent()
        assert agent.api_key == 'test_key'
        assert agent.llm is not None
        assert len(agent.tools) == 3
    
    def test_init_with_direct_key(self):
        """Test initialization with direct API key."""
        agent = StockAnalystAgent(api_key='direct_key')
        assert agent.api_key == 'direct_key'
    
    def test_init_without_key(self):
        """Test initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                StockAnalystAgent()
    
    def test_create_tools(self):
        """Test tool creation."""
        agent = StockAnalystAgent(api_key='test_key')
        tools = agent.tools
        
        assert len(tools) == 3
        tool_names = [tool.name for tool in tools]
        expected_names = ['get_stock_price', 'get_pe_ratio', 'get_news_sentiment']
        assert all(name in tool_names for name in expected_names)
    
    @patch('src.agents.stock_analyst.get_stock_price')
    def test_stock_price_tool(self, mock_get_stock_price):
        """Test stock price tool functionality."""
        mock_get_stock_price.return_value = {
            'ticker': 'AAPL',
            'current_price': 150.0,
            'previous_close': 145.0,
            'change': 5.0,
            'change_percent': 3.45,
            'volume': 1000000,
            'market_cap': 2500000000
        }
        
        agent = StockAnalystAgent(api_key='test_key')
        price_tool = next(tool for tool in agent.tools if tool.name == 'get_stock_price')
        
        result = price_tool.func('AAPL')
        
        assert 'AAPL' in result
        assert '$150.0' in result
        assert '$145.0' in result
        assert '$5.0' in result
        assert '3.45%' in result
        mock_get_stock_price.assert_called_once_with('AAPL')
    
    @patch('src.agents.stock_analyst.get_stock_price')
    def test_stock_price_tool_error(self, mock_get_stock_price):
        """Test stock price tool error handling."""
        mock_get_stock_price.return_value = {'error': 'Network error'}
        
        agent = StockAnalystAgent(api_key='test_key')
        price_tool = next(tool for tool in agent.tools if tool.name == 'get_stock_price')
        
        result = price_tool.func('INVALID')
        
        assert 'Error: Network error' in result
    
    @patch('src.agents.stock_analyst.get_pe_ratio')
    def test_pe_ratio_tool(self, mock_get_pe_ratio):
        """Test P/E ratio tool functionality."""
        mock_get_pe_ratio.return_value = {
            'ticker': 'AAPL',
            'pe_ratio': 25.5,
            'forward_pe': 22.3,
            'peg_ratio': 1.2,
            'price_to_book': 3.1,
            'eps': 6.11,
            'revenue': 365000000000
        }
        
        agent = StockAnalystAgent(api_key='test_key')
        pe_tool = next(tool for tool in agent.tools if tool.name == 'get_pe_ratio')
        
        result = pe_tool.func('AAPL')
        
        assert 'AAPL' in result
        assert '25.5' in result
        assert '22.3' in result
        assert '1.2' in result
        mock_get_pe_ratio.assert_called_once_with('AAPL')
    
    @patch('src.agents.stock_analyst.get_news_sentiment')
    def test_news_sentiment_tool(self, mock_get_news_sentiment):
        """Test news sentiment tool functionality."""
        mock_get_news_sentiment.return_value = {
            'ticker': 'AAPL',
            'sentiment_score': 0.3,
            'sentiment_label': 'positive',
            'news_count': 5,
            'top_headlines': ['Headline 1', 'Headline 2', 'Headline 3']
        }
        
        agent = StockAnalystAgent(api_key='test_key', news_api_key='news_key')
        sentiment_tool = next(tool for tool in agent.tools if tool.name == 'get_news_sentiment')
        
        result = sentiment_tool.func('AAPL')
        
        assert 'AAPL' in result
        assert '0.3' in result
        assert 'POSITIVE' in result
        assert 'Headline 1' in result
        mock_get_news_sentiment.assert_called_once_with('AAPL', 'news_key')
    
    @patch('src.agents.stock_analyst.create_react_agent')
    @patch('src.agents.stock_analyst.AgentExecutor')
    def test_analyze_stock_success(self, mock_agent_executor_class, mock_create_react_agent):
        """Test successful stock analysis."""
        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Analysis result: AAPL is a strong buy"}
        mock_agent_executor_class.return_value = mock_executor
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.analyze_stock('AAPL')
        
        assert result == "Analysis result: AAPL is a strong buy"
        mock_executor.invoke.assert_called_once()
        call_args = mock_executor.invoke.call_args[0][0]
        assert 'AAPL' in call_args["input"]
        assert 'stock market analyst' in call_args["input"].lower()
    
    @patch('src.agents.stock_analyst.create_react_agent')
    @patch('src.agents.stock_analyst.AgentExecutor')
    def test_analyze_stock_error(self, mock_agent_executor_class, mock_create_react_agent):
        """Test stock analysis error handling."""
        mock_executor = Mock()
        mock_executor.invoke.side_effect = Exception("API error")
        mock_agent_executor_class.return_value = mock_executor
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.analyze_stock('AAPL')
        
        assert "Error during analysis: API error" in result
    
    @patch('src.agents.stock_analyst.create_react_agent')
    @patch('src.agents.stock_analyst.AgentExecutor')
    def test_compare_stocks_success(self, mock_agent_executor_class, mock_create_react_agent):
        """Test successful stock comparison."""
        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Comparison: AAPL > GOOGL > MSFT"}
        mock_agent_executor_class.return_value = mock_executor
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.compare_stocks(['AAPL', 'GOOGL', 'MSFT'])
        
        assert result == "Comparison: AAPL > GOOGL > MSFT"
        mock_executor.invoke.assert_called_once()
        call_args = mock_executor.invoke.call_args[0][0]
        assert 'AAPL, GOOGL, MSFT' in call_args["input"]
    
    def test_compare_stocks_insufficient(self):
        """Test comparison with insufficient stocks."""
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.compare_stocks(['AAPL'])
        
        assert "At least 2 stocks are required" in result
    
    @patch('src.agents.stock_analyst.create_react_agent')
    @patch('src.agents.stock_analyst.AgentExecutor')
    def test_compare_stocks_error(self, mock_agent_executor_class, mock_create_react_agent):
        """Test stock comparison error handling."""
        mock_executor = Mock()
        mock_executor.invoke.side_effect = Exception("Comparison failed")
        mock_agent_executor_class.return_value = mock_executor
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.compare_stocks(['AAPL', 'GOOGL'])
        
        assert "Error during comparison: Comparison failed" in result
    
    @patch('src.agents.stock_analyst.get_news_sentiment')
    def test_quick_sentiment_check_success(self, mock_get_news_sentiment):
        """Test quick sentiment check."""
        expected_data = {
            'ticker': 'AAPL',
            'sentiment_score': 0.2,
            'sentiment_label': 'neutral'
        }
        mock_get_news_sentiment.return_value = expected_data
        
        agent = StockAnalystAgent(api_key='test_key', news_api_key='news_key')
        result = agent.quick_sentiment_check('AAPL')
        
        assert result == expected_data
        mock_get_news_sentiment.assert_called_once_with('AAPL', 'news_key')
    
    @patch('src.agents.stock_analyst.get_news_sentiment')
    def test_quick_sentiment_check_error(self, mock_get_news_sentiment):
        """Test quick sentiment check error handling."""
        mock_get_news_sentiment.side_effect = Exception("Sentiment error")
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.quick_sentiment_check('AAPL')
        
        assert 'error' in result
        assert 'Sentiment error' in result['error']
    
    @patch('src.agents.stock_analyst.get_stock_price')
    @patch('src.agents.stock_analyst.get_pe_ratio')
    def test_get_current_metrics_success(self, mock_get_pe_ratio, mock_get_stock_price):
        """Test getting current metrics successfully."""
        price_data = {
            'ticker': 'AAPL',
            'current_price': 150.0,
            'volume': 1000000
        }
        pe_data = {
            'ticker': 'AAPL',
            'pe_ratio': 25.5,
            'forward_pe': 22.3
        }
        
        mock_get_stock_price.return_value = price_data
        mock_get_pe_ratio.return_value = pe_data
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.get_current_metrics('AAPL')
        
        # Should combine both datasets, with pe_data not duplicating ticker
        expected = {
            'ticker': 'AAPL',
            'current_price': 150.0,
            'volume': 1000000,
            'pe_ratio': 25.5,
            'forward_pe': 22.3
        }
        
        assert result == expected
    
    @patch('src.agents.stock_analyst.get_stock_price')
    @patch('src.agents.stock_analyst.get_pe_ratio')
    def test_get_current_metrics_price_error(self, mock_get_pe_ratio, mock_get_stock_price):
        """Test getting metrics with price error."""
        mock_get_stock_price.return_value = {'error': 'Price error'}
        mock_get_pe_ratio.return_value = {
            'ticker': 'AAPL',
            'pe_ratio': 25.5
        }
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.get_current_metrics('AAPL')
        
        # Should only include PE data
        assert result == {'pe_ratio': 25.5}
    
    @patch('src.agents.stock_analyst.get_stock_price')
    @patch('src.agents.stock_analyst.get_pe_ratio')
    def test_get_current_metrics_both_errors(self, mock_get_pe_ratio, mock_get_stock_price):
        """Test getting metrics with both errors."""
        mock_get_stock_price.return_value = {'error': 'Price error'}
        mock_get_pe_ratio.return_value = {'error': 'PE error'}
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.get_current_metrics('AAPL')
        
        assert 'error' in result
        assert 'Failed to get stock data' in result['error']
    
    @patch('src.agents.stock_analyst.get_stock_price')
    def test_get_current_metrics_exception(self, mock_get_stock_price):
        """Test getting metrics with exception."""
        mock_get_stock_price.side_effect = Exception("Network error")
        
        agent = StockAnalystAgent(api_key='test_key')
        result = agent.get_current_metrics('AAPL')
        
        assert 'error' in result
        assert 'Network error' in result['error']


class TestIntegration:
    """Integration tests for the agent."""
    
    @patch('src.agents.stock_analyst.ChatOpenAI')
    @patch('src.agents.stock_analyst.create_react_agent')
    @patch('src.agents.stock_analyst.AgentExecutor')
    def test_full_agent_initialization(self, mock_agent_executor_class, mock_create_react_agent, mock_chat_openai):
        """Test full agent initialization process."""
        mock_llm = Mock()
        mock_chat_openai.return_value = mock_llm
        mock_agent = Mock()
        mock_create_react_agent.return_value = mock_agent
        mock_executor = Mock()
        mock_agent_executor_class.return_value = mock_executor
        
        agent = StockAnalystAgent(api_key='test_key', news_api_key='news_key')
        
        # Verify LLM was created with correct parameters
        mock_chat_openai.assert_called_once_with(
            api_key='test_key',
            model='gpt-3.5-turbo',
            temperature=0.1
        )
        
        # Verify agent was created with tools and LLM
        mock_create_react_agent.assert_called_once()
        call_args = mock_create_react_agent.call_args[0]
        assert call_args[0] == mock_llm  # LLM
        assert len(call_args[1]) == 3    # Tools
        
        # Verify agent attributes
        assert agent.llm == mock_llm
        assert agent.agent_executor == mock_executor
        assert len(agent.tools) == 3