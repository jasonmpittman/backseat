from backseat_server import server_loop

import sys
from shared import read_server_config

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"Needs 1 command line arguement [server_private_key] {len(sys.argv)-1} provided")
		exit()
	ip, port, server_public_key = read_server_config.get_server_config()

	server_private_key = sys.argv[1]

	SL = server_loop.ServerLoop(ip, port, 10, server_private_key, server_public_key)
	SL.server_loop()
