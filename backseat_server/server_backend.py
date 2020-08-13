from backseat_server import depot

# Track down and fix returning command id 0 bug

class ServerBackend:
	def __init__(self):
		self.depot_list = depot.DepotList()
		working_depot = self.depot_list.get_working_depot("localhost")
		working_depot.add("ls -al")
		working_depot.add("PWD")

	def client_handler(self, client_dict):
		#gets working depot
		working_depot = self.depot_list.get_working_depot(client_dict["whoami"])

		print(f"ping = {client_dict['ping']}")

		if client_dict["ping"]== False:
			if client_dict["completed"]:
				if client_dict["successful"]:
					depot_item = working_depot.get_by_id(client_dict["command_id"])
					if depot_item is not None:
						# print("setting depot item information")
						# print("client_dict", client_dict["completed"], client_dict["stdout"], client_dict["exit_code"])
						depot_item.set(client_dict["completed"], client_dict["stdout"], client_dict["exit_code"])
						# print(f"Modified Depot Item: {depot_item.output()}")
						print(lient_dict["stdout"])
						depot_item.count -= 1
					else:
						print("depot_item = none")
						pass
					# print(depot_item.output())
				else:
					#if unsequenced go onto the next item (table this one until the user has ruled on it), else wait for user responce
					print("unsuccessful")
			else:
				print("Not completed")
		else:
			print("Ping == True")
		print("-----@@@@@@@@-----")
		working_depot.print_depot_contents()
		if client_dict["ready"]:
			print("ready!")
			return working_depot.get_next()
		else:
			return None

if __name__ == "__main__":
	SB = ServerBackend()
	client_dict_test = {"whoami": "localhost", "ready": True, "completed": True, "stdout": "stdout: woo", "stderr": "no error today", "successful": True, "exit_code": 0, "command_id": 1}
	SB.client_handler(client_dict_test)









#
