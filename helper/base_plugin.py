class BasePlugin:
    def is_supported(self,link):
        raise NotImplementedError("Subclasses must implement this method")
    
    def test(self):
        raise NotImplementedError("Subclasses must implement this method")