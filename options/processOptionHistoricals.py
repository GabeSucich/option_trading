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
			return str(upperStrikes[interval -1])
		except:
			return str(upperStrikes[-1])

	elif optionType == "put":

		putStrikes = list(expirationData['puts'].keys())
		lowerStrikes = [eval(strike) for strike in putStrikes if eval(strike) < stockPrice]
		lowerStrikes.sort(reverse=True)
		try:
			return str(lowerStrikes[interval - 1])
		except:
			return str(lowerStrikes[-1])

def nearestCall(stockPrice, date, historicals, interval=1):

	expirationDate = nearestExpiration(date, historicals)
	call_strike = closestStrikeInExpiration(stockPrice, expirationDate, historicals, "call", interval)
	return {"expirationDate": expiration, "strikePrice": call_strike}


def nearestPut(stockPrice, date, historicals, interval=1):

	expirationDate = nearestExpiration(date, historicals)
	put_strike = closestStrikeInExpiration(stockPrice, expirationDate, historicals, "put", interval)
	return {"expirationDate": expiration, "strikePrice": put_strike}


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

	

def wholeDayAveragePrice(historicals, date):

	relevant = historicals[date]
	total = 0
	count = 0
	for data in relevant.values():
		total += data["open_price"]
		total += data["close_price"]
		count += 2

	return round(total/count, 2)

def wholeDayHighPrice(historicals, date):

	relevant = historicals[date]
	return max([data["high_price"] for data in list(relevant.values())])

def wholeDayLowPrice(historicals, date):
	relevant = historicals[date]
	return min([data["low_price"] for data in list(relevant.values())])

def wholeDayOpenPrice(historicals, date):
	relevant = historicals[date]
	return list(relevant.values())[0]["open_price"]

def wholeDayClosePrice(historicals, date):
	relevant = historicals[date]
	return list(relevant.values())[-1]["close_price"]

def wholeDayVolume(historicals, date):
	relevant = historicals[date]
	return sum([data["volume"] for data in list(relevant.values())])

def intervalData(historicals, date, time):

	return historicals[date][time]

def intervalAveragePrice(historicals, date, time):

	relevant = intervalData(historicals, date, time)
	return round(relevant["open_price"]/2 + relevant["close_price"]/2 , 2)

def intervalHighPrice(historicals, date, time):

	return intervalData(historicals, date, time)["high_price"]

def intervalLowPrice(historicals, date, time):

	return intervalData(historicals, date, time)["low_price"]

def intervalOpenPrice(historicals, date, time):

	return intervalData(historicals, date, time)["open_price"]

def intervalClosePrice(historicals, date, time):

	return intervalData(historicals, date, time)["close_price"]

def intervalVolume(historicals, date, time):

	return intervalData(historicals, date, time)["volume"]












		


