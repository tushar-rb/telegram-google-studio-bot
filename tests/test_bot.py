"""
Unit tests for the Telegram Google Studio Bot
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.google_studio_client import GoogleStudioClient
from src.message_handler import MessageProcessor

class TestGoogleStudioClient:
    """Test cases for GoogleStudioClient"""
    
    @patch.dict('os.environ', {'GOOGLE_AI_STUDIO_API_KEY': 'test_key'})
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_client_initialization(self, mock_model, mock_configure):
        """Test that the client initializes correctly"""
        client = GoogleStudioClient()
        assert client.api_key == 'test_key'
        assert client.model_name == 'gemini-pro'
        mock_configure.assert_called_once_with(api_key='test_key')
    
    @patch.dict('os.environ', {})
    def test_client_initialization_no_api_key(self):
        """Test that initialization fails without API key"""
        with pytest.raises(ValueError, match="GOOGLE_AI_STUDIO_API_KEY not found"):
            GoogleStudioClient()
    
    @patch.dict('os.environ', {'GOOGLE_AI_STUDIO_API_KEY': 'test_key'})
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_build_context_simple(self, mock_model, mock_configure):
        """Test building context without history"""
        client = GoogleStudioClient()
        context = client._build_context("Hello", None)
        assert "Hello" in context
    
    @patch.dict('os.environ', {'GOOGLE_AI_STUDIO_API_KEY': 'test_key'})
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_build_context_with_history(self, mock_model, mock_configure):
        """Test building context with conversation history"""
        client = GoogleStudioClient()
        history = [
            {'role': 'user', 'content': 'Hi'},
            {'role': 'assistant', 'content': 'Hello!'}
        ]
        context = client._build_context("How are you?", history)
        assert "Hi" in context
        assert "Hello!" in context
        assert "How are you?" in context


class TestMessageProcessor:
    """Test cases for MessageProcessor"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_client = Mock(spec=GoogleStudioClient)
        self.processor = MessageProcessor(self.mock_client)
    
    def test_get_conversation_history_new_user(self):
        """Test getting conversation history for new user"""
        history = self.processor._get_conversation_history(123)
        assert history == []
        assert 123 in self.processor.conversations
    
    def test_update_conversation(self):
        """Test updating conversation history"""
        user_id = 123
        self.processor._update_conversation(user_id, "Hello", "Hi there!")
        
        history = self.processor.conversations[user_id]
        assert len(history) == 2
        assert history[0]['role'] == 'user'
        assert history[0]['content'] == "Hello"
        assert history[1]['role'] == 'assistant'
        assert history[1]['content'] == "Hi there!"
    
    def test_clear_conversation(self):
        """Test clearing conversation history"""
        user_id = 123
        self.processor._update_conversation(user_id, "Hello", "Hi!")
        
        # Verify conversation exists
        assert user_id in self.processor.conversations
        
        # Clear conversation
        self.processor.clear_conversation(user_id)
        
        # Verify conversation is cleared
        assert user_id not in self.processor.conversations
    
    @pytest.mark.asyncio
    async def test_process_message_success(self):
        """Test successful message processing"""
        self.mock_client.generate_response = AsyncMock(return_value="Test response")
        
        result = await self.processor.process_message(123, "Test message")
        
        assert result == "Test response"
        self.mock_client.generate_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_message_error(self):
        """Test message processing with client error"""
        self.mock_client.generate_response = AsyncMock(side_effect=Exception("API Error"))
        
        result = await self.processor.process_message(123, "Test message")
        
        assert "error" in result.lower()
        assert "try again" in result.lower()


if __name__ == '__main__':
    pytest.main([__file__])
