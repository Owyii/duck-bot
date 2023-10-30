import requests
import shutil
import os 
from helper.bot_utils import get_max_size
from helper.bunkr_helper import bunkr_scraper

from telegram import InputMediaPhoto, InputMediaDocument

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

FOTO_EXT = ['.jpg', '.png',".jpeg",".webp",".gif",".svg",".ico",".raw" ]

async def exec_bunkr(message,context,url):

    chat_id = str(message.chat.id)
    msg_id = message.id

    await message.reply_text("Processing link...")

    r = session.get(url)
    if r.status_code == 403:
        print("*** Use Proxy ***")

    # TODO here is where i divide album from photo
    
    # if the connection is possible i get all the link that i need to dowload
    # from that page
    else:
        print(f"[{chat_id}] start scraping  {url}")
        url_dict = await bunkr_scraper(url)
        print(f"[{chat_id}] finished scraping: {len(url_dict)} links")
        await message.reply_text(f"{len(url_dict)} file found! Working...")


        file_count = 0
        os.mkdir(str(chat_id))

        #download every file
        for elem_url in url_dict.keys():
            extension = url_dict[elem_url]
            response = session.get(elem_url,
                                   allow_redirects= True, verify=False,
                                   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
                                   )
            print(f"[{chat_id}] {elem_url} - {response.status_code}")
            try:
                open(f"{chat_id}/{file_count}.{extension}","wb").write(response.content)                

            except Exception as e:
                print(e)
            
            file_count+=1

        # check max dimension of file 
        # so i wont send img that are too big
        big_files = False
        max_size = get_max_size(str(chat_id))
        print(f"[{chat_id}] requested {max_size} byte")
        if (max_size > 20000000):
            big_files = True
            await message.reply_text(f"The file exceed the limit given by telegram, expect slowdown")

        # Just one file, nothing much to do
        # I keep them separated because the are .zip
        # TODO just one function for one or more file
        if(file_count == 1):

            first_elem = next(iter(url_dict))
            first_elem_ext = url_dict[first_elem]

            if(not big_files and first_elem_ext in FOTO_EXT ):
                try:
                    await context.bot.send_photo(chat_id = chat_id, photo = open(f"{chat_id}/0.{first_elem_ext}","rb"),write_timeout=60)
                    print("Sent")

                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    print(e)
            else:      
                try:
                    await context.bot.send_document(chat_id = chat_id, document = open(f"{chat_id}/0.{first_elem_ext}","rb"), write_timeout=60)
                    print("Sent")

                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    print(e)
 
        # More file = I have an album 
        # there are two kind of album based on 
        # dimension
        else:            
            media_group = []
            element_limiter = 10
            for filename in os.listdir(str(chat_id)):

                current_file = chat_id + "/" + filename
                if(big_files):
                    media_group.append(InputMediaDocument(open(current_file,'rb')))
                else:
                    media_group.append(InputMediaPhoto(open(current_file,'rb')))
                element_limiter-= 1

                # Max size of space for telegram album
                if(element_limiter == 0):
                    try:
                        await context.bot.send_media_group(chat_id = chat_id, media=media_group,write_timeout=None)
                        print("Sent")

                    except Exception as e:
                        await message.reply_text(f"Error: {e}")
                        print(e)
                    element_limiter = 10
                    media_group.clear()

            # If have some leftover img 
            # TODO check if really necessary
            if(element_limiter < 10):
                try:
                    await context.bot.send_media_group(chat_id = chat_id, media=media_group,write_timeout=60)
                    print("Sent")

                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    print(e)

        shutil.rmtree(chat_id)
    pass