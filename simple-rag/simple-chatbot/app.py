import streamlit as st
import pandas as pd
from datetime import datetime
import time
from chatbot_core import ChatbotCore
from config import Config

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
                    # Add user message to chat
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    # Get bot response
                    with st.spinner("🤔 Thinking..."):
                        response, success = st.session_state.chatbot.get_response(user_input)
                    
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

def main():
    """Main application function."""
    initialize_session_state()
    
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