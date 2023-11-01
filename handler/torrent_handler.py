import requests
import os
from transmission_rpc import Client
import libtorrent as lt
import time

async def exec_torrent(message,bot,url):

    # Initialize client / create folder
    chat_id = str(message.chat.id)
    c = Client(host="localhost", port=9091, username="",password="")
    torrent_dl_path = os.path.join(os.getcwd(),chat_id)
    print(f"[{chat_id}] requested torrent in {torrent_dl_path}")
    
    if not os.path.exists(torrent_dl_path):
        os.mkdir(str(chat_id))
    
    t = c.add_torrent(url, download_dir=f"{torrent_dl_path}")
    torrent = c.get_torrent(t.id)

    message = await bot.send_message(chat_id=chat_id, text="Downloading torrent...")


    status_message = f'start'
    while not torrent.seeding:

        state = torrent.status
        progress = torrent.percent_done * 100
        download_rate = torrent.rate_download / 1024 # in kb/s

        status_message_new = f'{progress:.2f}% complete (down: {download_rate:.1f} kB/s) {state}'
        print(status_message_new)
        if(status_message != status_message_new):
            await bot.edit_message_text(chat_id=chat_id, message_id = message.message_id, text=status_message_new)
            status_message = status_message_new

        time.sleep(1)

    final_message = 'Download complete!'
    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=final_message)

async def exec_torrent_libtorrent(message,url):
    chat_id = str(message.chat.id)
    client_folder = os.path.join(os.getcwd(),chat_id)
    os.mkdir(client_folder)

    session = lt.session()
    info = lt.parse_magnet_uri(url)
    handle = session.add_torrent({'ti':info,'save_path': client_folder})
    message = None

    while not handle.is_seed():
        s = handle.status()
        progress = s.progress * 100
        download_rate = s.download_rate / 1000
        state = s.state

        status_message = f'{progress:.2f}% complete (down: {download_rate:.1f} kB/s {state}'

        if message is None:
            message = message.reply_text(chat_id=chat_id, text=status_message)
        else:
            message.edit_text(chat_id=chat_id, message_id=message.message_id, text=status_message)

        lt.sleep(1)

    