# 🤖 AI Chatbot Assistant

A comprehensive, feature-rich chatbot application built with Streamlit and OpenAI GPT. This chatbot includes multiple personalities, memory management, feedback system, and analytics.

## ✨ Features

### Core Features
- **🤖 LLM-Powered Chat**: Uses OpenAI GPT for intelligent, context-aware responses
- **🧠 Memory Management**: Maintains conversation history and context
- **🎭 Multiple Personalities**: Choose from 4 different assistant personalities:
  - 😊 **Friendly Assistant**: Warm, encouraging, and supportive
  - 💼 **Professional Assistant**: Formal, concise, and accurate
  - 😂 **Funny Assistant**: Witty, humorous, and entertaining
  - 🎨 **Creative Assistant**: Imaginative and innovative solutions

### Advanced Features
- **📊 Real-time Analytics**: Track interactions, personality usage, and feedback
- **💾 Chat Logging**: Automatically save all conversations to CSV/JSON
- **👍 Feedback System**: Rate responses with thumbs up/down
- **🎨 Modern UI**: Beautiful, responsive interface with custom styling
- **⚡ Error Handling**: Robust error handling for API timeouts, rate limits, etc.
- **📱 Responsive Design**: Works on desktop and mobile devices

### Export & Analytics
- **📄 Export Options**: Download chat history as CSV or JSON
- **📈 Statistics Dashboard**: View interaction counts, personality usage, and feedback
- **🔧 Settings Panel**: Configure model parameters and view API status

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd simple-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DEFAULT_MODEL=gpt-3.5-turbo
   MAX_TOKENS=1000
   TEMPERATURE=0.7
   LOG_LEVEL=INFO
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
simple-chatbot/
├── app.py                 # Main Streamlit application
├── chatbot_core.py        # Core chatbot functionality
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── chat_history.csv     # Generated chat logs
└── chatbot.log          # Application logs
```

## 🎯 Usage Guide

### Getting Started
1. **Choose a Personality**: Select from the sidebar to change the assistant's behavior
2. **Start Chatting**: Type your message and press "Send Message"
3. **Provide Feedback**: Use thumbs up/down buttons to rate responses
4. **View Analytics**: Check the Analytics tab for insights

### Features in Detail

#### Personality Selection
- **Friendly**: Best for casual conversations and emotional support
- **Professional**: Ideal for work-related questions and formal discussions
- **Funny**: Perfect for entertainment and light-hearted conversations
- **Creative**: Great for brainstorming and innovative problem-solving

#### Chat Controls
- **Clear History**: Remove all conversation history
- **Export Data**: Download chat logs in CSV or JSON format
- **View Statistics**: See interaction counts and usage patterns

#### Advanced Settings
- **Temperature Control**: Adjust response creativity (0.0 = focused, 1.0 = creative)
- **Token Limits**: Control response length
- **API Status**: Check OpenAI API connectivity

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DEFAULT_MODEL` | GPT model to use | `gpt-3.5-turbo` |
| `MAX_TOKENS` | Maximum response length | `1000` |
| `TEMPERATURE` | Response creativity | `0.7` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Custom Personalities
You can add custom personalities by modifying the `PERSONALITIES` dictionary in `config.py`:

```python
PERSONALITIES = {
    'your_personality': {
        'name': 'Your Assistant Name',
        'system_message': 'Your custom system message here.',
        'emoji': '🎯'
    }
}
```

## 🛠️ Development

### Adding New Features
1. **Core Logic**: Add new methods to `ChatbotCore` class in `chatbot_core.py`
2. **UI Components**: Create new functions in `app.py`
3. **Configuration**: Update `config.py` for new settings

### Testing
```bash
# Run with debug mode
streamlit run app.py --logger.level debug
```

### Logging
The application logs to both console and file (`chatbot.log`). Log levels:
- `INFO`: General application events
- `WARNING`: Non-critical issues
- `ERROR`: Critical errors and exceptions

## 📊 Data Storage

### Chat History
- **Format**: CSV with columns: timestamp, personality, user_message, bot_response, feedback
- **Location**: `chat_history.csv`
- **Backup**: Automatically created on first run

### Logs
- **Format**: Timestamped log entries
- **Location**: `chatbot.log`
- **Rotation**: Manual (delete old logs as needed)

## 🔮 Future Enhancements

### Planned Features
- **🖼️ Multimodal Support**: Image + text input/output
- **🔍 Web Search**: Integration with search engines
- **🎤 Voice Input/Output**: Speech-to-text and text-to-speech
- **🔗 External Tools**: Function calling for external APIs
- **👥 Multi-user Support**: User authentication and profiles
- **📱 Mobile App**: Native mobile application

### Advanced Integrations
- **Database Storage**: PostgreSQL/MongoDB for scalable storage
- **Real-time Updates**: WebSocket connections for live chat
- **AI Model Switching**: Support for multiple LLM providers
- **Custom Training**: Fine-tune models for specific domains

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**API Key Error**
```
Authentication error. Please check your API key.
```
- Verify your OpenAI API key is correct
- Ensure the key has sufficient credits
- Check if the key is properly set in `.env` file

**Timeout Error**
```
The request timed out. Please try again.
```
- Check your internet connection
- Try reducing `MAX_TOKENS` in configuration
- Wait a few minutes and retry

**Rate Limit Error**
```
I'm getting too many requests right now. Please try again in a moment.
```
- Wait 1-2 minutes before sending another message
- Consider upgrading your OpenAI plan for higher rate limits

### Getting Help
- Check the logs in `chatbot.log` for detailed error information
- Review the Analytics tab for usage patterns
- Ensure all dependencies are properly installed

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT API
- **Streamlit** for the amazing web framework
- **Pandas** for data manipulation and export features

---

**Happy Chatting! 🤖✨** 