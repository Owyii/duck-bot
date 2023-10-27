from bs4 import BeautifulSoup
from helper.bot_utils import get_text

async def imgur_scraper(url):

    html_text = await get_text(url)
    soup = BeautifulSoup(html_text,"html.parser")

    # Test with only the page with a foto
    for link in soup.select(".post-image a"):
        print(link)
