import socket

class Server:
	encoding = "utf-8"

	def __init__(self, ip, port, connections=10):
		self._ip = ip
		self._port = port
		self._connections = connections
		self._server = socket.socket()
		self._server.bind((self._ip, self._port))
		self._server.listen(self._connections)
		print("Server setup and Listening:")

	def server_loop(self):
		try:
			while True:
				client, c_ip = self._server.accept()
				print(f"Connected to {c_ip}")
				res = ""
				while res != "stop":
					res = client.recv(1024).decode()
					print(res)
					client.send(bytes(f"Server: Hi client, I have recieved your message:\n{res}", Server.encoding))
				client.close()
		except KeyboardInterrupt:
			print("\n Keyboard Interupt")

if __name__ == "__main__":
	s = Server("localhost", 9999, 5)
	s.server_loop()
