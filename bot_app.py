from pyrogram import Client, filters, idle
from pyrogram.handlers import message_handler
from decouple import config
import asyncio
from helper.plugin_manager import PluginManager

api_id = config("API_ID")
api_hash = config("API_HASH")
bot_token = config("BOT_TOKEN")

URL_PATTERN = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"


app = Client(
    "duck_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)

plugin_manager = PluginManager()

# --------------------- TEST ------------------------------
@app.on_message(filters.command("help"))
def send_help(bot,message):
    chat_id = message.chat.id
    bot.send_message(chat_id = chat_id, text = "This is a test!")

# -------------------- All link ----------------------------------
@app.on_message(filters.regex(pattern=URL_PATTERN))
async def links(bot,message):
    link = message.text
    chat_id = message.chat.id
    supported_plugin = plugin_manager.get_supported_plugin(link)

    if supported_plugin:
        await bot.send_message(chat_id = chat_id, text = "Plugin is selected")
    else:
        await bot.send_message(chat_id = chat_id, text = "Sorry, this link is not supported.")

if __name__ == "__main__":
    asyncio.run(app.run())