from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from decouple import config

from helper.select_handler import handler_selector

bot_token = config("BOT_TOKEN")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help!")

async def links(update,context):
    message = update.message
    await handler_selector(message,context)

def main():
    # Create the app and give it the bot token
    app = Application.builder().token(bot_token).build()

    # ----------- HANDLER ----------------
    app.add_handler(CommandHandler("help",help_handler))
    app.add_handler(MessageHandler(filters.Entity('url'),links))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()