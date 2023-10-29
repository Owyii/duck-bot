from tldextract import extract

from handler.bunkr_handler import exec_bunkr
from handler.imgur_handler import exec_imgur

async def handler_selector(message,context):
    """ Given a link find the correct site in question
    and call the proprer function to get the media in question
    """
    url = str(message.text)
    ext = extract(url)
    site_name = ext.domain

    match site_name:
        case "bunkrr":
            await exec_bunkr(message,context,url)
        case "imgur":
            await exec_imgur(message,url)
        case default:
            print(f"[{message.chat_id}] {ext.domain} request")
            await message.reply_text(f"{ext.domain} not supported")

    