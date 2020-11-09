"""
- Server uptime
- Current Depot Data
- Last successfully completed job (For each depot)
- Time since last heartbeat
"""

import time

import json

class ServerInfo:
	"""
	This class keeps track of attributes and information about the server. In addition it exports that information in json format.

	Attributes
	----------
	start_time : time as floating point value
	run_time : time as floating point value
	last_successful_job_time : time as floating point value
	last_successful_job : str
	last_heartbeat_time : time as floating point value
	depots_state : list of str
	"""
	def __init__(self):
		"""
		This function initializes all values that need initializing.

		Parameters
		----------
		"""
		self.start_time = time.time()
		self.run_time = None
		self.last_successful_job_time = time.time()
		self.last_successful_job = None
		self.last_heartbeat_time = time.time()
		self.depots_state = []
		self.time_since_heartbeat = time.time()

	def update_heatbeat(self):
		"""
		Updates the time since_since_heatbeat and last_heartbeat_time. This function is to be run after a heartbeat occurs.
		Parameters
		----------
		"""
		self.time_since_heartbeat = time.time() - self.last_heartbeat_time
		self.last_heatbeat_time = time.time()

	def update_runtime(self):
		"""
		Updates how long the server has been running. This function should be run any time you want to return the information stored in this class.

		Parameters
		----------
		"""
		self.run_time = time.time() - self.start_time

	def update_last_successful_job(self, job_output):
		"""
		Updates last_successful_job and last_successful_job_time. This function should be run after every successful job has run.

		Parameters
		----------
		job_output : str
		"""
		self.last_successful_job = job_output
		self.last_successful_job_time = time.time() - self.last_successful_job_time

	def update_depots_state(self, depot_data):
		"""
		Updates the depot state
		Parameters
		----------
		depot_data : list of lists that contain str
		"""
		self.depots_state = depot_data

	def to_json(self):
		"""
		Converts all useful data in this class into json format, then returns it as a str.

		Parameters
		----------
		"""
		self.update_runtime()
		output_dict = {"start_time": self.start_time, "run_time": self.run_time, "last_successful_job_time": self.last_successful_job_time, "last_successful_job": self.last_successful_job, "last_heartbeat_time": self.last_heartbeat_time, "time_since_heartbeat": self.time_since_heartbeat, "depots_state": self.depots_state}
		output_json = json.dumps(output_dict)
		return output_json
