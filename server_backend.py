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
		if not self.isin(client_dict):
			pass
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
		if client_dict["completed"]:
			if client_dict["successful"]:
				#depot interaction
				pass
			else:
				#if unsequenced go onto the next item (table this one until the user has ruled on it), else wait for user responce
				pass
		else:
			pass
