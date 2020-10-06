from backseat_server import server_loop

import sys
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print(f"Needs 2 command line arguements [server_ip and server_port], {len(sys.argv)-1} provided")
		exit()
	ip = sys.argv[1]
	port = int(sys.argv[2])
	SL = server_loop.ServerLoop(ip, port, 10)
	SL.server_loop()
