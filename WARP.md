# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Telegram chatbot powered by Google's AI Studio (Gemini) API that provides intelligent conversational capabilities. The bot maintains conversation history per user and supports standard Telegram bot commands.

## Essential Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with actual API keys: TELEGRAM_BOT_TOKEN and GOOGLE_AI_STUDIO_API_KEY
```

### Running the Application
```bash
# Start the bot
python main.py
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_bot.py

# Run with verbose output
pytest -v tests/
```

### Code Quality
```bash
# Format code
black src/ main.py

# Lint code
flake8 src/ main.py

# Run both formatting and linting
black src/ main.py && flake8 src/ main.py
```

## High-Level Architecture

### Core Components

**main.py** - Main application entry point
- `TelegramBot` class orchestrates the entire bot functionality
- Handles Telegram webhook setup and command routing
- Integrates GoogleStudioClient and MessageProcessor
- Provides command handlers: `/start`, `/help`, `/clear`

**src/google_studio_client.py** - Google AI Studio API integration
- `GoogleStudioClient` manages interactions with Gemini AI models
- Handles conversation context building with system prompts
- Configures safety settings and generation parameters
- Implements async response generation with error handling

**src/message_handler.py** - Message processing and conversation management
- `MessageProcessor` maintains per-user conversation history
- Implements conversation timeout and cleanup mechanisms
- Limits conversation history to prevent memory issues (50 messages max)
- Provides conversation export functionality for debugging

**config/settings.py** - Centralized configuration
- `BotSettings` class with environment variable management
- Configuration validation with error/warning reporting
- Secure configuration dictionary export (hides sensitive values)

### Data Flow Architecture

1. **Message Reception**: Telegram webhook → `main.py:handle_message()`
2. **Processing Pipeline**: `MessageProcessor.process_message()` → conversation history retrieval
3. **AI Generation**: `GoogleStudioClient.generate_response()` → context building → Gemini API call
4. **Response Delivery**: AI response → conversation history update → Telegram message reply
5. **Memory Management**: Automatic cleanup of inactive conversations and history limiting

### Key Design Patterns

**Conversation Context Management**: The system builds rich conversation context by:
- Adding a system prompt for consistent AI behavior
- Including last 10 message exchanges for context
- Maintaining conversation state per user with timestamps
- Auto-expiring conversations after configurable timeout (default: 1 hour)

**Error Handling Strategy**: Multi-layer error handling ensures robustness:
- API client level: Catches Google AI Studio API errors
- Message processor level: Handles processing errors gracefully  
- Bot level: Provides fallback responses for any unhandled exceptions

**Async Architecture**: Uses python-telegram-bot's async framework for:
- Non-blocking message processing
- Concurrent handling of multiple users
- Efficient Google AI Studio API calls

## Environment Configuration

Required environment variables:
- `TELEGRAM_BOT_TOKEN` - Bot token from @BotFather
- `GOOGLE_AI_STUDIO_API_KEY` - API key from Google AI Studio

Optional configuration:
- `GOOGLE_AI_MODEL` - AI model (default: gemini-1.5-flash)
- `MAX_TOKENS` - Response length limit (default: 1000) 
- `TEMPERATURE` - AI creativity 0.0-1.0 (default: 0.7)
- `CONVERSATION_TIMEOUT` - Memory timeout in seconds (default: 3600)
- `MAX_MESSAGE_LENGTH` - Telegram message limit (default: 4096)
- `LOG_LEVEL` - Logging verbosity (default: INFO)

## Bot Commands and Usage

- `/start` - Welcome message and bot introduction
- `/help` - Display available commands and usage instructions  
- `/clear` - Reset conversation history for the current user
- Any text message triggers AI conversation with context awareness

## Testing Strategy

The test suite focuses on:
- **GoogleStudioClient**: API configuration, context building, error scenarios
- **MessageProcessor**: Conversation management, history operations, async processing
- Mock-based testing to avoid external API dependencies during testing
- Async test support with pytest-asyncio

## Development Notes

- Conversation history is limited to 50 messages (25 exchanges) per user to prevent memory issues
- The system automatically cleans up inactive conversations based on configured timeout
- Context building includes system prompts for consistent AI assistant behavior
- Safety settings are configured to allow flexible conversations while blocking harmful content
- All sensitive configuration values are properly masked in logging and config exports
