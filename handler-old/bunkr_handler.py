from requests import Session
from bs4 import BeautifulSoup
from shutil import rmtree
import asyncio
import os
from pyrogram.types import InputMediaPhoto,InputMediaDocument
from utils.bot_utils import get_img_info, get_max_size,download_content


# Remove https warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://bunkrr.su"

async def process_bunkr_url(urls):
    """ Given a list of bunkr link give back
    a dict with the links as the keys and the estensions
    of the file as the values
    """ 
    url_dict = {}
    #TODO im not sure if i want to create another session here
    s = Session()
    for url in urls:
        site_request = s.get(url)
        # TODO check if the request crash
        soup = BeautifulSoup(site_request.content,"html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")
            if len(href) > 30:
                if("/report" not in href and "?download" not in href):
                    _,extension = get_img_info(href)
                    url_dict[href] = extension
    del s
    return url_dict

class BunkrManager:
    def __init__(self,message,url):
        self.message = message
        self.chat_id = str(message.chat.id)
        self.message_id = message.id
        self.url = url
        self.session = self.get_session(url)
    
    # TODO should be a global method (maybe)
    async def write(self,message_string):
        await self.message.reply_text(message_string)
        print(f"[{self.chat_id}] {message_string}")

    def get_session(self,url,complete=False):
        session = Session()
        if(complete):
            r = session.get(url,
                            allow_redirects= True, verify=False,
                            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
                            )
        else:
            r = session.get(url)

        if r.status_code == 403:
            self.write("Use proxy")
            return None
        else:
            return r
        
    def get_link(self):
        links = []
        if("/a/" in self.url):
            soup = BeautifulSoup(self.session.content,"html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                # TODO can album have only images?
                if("/i/" in href):
                    links.append(BASE_URL + href)
        else:
            links.append(self.url)
        return links
    
    # TODO think about is worth removing also file while sending
    # TODO file? hello?
    async def get_contents(self,url_dict,bot):
        """ For now it dowload the file 
        because saving 10 photo in ram doesnt seem
        a great idea
        """
        # For now i keep tracking of the task i create, and will wait for all
        # of them to finish to complete the function, this is because i want to start
        # sending img BEFORE i dowloaded everything
        tasks = []

        media_group = []
        file_count = 0
        for file_url in url_dict.keys():
            session = self.get_session(file_url,True)
            if(session):
                # I am passing the local path to the dowload folder specific to a user
                current_file = f"{self.chat_id}/{file_count}{url_dict[file_url]}"
                download_result = await download_content(session,current_file)
                
                if(not download_result):
                    self.write("Error during download")
                else:
                    if(os.path.getsize(current_file) < 20000000):
                        media_group.append(InputMediaPhoto(open(current_file,'rb')))
                    else:
                        media_group.append(InputMediaDocument(open(current_file,'rb')))
                    file_count += 1
            else:
                print("Cannot connect to session")
            
            if(file_count == 3):
                print("[LOG] Sending?")
                tasks.append(asyncio.create_task(bot.send_media_group(chat_id = self.chat_id,media=media_group.copy())))
                # Just to be safe
                await asyncio.sleep(5)
                media_group.clear()
                file_count = 0

        # Senting the remaining file (if they are present)
        if(len(media_group) > 0):
            tasks.append(asyncio.create_task(bot.send_media_group(chat_id = self.chat_id,media=media_group)))

        rmtree(self.chat_id)

        await asyncio.wait(tasks)

async def exec_bunkr(message,context,url):
    
    bunkr_manager = BunkrManager(message,url)
    await bunkr_manager.write("Processing Bunkr link")

    if(bunkr_manager.session):
        await bunkr_manager.write("Session ok")

        # there are 2 different possibilities:
        # > Single file
        # > Album
        # For now i put all the possible link ( 1 or many)
        # In a list/dict to iterate later
        url_to_process = bunkr_manager.get_link()
        await bunkr_manager.write(f"{len(url_to_process)} link found")

        # Processing link -> getting the exact link to the file
        url_dict = await process_bunkr_url(url_to_process)
        await bunkr_manager.write(f"{len(url_dict)} link processed")

        if not os.path.isdir(bunkr_manager.chat_id):
            os.mkdir(bunkr_manager.chat_id)

        # Dowloading and uploading photo
        await bunkr_manager.get_contents(url_dict,context)