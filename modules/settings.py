# Code by Nicc
# YellowFlower

# Module: settings
# Manages server settings database

import json, os, threading, typing

server_settings_lock = threading.Lock()


# Loads server settings from a file
def load_server_settings() -> typing.Optional[typing.Dict[str, typing.Any]]:
	global server_settings_lock

	server_settings_lock.acquire()

	with open('data/server_settings.json', 'r') as f:
		server_settings = json.loads(f.read())

		server_settings_lock.release()

		print('settings: loaded server settings')
		return server_settings

	print('settings: error reading server settings')
	return None


# Saves server settings to a file
def save_server_settings(server_settings: typing.Optional[typing.Dict[str, typing.Any]]) -> None:
	global server_settings_lock

	server_settings_lock.acquire()

	with open('data/server_settings.json', 'w') as f:
		f.write(json.dump(server_settings))

		print('settings: saved server settings')
		return

	print('settings: error writing server settings')
	return


# Loads bot settings from a file
def load_bot_settings() -> typing.Optional[typing.Dict[str, typing.Any]]:
	with open('data/bot_settings.json', 'r') as f:
		bot_settings = json.loads(f.read())

		print('settings: loaded bot settings')
		return bot_settings

	print ('settings: error reading bot settings')
	return None