from backseat_server import server_loop

import sys
from shared import read_server_config

if __name__ == "__main__":
	ip, port, server_private_key, server_public_key = read_server_config.get_server_config()


	SL = server_loop.ServerLoop(ip, port, 10, server_private_key, server_public_key)
	SL.server_loop()
