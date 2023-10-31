import requests
import os
from transmission_rpc import Client

c = Client(host="localhost", port=9091, username="owyii",password="voltaxic2k22")

async def exec_torrent(message, url):
    chat_id = str(message.chat.id)
    print(f"[{chat_id}] requested torrent ")
    torrent_dl_path = os.path.join(os.getcwd(),chat_id)
    print(f"[{chat_id}] dowloading in {torrent_dl_path}")
    os.mkdir(str(chat_id))
    c.add_torrent(url, download_dir=f"{torrent_dl_path}")
    pass