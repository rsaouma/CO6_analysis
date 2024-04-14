import QuantLib as ql
import datetime

def setDayToToday():
	today_i = datetime.date.today()
	today = ql.Date(today_i.day, today_i.month, today_i.year)
	ql.Settings.instance().evaluationDate = today
	print("Today's date:", today)
	return today


def getProcess(interest_rate, dividend_rate, underlying_price, volatility_rate):

	###################################################
	##2) Date setup
	###################################################

	#Assumptions
	calendar = ql.UnitedStates()
	day_counter = ql.ActualActual()





	###################################################
	##3)
	#Curve setup
	###################################################

	interest_curve = ql.FlatForward(valuation_date, ql.QuoteHandle(interest_rate), day_counter )

	dividend_curve = ql.FlatForward(valuation_date, ql.QuoteHandle(dividend_rate), day_counter )

	volatility_curve = ql.BlackConstantVol(valuation_date, calendar, ql.QuoteHandle(volatility_rate), day_counter )

	#Collate market data together
	u = ql.QuoteHandle(underlying_price)
	d = ql.YieldTermStructureHandle(dividend_curve)
	r = ql.YieldTermStructureHandle(interest_curve)
	v = ql.BlackVolTermStructureHandle(volatility_curve)

	return ql.BlackScholesMertonProcess(u, d, r, v)


###################################################
##4)
#Option setup
###################################################

def getAmericanOption(valuation_date, expiry_date, put_or_call, strike_price, process):
    grid_points = 100

    exercise = ql.AmericanExercise(valuation_date, expiry_date)

    payoff = ql.PlainVanillaPayoff(put_or_call, strike_price)

	#Option Setup
    option =  ql.VanillaOption(payoff, exercise)

    time_steps = 1000
    xGrid = 1000


    engine = ql.FdBlackScholesVanillaEngine(process, time_steps, xGrid)

    option.setPricingEngine(engine)

    return option


###################################################
##5)
##Collate results
###################################################

def getAmericanPrice(option):

    return option.NPV()



def getEuropeanOptionPrice(opt_type,u,s,expiry,sigma,r):
	opt_type = (ql.Option.Call if opt_type == "Call" else ql.Option.Put)
	return opt_type






