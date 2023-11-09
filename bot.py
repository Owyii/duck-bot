from telegram import Update, InputMediaPhoto, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ApplicationBuilder
from decouple import config
from handler.torrent_handler import stop_running_torrent

import asyncio

from helper.select_handler import handler_selector

import os

bot_token = config("BOT_TOKEN")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help!")

async def stop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await stop_running_torrent(message)

async def links(update,context):
    message = update.message
    await handler_selector(message,context)
    
def main():
    # Create the app and give it the bot token, now it run in a local server
    app = Application.builder().token(bot_token).base_url("http://0.0.0.0:8081/bot").read_timeout(600).write_timeout(600).build()

    # # ----------- HANDLER ----------------
    app.add_handler(CommandHandler("help",help_handler))
    app.add_handler(CommandHandler("Stop",stop_handler))
    app.add_handler(MessageHandler(filters.Entity('url'),links))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

    # Separate thread to get real time status update
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    main()