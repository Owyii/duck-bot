from abc import ABC, abstractmethod
import os
import io
from pyrogram.types import InputMediaPhoto,InputMediaDocument
from PIL import Image
from shutil import rmtree
import asyncio
from aiofiles.os import remove
from aiofiles import open

""" This is the father class for the bot's plugin. 
Follow the requirement stated to implement another site/services
all these method MUST be implemented to work and to maintain 
a certain logic.

The logic at this point of development is:
1. I load all the plugins from the plugins folder
2. The bot is started 

The bot now will receive imput from the users
    3. When the bot receive a link it choose witch plugin to use 
    4. A dict with the correct link to the file and other information(if needed)
    is prepared

    While i iterate through the dictionary
        5. I download the file 
        6. I upload the file to the user chat (optional)
        7. Remove the file locally 

The abstract class are used so these Method MUST be implemented.
"""

class BasePlugin(ABC):

    @abstractmethod
    def __init__(self,bot,chat_id,message=None):
        """ Those are the minimum paramethers to make a plugin
        download something and post it in a chat with a user. 
        Remember to put a self.name with the name of the plugin.
        """
        self.bot = bot
        self.chat_id = str(chat_id)
        self.message = message
        self.dowloading = False
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
        self.upload_queue = asyncio.Queue()

    @abstractmethod
    def is_supported(link):
        """ Given a link retrun true if the plugin support that link 
        and will operate, false is not
        """
        raise NotImplementedError("Subclasses must implement this method")
        
    @abstractmethod
    def process_link(self,master_link):
        """ Given the master link of a page the function should return a 
        dict with the real links to the content as the key and the extension
        of that file as the value. 
        This will need to parse the master link, since some site could host
        Album-like content, in that case the dict will need to have all the 
        file present in that album 
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def get_content(self,content_dict):
        """ Given the content_dict this method will: 
        1. Download the file 
        2. Send the file to the user 
        They are in the same routine because sometimes there is the need to send the file
        while the dowload process is still running.
        !! Remember that this is not true for every site !! 
        For example if i want to download a video from yt i will always have a single file
        the upload will start only when the dowload of the video is completed.
        If im processing a Bunkr album tho i will have multiple images. Since the telegram
        limit for albums is 10 file a good idea is to start uploading as soon as i get to 
        that limit with an asynchronous function.
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    async def Write(self,message_string):
        """ Simple function to write back to the bot chat and in the console, 
        using for debugging since i will change all message in one that i will 
        edit as i need.
        """
        await self.bot.send_message(chat_id = self.chat_id, text = message_string)
        print(f"[{self.chat_id}] {message_string}")

    async def progress(self,current, total):
        """ Sending Text/file has a progress param, pointing to this function
        Can log the progress of the upload (in %). For now i dont know how to
        show the value in the actual telegram chat, but i leave here the
        implementation to print in the console.
        """
        print(f"{current * 100 / total:.1f}%")

    # OLD keep for now if i change
    async def send_content(self):
        """ The function will check the user folder (every user will have a folder
        where the media will be dowloaded) and send in the chat the file.
        The function is a basic one that is planned to work with the majority of the site,
        if need overload this function in the specific plugin.
        """

        img_extension = [".png",'.jpg','.jpeg']
        video_extension = [".mov",".mp4"]
        media_group = []
        tasks = []

        for filename in  os.listdir(self.chat_id):

            file_path = os.path.join(self.chat_id,filename)
            _, ext = os.path.splitext(file_path)

            # if the file is a zip i guess i have to do something
            if(ext == ".zip"):
                tasks.append(asyncio.create_task(self.bot.send_document(chat_id=self.chat_id,document=open(file_path,'rb'))))
            
            # if it is an img
            elif(ext in img_extension):

                # PIL is used to fix the size problem, 
                img = Image.open(file_path)
                if(img.width > 1280 or img.height > 1280):
                    img.thumbnail((1280,1280))

                output = io.BytesIO()
                format_img = 'PNG' if ext=='.png' else 'JPEG'
                img.save(output, format=format_img)
                media_group.append(InputMediaPhoto(output))

            elif(ext in video_extension):
                tasks.append(asyncio.create_task(self.bot.send_video(chat_id=self.chat_id,video=open(file_path,'rb'))))

            # if it is a file
            else:
                tasks.append(asyncio.create_task(self.bot.send_document(chat_id=self.chat_id,document=open(file_path,'rb'),progress=self.progress)))

            #check if i have to send the album
            if(len(media_group) % 10 == 0):
                tasks.append(asyncio.create_task(self.bot.send_media_group(chat_id = self.chat_id,media=media_group.copy())))
                media_group.clear()

            await asyncio.sleep(1)

        tasks.append(asyncio.create_task(self.bot.send_media_group(chat_id = self.chat_id,media=media_group)))
        await asyncio.gather(*tasks)
        rmtree(self.chat_id)
        await self.Write("Upload completed")

    async def deamon_sender(self):
        """ The function will check the user folder (every user will have a folder
        where the media will be dowloaded) and send in the chat the file.
        The function is a basic one that is planned to work with the majority of the site,
        if need overload this function in the specific plugin.
        """

        print(f"[{self.chat_id}] Daemon Sender")

        # Some information on how to treat different type of file
        img_extension = [".png",'.jpg','.jpeg']
        video_extension = [".mov",".mp4"]
        media_group = []

        # The check is in the cycle
        while True:

            # Get the element to upload from the queue
            file_name = await self.upload_queue.get()
            if file_name is None:
                break

            _, ext = os.path.splitext(file_name)

            # Img are the most common i think
            if(ext in img_extension):
                # PIL is used to fix the size problem, 
                img = Image.open(file_name)
                if(img.width > 1280 or img.height > 1280):
                    img.thumbnail((1280,1280))

                output = io.BytesIO()
                format_img = 'PNG' if ext=='.png' else 'JPEG'
                img.save(output, format=format_img)
                media_group.append(InputMediaPhoto(output))
            
            # Other filetype
            else:
                if(ext == ".zip"):
                    # HERE IF I WANT TO DO SOMETHING WITH .zip
                    await self.bot.send_document(chat_id=self.chat_id,document=file_name)              
                elif(ext in video_extension):
                    await self.bot.send_video(chat_id=self.chat_id,video=open(file_name,'rb'))
                else:
                    await self.bot.send_document(chat_id=self.chat_id,document=file_name)
                
            if(len(media_group) % 10 == 0):
                print(f"[{self.chat_id}] sending 10...")
                await self.bot.send_media_group(chat_id = self.chat_id,media=media_group.copy())
                media_group.clear()

            # Removing the file every time to not have useless thing in disk
            await asyncio.sleep(1)
            await remove(file_name)

        print(f"[{self.chat_id}] Missing {len(media_group)}")
        await self.bot.send_media_group(chat_id = self.chat_id,media=media_group)
        rmtree(self.chat_id)
        await self.Write("Upload completed")