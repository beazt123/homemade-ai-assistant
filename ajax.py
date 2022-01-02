
import sys
import logging
from logging.handlers import SocketHandler
from logging import StreamHandler
from os import path
from lib.utils.setUp import createApp, getConfig, getSetUpConfig

args = sys.argv[1:]
kwargs = dict(arg.upper().split('=') for arg in args)

numeric_level = getattr(logging, kwargs.get('LOG', "CRITICAL"), None)

sockethandler = SocketHandler('localhost', 19996)
streamHandler = StreamHandler(sys.stdout)
streamHandler.setLevel(numeric_level)

logging.basicConfig(
	level=logging.NOTSET, 
	handlers=[
		sockethandler,
		streamHandler
		]
	)



def main():
	path_to_system_config = path.join("lib", "config", "files")
	path_to_user_config = path.join("lib", "config", "devices", "windowsLaptop")
	path_to_setup_config = path.join(path_to_user_config, "setup.yaml")
	system_config_files = [
		path.join(path_to_system_config, "sysconfig.ini"),
		path.join(path_to_system_config, "keys.ini"),
		path.join(path_to_user_config, "userconfig.ini")

	]


	config = getConfig(*system_config_files)
	setup_config = getSetUpConfig(path_to_setup_config)
	app = createApp(config, setup_config)

	app.run()
	

    


if __name__ == "__main__":
	main()
