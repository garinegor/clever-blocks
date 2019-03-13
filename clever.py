class Flight:
	def __init__(self):
		pass

	def takeoff(self, z):
		print("takeoff %s"%z)

	def get_to(self, x,y,z):
		print("getting to: %sm, %sm, %sm,"%(x,y,z))

	def sleep(self, t):
		print("sleeping for %ss"%t)

	def land(self):
		print("landing")

def run_code(code):
	flight = Flight()
	exec(code)