import depot

class ServerBackend:
	def __init__(self):
		self.depot_list = []

	def isin(self, dict):
		for item in self.depot_list:
			if dict["whoami"] == item.host:
				return True

		return False

	def client_handler(self, client_dict):
		working_depot = None
		if not self.isin(client_dict):
			new_depot = depot.Depot(client_dict["whoami"])
			self.depot_list.append(new_depot)
			working_depot = new_depot
		else:
			for depot_object in self.depot_list:
				if depot_object.host == client_dict["whoami"]:
					working_depot = depot_object

		#for testing
		working_depot.add("ls -al", 1)


		if client_dict["completed"]:
			if client_dict["successful"]:
				depot_item = working_depot.get_by_id(1)
				depot_item.set(client_dict["completed"], client_dict["stdout"], client_dict["exit_code"])
				depot_item.count -= 1
				# print(depot_item.output())
			else:
				#if unsequenced go onto the next item (table this one until the user has ruled on it), else wait for user responce
				print("unsuccessful")
		else:
			print("Not completed")

		if client_dict["ready"]:
			return working_depot.get_next()
		else:
			return None

		'''
		if completed:
			if sucessful:
				mark command with command id as done
				bring back stdout information
				give user exit code  --> perhaps attach to the item
			if failed:
				let user know, provide stderr
				if not in sequence go to next item
				Give user exitcode

		else (not completed):
			Assmue it to time to check for a ready

		if ready:
			send next command
		else:
			do not do anythnig
		'''


if __name__ == "__main__":
	SB = ServerBackend()
	client_dict_test = {"whoami": "localhost", "ready": True, "completed": True, "stdout": "stdout: woo", "stderr": "no error today", "successful": True, "exit_code": 0, "command_id": 1}
	SB.client_handler(client_dict_test)









#
