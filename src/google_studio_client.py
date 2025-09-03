"""
Google AI Studio API Client
Handles interactions with Google's Gemini AI models
"""

import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

logger = logging.getLogger(__name__)

class GoogleStudioClient:
    """Client for interacting with Google AI Studio API"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_AI_STUDIO_API_KEY')
        self.model_name = os.getenv('GOOGLE_AI_MODEL', 'gemini-1.5-flash')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '1000'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        
        if not self.api_key:
            raise ValueError("GOOGLE_AI_STUDIO_API_KEY not found in environment variables")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Safety settings to allow more flexible conversations
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        
        logger.info(f"GoogleStudioClient initialized with model: {self.model_name}")
    
    async def generate_response(self, prompt: str, conversation_history: Optional[list] = None) -> str:
        """
        Generate a response using Google AI Studio
        
        Args:
            prompt: The user's message
            conversation_history: Previous conversation context
            
        Returns:
            AI-generated response
        """
        try:
            # Prepare the full conversation context
            full_context = self._build_context(prompt, conversation_history)
            
            # Generate response
            response = await self.model.generate_content_async(
                full_context,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                ),
                safety_settings=self.safety_settings
            )
            
            if response.text:
                logger.info("Successfully generated response from Google AI Studio")
                return response.text.strip()
            else:
                logger.warning("Empty response from Google AI Studio")
                return "I'm sorry, I couldn't generate a response. Please try rephrasing your message."
                
        except Exception as e:
            logger.error(f"Error generating response from Google AI Studio: {e}")
            return "I'm experiencing technical difficulties. Please try again later."
    
    def _build_context(self, current_prompt: str, conversation_history: Optional[list] = None) -> str:
        """
        Build conversation context for the AI model
        
        Args:
            current_prompt: Current user message
            conversation_history: List of previous messages
            
        Returns:
            Formatted context string
        """
        if not conversation_history:
            return current_prompt
        
        # Build context from conversation history
        context_parts = []
        
        # Add a system prompt for better behavior
        context_parts.append(
            "You are a helpful AI assistant in a Telegram chat. "
            "Respond naturally and helpfully to user messages. "
            "Keep responses concise but informative.\n"
        )
        
        # Add conversation history (limit to recent messages to avoid token limits)
        recent_history = conversation_history[-10:]  # Last 10 exchanges
        
        for message in recent_history:
            if message.get('role') == 'user':
                context_parts.append(f"User: {message['content']}")
            elif message.get('role') == 'assistant':
                context_parts.append(f"Assistant: {message['content']}")
        
        # Add current prompt
        context_parts.append(f"User: {current_prompt}")
        context_parts.append("Assistant:")
        
        return "\n".join(context_parts)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model_name": self.model_name,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "api_configured": bool(self.api_key)
        }
