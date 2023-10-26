import os
from urllib.parse import urlparse

def get_img_info(href):
    parsed_url = urlparse(href)
    path = parsed_url.path
    filename = os.path.basename(path)
    filename_without_extension, file_extension = os.path.splitext(filename)
    return filename_without_extension,file_extension
