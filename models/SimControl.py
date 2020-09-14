import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Utils.datetime_funcs import *
from SimPortfolioControl import *
from SimCalendar import *

class Simulation:

	def __init__(self, symbolList, historicalsList, optionHistoricalsList, investment, timeStep, stratFuncName, stratParams):

		self.portfolio = SimPortfolioControl(symbolList, historicalsList, optionHistoricalsList)
		self.dateList = self.createDateList()
		self.calendar = SimCalendar()
		self.currentDate = None
		self.currentTime = None

		def createDateList(sampleHistoricals):

			return [date for date in list(sampleHistoricals.keys())]


