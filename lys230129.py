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
coinlist = ["KRW-APT", "KRW-BTC", "KRW-SAND", "KRW-MANA", "KRW-MTL", "KRW-PUNDIX", "KRW-ETH", "KRW-DOGE", "KRW-GMT", "KRW-BCH", "KRW-NEAR", "KRW-XTZ", "KRW-BTG", "KRW-BAT", "KRW-SBD", "KRW-ENJ", "KRW-SOL", "KRW-FLOW", "KRW-SRM", "KRW-AXS", "KRW-AVAX", "KRW-XRP", "KRW-ETC"]  
lower1 = [] 
lower2 = [] 
lower3 = [] 
higher1 = []
higher2 = [] 
higher3 = [] 

# auto trade start
upbit = pyupbit.Upbit(access, secret)
print("Auto angel start")

#get
def buy(coin): 
    money = upbit.get_balance("KRW") 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    avg_price = upbit.get_avg_buy_price(coin)
    total = amount * cur_price
    rate_return = cur_price / (avg_price + 0.00001) * 100
    h = 100000 # get unit 
    if total <= 100 and money > 100100 : 
        res = upbit.buy_market_order(coin, h) 
    elif 100 < total < 1000000 and 96 < rate_return <= 99 and money > 100100 : 
        res = upbit.buy_market_order(coin, h) 
    elif 100 < total < 1000000 and rate_return <= 96 and money > 100100 : 
        res = upbit.buy_market_order(coin, h * 2)
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
        
        if 36 <= now_rsi <= 66 :
            smember[i] = True 
            lower1[i] = False
            lower2[i] = False
            lower3[i] = False
            higher1[i] = False
            higher2[i] = False
            higher3[i] = False
            
            
        elif 29 < now_rsi <= 32 : 
            lower1[i] = True 
        elif now_rsi >= 34 and lower1[i] == True and smember[i] == True:
            buy(coinlist[i]) 
            smember[i] = False
            
        elif 23 < now_rsi <= 26 : 
            lower2[i] = True   
        elif now_rsi >= 28 and lower2[i] == True and smember[i] == True: 
            buy(coinlist[i]) 
            smember[i] = False
            
        elif now_rsi <= 18 : 
            lower3[i] = True   
        elif now_rsi >= 20 and lower3[i] == True: 
            buy(coinlist[i]) 
            smember[i] = False
            
            
        elif 70 <= now_rsi < 73 :
            higher1[i] = True
        elif now_rsi < 68 and higher1[i] == True and smember[i] == True: 
            sell(coinlist[i]) 
            smember[i] = False
            
        elif 76 <= now_rsi < 79 :
            higher2[i] = True
        elif now_rsi < 74 and higher2[i] == True and smember[i] == True: 
            sell(coinlist[i]) 
            smember[i] = False
            
        elif now_rsi >= 83 :
            higher3[i] = True            
        elif now_rsi < 81 and higher3[i] == True: 
            sell(coinlist[i]) 
            smember[i] = False
    
    time.sleep(5)
