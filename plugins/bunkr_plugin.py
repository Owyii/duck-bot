from helper.base_plugin import BasePlugin

class BunkrPlugin(BasePlugin):
    def __init__(self, bot, chat_id, message=None):
        super().__init__(bot, chat_id, message)
        self.name = "Bunkr"

    def test():
        print("[BUNKR] test function")

    def is_supported(link):
        if "bunkrr" in link:
            return True
        return False
    
    # Real implementation of the logic of the plugin
    def get_links(self, master_link):
        return super().get_links(master_link)
    