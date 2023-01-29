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
coinlist = ["KRW-KAVA", "KRW-MTL", "KRW-ZIL", "KRW-ETH", "KRW-EOS", "KRW-NEAR", "KRW-SBD", "KRW-BORA", "KRW-WAVES", "KRW-FLOW", "KRW-SRM", "KRW-AXS", "KRW-PLA", "KRW-XRP", "KRW-ETC"]  
lower25 = [] 
higher72 = []
higher77 = [] 

# auto trade start
upbit = pyupbit.Upbit(access, secret)
print("Auto angel start")

#get
def buy1(coin): 
    money = upbit.get_balance("KRW") 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    avg_price = upbit.get_avg_buy_price(coin)
    total = amount * cur_price
    rate_return = cur_price / (avg_price + 0.00001) * 100
    h = 100000 # get unit 
    if total <= 100 and money > 101000 : 
        res = upbit.buy_market_order(coin, h) 
    elif 100 < total < 1000000 and rate_return < 98 and money > 101000 : 
        res = upbit.buy_market_order(coin, h) 
    else :  
        pass 
    return

def buy(coin): 
    money = upbit.get_balance("KRW") 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    avg_price = upbit.get_avg_buy_price(coin)
    total = amount * cur_price
    rate_return = cur_price / (avg_price + 0.00001) * 100
    h = 100000 # get unit 
    if total <= 1000 and money > 101000 : 
        res = upbit.buy_market_order(coin, h) 
    elif 1000 < total < 1000000 and rate_return < 95 and money > 101000 : 
        res = upbit.buy_market_order(coin, h) 
    else :  
        pass 
    return

#sell
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    avg_price = upbit.get_avg_buy_price(coin)
    total = amount * cur_price 
    rate_return = cur_price / (avg_price + 0.00001) * 100
    if 100000 < total <= 500000 and rate_return > 101.5 : 
        res = upbit.sell_market_order(coin, amount) 
    elif total > 500000 and 101.5 < rate_return < 103 : 
        res = upbit.sell_market_order(coin, amount * 0.5) 
    elif total > 500000 and rate_return >= 103 :
        res = upbit.sell_market_order(coin, amount) 
    else : 
        pass
    return

    # initiate 
for i in range(len(coinlist)):
    smember.append(False)
    lower1.append(False) 
    lower2.append(False) 
    higher1.append(False)
    higher2.append(False)

while(True): 
    for i in range(len(coinlist)): 
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute5") # choose RSI time
        now_rsi = rsi(data, 14).iloc[-1] 
        print("coin name: ", coinlist[i]) 
        print("time: ", datetime.datetime.now()) 
        print("RSI :", now_rsi) 
        print() 
        
        if 35 <= now_rsi <= 68 :
            smember[i] = True 
            lower1[i] = False
            lower2[i] = False
            
        elif 29 < now_rsi <= 32 : 
            lower1[i] = True 
        elif now_rsi >= 34 and lower1[i] == True and smember[i] == True:
            buy1(coinlist[i]) 
            smember[i] = False
            
        elif 23 < now_rsi <= 26 : 
            lower2[i] = True   
        elif now_rsi >= 28 and lower2[i] == True and smember[i] == True: 
            buy(coinlist[i]) 
            smember[i] = False
            
        elif now_rsi <= 18 : 
            lower3[i] = True   
        elif now_rsi >= 20 and lower3[i] == True and smember[i] == True: 
            buy(coinlist[i]) 
            smember[i] = False
            
            
        elif 72 <= now_rsi < 77 :
            higher72[i] = True
        elif now_rsi < 70 and higher72[i] == True: 
            sell(coinlist[i]) 
            higher72[i] = False

        elif now_rsi >= 77 :
            higher77[i] = True
                
        elif now_rsi < 73 and higher77[i] == True: 
            sell(coinlist[i]) 
            higher77[i] = False
            higher72[i] = False
    
    time.sleep(5)
