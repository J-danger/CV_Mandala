import requests
from collections import defaultdict
from itertools import chain
from prettytable import PrettyTable
import time

# Pulls the volume of all available pairs (this works binance.com and all cloud exchanges)
mandala = requests.get("https://trade.mandala.exchange/v1/market/trading-pairs")

jsonMandala = mandala.json()

volumeMandala = jsonMandala.get('data').get('list')
my_List = []
my_Pairs = []
volume_list= []
totalCount = 0
error_list = ['AERGO', 'AGIX','AMB',  'ARK', 'AST', 'BDOT', 'BETH', 'BNX', 'BOND', 'BRD', 'CREAM', 'EZ', 'GAS',  'GLM', 'GO', 'GRS', 'IQ', 'LINK', 'LOOM', 'LUNC', 'LUNA', 'MDA', 'MDXT', 'NAS', 'NAV', 'NEBL', 'NXS', 'OAX', 'PHB', 'PIVX',  'PROS', 'PROM', 'QKC', 'QLC', 'QSP', 'QUICK', 'SFM', 'SNM', 'SNT', 'SPARTA', 'UFT', 'USTC', 'USDT', 'VAB', 'VIB', 'WABI', 'WBTC', 'GFT']
volumeCount = 0
subString = 'BUSD'
subString2 = ['BUSD_USDT', 'TUSD_BUSD', 'TUSD_USDT', 'USDC_BUSD', 'USDC_USDT', 'USDP_BUSD','USDP_USDT','BTC_BIDR', 'BTC_BUSD', 'BTC_TUSD', 'BTC_USDC', 'BTC_USDP','BTC_USDT']

# Removes pairs with 0 volume and assets with no price
for x in volumeMandala:        
    listedPairs = list(x.values()) 
    listedAsset = listedPairs[0]
    myPairs = listedPairs[5]    
    listedVolume = float(listedPairs[11]) 
    totalCount = totalCount  + 1   
    if listedAsset in error_list:
        None
    elif myPairs in subString2:  
        None     
    elif listedVolume > 0: 
        my_List.append(listedAsset)
        my_Pairs.append(myPairs)
        volume_list.append(listedVolume) 
        volumeCount = volumeCount + 1
print('volume done')

#Prices in the volume in USDT using the Binance.com API (cloud exchanges do not have this endpoint) 

base_url = "https://api.binance.com/api/v3"
symbols = my_List
data_dict = []
pricesValues = []
prices = {}
count = 0
data_dict = defaultdict(list)
for symbol in symbols:                
        url = base_url + f"/avgPrice?symbol={symbol}USDT"
        r = requests.get(url)   
        prices[symbol] = float(r.json()["price"])
        count = count + 1  
        data_dict[symbol].append(float(r.json()["price"]))        
        pricesValues = list(prices.values())
        time.sleep(2)
print('prices done')

#Combines the asset list with the volume prices in USDT

data_dict_list = list(data_dict.values())
data_pass = list(chain(*data_dict_list))

usdtValue = []        

for num1, num2 in zip(data_pass, volume_list):
    usdtValue.append(num1 * num2)
usdtSum = sum(usdtValue)
zippedThree = list(list(count) for count in zip(my_Pairs, usdtValue))
t = PrettyTable(['Pair', 'volume(USDT)'])
for u in zippedThree:
    t.add_row(u)    
print(t)
print('total Volume:', usdtSum)
print('total active Pairs:', volumeCount, '/', totalCount )
print('Revenue cap', ((usdtSum * 0.001)/2))

## PLUG-INS

# TIME
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


# MONGO
from pymongo import MongoClient  
try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")  
# database
db = conn.database  
# Created or Switched to collection names: my_gfg_collection
collection = db.my_gfg_collection  
emp_rec1 = {
        "total_Volume":usdtSum,
        "total_active_Pairs":(volumeCount),
        "revenue_Cap":((usdtSum * 0.001)/2),
        "time": dt_string
        }  
# Insert Data
rec_id1 = collection.insert_one(emp_rec1)  
print("Data inserted with record ids",rec_id1)
# Printing the data inserted
cursor = collection.find()
for record in cursor:
    print(record)
print('done')









