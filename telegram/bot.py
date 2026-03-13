import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Setup basic logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AGENTS_API_URL = os.getenv("AGENTS_API_URL", "http://agents:8000")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I am HomeAI. Send me a task and I will delegate it to my agents."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    
    await context.bot.send_message(chat_id=chat_id, text="Thinking...")

    try:
        response = requests.post(f"{AGENTS_API_URL}/tasks", json={"message": user_text}, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        agent_name = data.get("selected_agent", "unknown")
        result = data.get("result", "")
        
        reply_text = f"**Agent:** {agent_name}\n\n{result}"
        
        # Telegram messages have a length limit, truncating if necessary
        if len(reply_text) > 4000:
            reply_text = reply_text[:4000] + "\n...[truncated]"
            
        await context.bot.send_message(chat_id=chat_id, text=reply_text, parse_mode="Markdown")
        
    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id, 
            text=f"Error communicating with Agent API: {str(e)}"
        )

if __name__ == '__main__':
    if not TOKEN or TOKEN == "your_telegram_bot_token_here":
        logging.warning("TELEGRAM_BOT_TOKEN is not set properly. Bot will not start.")
    else:
        app = ApplicationBuilder().token(TOKEN).build();
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        logging.info("Starting Telegram Bot...")
        app.run_polling()
