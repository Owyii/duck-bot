from helper.base_plugin import BasePlugin

class BunkrPlugin(BasePlugin):

    def test(self):
        print("[BUNKR] test function")

    def is_supported(self, link):
        if "bunkrr" in link:
            return True
        return False