import os
import importlib.util

class PluginManager:
    def __init__(self,plugin_folder='./plugins'):
        self.plugins_folder = plugin_folder
        self.plugins = self._load_plugins()

    def _load_plugins(self):
        print("[INFO] Loading Plugin...")
        plugins = []
        for file_name in os.listdir(self.plugins_folder):
            if file_name.endswith('.py') and not file_name.startswith('__init__'):
                # Is important that the name of the module is also the name of the file
                module_name = file_name[:-3]
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.plugins_folder,file_name))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for name in dir(module):
                    item = getattr(module, name)
                    if (
                        isinstance(item, type) and
                        issubclass(item, BasePlugin) and
                        item is not BasePlugin
                    ):
                        plugins.append(item())
        return plugins
    
    def get_supported_plugin(self,link):
        for plugin in self.plugins:
            if plugin.is_