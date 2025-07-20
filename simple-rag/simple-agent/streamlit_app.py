#!/usr/bin/env python3
"""
🚀 Stock Market Analyst Agent - Interactive Web Interface

Phase 4: Human-in-the-Loop Visual Interface with Real-time Agent Display

This Streamlit application provides a beautiful, interactive interface to:
- Watch multiple AI agents collaborate in real-time
- Get live stock analysis with visual feedback
- Approve/reject AI recommendations
- Monitor agent performance and status
"""

import streamlit as st
import os
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Import our agent system
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.multi_agents.specialized_agents import MultiAgentCoordinator
from src.tools.stock_tools import get_news_sentiment


# Configure Streamlit page
st.set_page_config(
    page_title="🤖 AI Stock Analyst",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.agent-card {
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.status-working {
    color: #ff6b6b;
    font-weight: bold;
}
.status-complete {
    color: #51cf66;
    font-weight: bold;
}
.status-waiting {
    color: #868e96;
    font-weight: bold;
}
.recommendation-box {
    border: 3px solid #20c997;
    border-radius: 15px;
    padding: 2rem;
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'coordinator' not in st.session_state:
        api_key = os.getenv("OPENAI_API_KEY")
        news_api_key = os.getenv("NEWS_API_KEY")
        
        if api_key:
            st.session_state.coordinator = MultiAgentCoordinator(api_key=api_key, news_api_key=news_api_key)
            st.session_state.api_configured = True
        else:
            st.session_state.api_configured = False
    
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    if 'agent_status' not in st.session_state:
        st.session_state.agent_status = {
            'stock_fetcher': {'status': 'waiting', 'result': None},
            'news_analyst': {'status': 'waiting', 'result': None},
            'risk_assessor': {'status': 'waiting', 'result': None},
            'report_generator': {'status': 'waiting', 'result': None}
        }


def display_header():
    """Display the main header and description."""
    st.markdown('<h1 class="main-header">🤖 AI Stock Market Analyst</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 1.2rem; color: #666;">
        <strong>Multi-Agent Collaboration System</strong><br>
        Watch 4 specialized AI agents work together to analyze stocks
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")


def display_agent_architecture():
    """Display the multi-agent architecture diagram."""
    st.subheader("🏗️ Multi-Agent Architecture")
    
    col1, col2, col3, col4 = st.columns(4)
    
    agents = [
        {
            "name": "📊 Stock Fetcher",
            "role": "Financial Data Specialist", 
            "icon": "📊",
            "color": "#1f77b4",
            "description": "Gets stock prices, P/E ratios, financial metrics"
        },
        {
            "name": "📰 News Analyst", 
            "role": "Market Psychology Expert",
            "icon": "📰", 
            "color": "#ff7f0e",
            "description": "Analyzes news sentiment and market psychology"
        },
        {
            "name": "⚖️ Risk Assessor",
            "role": "Risk Management Expert",
            "icon": "⚖️",
            "color": "#2ca02c", 
            "description": "Evaluates investment risks and scoring"
        },
        {
            "name": "📋 Report Generator",
            "role": "Senior Investment Analyst",
            "icon": "📋",
            "color": "#d62728",
            "description": "Creates comprehensive investment reports"
        }
    ]
    
    for i, (col, agent) in enumerate(zip([col1, col2, col3, col4], agents)):
        with col:
            status = st.session_state.agent_status[list(st.session_state.agent_status.keys())[i]]['status']
            status_color = "#ff6b6b" if status == "working" else "#51cf66" if status == "complete" else "#868e96"
            
            st.markdown(f"""
            <div class="agent-card" style="border-color: {agent['color']};">
                <div style="text-align: center;">
                    <div style="font-size: 3rem;">{agent['icon']}</div>
                    <div style="font-size: 1.2rem; font-weight: bold; color: {agent['color']};">
                        {agent['name']}
                    </div>
                    <div style="font-size: 0.9rem; color: #666; margin: 0.5rem 0;">
                        {agent['role']}
                    </div>
                    <div style="font-size: 0.8rem; color: #888;">
                        {agent['description']}
                    </div>
                    <div style="margin-top: 1rem; color: {status_color};">
                        Status: {status.upper()}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def display_real_time_agent_status(ticker):
    """Display real-time agent execution status."""
    if not ticker:
        return
    
    st.subheader(f"🔄 Live Agent Analysis for {ticker}")
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    agent_names = ['Stock Fetcher', 'News Analyst', 'Risk Assessor', 'Report Generator']
    
    # Simulate real-time updates (in real implementation, this would be connected to actual agent execution)
    for i, agent_name in enumerate(agent_names):
        progress = (i + 1) / len(agent_names)
        progress_bar.progress(progress)
        status_text.text(f"🤖 {agent_name} is analyzing {ticker}...")
        time.sleep(1)  # Simulate processing time
    
    status_text.text("✅ All agents completed analysis!")


def run_collaborative_analysis(ticker):
    """Run the collaborative analysis and display results."""
    if not st.session_state.api_configured:
        st.error("❌ OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file.")
        return
    
    st.subheader(f"🔍 Multi-Agent Analysis for {ticker}")
    
    # Reset agent status
    for agent in st.session_state.agent_status:
        st.session_state.agent_status[agent] = {'status': 'waiting', 'result': None}
    
    with st.spinner("🤖 Initializing multi-agent analysis..."):
        try:
            # Run the actual analysis
            results = st.session_state.coordinator.analyze_stock_collaborative(ticker)
            st.session_state.analysis_results[ticker] = results
            
            # Display results in organized sections
            display_analysis_results(ticker, results)
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            st.info("💡 This might be due to API rate limits. The system handles errors gracefully.")


def display_analysis_results(ticker, results):
    """Display the analysis results from all agents."""
    st.success("✅ Multi-agent analysis complete!")
    
    # Create tabs for different agent results
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Stock Data", 
        "📰 Sentiment", 
        "⚖️ Risk Analysis", 
        "📋 Final Report",
        "🎯 Summary"
    ])
    
    with tab1:
        st.subheader("📊 Stock Data Analysis")
        price_data = results.get('price_data', 'No price data available')
        financial_data = results.get('financial_metrics', 'No financial data available')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Price Information:**")
            st.text(price_data[:300] + "..." if len(price_data) > 300 else price_data)
        
        with col2:
            st.markdown("**Financial Metrics:**")
            st.text(financial_data[:300] + "..." if len(financial_data) > 300 else financial_data)
    
    with tab2:
        st.subheader("📰 News Sentiment Analysis")
        sentiment_data = results.get('sentiment_analysis', 'No sentiment data available')
        st.text(sentiment_data)
        
        # Add sentiment visualization
        try:
            sentiment_result = get_news_sentiment(ticker)
            if 'sentiment_score' in sentiment_result:
                create_sentiment_gauge(sentiment_result['sentiment_score'], sentiment_result['sentiment_label'])
        except:
            pass
    
    with tab3:
        st.subheader("⚖️ Risk Assessment")
        risk_data = results.get('risk_assessment', 'No risk assessment available')
        st.text(risk_data)
    
    with tab4:
        st.subheader("📋 Investment Report")
        report_data = results.get('final_report', 'No report generated')
        st.text(report_data)
    
    with tab5:
        display_investment_summary(ticker, results)


def create_sentiment_gauge(score, label):
    """Create a sentiment gauge visualization."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Sentiment: {label.upper()}"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.33], 'color': "lightgray"},
                {'range': [-0.33, 0.33], 'color': "gray"},
                {'range': [0.33, 1], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.9
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)


def display_investment_summary(ticker, results):
    """Display investment summary with human approval interface."""
    st.markdown("### 🎯 Investment Summary & Human Approval")
    
    # Extract key information for summary
    final_report = results.get('final_report', 'No recommendation available')
    
    # Create recommendation box
    st.markdown(f"""
    <div class="recommendation-box">
        <h3>📈 AI Recommendation for {ticker}</h3>
        <p>{final_report}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Human-in-the-Loop approval interface
    st.markdown("### 👨‍💼 Human Review & Approval")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✅ APPROVE", type="primary", use_container_width=True):
            st.success(f"✅ You approved the recommendation for {ticker}")
            st.balloons()
            log_decision(ticker, "APPROVED", final_report)
    
    with col2:
        if st.button("❌ REJECT", use_container_width=True):
            st.error(f"❌ You rejected the recommendation for {ticker}")
            log_decision(ticker, "REJECTED", final_report)
    
    with col3:
        if st.button("⏸️ HOLD", use_container_width=True):
            st.warning(f"⏸️ Decision on {ticker} put on hold for further review")
            log_decision(ticker, "HOLD", final_report)
    
    with col4:
        if st.button("🔄 RE-ANALYZE", use_container_width=True):
            st.info(f"🔄 Re-analyzing {ticker}...")
            run_collaborative_analysis(ticker)
    
    # Display approval history
    if 'approval_history' in st.session_state:
        st.markdown("### 📊 Decision History")
        df = pd.DataFrame(st.session_state.approval_history)
        if not df.empty:
            st.dataframe(df, use_container_width=True)


def log_decision(ticker, decision, recommendation):
    """Log human decisions for tracking."""
    if 'approval_history' not in st.session_state:
        st.session_state.approval_history = []
    
    st.session_state.approval_history.append({
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Ticker': ticker,
        'Decision': decision,
        'Recommendation': recommendation[:100] + "..." if len(recommendation) > 100 else recommendation
    })


def display_sidebar():
    """Display the sidebar with controls and information."""
    st.sidebar.markdown("# 🎛️ Control Panel")
    
    # API Status
    st.sidebar.markdown("## 🔑 API Status")
    if st.session_state.api_configured:
        st.sidebar.success("✅ OpenAI API Connected")
        if os.getenv("NEWS_API_KEY"):
            st.sidebar.success("✅ News API Connected")
        else:
            st.sidebar.info("ℹ️ News API: Using mock data")
    else:
        st.sidebar.error("❌ OpenAI API Not Configured")
        st.sidebar.markdown("Add `OPENAI_API_KEY` to `.env` file")
    
    st.sidebar.markdown("---")
    
    # Quick Analysis
    st.sidebar.markdown("## ⚡ Quick Analysis")
    popular_tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA']
    
    for ticker in popular_tickers:
        if st.sidebar.button(f"📈 Analyze {ticker}", use_container_width=True):
            st.session_state.selected_ticker = ticker
    
    st.sidebar.markdown("---")
    
    # Statistics
    st.sidebar.markdown("## 📊 Session Stats")
    total_analyses = len(st.session_state.analysis_results)
    st.sidebar.metric("Analyses Completed", total_analyses)
    
    if 'approval_history' in st.session_state:
        approvals = len([d for d in st.session_state.approval_history if d['Decision'] == 'APPROVED'])
        st.sidebar.metric("Recommendations Approved", approvals)
    
    st.sidebar.markdown("---")
    
    # Help
    st.sidebar.markdown("## ❓ How It Works")
    st.sidebar.markdown("""
    1. **Enter a stock ticker** in the main interface
    2. **Watch AI agents collaborate** in real-time
    3. **Review the comprehensive analysis** across multiple tabs  
    4. **Approve or reject** the AI recommendation
    5. **Track your decisions** in the history log
    
    **The 4 AI agents work together:**
    - 📊 **Data Fetcher**: Gets financial metrics
    - 📰 **News Analyst**: Analyzes sentiment  
    - ⚖️ **Risk Assessor**: Evaluates investment risk
    - 📋 **Report Generator**: Creates final recommendation
    """)


def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    display_sidebar()
    
    # Main interface
    display_agent_architecture()
    
    st.markdown("---")
    
    # Stock input section
    st.subheader("🔍 Stock Analysis Interface")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Ticker Symbol:",
            value=st.session_state.get('selected_ticker', ''),
            placeholder="e.g., AAPL, GOOGL, TSLA",
            help="Enter a valid stock ticker symbol to analyze"
        ).upper()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        analyze_button = st.button("🚀 Start Analysis", type="primary", use_container_width=True)
    
    # Run analysis if button clicked or ticker selected from sidebar
    if analyze_button and ticker:
        run_collaborative_analysis(ticker)
    elif ticker and ticker in st.session_state.analysis_results:
        # Display previous results if available
        st.subheader(f"📊 Previous Analysis: {ticker}")
        display_analysis_results(ticker, st.session_state.analysis_results[ticker])
    
    # Demo section
    if not ticker:
        st.markdown("---")
        st.subheader("🎬 Demo: Try These Popular Stocks")
        
        demo_cols = st.columns(6)
        demo_tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA']
        
        for col, demo_ticker in zip(demo_cols, demo_tickers):
            with col:
                if st.button(f"📈 {demo_ticker}", use_container_width=True):
                    run_collaborative_analysis(demo_ticker)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 3rem;">
        <p>🤖 <strong>AI Stock Market Analyst</strong> | Multi-Agent Collaboration System</p>
        <p>Built with ❤️ using Streamlit, LangChain, and OpenAI | Phase 4: Human-in-the-Loop Interface</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()