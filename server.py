from backseat_server import server_loop


if __name__ == "__main__":
	# SL()
	SL = server_loop.ServerLoop("localhost", 9999)
	SL.server_loop()
