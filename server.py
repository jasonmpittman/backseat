from backseat_server import server_loop

import sys

from shared import read_server_config

from backseat_server import server_info

from exceptions.server_restart_exception import ServerRestartException

# def run():
# 	ip, port, server_private_key, server_public_key = read_server_config.get_server_config()
# 	SI = server_info.ServerInfo()
# 	SL = server_loop.ServerLoop(ip, port, 10, server_private_key, server_public_key, SI)
# 	SL.server_loop()

if __name__ == "__main__":
	while True:
		try:
			ip, port, server_private_key, server_public_key = read_server_config.get_server_config()
			SI = server_info.ServerInfo()
			SL = server_loop.ServerLoop(ip, port, 10, server_private_key, server_public_key, SI)
			SL.server_loop()
		except ServerRestartException as E:
			
			print(E)
		except Exception as E:
			print(E)
			break
	
