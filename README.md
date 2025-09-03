# Telegram Google Studio AI Bot

A Telegram chatbot powered by Google's AI Studio API that provides intelligent conversational capabilities.

## Features

- 🤖 Intelligent conversations using Google's Gemini AI model
- 💬 Seamless Telegram integration with command support
- 🧠 Conversation history management per user
- 🔧 Easy configuration via environment variables
- 📊 Comprehensive logging for monitoring and debugging

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (from @BotFather)
- Google AI Studio API Key

## Setup

### 1. Get Your API Keys

#### Telegram Bot Token
1. Open Telegram and search for @BotFather
2. Start a chat and use `/newbot` command
3. Follow the instructions to create your bot
4. Save the bot token provided

#### Google AI Studio API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Save the API key securely

### 2. Install Dependencies

```bash
# Clone or navigate to the project directory
cd telegram-google-studio-bot

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your actual API keys
# TELEGRAM_BOT_TOKEN=your_actual_bot_token
# GOOGLE_AI_STUDIO_API_KEY=your_actual_api_key
```

### 4. Run the Bot

```bash
python main.py
```

## Project Structure

```
telegram-google-studio-bot/
├── main.py                 # Main application entry point
├── src/
│   ├── __init__.py
│   ├── google_studio_client.py  # Google AI Studio API client
│   └── message_handler.py       # Message processing logic
├── config/
│   └── settings.py         # Configuration management
├── tests/
│   └── test_bot.py        # Unit tests
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Usage

Once the bot is running, users can:

- Send `/start` to get a welcome message
- Send `/help` to see available commands
- Send `/clear` to reset their conversation history
- Send any text message to chat with the AI

## Configuration Options

You can customize the bot behavior by modifying these environment variables in your `.env` file:

- `GOOGLE_AI_MODEL`: AI model to use (default: gemini-pro)
- `MAX_TOKENS`: Maximum tokens for AI responses (default: 1000)
- `TEMPERATURE`: AI creativity level 0.0-1.0 (default: 0.7)
- `LOG_LEVEL`: Logging verbosity (default: INFO)
- `MAX_MESSAGE_LENGTH`: Maximum message length (default: 4096)
- `CONVERSATION_TIMEOUT`: Conversation memory timeout in seconds (default: 3600)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ main.py
```

### Linting

```bash
flake8 src/ main.py
```

## Troubleshooting

1. **Bot not responding**: Check that your Telegram Bot Token is correct
2. **AI responses failing**: Verify your Google AI Studio API key is valid
3. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
