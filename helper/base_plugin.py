from abc import ABC, abstractmethod

""" This is the father class for the bot's plugin. 
Follow the requirement stated to implement another site/services
all these method MUST be implemented to work and to maintain 
a certain logic.

The logic at this point of development is:
1. I load all the plugins from the plugins folder
2. The bot is started 

The bot now will receive imput from the users
    3. When the bot receive a link it choose witch plugin to use 
    4. A dict with the correct link to the file and other information(if needed)
    is prepared

    While i iterate through the dictionary
        5. I download the file 
        6. I upload the file to the user chat (optional)
        7. Remove the file locally 

The abstract class are used so these Method MUST be implemented.
"""

class BasePlugin(ABC):

    @abstractmethod
    def __init__(self,bot,chat_id,message=None):
        """ Those are the minimum paramethers to make a plugin
        download something and post it in a chat with a user. 
        """
        self.bot = bot
        self.chat_id = chat_id
        self.message = message

    @abstractmethod
    def is_supported(link):
        """ Given a link retrun true if the plugin support that link 
        and will operate, false is not
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def test(self):
        """ Simple test function, just print something to know if the plugin
        is working or not 
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def process_link(self,master_link):
        """ Given the master link of a page the function should return a 
        dict with the real links to the content as the key and the extension
        of that file as the value. 
        This will need to parse the master link, since some site could host
        Album-like content, in that case the dict will need to have all the 
        file present in that album 
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def get_content(self,content_dict):
        """ Given the content_dict this method will: 
        1. Download the file 
        2. Send the file to the user 
        They are in the same routine because sometimes there is the need to send the file
        while the dowload process is still running.
        !! Remember that this is not true for every site !! 
        For example if i want to download a video from yt i will always have a single file
        the upload will start only when the dowload of the video is completed.
        If im processing a Bunkr album tho i will have multiple images. Since the telegram
        limit for albums is 10 file a good idea is to start uploading as soon as i get to 
        that limit with an asynchronous function.
        """
        raise NotImplementedError("Subclasses must implement this method")