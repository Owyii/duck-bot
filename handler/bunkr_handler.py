import requests
import shutil
import os 
from helper.bunkr_helper import bunkr_scraper

from telegram import InputMediaPhoto

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

        # check of many file I have

        # Just one file, nothing much to do
        # i keep them separated because the are .zip
        if(file_count == 1):

            first_elem = next(iter(url_dict))
            first_elem_ext = url_dict[first_elem]

            if(first_elem_ext in FOTO_EXT):
                try:
                    await context.bot.send_photo(chat_id = chat_id, photo = open(f"{chat_id}/0.{first_elem_ext}","rb"))
                    print("Sent")

                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    print(e)
            else:      
                try:
                    await context.bot.send_document(chat_id = chat_id, document = open(f"{chat_id}/0.{first_elem_ext}","rb"))
                    print("Sent")

                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    print(e)


        
        # More file = I have an album 
        else:
            media_group = []
            element_limiter = 10
            for filename in os.listdir(str(chat_id)):

                current_file = chat_id + "/" + filename
                media_group.append(InputMediaPhoto(open(current_file,'rb')))
                element_limiter-= 1

                # Max size of space for telegram album
                if(element_limiter == 0):
                    print(f"[TEST] {len(media_group)} element")
                    try:
                        await context.bot.send_media_group(chat_id = chat_id, media=media_group)
                        print("Sent")

                    except Exception as e:
                        await message.reply_text(f"Error: {e}")
                        print(e)
                    element_limiter = 10
                    media_group.clear()

            # If have some leftover img 
            if(element_limiter < 10):
                try:
                    await context.bot.send_media_group(chat_id = chat_id, media=media_group)
                    print("Sent")

                except Exception as e:
                    await message.reply_text(f"Error: {e}")
                    print(e)

        shutil.rmtree(chat_id)
    pass