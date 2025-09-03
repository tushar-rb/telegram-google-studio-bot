"""
Message Handler
Processes user messages and manages conversation state
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.google_studio_client import GoogleStudioClient

logger = logging.getLogger(__name__)

class MessageProcessor:
    """Handles message processing and conversation management"""
    
    def __init__(self, google_studio_client: GoogleStudioClient):
        self.client = google_studio_client
        self.conversations: Dict[int, List[Dict]] = {}
        self.last_activity: Dict[int, datetime] = {}
        self.timeout_minutes = int(os.getenv('CONVERSATION_TIMEOUT', '3600')) / 60  # Convert to minutes
    
    async def process_message(self, user_id: int, message: str) -> str:
        """
        Process a user message and return AI response
        
        Args:
            user_id: Telegram user ID
            message: User's message text
            
        Returns:
            AI response string
        """
        try:
            # Clean up old conversations
            self._cleanup_old_conversations()
            
            # Get or initialize conversation history
            conversation_history = self._get_conversation_history(user_id)
            
            # Generate response using Google Studio API
            response = await self.client.generate_response(message, conversation_history)
            
            # Update conversation history
            self._update_conversation(user_id, message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {e}")
            return "Sorry, I encountered an error while processing your message. Please try again."
    
    def _get_conversation_history(self, user_id: int) -> List[Dict]:
        """Get conversation history for a user"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        return self.conversations[user_id]
    
    def _update_conversation(self, user_id: int, user_message: str, ai_response: str):
        """Update conversation history with new exchange"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        # Add user message
        self.conversations[user_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now()
        })
        
        # Add AI response
        self.conversations[user_id].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now()
        })
        
        # Update last activity
        self.last_activity[user_id] = datetime.now()
        
        # Limit conversation history to prevent memory issues
        max_history = 50  # Keep last 50 messages (25 exchanges)
        if len(self.conversations[user_id]) > max_history:
            self.conversations[user_id] = self.conversations[user_id][-max_history:]
        
        logger.debug(f"Updated conversation for user {user_id}, total messages: {len(self.conversations[user_id])}")
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            del self.conversations[user_id]
        if user_id in self.last_activity:
            del self.last_activity[user_id]
        
        logger.info(f"Cleared conversation history for user {user_id}")
    
    def _cleanup_old_conversations(self):
        """Remove conversations that have been inactive for too long"""
        cutoff_time = datetime.now() - timedelta(minutes=self.timeout_minutes)
        users_to_remove = []
        
        for user_id, last_time in self.last_activity.items():
            if last_time < cutoff_time:
                users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            if user_id in self.conversations:
                del self.conversations[user_id]
            del self.last_activity[user_id]
            logger.info(f"Cleaned up inactive conversation for user {user_id}")
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about current conversations"""
        active_users = len(self.conversations)
        total_messages = sum(len(conv) for conv in self.conversations.values())
        
        return {
            'active_users': active_users,
            'total_messages': total_messages,
            'average_messages_per_user': total_messages / active_users if active_users > 0 else 0
        }
    
    def export_conversation(self, user_id: int) -> Optional[List[Dict]]:
        """Export conversation history for a user (for debugging/analysis)"""
        return self.conversations.get(user_id, None)
