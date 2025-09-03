"""
Configuration Settings
Centralized configuration management for the bot
"""

import os
from typing import Dict, Any

class BotSettings:
    """Bot configuration settings"""
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Google AI Studio Configuration
    GOOGLE_AI_STUDIO_API_KEY = os.getenv('GOOGLE_AI_STUDIO_API_KEY')
    GOOGLE_AI_MODEL = os.getenv('GOOGLE_AI_MODEL', 'gemini-1.5-flash')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Bot Behavior Configuration
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4096'))
    CONVERSATION_TIMEOUT = int(os.getenv('CONVERSATION_TIMEOUT', '3600'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """
        Validate that all required settings are present
        
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        # Check required settings
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is required")
        
        if not cls.GOOGLE_AI_STUDIO_API_KEY:
            errors.append("GOOGLE_AI_STUDIO_API_KEY is required")
        
        # Check optional but recommended settings
        if cls.MAX_TOKENS > 2000:
            warnings.append("MAX_TOKENS is set very high, this may impact performance")
        
        if cls.TEMPERATURE > 1.0 or cls.TEMPERATURE < 0.0:
            warnings.append("TEMPERATURE should be between 0.0 and 1.0")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary"""
        return {
            'telegram_bot_token': bool(cls.TELEGRAM_BOT_TOKEN),  # Don't expose actual token
            'google_ai_studio_api_key': bool(cls.GOOGLE_AI_STUDIO_API_KEY),  # Don't expose actual key
            'google_ai_model': cls.GOOGLE_AI_MODEL,
            'max_tokens': cls.MAX_TOKENS,
            'temperature': cls.TEMPERATURE,
            'max_message_length': cls.MAX_MESSAGE_LENGTH,
            'conversation_timeout': cls.CONVERSATION_TIMEOUT,
            'log_level': cls.LOG_LEVEL
        }
