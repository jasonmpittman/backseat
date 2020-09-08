from backseat_endpoint import agent

from backseat_endpoint import client

class Endpoint:
	def __init__(self, serv_ip="localhost", serv_port=9999):
		self._agent = agent.Agent()
		self._client = client.Client(serv_ip, serv_port)

	def run_local_command(self):
		#get command from server
		self._client.connect()
		responce = self._client.get_command()
		print("Responce")
		print(responce)
		print("--")
		if responce != None:
			result, exit_code = self._agent.run_command(responce["command"])
			# print(result)
			# command_id, stdout, stderr=""

			print(f"responce['command_id'] = {responce['command_id']}")
			#add stderrr
			self._client.send_results(responce["command_id"], exit_code, result)
		else:
			print("run_local_command: None")

		#run command
		#send results back to the server

	def ready_accept(self):
		self._client.connect()


if __name__ == "__main__":
	E = Endpoint()
	E.run_local_command()
