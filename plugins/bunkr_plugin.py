from helper.base_plugin import BasePlugin
from bs4 import BeautifulSoup
from requests import Session
import os
from shutil import rmtree
from pyrogram.types import InputMediaPhoto,InputMediaDocument
from utils.bot_utils import get_file_info, download_content
import asyncio
import aiofiles

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BunkrPlugin(BasePlugin):
    def __init__(self, bot, chat_id, message=None):
        super().__init__(bot, chat_id, message)
        self.name = "Bunkr"
        self.base_url = "https://bunkrr.su"

    def is_supported(link):
        if "bunkrr" in link:
            return True
        return False
        
    async def process_link(self, master_link):
        
        links = []
        session = Session()
        r = session.get(master_link)

        # The first part get a link of all the links (because album exists)
        if(r.status_code == 200):
            if("/a/" in master_link):
                soup = BeautifulSoup(r.content,"html.parser")
                for link in soup.find_all("a"):
                    href = link.get("href")
                    # TODO can album have only images?
                    if("/i/" in href):
                        links.append(self.base_url + href)
            else:
                links.append(master_link)

            # Now that i have a list with all the link i can process them
            url_dict = {}
            for url in links:
                specific_url_request = session.get(url)
                # Check if the request is ended in a good way or not
                if(specific_url_request.status_code == 200):
                    soup = BeautifulSoup(specific_url_request.content,"html.parser")
                    for link in soup.find_all("a"):
                        href = link.get("href")
                        if len(href) > 30:
                            if("/report" not in href and "?download" not in href):
                                name,extension = get_file_info(href)
                                url_dict[href] = {
                                    "ext":extension,
                                    "name":name
                                }
            del r
            await super().Write(f"Parsed {len(url_dict)} links")
            return url_dict
            
        # ---------- The first session is not good -----------------
        else:
            await super().Write(f"Link not valid, exit code: {r.status_code}")
    
    async def get_content(self, content_dict):
        """ For now it dowload the file 
        because saving 10 photo in ram doesnt seem
        a great idea
        """
        print(f"[{self.chat_id}] Get content")
        self.dowloading = True

        if not os.path.isdir(self.chat_id):
            os.mkdir(self.chat_id)

        error = 0
        file_count = 0
        session = Session()
        message = await self.bot.send_message(chat_id=self.chat_id, text="Downloading content...")
        for file_url in content_dict.keys():
            file_information = content_dict[file_url]
            with session.get(file_url,
                            allow_redirects= True, verify=False,
                            headers=self.header,stream=True) as specific_url_request:
                if(specific_url_request.status_code == 200):
                    current_file = f"{self.chat_id}/{file_information['name']}{file_information['ext']}"
                    #download_result = await download_content(specific_url_request,current_file)

                    #dowload splitted in chunksize
                    download_result = False
                    print(f"[DOWNLOAD_CONTENT]{current_file}")
                    try: 
                        async with aiofiles.open(current_file,"wb") as file:
                            for chunk in specific_url_request.iter_content(chunk_size=8192):
                                await file.write(chunk)
                            download_result = True
                    except Exception as e:
                        print(f"Exception on writing {e}")

                    # Updating counting
                    file_count += 1
                    if(not download_result):
                        error+=1

                    await self.bot.edit_message_text(chat_id=self.chat_id, message_id = message.id, text=f"Dowloaded {file_count}/{len(content_dict)} {error} errori")
                    
                else:
                    print(f"[CHECK] NOT ok for {file_url}")

                # Introduce a delay of 1 second without blocking the event loop
                # An for safety
            await asyncio.sleep(1)

        self.dowloading = False
        await super().Write("Finished dowloading")    