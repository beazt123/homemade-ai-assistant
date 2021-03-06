
import sys
import logging
import argparse
from os import path, listdir
from pathlib import Path
from logging.handlers import SocketHandler
from logging import StreamHandler
from lib.utils.utils import getConfig, getSetUpConfig
from lib.utils.setUp import createApp




def main(path_to_setup_config):
	path_to_system_config = path.join("lib", "config", "files")
	system_config_files = [
		path.join(path_to_system_config, "sysconfig.ini"),
		path.join(path_to_system_config, "keys.ini")
	]
	config = getConfig(*system_config_files)

	# path_to_setup_config = path.join("lib", "config", "devices", "windowsLaptop.yaml")
	setup_config = getSetUpConfig(path_to_setup_config)


	app = createApp(config, setup_config)
	app.run()
	

    


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("config",
						help="Name of the file without extension if it's in the config/devices folder, else full path",
						type=str)

	parser.add_argument("--list",
						action="store_true",
						help="Displays the list of config files")

	parser.add_argument("-l", "--log",
						type=str,
						help="Set the log level")

	args = parser.parse_args()
	config = args.config
	ls = args.list
	if args.log == None:
		log_level = "CRITICAL"
	else:
		log_level = args.log.upper()


	numeric_level = getattr(logging, log_level, None)
	sockethandler = SocketHandler('localhost', 19996)
	streamHandler = StreamHandler(sys.stdout)
	streamHandler.setLevel(numeric_level + 10)

	logging.basicConfig(
		level=logging.NOTSET, 
		handlers=[
			sockethandler,
			streamHandler
			]
		)

	pathToConfigFiles = path.join("lib", "config", "devices")
	allConfigFiles = listdir(pathToConfigFiles)
	configFiles = list(map(lambda x : Path(x).stem, allConfigFiles))
	configFiles.remove("__pycache__")

	if path.exists(config):
		configfilepath = config

	elif config.lower() == "config" and ls:
		print("The following config files were found:")
		for file in configFiles:
			print(f"\t{file}")
		exit()

	else:
		try:
			chosenConfigIndex = configFiles.index(config)
		except ValueError:
			print(f"{config} is not found in available configurations. The following files were found instead:")
			for file in configFiles:
				print(file)
			exit()
		
		configfilepath = path.join(pathToConfigFiles, allConfigFiles[chosenConfigIndex])
	# print("Running main...")
	# print(configfilepath)

	main(configfilepath)
