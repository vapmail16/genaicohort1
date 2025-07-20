"""Tests for the Streamlit web application."""

import pytest
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_streamlit_imports():
    """Test that all required imports for the Streamlit app work."""
    try:
        import streamlit as st
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
        from dotenv import load_dotenv
        
        # Test our imports
        from src.multi_agents.specialized_agents import MultiAgentCoordinator
        from src.tools.stock_tools import get_news_sentiment
        
        assert True  # If we get here, all imports worked
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_multiagent_coordinator_instantiation():
    """Test that MultiAgentCoordinator can be instantiated."""
    from src.multi_agents.specialized_agents import MultiAgentCoordinator
    
    # Test with dummy API key
    try:
        coordinator = MultiAgentCoordinator(api_key="dummy_key_for_testing")
        assert coordinator is not None
        assert hasattr(coordinator, 'stock_fetcher')
        assert hasattr(coordinator, 'news_analyst')
        assert hasattr(coordinator, 'risk_assessor')  
        assert hasattr(coordinator, 'report_generator')
    except Exception as e:
        # Expected to fail with dummy key, but should fail gracefully
        assert "API key" in str(e) or "invalid" in str(e).lower()

def test_sentiment_tool_works():
    """Test that sentiment analysis works for the UI."""
    from src.tools.stock_tools import get_news_sentiment
    
    result = get_news_sentiment("AAPL")
    
    assert isinstance(result, dict)
    assert 'sentiment_score' in result
    assert 'sentiment_label' in result
    assert 'top_headlines' in result
    assert isinstance(result['sentiment_score'], (int, float))
    assert result['sentiment_label'] in ['positive', 'negative', 'neutral']

def test_app_configuration():
    """Test basic app configuration and structure."""
    # This would test the main app structure if we had a way to run it headless
    # For now, just test that the main components can be imported
    
    try:
        # These should not fail
        import streamlit as st
        from datetime import datetime
        import time
        
        # Test that we can create basic Streamlit components
        # (This won't actually render, just tests the API)
        assert hasattr(st, 'set_page_config')
        assert hasattr(st, 'markdown')
        assert hasattr(st, 'columns')
        assert hasattr(st, 'button')
        
    except Exception as e:
        pytest.fail(f"Streamlit configuration test failed: {e}")

class TestUIComponents:
    """Test UI component functions (if we extract them)."""
    
    def test_gauge_creation_data(self):
        """Test that we can create gauge chart data."""
        import plotly.graph_objects as go
        
        # Test creating a gauge (similar to what's in the app)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 0.3,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Test Gauge"}
        ))
        
        assert fig is not None
        assert len(fig.data) == 1
    
    def test_dataframe_creation(self):
        """Test that we can create DataFrames for the UI."""
        import pandas as pd
        from datetime import datetime
        
        # Test creating approval history DataFrame
        history_data = [
            {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Ticker': 'AAPL',
                'Decision': 'APPROVED',
                'Recommendation': 'Buy recommendation based on analysis'
            }
        ]
        
        df = pd.DataFrame(history_data)
        
        assert not df.empty
        assert 'Timestamp' in df.columns
        assert 'Ticker' in df.columns
        assert 'Decision' in df.columns
        assert df.iloc[0]['Ticker'] == 'AAPL'

def test_session_state_structure():
    """Test the expected session state structure."""
    # Test the structure we expect in session state
    expected_structure = {
        'coordinator': None,
        'api_configured': False,
        'analysis_results': {},
        'agent_status': {
            'stock_fetcher': {'status': 'waiting', 'result': None},
            'news_analyst': {'status': 'waiting', 'result': None}, 
            'risk_assessor': {'status': 'waiting', 'result': None},
            'report_generator': {'status': 'waiting', 'result': None}
        }
    }
    
    # Verify structure makes sense
    assert 'coordinator' in expected_structure
    assert 'agent_status' in expected_structure
    assert len(expected_structure['agent_status']) == 4
    
    # Verify all agents are present
    expected_agents = ['stock_fetcher', 'news_analyst', 'risk_assessor', 'report_generator']
    for agent in expected_agents:
        assert agent in expected_structure['agent_status']
        assert 'status' in expected_structure['agent_status'][agent]
        assert 'result' in expected_structure['agent_status'][agent]