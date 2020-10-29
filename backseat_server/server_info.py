"""
- Server uptime
- Current Depot Data
- Last successfully completed job (For each depot)
- Time since last heartbeat
"""

import time

class ServerInfo:
	def __init__(self):
		self.start_time = time.time()
		self.run_time = None
		self.depot_list = None
		self.last_successful_job_time = time.time()
		self.last_successful_job = None
		self.last_heartbeat_time = time.time()
		self.time_since_heatbeat = self.update_heartbeat()
		self.depots_state = []

	def update_heatbeat(self):
		self.time_since_hearbeat = time.time() - self.last_heatbeat_time
		self.last_heatbeat_time = time.time()

	def update_runtime(self):
		self.run_time = time.time() - self.run_time

	def update_last_successful_job(self, job_output):
		self.last_successful_job = job_output
		self.last_successful_job_time = time.time() - self.last_successful_job_time

	def update_depots_state(self, depot_data):
		self.depot_state = depot_data

	def make_json(self):
		pass
