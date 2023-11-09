import os
import requests
from urllib.parse import urlparse

def get_img_info(href):
    """ Given a link to a media it give back
    the name without extension and the extension
    """
    parsed_url = urlparse(href)
    path = parsed_url.path
    filename = os.path.basename(path)
    filename_without_extension, file_extension = os.path.splitext(filename)
    return filename_without_extension,file_extension

async def get_text(url):
    """ Given an url it give back the
    html content
    """
    site_request = requests.get(url)
    return site_request.content

def get_max_size(directory):
    """Given a directory it give back 
    the dimension of the bigger file in 
    byte
    """
    max_size = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            if file_size > max_size:
                max_size = file_size
    return max_size

async def download_content(session,path):
    """ The method will try to dowload any bunkr file
    """
    print(f"[DOWNLOAD_CONTENT]{path}")
    try: 
        open(path,"wb").write(session.content)
        return True 
    except Exception as e:
        print(f"Exception on writing {e}")
        return False
