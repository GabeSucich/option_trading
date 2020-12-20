import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import Utils.validTimes as vt

validStockTimes = vt.allStockTimes

def dailyOpenPrice(priceData):

	return priceData["630"]["open_price"]

def dailyClosePrice(priceData):

	return priceData["1255"]["close_price"]

def dailyHighPrice(priceData):

	return max([timePoint["low_price"] for timePoint in list(priceData.values())])

def dailyLowPrice(priceData):

	return max([timePoint["low_price"] for timePoint in list(priceData.values())])

def dailyAveragePrice(priceData):

	total = 0
	count = 0
	for timePoint in priceData.values():
		total += timePoint["open_price"]
		total += timePoint["close_price"]
		count += 2

	return round(total/count, 2)

def dailyVolume(priceData):

	return sum([timePoint["volume"] for timePoint in list(priceData.values())])

"""These functions extract stock price metrics for certain intervals"""

def getIntervalTimes(priceData, startTime, endTime):

	startTime, endTime = eval(startTime), eval(endTime)

	times = []
	for time in list(priceData.keys()):

		if eval(time) >= startTime and eval(time) <= endTime:

			times.append(time)

	return times


def intervalAveragePrice(priceData, intervalTimes):

	total = 0
	count = 0

	for time in intervalTimes:

		total += priceData[time]["open_price"] + priceData[time]["close_price"]
		count += 2

	return round(total/count, 2)

def intervalHighPrice(priceData, intervalTimes):

	return max([priceData[data] for date in intervalTimes])

def intervalLowPrice(priceData, intervalTimes):

	return min([priceData[data] for date in intervalTimes])

def intervalClosePrice(priceData, intervalTimes):

	return priceData[intervalTimes[-1]]["low_price"]

def intervalOpenPrice(priceData, intervalTimes):

	return priceData[intervalTimes[0]]["open_price"]

def intervalVolume(priceData, intervalTimes):

	return sum([priceData[time]["volume"] for time in intervalTimes])






		





