import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from volumeAnalysisUtils import *
from Utils.datetime_funcs import *

def volumeAnalysis(sellParams, buyParams, recordLength, simulation):

	intervalSize = 1

	if simulation.timeStep == "fiveMinute":

		intervalSize = 78


	if not simulation.persistentVariables:

		createRecords(simulation)

	if simulation.currentTime == "630":

		refreshRecords(simulation)

	for stockPortfolio in list(simulation.portfolio.stockPortfolios.values()):

		stock = stockPortfolio.stock
		symbol = stockPortfolio.symbol
		currentRecords = simulation.persistentVariables["records"][symbol]

		sellPressure = getSellPressure(stock, intervalSize)
		buyPressure = getBuyPressure(stock, intervalSize)
		data = {"volume": stock.volume, "sellPressure": sellPressure, "buyPressure": buyPressure}
		addDataToRecords(data, currentRecords, recordLength)


		if len(currentRecords) >= recordLength:

			
			if eval(simulation.currentTime) <= 1230: 

				[sellPressureGradient, sellPressureConcavity, sellPressureJerk] = desctructureCubic(cubicRegression(currentRecords, "sellPressure"))
				buyPressureGradient, buyPressureConcavity, buyPressureJerk = -sellPressureGradient, -sellPressureConcavity, -sellPressureJerk

				volumeGradient = linearRegression(currentRecords, "volume")
				normalizedVolumeGradient = volumeGradient*100/(currentRecords[0]["volume"])

				if sellParams:

					volumeAnalysisDrops(sellParams, normalizedVolumeGradient, sellPressure, sellPressureGradient, sellPressureConcavity, sellPressureJerk, stockPortfolio)

				if buyParams:

					volumeAnalysisJumps(buyParams, normalizedVolumeGradient, buyPressure, buyPressureGradient, buyPressureConcavity, buyPressureJerk, stockPortfolio)

			for option in stockPortfolio.options:

				if option.isActive() and (option.percentChange > 30 or option.percentChange < -20):
					print("selling option")
					print(option.percentChange)
					stockPortfolio.sellOption(option)
					
					


def createRecords(simulation):

	simulation.persistentVariables["records"] = {}

	refreshRecords(simulation)

def refreshRecords(simulation):

	for stockPortfolio in list(simulation.portfolio.stockPortfolios.values()):

		simulation.persistentVariables["records"][stockPortfolio.symbol] = []

def volumeAnalysisDrops(sellParams, vg, sp, sg, sc, sj, stockPortfolio):

	[csvg, csp, csg, csc, csj] = sellParams

	def checkSellCriteria():

		if (vg >= csvg and sp <= csp and sg >= csg and sc >= csc and sj >= csj):

			return True

		return False

	if checkSellCriteria():

		print(vg, sp, sg, sc, sj)

		purchaseMax = stockPortfolio.availableCash/2

		
		print("Sell trigger")
		stockPortfolio.purchaseShortestPut(purchaseMax)

def volumeAnalysisJumps(buyParams, vg, bp, bg, bc, bj, stockPortfolio):

	[cbvg, cbp, cbg, cbc, cbj] = buyParams

	def checkBuyCriteria():

		if (bg >= cbvg and bp <= cbp and bg >= cbg and bc >= cbc and bj >= cbj):

			return True

		return False

	if checkBuyCriteria():

		purchaseMax = stockPortfolio.availableCash/2

		stockPortfolio.purchaseShortestCall(purchaseMax)


def getSellPressure(stock, intervalSize):

	epsilon = 1 - (stock.closePrice - stock.openPrice)**2/(stock.closePrice + stock.openPrice)**2
	
	return 10000*intervalSize*(1/epsilon - 1)*np.sign(stock.openPrice - stock.closePrice)

def getBuyPressure(stock, intervalSize):

	epsilon = 1 - (stock.closePrice - stock.openPrice)**2/(stock.closePrice + stock.openPrice)**2
	return 10000*intervalSize*(1/epsilon - 1)*np.sign(stock.closePrice - stock.openPrice)


