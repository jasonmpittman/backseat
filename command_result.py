class Command_Result:
	def __init__(self, output, error, exit_code):
		self.output = output
		self.error = error
		self.exit_code = exit_code

	def create_output(self):
		return f"Exit Code: {self.exit_code} \n{self.output}{self.error}"
