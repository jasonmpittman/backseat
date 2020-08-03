import agent

import client

class Endpoint:
	def __init__(self, serv_ip="localhost", serv_port=9999):
		self._agent = agent.Agent()
		self._client = client.Client(serv_ip, serv_port)

	def run_local_command(self):
		#get command from server
		self._client.connect()
		responce = self._client.send_recv()
		result = self._agent.run_command(responce["command"])
		print(result)
		self._client.send_results(result)
		#run command
		#send results back to the server

if __name__ == "__main__":
	E = Endpoint()
	E.run_local_command()
