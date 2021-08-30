import pyupbit 
import pandas 
import datetime 
import time

access = ""
secret = ""

# RSI get start
def rsi(ohlc: pandas.DataFrame, period: int = 14): 
    delta = ohlc["close"].diff() 
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

# coin list
coinlist = ["KRW-BCHA", "KRW-ADA", "KRW-XLM", "KRW-BCH", "KRW-QTUM", "KRW-EOS", "KRW-XTZ", "KRW-BCH", "KRW-WAVES", "KRW-FLOW", "KRW-BTC", "KRW-SRM", "KRW-AXS", "KRW-PLA", "KRW-XRP", "KRW-SAND", "KRW-BTG", "KRW-BSV", "KRW-ETC"]  
lower25 = [] 
higher72 = []
higher77 = [] 

# auto trade start
upbit = pyupbit.Upbit(access, secret)
print("Auto angel start")

#get
def buy(coin): 
    money = upbit.get_balance("KRW") 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    h = 2000000 # get unit
    w = 0.97
    if total < h * w : 
        res = upbit.buy_market_order(coin, h) 
    else : 
        pass 
    return

#sell
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    ys = 1.011 #target gain
    h = 2000000 # get unit
    if h * ys < total < h * 1.5 : 
        res = upbit.sell_market_order(coin, amount) 
    elif h * 2 * ys < total < h * 3 : 
        res = upbit.sell_market_order(coin, amount * 0.5) 
    else : 
        pass
    return

    # initiate 
for i in range(len(coinlist)): 
    lower25.append(False) 
    higher72.append(False)
    higher77.append(False)

while(True): 
    for i in range(len(coinlist)): 
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3") 
        now_rsi = rsi(data, 14).iloc[-1] 
        print("coin name: ", coinlist[i]) 
        print("time: ", datetime.datetime.now()) 
        print("RSI :", now_rsi) 
        print() 
        if now_rsi <= 25 : 
            lower25[i] = True 
        elif now_rsi >= 29 and lower25[i] == True: 
            buy(coinlist[i]) 
            lower25[i] = False

        elif 72 <= now_rsi < 77 :
            higher72[i] = True
        elif now_rsi < 68 and higher72[i] == True: 
            sell(coinlist[i]) 
            higher72[i] = False

        elif now_rsi >= 77 :
            higher77[i] = True
        
        elif now_rsi < 73 and higher77[i] == True: 
            sell(coinlist[i]) 
            higher77[i] = False
            higher72[i] = False
    
    time.sleep(3)
