"""Tests for Multi-Agent Collaboration System."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os

from src.multi_agents.specialized_agents import (
    BaseSpecializedAgent,
    StockFetcherAgent, 
    NewsAnalystAgent,
    RiskAssessmentAgent,
    ReportGeneratorAgent,
    MultiAgentCoordinator
)


class TestBaseSpecializedAgent:
    """Tests for BaseSpecializedAgent class."""
    
    def test_init(self):
        """Test base agent initialization."""
        agent = BaseSpecializedAgent(
            name="Test Agent",
            role="Tester",
            goal="Test everything", 
            api_key="test_key"
        )
        
        assert agent.name == "Test Agent"
        assert agent.role == "Tester"
        assert agent.goal == "Test everything"
        assert agent.api_key == "test_key"
        assert agent.llm is not None
    
    @patch('src.multi_agents.specialized_agents.create_react_agent')
    @patch('src.multi_agents.specialized_agents.AgentExecutor')
    def test_execute(self, mock_agent_executor_class, mock_create_react_agent):
        """Test task execution."""
        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Test result"}
        mock_agent_executor_class.return_value = mock_executor
        
        agent = BaseSpecializedAgent(
            name="Test Agent",
            role="Tester", 
            goal="Test everything",
            api_key="test_key"
        )
        
        result = agent.execute("test task")
        assert result == "Test result"
        mock_executor.invoke.assert_called_once_with({"input": "test task"})
    
    @patch('src.multi_agents.specialized_agents.create_react_agent')
    @patch('src.multi_agents.specialized_agents.AgentExecutor')
    def test_execute_error(self, mock_agent_executor_class, mock_create_react_agent):
        """Test error handling in task execution."""
        mock_executor = Mock()
        mock_executor.invoke.side_effect = Exception("Test error")
        mock_agent_executor_class.return_value = mock_executor
        
        agent = BaseSpecializedAgent(
            name="Test Agent",
            role="Tester",
            goal="Test everything", 
            api_key="test_key"
        )
        
        result = agent.execute("test task")
        assert "Error in Test Agent: Test error" in result


class TestStockFetcherAgent:
    """Tests for StockFetcherAgent."""
    
    def test_init(self):
        """Test StockFetcherAgent initialization."""
        agent = StockFetcherAgent(api_key="test_key")
        
        assert agent.name == "Stock Data Fetcher"
        assert agent.role == "Financial Data Specialist"
        assert "stock prices" in agent.goal.lower()
        assert len(agent.tools) == 2
    
    def test_tool_names(self):
        """Test that correct tools are created."""
        agent = StockFetcherAgent(api_key="test_key")
        
        tool_names = [tool.name for tool in agent.tools]
        assert "fetch_stock_price" in tool_names
        assert "fetch_financial_metrics" in tool_names
    
    @patch('src.multi_agents.specialized_agents.get_stock_price')
    def test_fetch_stock_price_tool(self, mock_get_stock_price):
        """Test stock price fetching tool."""
        mock_get_stock_price.return_value = {
            'current_price': 150.0,
            'previous_close': 145.0,
            'change': 5.0,
            'change_percent': 3.45,
            'volume': 1000000,
            'market_cap': 2500000000,
            'timestamp': '2024-01-01T12:00:00'
        }
        
        agent = StockFetcherAgent(api_key="test_key")
        price_tool = next(tool for tool in agent.tools if tool.name == "fetch_stock_price")
        
        result = price_tool.func("AAPL")
        
        assert "AAPL" in result
        assert "$150.0" in result
        assert "3.45%" in result
        mock_get_stock_price.assert_called_once_with("AAPL")
    
    @patch('src.multi_agents.specialized_agents.get_pe_ratio')
    def test_fetch_financial_metrics_tool(self, mock_get_pe_ratio):
        """Test financial metrics fetching tool.""" 
        mock_get_pe_ratio.return_value = {
            'pe_ratio': 25.5,
            'forward_pe': 22.3,
            'peg_ratio': 1.2,
            'price_to_book': 3.1,
            'eps': 6.11,
            'revenue': 365000000000,
            'timestamp': '2024-01-01T12:00:00'
        }
        
        agent = StockFetcherAgent(api_key="test_key")
        metrics_tool = next(tool for tool in agent.tools if tool.name == "fetch_financial_metrics")
        
        result = metrics_tool.func("AAPL")
        
        assert "AAPL" in result
        assert "25.5" in result
        assert "22.3" in result
        mock_get_pe_ratio.assert_called_once_with("AAPL")


class TestNewsAnalystAgent:
    """Tests for NewsAnalystAgent."""
    
    def test_init(self):
        """Test NewsAnalystAgent initialization."""
        agent = NewsAnalystAgent(api_key="test_key", news_api_key="news_key")
        
        assert agent.name == "News Sentiment Analyst"
        assert agent.role == "Market Psychology Expert"
        assert "sentiment" in agent.goal.lower()
        assert agent.news_api_key == "news_key"
        assert len(agent.tools) == 1
    
    @patch('src.multi_agents.specialized_agents.get_news_sentiment')
    def test_analyze_news_sentiment_tool(self, mock_get_news_sentiment):
        """Test news sentiment analysis tool."""
        mock_get_news_sentiment.return_value = {
            'sentiment_score': 0.3,
            'sentiment_label': 'positive',
            'news_count': 5,
            'top_headlines': ['Good news 1', 'Good news 2'],
            'timestamp': '2024-01-01T12:00:00'
        }
        
        agent = NewsAnalystAgent(api_key="test_key", news_api_key="news_key")
        sentiment_tool = agent.tools[0]
        
        result = sentiment_tool.func("AAPL")
        
        assert "AAPL" in result
        assert "POSITIVE" in result
        assert "0.3" in result
        assert "Good news 1" in result
        mock_get_news_sentiment.assert_called_once_with("AAPL", "news_key")
    
    def test_interpret_sentiment(self):
        """Test sentiment interpretation logic."""
        agent = NewsAnalystAgent(api_key="test_key")
        
        # Test positive sentiment
        result = agent._interpret_sentiment(0.4, "positive")
        assert "Strong positive momentum" in result
        
        # Test negative sentiment
        result = agent._interpret_sentiment(-0.4, "negative")
        assert "Significant negative sentiment" in result
        
        # Test neutral sentiment
        result = agent._interpret_sentiment(0.05, "neutral")
        assert "Market neutrality" in result


class TestRiskAssessmentAgent:
    """Tests for RiskAssessmentAgent."""
    
    def test_init(self):
        """Test RiskAssessmentAgent initialization."""
        agent = RiskAssessmentAgent(api_key="test_key")
        
        assert agent.name == "Risk Assessment Specialist"
        assert agent.role == "Risk Management Expert"
        assert "risk" in agent.goal.lower()
        assert len(agent.tools) == 2
    
    def test_assess_valuation_risk_low(self):
        """Test valuation risk assessment - low risk scenario."""
        agent = RiskAssessmentAgent(api_key="test_key")
        valuation_tool = next(tool for tool in agent.tools if tool.name == "assess_valuation_risk")
        
        # Low P/E, good PEG
        result = valuation_tool.func("12,10,0.8")
        
        assert "LOW" in result
        assert "undervaluation" in result.lower()
        assert "conservative investors" in result.lower()
    
    def test_assess_valuation_risk_high(self):
        """Test valuation risk assessment - high risk scenario."""
        agent = RiskAssessmentAgent(api_key="test_key")
        valuation_tool = next(tool for tool in agent.tools if tool.name == "assess_valuation_risk")
        
        # High P/E, high PEG
        result = valuation_tool.func("45,40,2.5")
        
        assert "HIGH" in result
        assert "overvaluation" in result.lower()
        assert "caution advised" in result.lower()
    
    def test_assess_sentiment_risk_positive(self):
        """Test sentiment risk assessment - positive scenario."""
        agent = RiskAssessmentAgent(api_key="test_key")
        sentiment_tool = next(tool for tool in agent.tools if tool.name == "assess_sentiment_risk")
        
        result = sentiment_tool.func("0.4,positive")
        
        assert "LOW" in result
        assert "reduces" in result.lower()
        assert "positive" in result.lower()
    
    def test_assess_sentiment_risk_negative(self):
        """Test sentiment risk assessment - negative scenario."""
        agent = RiskAssessmentAgent(api_key="test_key")
        sentiment_tool = next(tool for tool in agent.tools if tool.name == "assess_sentiment_risk")
        
        result = sentiment_tool.func("-0.4,negative")
        
        assert "HIGH" in result
        assert "increases" in result.lower()
        assert "downside risk" in result.lower()


class TestReportGeneratorAgent:
    """Tests for ReportGeneratorAgent."""
    
    def test_init(self):
        """Test ReportGeneratorAgent initialization."""
        agent = ReportGeneratorAgent(api_key="test_key")
        
        assert agent.name == "Investment Report Generator"
        assert agent.role == "Senior Investment Analyst"
        assert "reports" in agent.goal.lower()
        assert len(agent.tools) == 1
    
    def test_generate_investment_recommendation_tool(self):
        """Test investment recommendation generation tool."""
        agent = ReportGeneratorAgent(api_key="test_key")
        report_tool = agent.tools[0]
        
        test_data = "AAPL analysis data here..."
        result = report_tool.func(test_data)
        
        assert "investment recommendation" in result.lower()
        assert "Executive Summary" in result
        assert "Risk-Reward Analysis" in result
        assert test_data in result


class TestMultiAgentCoordinator:
    """Tests for MultiAgentCoordinator."""
    
    def test_init(self):
        """Test MultiAgentCoordinator initialization.""" 
        coordinator = MultiAgentCoordinator(api_key="test_key", news_api_key="news_key")
        
        assert coordinator.api_key == "test_key"
        assert coordinator.news_api_key == "news_key"
        assert isinstance(coordinator.stock_fetcher, StockFetcherAgent)
        assert isinstance(coordinator.news_analyst, NewsAnalystAgent)
        assert isinstance(coordinator.risk_assessor, RiskAssessmentAgent)
        assert isinstance(coordinator.report_generator, ReportGeneratorAgent)
    
    @patch('builtins.print')
    def test_analyze_stock_collaborative(self, mock_print):
        """Test collaborative stock analysis."""
        coordinator = MultiAgentCoordinator(api_key="test_key")
        
        # Mock agent responses
        coordinator.stock_fetcher.execute = Mock(return_value="Stock data result")
        coordinator.news_analyst.execute = Mock(return_value="Sentiment analysis result")
        coordinator.risk_assessor.execute = Mock(return_value="Risk assessment result")
        coordinator.report_generator.execute = Mock(return_value="Final report result")
        
        result = coordinator.analyze_stock_collaborative("AAPL")
        
        assert "price_data" in result
        assert "financial_metrics" in result
        assert "sentiment_analysis" in result
        assert "risk_assessment" in result
        assert "final_report" in result
        
        # Verify all agents were called
        assert coordinator.stock_fetcher.execute.call_count == 2  # Price and metrics
        coordinator.news_analyst.execute.assert_called_once()
        coordinator.risk_assessor.execute.assert_called_once()
        coordinator.report_generator.execute.assert_called_once()
    
    @patch('builtins.print')
    def test_compare_stocks_collaborative(self, mock_print):
        """Test collaborative stock comparison."""
        coordinator = MultiAgentCoordinator(api_key="test_key")
        
        # Mock analyze_stock_collaborative
        coordinator.analyze_stock_collaborative = Mock(return_value={
            "final_report": "Individual stock analysis"
        })
        coordinator.report_generator.execute = Mock(return_value="Comparative report")
        
        result = coordinator.compare_stocks_collaborative(["AAPL", "GOOGL"])
        
        assert "individual_analyses" in result
        assert "comparative_report" in result
        assert "AAPL" in result["individual_analyses"]
        assert "GOOGL" in result["individual_analyses"]
        
        # Verify analyze_stock_collaborative called for each ticker
        assert coordinator.analyze_stock_collaborative.call_count == 2


class TestIntegration:
    """Integration tests for multi-agent system."""
    
    @patch('src.multi_agents.specialized_agents.ChatOpenAI')
    @patch('src.multi_agents.specialized_agents.create_react_agent')
    @patch('src.multi_agents.specialized_agents.AgentExecutor')
    def test_full_multi_agent_initialization(self, mock_executor_class, mock_create_agent, mock_openai):
        """Test full multi-agent system initialization."""
        mock_llm = Mock()
        mock_openai.return_value = mock_llm
        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor
        
        coordinator = MultiAgentCoordinator(api_key="test_key", news_api_key="news_key")
        
        # Verify all agents were created
        assert len(mock_openai.call_args_list) == 4  # 4 agents created
        assert len(mock_create_agent.call_args_list) == 4  # 4 agents created
        assert len(mock_executor_class.call_args_list) == 4  # 4 executors created
        
        # Verify agent types
        assert isinstance(coordinator.stock_fetcher, StockFetcherAgent)
        assert isinstance(coordinator.news_analyst, NewsAnalystAgent) 
        assert isinstance(coordinator.risk_assessor, RiskAssessmentAgent)
        assert isinstance(coordinator.report_generator, ReportGeneratorAgent)
    
    def test_agent_specialization(self):
        """Test that each agent has correct specialization."""
        coordinator = MultiAgentCoordinator(api_key="test_key")
        
        # Test agent roles
        assert "Data Specialist" in coordinator.stock_fetcher.role
        assert "Psychology Expert" in coordinator.news_analyst.role
        assert "Risk Management" in coordinator.risk_assessor.role
        assert "Investment Analyst" in coordinator.report_generator.role
        
        # Test agent goals
        assert "stock prices" in coordinator.stock_fetcher.goal.lower()
        assert "sentiment" in coordinator.news_analyst.goal.lower()
        assert "risk" in coordinator.risk_assessor.goal.lower()
        assert "reports" in coordinator.report_generator.goal.lower()
    
    @patch('builtins.print')
    def test_workflow_coordination(self, mock_print):
        """Test proper workflow coordination between agents."""
        coordinator = MultiAgentCoordinator(api_key="test_key")
        
        # Track execution order
        execution_order = []
        
        def track_execution(agent_name):
            def mock_execute(task):
                execution_order.append(agent_name)
                return f"{agent_name} result"
            return mock_execute
        
        coordinator.stock_fetcher.execute = track_execution("stock_fetcher")
        coordinator.news_analyst.execute = track_execution("news_analyst")
        coordinator.risk_assessor.execute = track_execution("risk_assessor")
        coordinator.report_generator.execute = track_execution("report_generator")
        
        coordinator.analyze_stock_collaborative("AAPL")
        
        # Verify execution order: fetcher -> fetcher -> news -> risk -> report
        expected_order = ["stock_fetcher", "stock_fetcher", "news_analyst", "risk_assessor", "report_generator"]
        assert execution_order == expected_order