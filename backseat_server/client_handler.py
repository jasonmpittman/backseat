from backseat_server import depot

# Track down and fix returning command id 0 bug

class ClientHandler:
	'''
	This is the logical backend to the functionality of the server. The messages
	are sent here for processing. The messages are deconstructed and the necissary
	subsystems are run.
	'''
	def __init__(self):
		'''
		Initializes the depot list.
		'''
		self.depot_list = depot.DepotList()
		working_depot = self.depot_list.get_working_depot("public.pem")
		#for testing
		working_depot.add("ls -al")
		working_depot.add("PWD")

	def client_handler(self, client_dict, sender_key):
		'''
		Decides what subsystem should run based on what message the client has
		sent to the server.
		'''
		#gets working depot
		print("-------")
		print(type(client_dict))
		working_depot = self.depot_list.get_working_depot(sender_key)

		if client_dict["ping"] == False:
			if client_dict["completed"]:
				if client_dict["successful"]:
					depot_item = working_depot.get_by_id(client_dict["command_id"])
					if depot_item is not None:
						# sets the valus of depot item because the depot_item is completed
						depot_item.set(client_dict["completed"], client_dict["stdout"], client_dict["exit_code"])
						# print(f"Modified Depot Item: {depot_item.output()}")
						working_depot.count -= 1
					else:
						# is unable to obtain the depot_item by id
						print("depot_item = none")
						pass
					# print(depot_item.output())
				else:
					#if unsequenced go onto the next item (table this one until the user has ruled on it), else wait for user responce
					# The command was not successful
					print("unsuccessful")
			else:
				# the command was not completed
				# the next step should be to wait until command is done
				print("Not completed")
		else:
			# Pinging the server to figure out if there is a command that can be picked up
			print("Ping == True")
		print("-----@@@@@@@@-----")
		working_depot.print_depot_contents()
		if client_dict["ready"] and working_depot.count > 0:
			print("ready!")
			return working_depot.get_next(), working_depot.count
		else:
			return None, working_depot.count
