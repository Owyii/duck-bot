from tldextract import extract

from handler.bunkr_handler import exec_bunkr

async def handler_selector(message,context):
    
    url = str(message.text)
    ext = extract(url)
    
    match ext.domain:
        case "bunkrr":
            await exec_bunkr(message,context,url)
        case default:
            print("Site not supported")

    