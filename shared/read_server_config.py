def get_server_config():
	"""his function gets the server configuration from server_info.config which has the format
	|ip port server_private_key server_public_key|

	Returns:
		[touple]: ip, port, server_private_key, server_public_key
	"""
	try:
		with open("server_info.config", "r") as server_config:

			line = server_config.readline().strip("\n").split(" ")
			ip = line[0]
			port = int(line[1])
			server_private_key = line[2]
			server_public_key = line[3]
			return ip, port, server_private_key, server_public_key
	except Exception as E:
		print("Create a server_info.config file")
		print(E)
