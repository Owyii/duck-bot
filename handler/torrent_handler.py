import requests
import os
from transmission_rpc import Client
import time
import asyncio
from decouple import config

# check if the torrent is currently working    
def is_running(torrent):
    if(torrent) and (not torrent.seeding):
        return True
    return False

# Return a string with the information
def get_info(torrent):

    state = torrent.status
    progress = torrent.percent_done * 100
    download_rate = torrent.rate_download / 1024 # in kb/s

    return f'{progress:.2f}% complete (down: {download_rate:.1f} kB/s) {state}'

class Torrentmanager:

    def __init__(self,host,port,username,password):
        self.active_dowloads = {}
        self.status_task = {}
        self.torrent_client_api = Client(host=host, port=port, username=username,password=password)

    def start_download(self, user_id, magent_link):
        torrent_dl_path = os.path.join(os.getcwd(),user_id)
        self.active_dowloads[user_id] = self.torrent_client_api.add_torrent(magent_link,download_dir=f"{torrent_dl_path}")
    
    def remove_download(self, user_id):
        self.torrent_client_api.remove_torrent(self.active_dowloads[user_id].id)
        del self.active_dowloads[user_id]
        

    def get_torrent(self,user_id):
        if user_id in self.active_dowloads:
            t = self.active_dowloads[user_id]
            return self.torrent_client_api.get_torrent(t.id)
        else:
            return None

    def close_task(self,chat_id):
        status_task = self.status_task[chat_id]
        status_task.cancel()
        del self.status_task[chat_id]

    async def check_dowload_status(self,bot,chat_id,message):
        torrent = torrent_manager.get_torrent(chat_id)
        status_message = "start"
        while is_running(torrent):
            status_message_new = get_info(torrent)
            print(f"[{chat_id}] {status_message_new}")

            if(status_message != status_message_new):
                await bot.edit_message_text(chat_id=chat_id, message_id = message.message_id, text=status_message_new)
                status_message = status_message_new
            
            await asyncio.sleep(5)
            torrent = torrent_manager.get_torrent(chat_id)

        if(torrent.seeding):
            final_message = 'Download complete!'
            print(f"[{chat_id}] torrent is ended")
            torrent_manager.remove_download(chat_id)
        else:
            print(f"[{chat_id}] has removed the torrent")
            final_message = 'Torrent is been removed'

        await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=final_message)
        self.close_task(chat_id)

        await asyncio.sleep(2)

daemon_user = config("TRANSMISSION_USER")
daemon_password = config("TRANSMISSION_PASSWORD")    
torrent_manager = Torrentmanager("localhost",9091,daemon_user,daemon_password)

async def exec_torrent(message,bot,url):

    chat_id = str(message.chat.id)
    print(f"[{chat_id}] requested torrent")
    torrent_manager.start_download(chat_id,url)

    message = await bot.send_message(chat_id=chat_id, text="Downloading torrent...")

    status_task = asyncio.create_task(torrent_manager.check_dowload_status(bot,chat_id,message))
    torrent_manager.status_task[chat_id] = status_task

async def stop_running_torrent(message):
    chat_id = str(message.chat.id)
    torrent = torrent_manager.get_torrent(chat_id)

    if torrent:
        torrent_manager.remove_download(chat_id)

        await message.reply_text("Torrent Removed")
    else:
        await message.reply_text("No active torrent")
    