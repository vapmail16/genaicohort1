import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import os

class ChatAnalytics:
    """Analytics tracking for the chatbot application."""
    
    def __init__(self):
        self.analytics_file = "chat_analytics.json"
        self.session_data = {}
        self.load_analytics()
    
    def load_analytics(self):
        """Load existing analytics data."""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    self.analytics_data = json.load(f)
            else:
                self.analytics_data = {
                    'sessions': {},
                    'messages': [],
                    'personalities': {},
                    'devices': {},
                    'locations': {},
                    'total_users': 0,
                    'total_messages': 0,
                    'start_date': datetime.now().isoformat()
                }
        except Exception as e:
            logging.error(f"Error loading analytics: {e}")
            self.analytics_data = {
                'sessions': {},
                'messages': [],
                'personalities': {},
                'devices': {},
                'locations': {},
                'total_users': 0,
                'total_messages': 0,
                'start_date': datetime.now().isoformat()
            }
    
    def save_analytics(self):
        """Save analytics data to file."""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.analytics_data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving analytics: {e}")
    
    def track_session_start(self, session_id: str, user_agent: str = None):
        """Track when a new session starts."""
        try:
            # Get basic device info from user agent
            device_info = self._parse_user_agent(user_agent)
            
            # Get approximate location (this is basic - for production use a proper geolocation service)
            location = self._get_approximate_location()
            
            session_data = {
                'session_id': session_id,
                'start_time': datetime.now().isoformat(),
                'device': device_info,
                'location': location,
                'messages_count': 0,
                'personalities_used': [],
                'last_activity': datetime.now().isoformat()
            }
            
            self.analytics_data['sessions'][session_id] = session_data
            self.analytics_data['total_users'] = len(self.analytics_data['sessions'])
            
            # Track device
            device_type = device_info.get('device_type', 'Unknown')
            self.analytics_data['devices'][device_type] = self.analytics_data['devices'].get(device_type, 0) + 1
            
            # Track location
            country = location.get('country', 'Unknown')
            self.analytics_data['locations'][country] = self.analytics_data['locations'].get(country, 0) + 1
            
            self.save_analytics()
            
        except Exception as e:
            logging.error(f"Error tracking session start: {e}")
    
    def track_message(self, session_id: str, message_type: str, content: str, personality: str = None):
        """Track a message sent or received."""
        try:
            message_data = {
                'session_id': session_id,
                'message_type': message_type,  # 'user' or 'bot'
                'content': content[:100] + '...' if len(content) > 100 else content,  # Truncate for privacy
                'personality': personality,
                'timestamp': datetime.now().isoformat(),
                'message_length': len(content)
            }
            
            self.analytics_data['messages'].append(message_data)
            self.analytics_data['total_messages'] += 1
            
            # Update session data
            if session_id in self.analytics_data['sessions']:
                self.analytics_data['sessions'][session_id]['messages_count'] += 1
                self.analytics_data['sessions'][session_id]['last_activity'] = datetime.now().isoformat()
                
                if personality and personality not in self.analytics_data['sessions'][session_id]['personalities_used']:
                    self.analytics_data['sessions'][session_id]['personalities_used'].append(personality)
            
            # Track personality usage
            if personality:
                self.analytics_data['personalities'][personality] = self.analytics_data['personalities'].get(personality, 0) + 1
            
            self.save_analytics()
            
        except Exception as e:
            logging.error(f"Error tracking message: {e}")
    
    def track_personality_change(self, session_id: str, personality: str):
        """Track when a user changes personality."""
        try:
            if session_id in self.analytics_data['sessions']:
                if personality not in self.analytics_data['sessions'][session_id]['personalities_used']:
                    self.analytics_data['sessions'][session_id]['personalities_used'].append(personality)
                self.analytics_data['sessions'][session_id]['last_activity'] = datetime.now().isoformat()
            
            self.analytics_data['personalities'][personality] = self.analytics_data['personalities'].get(personality, 0) + 1
            self.save_analytics()
            
        except Exception as e:
            logging.error(f"Error tracking personality change: {e}")
    
    def _parse_user_agent(self, user_agent: str) -> Dict:
        """Parse user agent string to extract device info."""
        if not user_agent:
            return {'device_type': 'Unknown', 'browser': 'Unknown', 'os': 'Unknown'}
        
        user_agent = user_agent.lower()
        
        # Device type detection
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            device_type = 'Mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            device_type = 'Tablet'
        else:
            device_type = 'Desktop'
        
        # Browser detection
        if 'chrome' in user_agent:
            browser = 'Chrome'
        elif 'firefox' in user_agent:
            browser = 'Firefox'
        elif 'safari' in user_agent:
            browser = 'Safari'
        elif 'edge' in user_agent:
            browser = 'Edge'
        else:
            browser = 'Other'
        
        # OS detection
        if 'windows' in user_agent:
            os = 'Windows'
        elif 'mac' in user_agent:
            os = 'macOS'
        elif 'linux' in user_agent:
            os = 'Linux'
        elif 'android' in user_agent:
            os = 'Android'
        elif 'ios' in user_agent:
            os = 'iOS'
        else:
            os = 'Unknown'
        
        return {
            'device_type': device_type,
            'browser': browser,
            'os': os
        }
    
    def _get_approximate_location(self) -> Dict:
        """Get approximate location (simplified version)."""
        # In a real implementation, you'd use a geolocation service
        # For now, we'll return a placeholder
        return {
            'country': 'Unknown',
            'region': 'Unknown',
            'city': 'Unknown'
        }
    
    def get_analytics_summary(self) -> Dict:
        """Get a summary of analytics data."""
        try:
            # Calculate time-based stats
            now = datetime.now()
            last_24h = now - timedelta(hours=24)
            last_7d = now - timedelta(days=7)
            
            # Count recent sessions
            recent_sessions = 0
            for session_data in self.analytics_data['sessions'].values():
                session_time = datetime.fromisoformat(session_data['start_time'])
                if session_time > last_24h:
                    recent_sessions += 1
            
            # Count recent messages
            recent_messages = 0
            for message in self.analytics_data['messages']:
                message_time = datetime.fromisoformat(message['timestamp'])
                if message_time > last_24h:
                    recent_messages += 1
            
            # Calculate average session duration
            avg_duration = 0
            if self.analytics_data['sessions']:
                total_duration = 0
                for session_data in self.analytics_data['sessions'].values():
                    start_time = datetime.fromisoformat(session_data['start_time'])
                    last_activity = datetime.fromisoformat(session_data['last_activity'])
                    duration = (last_activity - start_time).total_seconds() / 60  # minutes
                    total_duration += duration
                avg_duration = total_duration / len(self.analytics_data['sessions'])
            
            return {
                'total_users': self.analytics_data['total_users'],
                'total_messages': self.analytics_data['total_messages'],
                'recent_users_24h': recent_sessions,
                'recent_messages_24h': recent_messages,
                'avg_session_duration_min': round(avg_duration, 2),
                'top_personality': max(self.analytics_data['personalities'].items(), key=lambda x: x[1])[0] if self.analytics_data['personalities'] else 'None',
                'device_breakdown': self.analytics_data['devices'],
                'location_breakdown': self.analytics_data['locations'],
                'personality_usage': self.analytics_data['personalities']
            }
            
        except Exception as e:
            logging.error(f"Error getting analytics summary: {e}")
            return {}
    
    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Get recent activity data."""
        try:
            recent_messages = sorted(
                self.analytics_data['messages'],
                key=lambda x: x['timestamp'],
                reverse=True
            )[:limit]
            
            return recent_messages
            
        except Exception as e:
            logging.error(f"Error getting recent activity: {e}")
            return []
    
    def get_session_details(self, session_id: str) -> Optional[Dict]:
        """Get details for a specific session."""
        return self.analytics_data['sessions'].get(session_id)
    
    def get_top_personalities(self, limit: int = 5) -> List[tuple]:
        """Get top personalities by usage."""
        return sorted(
            self.analytics_data['personalities'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
    
    def get_device_stats(self) -> Dict:
        """Get device statistics."""
        return self.analytics_data['devices']
    
    def get_location_stats(self) -> Dict:
        """Get location statistics."""
        return self.analytics_data['locations']
