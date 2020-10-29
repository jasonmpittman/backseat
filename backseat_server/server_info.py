"""
- Server uptime
- Current Depot Data
- Last successfully completed job (For each depot)
- Time since last heartbeat
"""

import time

import json

class ServerInfo:
	def __init__(self):
		self.start_time = time.time()
		self.run_time = None
		self.last_successful_job_time = time.time()
		self.last_successful_job = None
		self.last_heartbeat_time = time.time()
		self.time_since_heartbeat = self.update_heartbeat()
		self.depots_state = []

	def update_heatbeat(self):
		self.time_since_heartbeat = time.time() - self.last_heartbeat_time
		self.last_heatbeat_time = time.time()

	def update_runtime(self):
		self.run_time = time.time() - self.run_time

	def update_last_successful_job(self, job_output):
		self.last_successful_job = job_output
		self.last_successful_job_time = time.time() - self.last_successful_job_time

	def update_depots_state(self, depot_data):
		self.depots_state = depot_data

	def to_json(self):
		self.update_runtime()
		output_dict = {"start_time": self.start_time, "run_time": self.run_time, "last_successful_job_time": self.last_successful_job_time, "last_successful_job": self.last_successful_job, "last_heartbeat_time": self.last_heartbeat_time, "time_since_heartbeat": self.time_since_heartbeat}
		output_json = json.dumps(output_dict)
