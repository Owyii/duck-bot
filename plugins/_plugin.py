from helper.base_plugin import BasePlugin

class Plugin(BasePlugin):
    def __init__(self, bot, chat_id, message=None):
        super().__init__(bot, chat_id, message)

    def is_supported(link):
        return super().is_supported()
    
    def test(self):
        return super().test()
    
    def process_link(self, master_link):
        return super().process_link(master_link)
    
    def get_content(self, content_dict):
        return super().get_content(content_dict)