#!/usr/bin/env python3
"""
Telegram Bot with Google Studio API Integration
Main application file for the chatbot
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.google_studio_client import GoogleStudioClient
from src.message_handler import MessageProcessor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.google_studio_client = GoogleStudioClient()
        self.message_processor = MessageProcessor(self.google_studio_client)
        
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        welcome_message = (
            "🤖 Welcome to the Google Studio AI Bot!\n\n"
            "I'm powered by Google's AI Studio and ready to help you with various tasks.\n\n"
            "Just send me any message and I'll respond using advanced AI capabilities!"
        )
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_message = (
            "🆘 How to use this bot:\n\n"
            "• Simply send me any message or question\n"
            "• I'll process it using Google's AI Studio\n"
            "• Get intelligent responses powered by advanced AI\n\n"
            "Commands:\n"
            "/start - Welcome message\n"
            "/help - This help message\n"
            "/clear - Clear conversation history"
        )
        await update.message.reply_text(help_message)
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /clear command to reset conversation"""
        user_id = update.effective_user.id
        self.message_processor.clear_conversation(user_id)
        await update.message.reply_text("🗑️ Conversation history cleared!")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        try:
            user_id = update.effective_user.id
            user_message = update.message.text
            
            logger.info(f"Received message from user {user_id}: {user_message}")
            
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Process message through Google Studio API
            response = await self.message_processor.process_message(user_id, user_message)
            
            # Send response back to user
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "❌ Sorry, I encountered an error while processing your message. Please try again."
            )
    
    def run(self):
        """Start the bot"""
        try:
            # Create application
            application = Application.builder().token(self.token).build()
            
            # Add handlers
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("clear", self.clear_command))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            # Start the bot
            logger.info("Starting Telegram Bot...")
            application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
