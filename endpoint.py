# from shared import tcp_socket_handler

# socket_handler = tcp_socket_handler.TcpSocketHandler()

# client_socket = socket_handler.create_client_socket_connect("localhost", 9999)
import sys
from backseat_endpoint import endpoint

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print(f"Needs 4 command line arguements [server_ip, server_port, my_private, their_public], {len(sys.argv)-1} provided")
		exit()
	ip = sys.argv[1]
	port = int(sys.argv[2])
	my_private = sys.argv[3]
	their_public = sys.argv[4]
	E = endpoint.Endpoint(ip, port, my_private, their_public)
	E.operate()
