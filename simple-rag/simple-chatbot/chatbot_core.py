import openai
import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import time
from config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ChatbotCore:
    """Core chatbot functionality with LLM integration and memory management."""
    
    def __init__(self):
        """Initialize the chatbot with OpenAI client and conversation memory."""
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.conversation_history: List[Dict] = []
        self.current_personality = 'friendly'
        self.system_message = Config.PERSONALITIES[self.current_personality]['system_message']
        
        # Cost tracking
        self.total_cost = 0.0
        self.total_tokens_used = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        
        # Initialize chat log
        self._initialize_chat_log()
        
        logger.info("Chatbot initialized successfully")
    
    def _initialize_chat_log(self):
        """Initialize the chat log CSV file if it doesn't exist."""
        try:
            # Check if file exists, if not create with headers
            try:
                pd.read_csv(Config.CHAT_LOG_FILE)
            except FileNotFoundError:
                df = pd.DataFrame(columns=['timestamp', 'personality', 'user_message', 'bot_response', 'feedback'])
                df.to_csv(Config.CHAT_LOG_FILE, index=False)
                logger.info(f"Created new chat log file: {Config.CHAT_LOG_FILE}")
        except Exception as e:
            logger.error(f"Error initializing chat log: {e}")
    
    def set_personality(self, personality: str) -> bool:
        """Set the chatbot personality."""
        if personality in Config.PERSONALITIES:
            self.current_personality = personality
            self.system_message = Config.PERSONALITIES[personality]['system_message']
            logger.info(f"Personality changed to: {personality}")
            return True
        else:
            logger.warning(f"Invalid personality: {personality}")
            return False
    
    def _detect_abusive_language(self, message: str) -> bool:
        """Detect if the message contains abusive or rude language."""
        abusive_keywords = [
            'fuck', 'shit', 'bitch', 'asshole', 'dick', 'pussy', 'cunt', 'bastard',
            'idiot', 'stupid', 'dumb', 'moron', 'retard', 'fool', 'jerk', 'douche',
            'suck', 'sucks', 'sucking', 'fucking', 'fucked', 'fucker',
            'hate', 'hate you', 'you suck', 'you\'re stupid', 'you\'re dumb',
            'shut up', 'shut the fuck up', 'fuck off', 'fuck you', 'go to hell',
            'kill yourself', 'die', 'you\'re worthless', 'you\'re useless'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in abusive_keywords)

    def get_response(self, user_message: str) -> Tuple[str, bool]:
        """
        Get response from the chatbot.
        
        Args:
            user_message: User's input message
            
        Returns:
            Tuple of (response, success_status)
        """
        if not user_message.strip():
            return "Please provide a message to chat with me!", False
        
        # Check for abusive language and switch to savage mode if detected
        original_personality = self.current_personality
        if self._detect_abusive_language(user_message):
            logger.info("Abusive language detected, switching to savage mode")
            self.set_personality('savage')
        
        try:
            # Prepare messages for the API call
            messages = [{"role": "system", "content": self.system_message}]
            
            # Add conversation history (last 10 messages to avoid token limits)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API with timeout
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE,
                timeout=30  # 30 second timeout
            )
            
            bot_response = response.choices[0].message.content
            
            # Track token usage and calculate cost
            self._track_usage_and_cost(response)
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            
            # Log the interaction
            self._log_interaction(user_message, bot_response)
            
            # Switch back to original personality after savage response
            if original_personality != self.current_personality:
                self.set_personality(original_personality)
            
            logger.info(f"Response generated successfully in {time.time() - start_time:.2f}s")
            return bot_response, True
            
        except openai.RateLimitError:
            error_msg = "I'm getting too many requests right now. Please try again in a moment."
            logger.error("OpenAI rate limit exceeded")
            return error_msg, False
            
        except openai.APITimeoutError:
            error_msg = "The request timed out. Please try again."
            logger.error("OpenAI API timeout")
            return error_msg, False
            
        except openai.AuthenticationError:
            error_msg = "Authentication error. Please check your API key."
            logger.error("OpenAI authentication failed")
            return error_msg, False
            
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            logger.error(f"Unexpected error in get_response: {e}")
            return error_msg, False
    
    def _track_usage_and_cost(self, response):
        """Track token usage and calculate API costs."""
        try:
            # Get token usage from response
            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens
            
            # Update token counters
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_tokens_used += total_tokens
            
            # Calculate cost based on model pricing
            model = Config.DEFAULT_MODEL
            if model in Config.MODEL_PRICING:
                pricing = Config.MODEL_PRICING[model]
                input_cost = (input_tokens / 1000) * pricing['input']
                output_cost = (output_tokens / 1000) * pricing['output']
                total_cost = input_cost + output_cost
                
                self.total_cost += total_cost
                
                logger.info(f"Tokens: {input_tokens} input + {output_tokens} output = {total_tokens} total")
                logger.info(f"Cost: ${input_cost:.6f} + ${output_cost:.6f} = ${total_cost:.6f}")
            else:
                logger.warning(f"Pricing not available for model: {model}")
                
        except Exception as e:
            logger.error(f"Error tracking usage and cost: {e}")

    def _log_interaction(self, user_message: str, bot_response: str):
        """Log the interaction to CSV file."""
        try:
            new_row = {
                'timestamp': datetime.now().isoformat(),
                'personality': self.current_personality,
                'user_message': user_message,
                'bot_response': bot_response,
                'feedback': ''  # Will be updated when user provides feedback
            }
            
            df = pd.read_csv(Config.CHAT_LOG_FILE)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(Config.CHAT_LOG_FILE, index=False)
            
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
    
    def add_feedback(self, timestamp: str, feedback: str):
        """Add user feedback to a specific interaction."""
        try:
            df = pd.read_csv(Config.CHAT_LOG_FILE)
            mask = df['timestamp'] == timestamp
            if mask.any():
                df.loc[mask, 'feedback'] = feedback
                df.to_csv(Config.CHAT_LOG_FILE, index=False)
                logger.info(f"Feedback added: {feedback}")
            else:
                logger.warning(f"Timestamp not found: {timestamp}")
        except Exception as e:
            logger.error(f"Error adding feedback: {e}")
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_conversation_summary(self) -> Dict:
        """Get summary statistics of the conversation."""
        try:
            df = pd.read_csv(Config.CHAT_LOG_FILE)
            return {
                'total_interactions': len(df),
                'personalities_used': df['personality'].value_counts().to_dict(),
                'feedback_stats': df['feedback'].value_counts().to_dict() if 'feedback' in df.columns else {},
                'last_interaction': df['timestamp'].iloc[-1] if len(df) > 0 else None,
                'cost_stats': {
                    'total_cost': self.total_cost,
                    'total_tokens': self.total_tokens_used,
                    'input_tokens': self.total_input_tokens,
                    'output_tokens': self.total_output_tokens,
                    'avg_cost_per_interaction': self.total_cost / len(df) if len(df) > 0 else 0,
                    'current_model': Config.DEFAULT_MODEL
                }
            }
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return {}
    
    def export_chat_history(self, format: str = 'csv') -> str:
        """Export chat history in specified format."""
        try:
            if format == 'csv':
                return Config.CHAT_LOG_FILE
            elif format == 'json':
                df = pd.read_csv(Config.CHAT_LOG_FILE)
                json_file = Config.CHAT_LOG_FILE.replace('.csv', '.json')
                df.to_json(json_file, orient='records', indent=2)
                return json_file
            else:
                logger.warning(f"Unsupported export format: {format}")
                return ""
        except Exception as e:
            logger.error(f"Error exporting chat history: {e}")
            return "" 