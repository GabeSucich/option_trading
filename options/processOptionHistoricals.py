import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Utils.datetime_funcs import *


def nearestExpiration(date, historicals):
	allExpirations = list(historicals.keys())
	for expiration in allExpirations:

		futureDates = [int(date_remove_dashes(expiration)) for expiration in allExpirations if is_not_past(expiration, date) and days_between(date, expiration) >= 2]
		return date_add_dashes(str(min(futureDates)))

def closestStrikeInExpiration(stockPrice, expirationDate, historicals, optionType, interval=1):

	assert optionType in ["call", "put"]
	expirationData = historicals[expirationDate]

	if optionType == "call":

		callStrikes = list(expirationData["calls"].keys())
		upperStrikes = [eval(strike) for strike in callStrikes if eval(strike) > stockPrice]
		upperStrikes.sort()
		try:
			return formatStrikePrice(str(upperStrikes[interval -1]))
		except:
			return formatStrikePrice(str(upperStrikes[-1]))

	elif optionType == "put":

		putStrikes = list(expirationData['puts'].keys())
		lowerStrikes = [eval(strike) for strike in putStrikes if eval(strike) < stockPrice]
		lowerStrikes.sort(reverse=True)
		try:
			return formatStrikePrice(str(lowerStrikes[interval - 1]))
		except:
			return formatStrikePrice(str(lowerStrikes[-1]))

def nearestCall(stockPrice, date, historicals, interval=1):

	expirationDate = nearestExpiration(date, historicals)
	call_strike = closestStrikeInExpiration(stockPrice, expirationDate, historicals, "call", interval)
	return {"expirationDate": expirationDate, "strikePrice": call_strike}


def nearestPut(stockPrice, date, historicals, interval=1):

	expirationDate = nearestExpiration(date, historicals)
	put_strike = closestStrikeInExpiration(stockPrice, expirationDate, historicals, "put", interval)
	return {"expirationDate": expirationDate, "strikePrice": put_strike}


def formatStrikePrice(strikePrice):

	splitString = strikePrice.split(".")

	decimal = splitString[1]
	remainingDigits = 4 - len(decimal)
	for i in range(remainingDigits):

		decimal += "0"

	return splitString[0] + "." + decimal

def roundTimeUp(time):

	time = eval(time)
	validTimes = ["630", "700", "730", "800", "830", "900", "930", "1000", "1030", "1100", "1130", "1200", "1230"]

	for validTime in validTimes:

		if time <= eval(validTime):

			return validTime

	return "1230"

def roundTimeDown(time):

	time = eval(time)
	validTimes = ["630", "700", "730", "800", "830", "900", "930", "1000", "1030", "1100", "1130", "1200", "1230"]

	prevTime = "630"
	for validTime in validTimes:

		if time < eval(validTime):

			return prevTime

		prevTime = validTime

	return "1230"

	

def wholeDayAveragePrice(historicals, date):
	try:

		relevant = historicals[date]
		total = 0
		count = 0
		for data in relevant.values():
			total += data["open_price"]
			total += data["close_price"]
			count += 2

		return round(total/count, 2)

	except:

		return 0

def wholeDayHighPrice(historicals, date):
	try:
		relevant = historicals[date]
		return max([data["high_price"] for data in list(relevant.values())])
	except:
		return 0

def wholeDayLowPrice(historicals, date):
	try:
		relevant = historicals[date]
		return min([data["low_price"] for data in list(relevant.values())])
	except:
		return 0

def wholeDayOpenPrice(historicals, date):
	try:
		relevant = historicals[date]
		return list(relevant.values())[0]["open_price"]
	except:
		return 0

def wholeDayClosePrice(historicals, date):
	try:
		relevant = historicals[date]
		return list(relevant.values())[-1]["close_price"]
	except:
		return 0


def wholeDayVolume(historicals, date):
	try:
		relevant = historicals[date]
		return sum([data["volume"] for data in list(relevant.values())])
	except:
		return 0

def intervalData(historicals, date, time):
	try:
		return historicals[date][time]
	except:
		return None

def intervalAveragePrice(historicals, date, time):
	try:
		relevant = intervalData(historicals, date, time)
		return round(relevant["open_price"]/2 + relevant["close_price"]/2 , 2)
	except:
		return 0

def intervalHighPrice(historicals, date, time):

	try:
		return intervalData(historicals, date, time)["high_price"]
	except:
		return 0

def intervalLowPrice(historicals, date, time):
	try:
		return intervalData(historicals, date, time)["low_price"]
	except:
		return 0

def intervalOpenPrice(historicals, date, time):
	try:

		return intervalData(historicals, date, time)["open_price"]
	except:
		return 0

def intervalClosePrice(historicals, date, time):
	try:
		return intervalData(historicals, date, time)["close_price"]
	except:
		return 0

def intervalVolume(historicals, date, time):
	try:
		return intervalData(historicals, date, time)["volume"]
	except:
		return 0












		


