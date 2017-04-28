
class TempPID(object):
	"""Implements a temperature pid"""
	def __init__(self, set_point_temp, dt):
		self.setpt = set_point_temp
		self.dt = dt
		self.max = # will hardcode the max voltage
		self.min = # will hardcode the min voltage
		self.p_factor = # will hardcode this value #this should be roughly the power per degree change.
		self.i_factor = # will hardcode this value
		self.d_factor = # will hardcode this value
		self.prev_error = 0
		self.integral = 0

	def getUpdate(self, process_var):
		error = self.setpt - process_var

		pout = self.p_factor*error

		self.integral += error*self.dt
		iout = self.i_factor*self.integral

		derivative = (error - self.prev_error)/self.dt
		dout = self.d_factor*derivative

		output = pout + iout + dout
		output = output if output < self.max else self.max
		output = output if output > self.min else self.min

		self.prev_error = error

		return output

		