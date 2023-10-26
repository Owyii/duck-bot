import requests
from bs4 import BeautifulSoup
from helper.bot_utils import get_img_info


async def get_text(url):
    site_request = requests.get(url)
    return site_request.content

async def bunkr_scraper(url):

    url_dict = {}

    # Getting the html file to parsing
    html_text = await get_text(url)
    soup = BeautifulSoup(html_text,"html.parser")

    # Test with only the page with a foto
    for link in soup.find_all("a"):
        href = link.get("href")
        if len(href) > 30:
            if("/report" not in href and "?download" not in href):
                element_url, extension = get_img_info(href)
                image_extension_list = ['.jpg', '.png',".jpeg",".webp",".gif",".svg",".ico",".raw" ]
                if extension in image_extension_list:
                    url_dict[href] = extension
    return url_dict