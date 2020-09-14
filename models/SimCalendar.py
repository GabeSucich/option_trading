import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Utils.datetime_funcs import *

class SimCalendar:

	def __init__(self, dateList, timeStep):

		assert timeStep in SimDay.possibleTimeSteps, "Invalid time step"

		self.timeStep = timeStep
		self.calendar = self.createCalendar(dateList)
		self.dailyClock = SimDay(self.timeStep)
		self.currentDate = self.getNextDate()
		self.currentTime = self.getNextTime()
		self.finished = False

	def createCalendar(self, dateList):

			for date in dateList:

				yield date

	def refreshDailyClock(self):

		self.dailyClock = SimDay(self.timeStep)
		
	def getNextDate(self):

		return next(self.calendar, None)


	def getNextTime(self):

		return self.dailyClock.getNextTime()


	def getNextPoint(self):

		nextTime = self.getNextTime()

		if not nextTime:

			self.currentDate = self.getNextDate()

			if self.currentDate:

				self.refreshDailyClock()
				self.currentTime = self.getNextTime()

			else:

				self.finished = True
				return

		else:

			self.currentTime = nextTime

		return [self.currentDate, self.currentTime]


	def testCalendar(self):

		while not self.finished:

			data = self.getNextPoint()
			if data:
				print(data)
			
			

class SimDay:

	possibleTimeSteps = ["fiveMinute", "tenMinute", "thirtyMinute"]

	fiveMinute = ['630', '635', '640', '645', '650', '655', '700', '705', '710', '715', '720', '725', '730', '735', '740', '745', '750', '755', '800', '805', '810', '815', '820', '825', '830', '835', '840', '845', '850', '855', '900', '905', '910', '915', '920', '925', '930', '935', '940', '945', '950', '955', '1000', '1005', '1010', '1015', '1020', '1025', '1030', '1035', '1040', '1045', '1050', '1055', '1100', '1105', '1110', '1115', '1120', '1125', '1130', '1135', '1140', '1145', '1150', '1155', '1200', '1205', '1210', '1215', '1220', '1225', '1230', '1235', '1240', '1245', '1250', '1255']
	tenMinute = ['630', '640', '650', '700', '710', '720', '730', '740', '750', '800', '810', '820', '830', '840', '850', '900', '910', '920', '930', '940', '950', '1000', '1010', '1020', '1030', '1040', '1050', '1100', '1110', '1120', '1130', '1140', '1150', '1200', '1210', '1220', '1230', '1240', '1250']
	thirtyMinute = ['630', '730', '830', '930', '1030', '1130', '1230']

	def __init__(self, timeStep):

		self.timeStep = timeStep
		self.schedule = self.createDailySchedule()

	def getNextTime(self):

		return next(self.schedule, None)


	def createDailySchedule(self):

		if self.timeStep == "fiveMinute":

			return self.fiveMinuteTimes()

	def fiveMinuteTimes(self):

		yield from self.fiveMinute


