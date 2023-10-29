from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from decouple import config

from helper.select_handler import handler_selector

import os

bot_token = config("BOT_TOKEN")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help!")

async def links(update,context):
    message = update.message
    await handler_selector(message,context)

# async def test(update,context):
#     chat_id = str(247121519)

#     media_group = []
#     element_limiter = 10
#     for filename in os.listdir(chat_id):
#         current_file = chat_id + "/" + filename
#         media_group.append(InputMediaPhoto(open(current_file,'rb')))
#         element_limiter-= 1 

#         if(element_limiter == 0):
#             try:
#                 await context.bot.send_media_group(chat_id = chat_id, media=media_group)
#                 print("Sent")

#             except Exception as e:
#                 print(e)
#             element_limiter = 10
#             media_group.clear()

#     if(element_limiter < 10):
#         try:
#             await context.bot.send_media_group(chat_id = chat_id, media=media_group)
#             print("Sent")

#         except Exception as e:
#             print(e)

    
def main():
    # Create the app and give it the bot token
    app = Application.builder().token(bot_token).build()

    # ----------- HANDLER ----------------
    app.add_handler(CommandHandler("help",help_handler))
    app.add_handler(MessageHandler(filters.Entity('url'),links))
    #app.add_handler(CommandHandler("test",test))
    

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()