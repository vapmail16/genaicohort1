import streamlit as st
import pandas as pd
from datetime import datetime
import time
import json
from chatbot_core import ChatbotCore
from config import Config
from analytics import ChatAnalytics

# Page configuration
st.set_page_config(
    page_title="AI Chatbot Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .bot-message {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        margin-right: 2rem;
    }
    
    .personality-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .personality-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .personality-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .feedback-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    
    .stButton > button {
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotCore()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'current_personality' not in st.session_state:
        st.session_state.current_personality = 'friendly'
    
    if 'feedback_given' not in st.session_state:
        st.session_state.feedback_given = set()
    
    # Track manual personality selections
    if 'manual_personality_counts' not in st.session_state:
        st.session_state.manual_personality_counts = {key: 0 for key in Config.PERSONALITIES.keys()}
    
    # Initialize analytics
    if 'analytics' not in st.session_state:
        st.session_state.analytics = ChatAnalytics()
    
    # Track session start
    if 'session_tracked' not in st.session_state:
        session_id = st.session_state.get('session_id', f"session_{int(time.time())}")
        st.session_state.session_id = session_id
        st.session_state.analytics.track_session_start(session_id)
        st.session_state.session_tracked = True

def render_personality_selector():
    """Render the personality selection interface."""
    st.sidebar.markdown("### 🤖 Choose Your Assistant")
    
    for key, personality in Config.PERSONALITIES.items():
        is_selected = st.session_state.current_personality == key
        card_class = "personality-card selected" if is_selected else "personality-card"
        
        with st.sidebar.container():
            st.markdown(f"""
            <div class="{card_class}" onclick="document.querySelector('[data-testid=stRadio] input[value=\"{key}\"]').click()">
                <h4>{personality['emoji']} {personality['name']}</h4>
                <p style="font-size: 0.9rem; opacity: 0.8;">{personality['system_message'][:100]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {personality['name']}", key=f"btn_{key}"):
                if st.session_state.chatbot.set_personality(key):
                    st.session_state.current_personality = key
                    # Increment manual personality count
                    st.session_state.manual_personality_counts[key] += 1
                    # Track personality change
                    st.session_state.analytics.track_personality_change(st.session_state.session_id, key)
                    st.rerun()

def render_chat_interface():
    """Render the main chat interface."""
    st.markdown('<h1 class="main-header">🤖 AI Chatbot Assistant</h1>', unsafe_allow_html=True)
    
    # Display current personality
    current_personality = Config.PERSONALITIES[st.session_state.current_personality]
    st.info(f"**Current Assistant:** {current_personality['emoji']} {current_personality['name']}")
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Bot message with feedback buttons
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Assistant:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Feedback buttons (only for bot messages)
                if i not in st.session_state.feedback_given:
                    col1, col2, col3 = st.columns([1, 1, 6])
                    with col1:
                        if st.button("👍", key=f"like_{i}"):
                            st.session_state.feedback_given.add(i)
                            # Add feedback to log
                            if hasattr(message, 'timestamp'):
                                st.session_state.chatbot.add_feedback(message.timestamp, "positive")
                            st.rerun()
                    
                    with col2:
                        if st.button("👎", key=f"dislike_{i}"):
                            st.session_state.feedback_given.add(i)
                            # Add feedback to log
                            if hasattr(message, 'timestamp'):
                                st.session_state.chatbot.add_feedback(message.timestamp, "negative")
                            st.rerun()
    
    # Chat input
    with st.container():
        user_input = st.text_area(
            "Type your message here...",
            key="user_input",
            height=100,
            placeholder="Ask me anything! I'm here to help."
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🚀 Send Message", use_container_width=True):
                if user_input.strip():
                    # Track user message
                    st.session_state.analytics.track_message(
                        st.session_state.session_id, 
                        "user", 
                        user_input, 
                        st.session_state.current_personality
                    )
                    
                    # Add user message to chat
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    # Get bot response
                    with st.spinner("🤔 Thinking..."):
                        response, success = st.session_state.chatbot.get_response(user_input)
                    
                    # Track bot response
                    st.session_state.analytics.track_message(
                        st.session_state.session_id, 
                        "bot", 
                        response, 
                        st.session_state.current_personality
                    )
                    
                    # Add bot response to chat
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Show savage mode indicator if abusive language was detected
                    if st.session_state.chatbot.current_personality == 'savage':
                        st.warning("😈 Savage mode activated! The assistant detected inappropriate language.")
                    
                    # Clear input by rerunning
                    st.rerun()

def render_sidebar_features():
    """Render sidebar features and controls."""
    st.sidebar.markdown("---")
    
    # Conversation controls
    st.sidebar.markdown("### 🛠️ Controls")
    
    if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chatbot.clear_history()
        st.session_state.feedback_given = set()
        # Reset manual personality counts
        st.session_state.manual_personality_counts = {key: 0 for key in Config.PERSONALITIES.keys()}
        st.rerun()
    
    # Export options
    st.sidebar.markdown("### 📊 Export Options")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📄 CSV", use_container_width=True):
            csv_file = st.session_state.chatbot.export_chat_history('csv')
            if csv_file:
                with open(csv_file, 'r') as f:
                    st.download_button(
                        label="Download CSV",
                        data=f.read(),
                        file_name="chat_history.csv",
                        mime="text/csv"
                    )
    
    with col2:
        if st.button("📋 JSON", use_container_width=True):
            json_file = st.session_state.chatbot.export_chat_history('json')
            if json_file:
                with open(json_file, 'r') as f:
                    st.download_button(
                        label="Download JSON",
                        data=f.read(),
                        file_name="chat_history.json",
                        mime="application/json"
                    )
    
    # Statistics
    st.sidebar.markdown("### 📈 Statistics")
    summary = st.session_state.chatbot.get_conversation_summary()
    
    if summary:
        # Basic stats
        st.sidebar.markdown(f"""
        <div class="metric-card">
            <h3>Total Interactions</h3>
            <h2>{summary.get('total_interactions', 0)}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Cost stats
        cost_stats = summary.get('cost_stats', {})
        if cost_stats:
            st.sidebar.markdown("### 💰 API Costs")
            st.sidebar.markdown(f"""
            <div class="metric-card">
                <h3>Total Cost</h3>
                <h2>${cost_stats.get('total_cost', 0):.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.sidebar.markdown(f"""
            <div class="metric-card">
                <h3>Total Tokens</h3>
                <h2>{cost_stats.get('total_tokens', 0):,}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.sidebar.markdown(f"""
            <div class="metric-card">
                <h3>Avg Cost/Interaction</h3>
                <h2>${cost_stats.get('avg_cost_per_interaction', 0):.4f}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.sidebar.markdown(f"**Model:** {cost_stats.get('current_model', 'Unknown')}")
            st.sidebar.markdown(f"**Input Tokens:** {cost_stats.get('input_tokens', 0):,}")
            st.sidebar.markdown(f"**Output Tokens:** {cost_stats.get('output_tokens', 0):,}")
    
    # Analytics Dashboard
    st.sidebar.markdown("### 📊 Analytics Dashboard")
    
    # Get analytics summary
    analytics_summary = st.session_state.analytics.get_analytics_summary()
    
    if analytics_summary:
        # Total users
        st.sidebar.markdown(f"""
        <div class="metric-card">
            <h3>Total Users</h3>
            <h2>{analytics_summary.get('total_users', 0)}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent activity
        st.sidebar.markdown(f"""
        <div class="metric-card">
            <h3>Recent Users (24h)</h3>
            <h2>{analytics_summary.get('recent_users_24h', 0)}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Total messages
        st.sidebar.markdown(f"""
        <div class="metric-card">
            <h3>Total Messages</h3>
            <h2>{analytics_summary.get('total_messages', 0)}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent messages
        st.sidebar.markdown(f"""
        <div class="metric-card">
            <h3>Recent Messages (24h)</h3>
            <h2>{analytics_summary.get('recent_messages_24h', 0)}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Average session duration
        avg_duration = analytics_summary.get('avg_session_duration_min', 0)
        st.sidebar.markdown(f"""
        <div class="metric-card">
            <h3>Avg Session Duration</h3>
            <h2>{avg_duration:.1f} min</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Top personality
        top_personality = analytics_summary.get('top_personality', 'None')
        st.sidebar.markdown(f"**Most Popular:** {top_personality}")
        
        # Device breakdown
        device_breakdown = analytics_summary.get('device_breakdown', {})
        if device_breakdown:
            st.sidebar.markdown("### 📱 Device Types")
            for device, count in device_breakdown.items():
                st.sidebar.markdown(f"**{device}:** {count}")
        
        # Location breakdown
        location_breakdown = analytics_summary.get('location_breakdown', {})
        if location_breakdown:
            st.sidebar.markdown("### 🌍 Locations")
            for location, count in location_breakdown.items():
                st.sidebar.markdown(f"**{location}:** {count}")
        
        # Personality usage
        personality_usage = analytics_summary.get('personality_usage', {})
        if personality_usage:
            st.sidebar.markdown("### 🤖 Personality Usage")
            for personality, count in personality_usage.items():
                st.sidebar.markdown(f"**{personality}:** {count}")
    
    # Show detailed analytics button
    if st.sidebar.button("📈 View Detailed Analytics", use_container_width=True):
        st.session_state.show_analytics = True
        st.rerun()
        
        # Manual personality selection stats
        manual_counts = st.session_state.manual_personality_counts
        if any(count > 0 for count in manual_counts.values()):
            st.sidebar.markdown("**Personalities Manually Selected:**")
            for key, count in manual_counts.items():
                if count > 0:
                    emoji = Config.PERSONALITIES.get(key, {}).get('emoji', '🤖')
                    st.sidebar.markdown(f"{emoji} {Config.PERSONALITIES[key]['name']}: {count}")

def render_advanced_features():
    """Render advanced features in tabs."""
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "🔧 Settings", "ℹ️ About"])
    
    with tab1:
        st.markdown("### Chat Analytics")
        summary = st.session_state.chatbot.get_conversation_summary()
        
        if summary:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Interactions", summary.get('total_interactions', 0))
            
            with col2:
                st.metric("Personalities Used", len(summary.get('personalities_used', {})))
            
            with col3:
                feedback_count = len([f for f in summary.get('feedback_stats', {}).values() if f])
                st.metric("Feedback Given", feedback_count)
            
            # Personality usage chart
            if summary.get('personalities_used'):
                st.markdown("### Personality Usage")
                personality_df = pd.DataFrame(
                    list(summary['personalities_used'].items()),
                    columns=['Personality', 'Count']
                )
                st.bar_chart(personality_df.set_index('Personality'))
            
            # Cost breakdown
            cost_stats = summary.get('cost_stats', {})
            if cost_stats:
                st.markdown("### 💰 Cost Breakdown")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Cost", f"${cost_stats.get('total_cost', 0):.4f}")
                with col2:
                    st.metric("Total Tokens", f"{cost_stats.get('total_tokens', 0):,}")
                with col3:
                    st.metric("Avg Cost/Interaction", f"${cost_stats.get('avg_cost_per_interaction', 0):.4f}")
                
                # Token breakdown
                st.markdown("#### Token Usage")
                token_data = {
                    'Input Tokens': cost_stats.get('input_tokens', 0),
                    'Output Tokens': cost_stats.get('output_tokens', 0)
                }
                st.bar_chart(token_data)
                
                # Cost projection
                if summary.get('total_interactions', 0) > 0:
                    st.markdown("#### Cost Projections")
                    interactions = summary.get('total_interactions', 0)
                    avg_cost = cost_stats.get('avg_cost_per_interaction', 0)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Cost for 100 interactions", f"${avg_cost * 100:.4f}")
                    with col2:
                        st.metric("Cost for 1000 interactions", f"${avg_cost * 1000:.4f}")
                    with col3:
                        st.metric("Cost for 10000 interactions", f"${avg_cost * 10000:.4f}")
    
    with tab2:
        st.markdown("### Chatbot Settings")
        
        # Model settings
        st.markdown("#### Model Configuration")
        temperature = st.slider("Temperature (Creativity)", 0.0, 1.0, Config.TEMPERATURE, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 2000, Config.MAX_TOKENS, 100)
        
        if st.button("Apply Settings"):
            # Update config (in a real app, you'd save these to a config file)
            st.success("Settings applied! (Note: Changes will take effect on next restart)")
        
        # API Status
        st.markdown("#### API Status")
        if Config.OPENAI_API_KEY:
            st.success("✅ OpenAI API Key configured")
        else:
            st.error("❌ OpenAI API Key not found")
            st.info("Please set your OPENAI_API_KEY in the environment variables")
    
    with tab3:
        st.markdown("### About This Chatbot")
        st.markdown("""
        This is a comprehensive AI chatbot built with:
        
        - **Streamlit** for the web interface
        - **OpenAI GPT** for natural language processing
        - **Multiple personalities** for different interaction styles
        - **Memory management** to maintain conversation context
        - **Feedback system** for continuous improvement
        - **Analytics and logging** for insights
        
        ### Features:
        ✅ Rule-based vs LLM-powered responses  
        ✅ Memory-based conversation history  
        ✅ Multiple personality modes  
        ✅ Error handling and timeouts  
        ✅ Chat logging and export  
        ✅ User feedback system  
        ✅ Analytics dashboard  
        
        ### Advanced Features (Coming Soon):
        🔄 Multimodal support (images + text)  
        🔄 External tool integration  
        🔄 Web search capabilities  
        🔄 Voice input/output  
        """)

def render_analytics_page():
    """Render the detailed analytics page."""
    st.markdown("# 📊 Detailed Analytics Dashboard")
    
    # Get analytics data
    analytics_summary = st.session_state.analytics.get_analytics_summary()
    recent_activity = st.session_state.analytics.get_recent_activity(20)
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", analytics_summary.get('total_users', 0))
    with col2:
        st.metric("Total Messages", analytics_summary.get('total_messages', 0))
    with col3:
        st.metric("Recent Users (24h)", analytics_summary.get('recent_users_24h', 0))
    with col4:
        st.metric("Recent Messages (24h)", analytics_summary.get('recent_messages_24h', 0))
    
    # Charts and detailed breakdowns
    col1, col2 = st.columns(2)
    
    with col1:
        # Device breakdown chart
        device_breakdown = analytics_summary.get('device_breakdown', {})
        if device_breakdown:
            st.markdown("### 📱 Device Types")
            st.bar_chart(device_breakdown)
        
        # Personality usage chart
        personality_usage = analytics_summary.get('personality_usage', {})
        if personality_usage:
            st.markdown("### 🤖 Personality Usage")
            st.bar_chart(personality_usage)
    
    with col2:
        # Location breakdown chart
        location_breakdown = analytics_summary.get('location_breakdown', {})
        if location_breakdown:
            st.markdown("### 🌍 Locations")
            st.bar_chart(location_breakdown)
        
        # Session duration
        avg_duration = analytics_summary.get('avg_session_duration_min', 0)
        st.markdown("### ⏱️ Average Session Duration")
        st.metric("Duration", f"{avg_duration:.1f} minutes")
    
    # Recent activity table
    if recent_activity:
        st.markdown("### 📝 Recent Activity")
        activity_df = pd.DataFrame(recent_activity)
        activity_df['timestamp'] = pd.to_datetime(activity_df['timestamp'])
        activity_df = activity_df.sort_values('timestamp', ascending=False)
        
        # Display only relevant columns
        display_columns = ['timestamp', 'message_type', 'personality', 'message_length']
        if all(col in activity_df.columns for col in display_columns):
            st.dataframe(
                activity_df[display_columns].head(10),
                use_container_width=True
            )
    
    # Session details
    st.markdown("### 🔍 Session Details")
    sessions = st.session_state.analytics.analytics_data.get('sessions', {})
    
    if sessions:
        # Create a summary table of sessions
        session_data = []
        for session_id, session_info in sessions.items():
            session_data.append({
                'Session ID': session_id[:8] + '...',  # Truncate for privacy
                'Start Time': session_info.get('start_time', 'Unknown'),
                'Messages': session_info.get('messages_count', 0),
                'Device': session_info.get('device', {}).get('device_type', 'Unknown'),
                'Personalities Used': len(session_info.get('personalities_used', [])),
                'Last Activity': session_info.get('last_activity', 'Unknown')
            })
        
        session_df = pd.DataFrame(session_data)
        st.dataframe(session_df, use_container_width=True)
    
    # Export analytics data
    st.markdown("### 📤 Export Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Analytics as JSON"):
            analytics_json = json.dumps(st.session_state.analytics.analytics_data, indent=2)
            st.download_button(
                label="Download Analytics JSON",
                data=analytics_json,
                file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📈 Export Analytics as CSV"):
            # Create a CSV with session data
            if sessions:
                session_df.to_csv(index=False)
                csv_data = session_df.to_csv(index=False)
                st.download_button(
                    label="Download Sessions CSV",
                    data=csv_data,
                    file_name=f"sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

def main():
    """Main application function."""
    initialize_session_state()
    
    # Check if analytics page should be shown
    if st.session_state.get('show_analytics', False):
        render_analytics_page()
        
        # Back button
        if st.button("← Back to Chat"):
            st.session_state.show_analytics = False
            st.rerun()
    else:
        # Sidebar
        with st.sidebar:
            render_personality_selector()
            render_sidebar_features()
        
        # Main content
        render_chat_interface()
        
        # Advanced features in tabs
        render_advanced_features()

if __name__ == "__main__":
    main() 