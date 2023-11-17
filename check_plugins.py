from helper.plugin_manager import PluginManager

def main():
    print("[TEST] Launch test for plugin:")
    plugin_manager = PluginManager()
    plugin_manager.test_supported_plugin()

if __name__ == '__main__':
    main()