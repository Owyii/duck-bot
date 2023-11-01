import requests
from bs4 import BeautifulSoup
from helper.bot_utils import get_img_info

base_bunkr_url = "https://bunkrr.su"

async def get_text(url):
    site_request = requests.get(url)
    return site_request.content

# TODO change all handler in different function
def img_page(soup,url_dict):
    for link in soup.find("a"):
        href = link.get("href")
        if len(href) > 30:
            if("/report" not in href and "?download" not in href):
                element_url, extension = get_img_info(href)
                image_extension_list = ['.jpg', '.png',".jpeg",".webp",".gif",".svg",".ico",".raw" ]
                if extension in image_extension_list:
                    url_dict[href] = extension
    return url_dict    


async def bunkr_scraper(url):

    url_dict = {}
    url_to_process = []

    # check if album, in case fill a list with all the element
    if("/a/" in url):
        # Getting the html file to parsing
        html_text = await get_text(url)
        soup = BeautifulSoup(html_text,"html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if("/i/" in href):
                url_to_process.append(base_bunkr_url + href)
    else:
        url_to_process.append(url)

    
    print("list of page ready")
    for page in url_to_process:

        # Getting the html file to parsing
        html_text = await get_text(page)
        soup = BeautifulSoup(html_text,"html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")
            if len(href) > 30:
                if("/report" not in href and "?download" not in href):
                    element_url, extension = get_img_info(href)
                    url_dict[href] = extension
    return url_dict