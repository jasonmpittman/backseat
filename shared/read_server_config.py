
def get_server_config():
	try:
		with open("server_info.config", "r") as server_config:

			line = server_config.readline().strip("\n").split(" ")
			ip = line[0]
			port = int(line[1])
			server_public_key = line[2]
			return ip, port, server_public_key
	except:
		print("Create a server_info.config file")
