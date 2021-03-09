import shelve
import robin_stocks


class Example:

	def __init__(self, a, b):
		self.first = a
		self.second = b
		self.add = self.first + self.second

	@property
	def sum(self):
		return self.first + self.second 

