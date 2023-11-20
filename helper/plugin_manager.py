import os
import importlib.util
from helper.base_plugin import BasePlugin

class PluginManager:
    def __init__(self,plugin_folder='./plugins'):
        self.plugins_folder = plugin_folder
        self.plugins = self._load_plugins()

    def _load_plugins(self):
        print("[INFO] Loading Plugin...")
        plugins = []
        plugin_counter = 0
        for file_name in os.listdir(self.plugins_folder):
            if file_name.endswith('.py') and not file_name.startswith('_'):
                # Is important that the name of the module is also the name of the file
                module_name = file_name[:-3]
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.plugins_folder,file_name))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Eventually you can add here some code to inspect the content
                # of the .py file (for example check if the class is a base plugin) 
                # For now we assuming class name is the same as the module name
                for name in dir(module):
                    item = getattr(module, name)
                    if (
                        isinstance(item, type) and
                        issubclass(item, BasePlugin) and
                        item is not BasePlugin
                    ):
                        plugins.append(item)
                        plugin_counter += 1

        print(f"[INFO] Loaded {plugin_counter} plugins")
        return plugins
    
    def get_supported_plugin(self,link):
        for plugin in self.plugins:
            if plugin.is_supported(link):
                return plugin
        return None
    
    def test_supported_plugin(self):
        """ The function is just use to check if all the plugin are
        implemented, nothing more
        """
        valid_istance = True
        for plugin in self.plugins:
            try:
                obj = plugin(None,None)
                print(f"[TEST] {obj.name} plugin is implemented correctly")
            except TypeError as e:
                print(f"[TEST] {e}")
                valid_istance = False
        return valid_istance
                