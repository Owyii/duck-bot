import requests
from helper.imgur_helper import imgur_scraper

headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}
session = requests.Session()
session.headers = headers 

async def exec_imgur(message,url):

    chat_id = message.chat.id
    msg_id = message.id

    r = session.get(url)

    # TODO condition of error
    if False:
        print("error")
    else:
        await imgur_scraper(url)
        pass