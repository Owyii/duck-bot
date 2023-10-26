import requests
from helper.bunkr_helper import bunkr_scraper

session = requests.Session()

async def exec_bunkr(message,context,url):

    chat_id = message.chat.id
    msg_id = message.id

    await message.reply_text("Processing link...")

    r = session.get(url)

    
    if r.status_code == 403:
        print("*** Use Proxy ***")
    # if the connection is possible i get all the link that i need to dowload
    # from that page
    else:
        url_dict = await bunkr_scraper(url)

        for elem_url in url_dict.keys():
            extension = url_dict[elem_url]
            print(f"Processing {elem_url}")
            response = session.get(elem_url,
                                   allow_redirects= True, verify=False,
                                   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
                                   )
            print(response.status_code)
            try:
                open(f"image.{extension}","wb").write(response.content)
                print(f"Uploading {url_dict[elem_url]}...")
                
                try:
                    await context.bot.send_photo(chat_id = chat_id, photo = open(f"image.{extension}","rb"))
                    print("Sent")

                except Exception as e:
                    print(e)

            except Exception as e:
                print(e)
    pass