from backseat_server import server_loop

import sys
if __name__ == "__main__":
	if len(sys.argv) != 5:
		print(f"Needs 4 command line arguements [server_ip, server_port, server_private_key, server_public_key], {len(sys.argv)-1} provided")
		exit()
	ip = sys.argv[1]
	port = int(sys.argv[2])
	server_private_key = sys.argv[3]
	server_public_key = sys.argv[4]
	SL = server_loop.ServerLoop(ip, port, 10, server_private_key, server_public_key)
	SL.server_loop()
