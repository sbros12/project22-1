import pyupbit 
import pandas 
import datetime 
import time

access = ""
secret = ""

h = 200000
s = 101.5

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
coinlist = ["KRW-HUNT", "KRW-RFR", "KRW-STRAX", "KRW-AHT", "KRW-GAS", "KRW-REP", "KRW-BTC", "KRW-ARDR", "KRW-AAVE", "KRW-MVL", "KRW-ATOM", "KRW-STEEM", "KRW-IQ", "KRW-CHZ", "KRW-HIFI", "KRW-TRX", "KRW-STPT", "KRW-TFUEL", "KRW-SHIB", "KRW-HIVE", "KRW-META", "KRW-T", "KRW-LOOM", "KRW-ANKR", "KRW-CRE", "KRW-WAXP", "KRW-SNT", "KRW-APT", "KRW-SAND", "KRW-MANA", "KRW-MTL", "KRW-PUNDIX", "KRW-ETH", "KRW-DOGE", "KRW-GMT", "KRW-BCH", "KRW-NEAR", "KRW-XTZ", "KRW-BTG", "KRW-BAT", "KRW-SBD", "KRW-ENJ", "KRW-SOL", "KRW-FLOW", "KRW-SRM", "KRW-AXS", "KRW-AVAX", "KRW-XRP", "KRW-ETC"]  
lower1 = [] 
lower2 = [] 
lower3 = [] 
lower4 = [] 
lower5 = [] 
lower6 = [] 
lower7 = []  
higher1 = []
higher2 = [] 
higher3 = [] 
higher4 = []
higher5 = [] 
higher6 = [] 
higher7 = [] 

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

    if total <= 1000 and money > h * 1.0006 : 
        res = upbit.buy_market_order(coin, h) 
    elif 1000 < total < h and rate_return <= 95 and money > h * 1.006 : 
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

    if 10000 < total and rate_return > s : 
        res = upbit.sell_market_order(coin, amount) 
    else : 
        pass
    return


    # initiate 
for i in range(len(coinlist)):
    lower1.append(False) 
    lower2.append(False) 
    lower3.append(False)
    lower4.append(False) 
    lower5.append(False) 
    lower6.append(False)
    lower7.append(False)
    higher1.append(False)
    higher2.append(False)
    higher3.append(False)
    higher4.append(False)
    higher5.append(False)
    higher6.append(False)
    higher7.append(False)


while(True): 
    for i in range(len(coinlist)): 
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute5") # choose RSI time
        now_rsi = rsi(data, 14).iloc[-1] 

        print("coin name: ", coinlist[i]) 
        print("time: ", datetime.datetime.now()) 
        print("RSI :", now_rsi) 
    

        time.sleep(0.05)
        lo = 33
        hi = 68


        if lo + 5 <= now_rsi <= hi - 5 :
            lower1[i] = False
            lower2[i] = False
            lower3[i] = False
            lower4[i] = False
            lower5[i] = False
            lower6[i] = False
            lower7[i] = False
            higher1[i] = False
            higher2[i] = False
            higher3[i] = False
            higher4[i] = False
            higher5[i] = False
            higher6[i] = False
            higher7[i] = False
                      
        elif lo - 3 < now_rsi <= lo : 
            lower1[i] = True 
        elif now_rsi > lo + 3 and lower1[i] == True :
            buy(coinlist[i]) 
            lower1[i] = False

        elif lo - 6 < now_rsi <= lo - 3 : 
            lower2[i] = True 
        elif now_rsi > lo and lower2[i] == True : 
            buy(coinlist[i]) 
            lower2[i] = False
            
        elif lo - 9 < now_rsi <= lo - 6 : 
            lower3[i] = True   
        elif now_rsi > lo - 3 and lower3[i] == True : 
            buy(coinlist[i]) 
            lower3[i] = False

        elif lo - 12 < now_rsi <= lo - 9 : 
            lower4[i] = True   
        elif now_rsi > lo - 6 and lower4[i] == True : 
            buy(coinlist[i]) 
            lower4[i] = False
            
        elif lo - 15 < now_rsi <= lo - 12 : 
            lower5[i] = True   
        elif now_rsi > lo - 9 and lower5[i] == True : 
            buy(coinlist[i])
            lower5[i] = False

        elif lo - 18 < now_rsi <= lo - 15 : 
            lower6[i] = True   
        elif now_rsi > lo - 12 and lower6[i] == True : 
            buy(coinlist[i]) 
            lower6[i] = False
 
        elif now_rsi <= lo - 18 : 
            lower7[i] = True   
        elif now_rsi > lo - 15 and lower7[i] == True : 
            buy(coinlist[i]) 
            lower7[i] = False



        elif hi < now_rsi <= hi + 3 : 
            higher1[i] = True 
        elif now_rsi < hi - 3 and higher1[i] == True :
            sell(coinlist[i]) 
            higher1[i] = False

        elif hi + 3 <= now_rsi < hi + 6 :
            higher2[i] = True
        elif now_rsi < hi and higher2[i] == True :
            sell(coinlist[i]) 
            higher2[i] = False

        elif hi + 6 <= now_rsi < hi + 9 :
            higher3[i] = True
        elif now_rsi < hi + 3 and higher3[i] == True :
            sell(coinlist[i]) 
            higher3[i] = False

        elif hi + 9 <= now_rsi < hi + 12 :
            higher4[i] = True 
        elif now_rsi < hi + 6 and higher4[i] == True :
            sell(coinlist[i]) 
            higher4[i] = False
            
        elif hi + 12 <= now_rsi < hi + 15 :
            higher5[i] = True
        elif now_rsi < hi + 9 and higher5[i] == True :
            sell(coinlist[i]) 
            higher5[i] = False

        elif hi + 15 <= now_rsi < hi + 18 :
            higher6[i] = True
        elif now_rsi < hi + 12 and higher6[i] == True :
            sell(coinlist[i]) 
            higher6[i] = False
            
        elif now_rsi >= hi + 18 :
            higher7[i] = True            
        elif now_rsi < hi + 15 and higher7[i] == True : 
            sell(coinlist[i]) 
            higher7[i] = False
            
    
    time.sleep(3)
