import pickle
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView, ListCreateAPIView
)
from rest_framework.views import APIView
from .models import BackTest
from .serializers import ImageSerializer
# from beautifultable import BeautifulTable
import pandas as pd
from pandas import json_normalize
import numpy as np
import talib as ta
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from webbot import Browser
import time
import os
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import talib
import requests
import logging
import asyncio
import eventlet
import socketio
from aiohttp import web
from aiohttp import WSMsgType
async_mode = None
basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(cors_allowed_origins='*', async_mode=async_mode)


def access_token(api_secret, request_token, kite):
    user = pd.DataFrame()
    try:
        user = kite.generate_session(request_token, api_secret)
        print("Access token ->" + user["access_token"])
        acc_key = user["access_token"]

    except Exception as e:
        print("Authentication failed", str(e))
        raise

    print(user["user_name"], "has successfully signed in.")
    return user


def accesskey():
    web = Browser()
    web.go_to('https://kite.trade/connect/login?api_key=pv2830q1vbrhu1eu&v=3')
    time.sleep(1)
    web.type('RK2267', into='User ID', id='userid')
    web.type('Sbi@2021', into='Password', id='password')
    web.click('Login')
    time.sleep(1)
    web.type('489111', into='PIN', id='pin')
    web.click('Continue')
    time.sleep(1)
    webbot_result_url = web.get_current_url()
    print(webbot_result_url)
    url = webbot_result_url
    url = url.split('request_token=')[1]
    url = url.split('&')[0]
    print(url)
    web.quit()

    my_api_key = "pv2830q1vbrhu1eu"
    kite = KiteConnect(api_key=my_api_key)
    req_key = url
    user_details = access_token(
        "8h662dsfl0ut8sh72g89ni52m60s267c", req_key, kite)
    acc_key = user_details["access_token"]
    print("Access token ->" + acc_key)
    return acc_key


def on_connect(ws, response):
    # dict3 = [895745, 256265, 260105, 264969]
    global dict3
    for i in range(len(dict3)):
        ws.subscribe([dict3[i]])
        ws.set_mode(ws.MODE_FULL, [dict3[i]])
    print("Trading Started....")


def on_close(ws, code, reason):

    # kws.enable_reconnect(reconnect_interval=5, reconnect_tries=50)
    # print("reconnecting...")
    logging.info(
        "Connection closed: {code} - {reason}".format(code=code, reason=reason))
    # ws.stop()


def on_error(ws, code, reason):
    logging.info(
        "123456Connection error: {code} - {reason}".format(code=code, reason=reason))


def on_reconnect(ws, attempts_count):
    logging.info("123456Reconnecting: {}".format(attempts_count))


def on_noreconnect(ws):
    logging.info("123456Reconnect failed.")


def on_ticks(ws, ticks):
    logging.debug("Ticks: {}".format(ticks))
    # print(ticks)
    global nltp
    global ntime
    global sltp
    global stime
    global bltp
    global btime
    global iltp
    global itime
    global s
    for i in range(len(ticks)):
        c = close[ticks[i]['instrument_token']]
        s[ticks[i]['instrument_token']] = ((ticks[i]['last_price']-c)/c)*100
        # print(s)
        if ticks[i]['instrument_token'] == 256265:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)
            nltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            ntime = time
        if ticks[i]['instrument_token'] == 265:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)
            sltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            stime = time
        if ticks[i]['instrument_token'] == 260105:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)
            bltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            btime = time
        if ticks[i]['instrument_token'] == 264969:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)
            iltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            itime = time
    s = {k: v for k, v in sorted(s.items(), key=lambda item: item[1])}

    # print(time)

    # sio.sleep(10)
    # print(sio.emit('message', {'data': 'Server generated event'}))

    # niftiltp.append(ltp)
    # niftitime.append(time)
    # print(niftitime)
    # print("lp")


def index(request):

    return Response({"output": 123})


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    print("hi")
    kws.connect(threaded=True, disable_ssl_verification=False)
    while True:
        if count % 120 == 1:
            print(count)
            # print(datetime.now())
            niftiltp.append(nltp[0])
            niftitime.append(ntime)
            sio.emit('niftidata', niftiltp)
            sio.emit('niftitime', niftitime)
            sensexltp.append(sltp[0])
            sensextime.append(stime)
            sio.emit('sensexdata', sensexltp)
            sio.emit('sensextime', sensextime)
            bankltp.append(bltp[0])
            banktime.append(btime)
            sio.emit('bankdata', bankltp)
            sio.emit('banktime', banktime)
            indialtp.append(iltp[0])
            indiatime.append(itime)
            sio.emit('indiadata', indialtp)
            sio.emit('indiatime', indiatime)
        k = list(s)
        # print(s)
        if k != []:
            loosersName = []
            loosersltp = []
            # print(k, "k")
            for i in range(5):
                loosersName.append(dict1[k[i]])
                loosersltp.append(s[k[i]])

                # print(dict1[k[i]])
                # x = str(dict1[k[i]]).split('"')

            gainersName = []
            gainersltp = []
            g = k[-5:]
            for i in range(5):
                gainersName.append(dict1[g[i]])
                gainersltp.append(s[g[i]])
                # x = str(dict1[g[i]]).split('"')
                # gainers[i] = [dict1[g[i]], s[g[i]]]
            # print(gainersltp, "ltp")
            # print(gainersName, "gainers")
            sio.emit('loosers', loosersName)
            sio.emit('gainers', gainersName)
            sio.emit('loosersltp', loosersltp)
            sio.emit('gainersltp', gainersltp)
        sio.emit('nltp', nltp)
        sio.emit('sltp', sltp)
        sio.emit('bltp', bltp)
        sio.emit('bltp', bltp)
        sio.emit('iltp', iltp)
        sio.emit('iltp', iltp)
        count += 1
        sio.sleep(1)


@sio.event
def connect(sid, environ):
    print('Client connected', sid)
    # sio.start_background_task()
    sio.start_background_task(background_thread)
    # sio.emit('message', 123)


@sio.event
def disconnect(sid):
    print('Client disconnected')


def prevdata(token, acc_key):
    t2 = (datetime.now())
    t1 = (datetime.now())

    # if str(t2.time()) > '15:30:00':
    #     t2 = str(t2.date())+' '+'15:30:00'
    #     print(t2)
    t1 = str(t1)
    t2 = str(t2)
    t1 = t1.split(" ")
    t3 = t1[1].split(':')
    t3[0] = '09'
    t3[1] = '15'
    t3 = t3[0]+':'+t3[1]+':'+t3[2]
    t1 = t1[0]+"+"+t3
    t2 = t2.split(" ")
    t2 = t2[0]+"+"+t2[1]
    print(t1)
    print(t2)
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(token)+"/minute?from="+t1+"&to="+t2
    print(url2)
    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
    res2 = requests.get(url2, headers=HEADERS)
    data2 = res2.json()
    data2 = data2["data"]["candles"]

    # print(data2)
    # print(data2)
    timestamp = []
    close = []
    for i in range(len(data2)):
        d = data2[i][0].split("T")
        d = d[1].split("+")
        timestamp.append(d[0])
        close.append(data2[i][4])
    return timestamp, close


with open('D:/QuantAlgo/quant-app/Server/app/tokens.p', 'rb') as fp:
    dict3 = pickle.load(fp)
with open('D:/QuantAlgo/quant-app/Server/app/instruments.p', 'rb') as fp:
    dict1 = pickle.load(fp)
dict3[137] = 256265
dict3[138] = 265
dict3[139] = 260105
dict3[140] = 264969
dict1[256265] = '"NIFTI"'
dict1[265] = '"SENSEX"'
dict1[260105] = '"NIFTI BANK"'
dict1[264969] = '"INDIA VIX"'

acc_key = accesskey()
niftiltp = []
niftitime = []
nltp = 0
ntime = ''

sensexltp = []
sensextime = []
sltp = 0
stime = ''

bankltp = []
banktime = []
bltp = 0
btime = ''

indialtp = []
indiatime = []
iltp = 0
itime = ''

close = {}
s = {}

keys = list(dict1)
close = {}
s = {}
today = datetime.utcnow().date()
print(today)
yesterday = today - timedelta(days=1)
t1 = str(yesterday)+"+"+"14:15:00"
t2 = str(today)+"+"+"04:30:00"

print(t1)
print(t2)

for i in range(len(dict3)):
    # print(i)
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(dict3[i])+"/15minute?from="+t1+"&to="+t2

    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
    res2 = requests.get(url2, headers=HEADERS)
    data2 = res2.json()
    data2 = data2["data"]["candles"]
    print(data2)
    # if i == 137:
    #     # print(data2)
    close[keys[i]] = data2[-1][4]


niftitime, niftiltp = prevdata(256265, acc_key)
print(niftiltp)
sensextime, sensexltp = prevdata(265, acc_key)
banktime, bankltp = prevdata(260105, acc_key)
indiatime, indialtp = prevdata(264969, acc_key)
# print(sensextime, "nifti")
kws = KiteTicker("pv2830q1vbrhu1eu", acc_key)
kws.on_ticks = on_ticks
kws.on_close = on_close
kws.on_error = on_error
kws.on_connect = on_connect
kws.on_reconnect = on_reconnect
kws.on_noreconnect = on_noreconnect


class ImageCreateView(CreateAPIView):
    queryset = BackTest.objects.all()
    serializer_class = ImageSerializer

    def __init__(self):
        # self.df2_nifty_CE = pd.read_csv(
        #     "C:/Users/Dell/Desktop/quant-app/Server/app//acc_15min.csv")
        self.df1 = pd.read_csv(
            "C:/Users/Dell/Downloads/QuantAlgo/quant-app/Server/app//SBIN_15_min.csv")
        self.lot_size = 0
        self.request = ""

    def post(self, request):
        self.request = request
        x = {"hello": request.data["symbol"]}
        print(self.request.data["symbol"], "helllooo")
        # self.lot_size = int(self.request.data["Quantity"])
        start_date = self.request.data["from_date"]
        date1 = start_date.split("T")
        start_date = date1[0]+" "+date1[1]
        to_date = self.request.data["to_date"]
        date2 = to_date.split("T")
        to_date = date2[0]+" "+date2[1]
        # start_date = "2019-01-06 15:15:00"
        # end_date = "2020-10-30 15:30:00"

        self.df1['PLUS_DI'] = ta.PLUS_DI(np.asarray(self.df1['high'], dtype='f8'), np.asarray(
            self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=14)
        self.df1['MINUS_DI'] = ta.MINUS_DI(np.asarray(self.df1['high'], dtype='f8'), np.asarray(
            self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=14)

        self.df1['ADX'] = ta.ADX(np.asarray(self.df1['high'], dtype='f8'), np.asarray(
            self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=14)
        self.df1['macd'], self.df1['signal'], self.df1['macdhist'] = ta.MACD(np.asarray(
            self.df1['close'], dtype='f8'), fastperiod=12, slowperiod=26, signalperiod=9)
        self.df1['EMA_S'] = ta.EMA(np.asarray(
            self.df1['close'], dtype='f8'), timeperiod=8)
        self.df1['EMA_L'] = ta.EMA(np.asarray(
            self.df1['close'], dtype='f8'), timeperiod=21)
        self.df1['UPPERBAND'], self.df1['MIDDLEBAND'], self.df1['LOWERBAND'] = ta.BBANDS(np.asarray(
            self.df1['close'], dtype='f8'), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

        # some variables.
        no_of_trades = []
        order = []
        buy_sell = []
        Entry_price = []
        Exit_price = []
        profit = []
        mtm = []

        lot_size = int(self.request.data["Quantity"])
        pro = 0
        trade = 0
        buying_price = 0
        selling_price = 0

        len_df1 = self.df1["close"].size
        buy_flag = False
        sell_flag = True
        buy_flag1 = False

        self.df1["Position"] = 0
        print(self.df1)
        stoploss = 0
        target = 0

        self.df1["ADX_COMP"] = 0
        self.df1["EMA_COMP"] = 0
        self.df1["MACD_COMP"] = 0
        #self.df1.dropna(inplace = True)
        for i in range(len_df1):
            if (i > 1) and (self.df1['PLUS_DI'].iloc[i] > self.df1['MINUS_DI'].iloc[i]) and (self.df1['ADX'].iloc[i] > self.df1['MINUS_DI'].iloc[i]) and (self.df1['ADX'].iloc[i-1] < self.df1['MINUS_DI'].iloc[i-1]):
                self.df1.loc[i, "ADX_COMP"] = 1
            else:
                self.df1.loc[i, "ADX_COMP"] = 0

            if (i > 1) and (self.df1['EMA_S'].iloc[i] > self.df1['EMA_L'].iloc[i]) and (self.df1['EMA_S'].iloc[i-1] < self.df1['EMA_L'].iloc[i-1]):
                self.df1.loc[i, "EMA_COMP"] = 1
            else:
                self.df1.loc[i, "EMA_COMP"] = 0

            if (i > 1) and (self.df1['macd'].iloc[i] > self.df1['signal'].iloc[i]) and (self.df1['macd'].iloc[i-1] < self.df1['signal'].iloc[i-1]):
                self.df1.loc[i, "MACD_COMP"] = 1
            else:
                self.df1.loc[i, "MACD_COMP"] = 0

        for x in range(len_df1):
            pro = 0

            if((self.df1['PLUS_DI'].iloc[x] > self.df1['MINUS_DI'].iloc[x]) and (self.df1['ADX'].iloc[x] > self.df1['MINUS_DI'].iloc[x]) and (self.df1['ADX'].iloc[x-1] < self.df1['MINUS_DI'].iloc[x-1]) or (1 in self.df1['ADX_COMP'].iloc[x-7:x].values)) and ((self.df1['macd'].iloc[x] > self.df1['signal'].iloc[x]) and (self.df1['macd'].iloc[x-1] < self.df1['signal'].iloc[x-1]) or (1 in self.df1['MACD_COMP'].iloc[x-5:x].values)) and ((self.df1['EMA_S'].iloc[x] > self.df1['EMA_L'].iloc[x]) and (self.df1['EMA_S'].iloc[x-1] < self.df1['EMA_L'].iloc[x-1]) or (1 in self.df1['EMA_COMP'].iloc[x-5:x].values)) and (not buy_flag):
                trade += 1
                buying_price = self.df1['close'].iloc[x]

                order.append(-1)
                buy_sell.append("Buy")
                Entry_price.append(buying_price)
                Exit_price.append("")
                mtm.append("Position Taken")
                self.df1["Position"][x+1] = 1
                # print(self.df1["Position"][x+1])

                buy_flag1 = True
                buy_flag = True
                sell_flag = False

            elif(((self.df1['UPPERBAND'].iloc[x-1] < self.df1['close'].iloc[x-1]) and (self.df1['UPPERBAND'].iloc[x] > self.df1['close'].iloc[x]) and (self.df1['ADX'].iloc[x] > self.df1['PLUS_DI'].iloc[x])) or (self.df1['close'].iloc[x] < (0.99 * buying_price))) and (not sell_flag):
                trade += 1
                selling_price = self.df1['close'].iloc[x]
                pro = selling_price - buying_price

                order.append(1)
                buy_sell.append("Sell")
                Entry_price.append("")
                Exit_price.append(selling_price)
                mtm.append("Position closed")

                if buy_flag1 == True:
                    buy_flag1 = False
                buy_flag = False
                sell_flag = True

            else:
                if (buy_flag == True):
                    yy = (self.df1['close'].iloc[x] - buying_price) * lot_size
                else:
                    yy = "0"

                order.append(0)
                buy_sell.append("No Trade")
                Entry_price.append("")
                Exit_price.append("")
                mtm.append(yy)

                if buy_flag1 == True:
                    self.df1["Position"][x] = 1
                    # print(self.df1["Position"][x])

            no_of_trades.append(trade)
            profit.append(pro)
        initial_capital = int(self.request.data["Initial_Capital"])
        self.df1['Returns'] = np.log(
            self.df1["close"] / self.df1["close"].shift(1))
        self.df1['Strategy_Return'] = self.df1['Position'].shift(
            1) * self.df1['Returns']
        self.df1["placed_order"] = order
        self.df1["buy_sell"] = buy_sell
        self.df1["Entry"] = Entry_price
        self.df1["Exit"] = Exit_price
        self.df1['profit'] = profit
        self.df1['profit'] = (self.df1['profit']) * lot_size
        self.df1["mtm"] = mtm
        self.df1["cost"] = (self.df1["placed_order"].multiply(
            self.df1["close"])) * lot_size
        self.df1["Account"] = initial_capital + self.df1["cost"].cumsum()
        self.df1["Trades"] = no_of_trades

        self.df1.set_index('Date', inplace=True)

        risk_free_rate = 0.061/252
        sharpe = np.sqrt(252)*(np.mean(self.df1.Strategy_Return) -
                               (risk_free_rate))/np.std(self.df1.Strategy_Return)

        cumulative_returns = self.df1.Strategy_Return.cumsum().iloc[-1]
        period_in_days = len(self.df1.Strategy_Return)
        CAGR = 100*((cumulative_returns+1)**(252.0/period_in_days)-1)

        self.df1.dropna(inplace=True)
        cum_ret = self.df1.Strategy_Return.cumsum()

        peak = (np.maximum.accumulate(cum_ret) - cum_ret).idxmax()
        trough = cum_ret[:peak].idxmax()
        drawdown = (cum_ret[trough] - cum_ret[peak]) * 100

        buy_records = self.df1[self.df1["buy_sell"] == "Buy"]
        sell_records = self.df1[self.df1["buy_sell"] == "Sell"]

        trade_details = pd.DataFrame(0, index=range(len(buy_records)),
                                     columns=["Entry", "Date",
                                              "Price", "Exit",
                                              "ExDate", "ExPrice"])

        trade_details["Entry"] = buy_records["buy_sell"].values
        trade_details["Date"] = buy_records.index.values  # buy date
        trade_details["Price"] = buy_records["close"].values  # buy price
        trade_details["Exit"] = sell_records["buy_sell"].values
        trade_details["ExDate"] = sell_records.index.values  # sell date
        trade_details["ExPrice"] = sell_records["close"].values  # sell price
        trade_details['% Change'] = (
            trade_details['ExPrice'] / trade_details['Price']) - 1
        trade_details['Profit'] = trade_details['ExPrice'] - \
            trade_details['Price']
        trade_details['% Profit'] = (
            trade_details['ExPrice'] / trade_details['Price']) - 1
        trade_details['Position value'] = trade_details['Price']
        trade_details['Cumm Profit'] = trade_details['Profit'].cumsum()
        trade_details['MAE'] = 0
        trade_details['MFE'] = 0
        trade_details['Scale In / Scale Out'] = 0

        profit = trade_details[trade_details["Profit"] >= 1]
        loss = trade_details[trade_details["Profit"] <= -1]
        trade = trade_details.to_dict()
        print(trade_details)
        output = {}
        output["Trade start date"] = self.df1.index[-1]
        output['Trade end date'] = self.df1.index[0]
        output['Initial_Capital'] = self.df1["Account"].iloc[0]
        output['Ending_Capital'] = self.df1["Account"].iloc[-1]
        output['Total no trades'] = len(buy_records)
        output['Positive_trades'] = len(self.df1[self.df1["profit"] >= 1])
        output['Negative_trades'] = len(self.df1[self.df1["profit"] <= -1])
        output['Total_profit'] = self.df1[self.df1["profit"] >= 1]["profit"].sum()
        output['Total_loss'] = self.df1[self.df1["profit"] <= -1]["profit"].sum()
        output['Net Profit'] = self.df1["Account"].iloc[-1] - \
            self.df1["Account"].iloc[0]
        output['Net Profit (%)'] = (
            (self.df1["Account"].iloc[-1] / self.df1["Account"].iloc[0]) - 1) * 100
        output['Avg. Profit / Loss'] = np.mean(
            profit["Profit"].values) / np.mean(loss["Profit"].values)
        output['Sharpe ratio'] = sharpe
        output['CAGR (%)'] = CAGR
        output['Maximum Drawdown (%)'] = drawdown
        output['CAGR / MDD (%)'] = CAGR / drawdown
        print(output)
        return Response({"output": output, "trade": trade})


class Nefti(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    def access_token(self, api_secret, request_token, kite):
        user = pd.DataFrame()
        try:
            user = kite.generate_session(request_token, api_secret)
            print("Access token ->" + user["access_token"])
            acc_key = user["access_token"]

        except Exception as e:
            print("Authentication failed", str(e))
            raise

        print(user["user_name"], "has successfully signed in.")
        return user

    def accesskey(self):
        web = Browser()
        web.go_to('https://kite.trade/connect/login?api_key=pv2830q1vbrhu1eu&v=3')
        time.sleep(1)
        web.type('RK2267', into='User ID', id='userid')
        web.type('Sbi@2021', into='Password', id='password')
        web.click('Login')
        time.sleep(1)
        web.type('489111', into='PIN', id='pin')
        web.click('Continue')
        time.sleep(1)
        webbot_result_url = web.get_current_url()
        print(webbot_result_url)
        url = webbot_result_url
        url = url.split('request_token=')[1]
        url = url.split('&')[0]
        print(url)
        web.quit()

        my_api_key = "pv2830q1vbrhu1eu"
        kite = KiteConnect(api_key=my_api_key)
        req_key = url
        user_details = self.access_token(
            "8h662dsfl0ut8sh72g89ni52m60s267c", req_key, kite)
        acc_key = user_details["access_token"]
        print("Access token ->" + acc_key)
        return acc_key

    def NIFTI(self, acc_key):
        t2 = (datetime.now())
        t1 = (datetime.now() - timedelta(days=1))
        # print(t1)
        t1 = str(t1)
        t2 = str(t2)
        t1 = t1.split(" ")
        t3 = t1[1].split(':')
        # print(t3)
        t3[0] = '09'
        t3[1] = '15'
        t3 = t3[0]+':'+t3[1]+':'+t3[2]
        t1 = t1[0]+"+"+t3
        t2 = t2.split(" ")
        t2 = t2[0]+"+"+t2[1]
        # print(t1,t2)
        url2 = "https://api.kite.trade/instruments/historical/" + \
            str(969473)+"/" + str(15)+"minute?from="+t1+"&to="+t2
        # print(url2)
        HEADERS = {"X-Kite-Version": "3",
                   "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
        res2 = requests.get(url2, headers=HEADERS)
        data = res2.json()
        # print(data)
        data = data["data"]["candles"]
        data = pd.DataFrame(data)
        print(data)
        data = data.rename(
            columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})
        print(data['Time'][0])
        print(type(data['Time'][0]))
        # data['Time'] = [d[1] d = d.split("T") for d in data['Time']]
        for i in range(len(data['Time'])):
            d = data['Time'][i].split("T")
            d = d[1].split("+")
            data["Time"][i] = d[0]
        return data

    def get(self, request, format=None):
        # acc_key = self.accesskey()
        # data = self.NIFTI(acc_key)
        print("hello")
        sio.emit('message', "good")
        # return Response({"labelsNifti": data["Time"], "closeNifti": data["Close"]})
        return Response({'hello': 'hello'})

    #

    #     date1 = start_date.split("T")
    #     d1 = date1[0].split("-")
    #     if d1[1][0] != "0" and d1[2][0] != "0":
    #         final1 = d1[1]+"/"+d1[2]+"/"+d1[0]
    #     elif d1[1][0] == "0" and d1[2][0] != "0":
    #         final1 = d1[1][1]+"/"+d1[2]+"/"+d1[0]
    #     elif d1[1][0] != "0" and d1[2][0] == "0":
    #         final1 = d1[1]+"/"+d1[2][1]+"/"+d1[0]
    #     else:
    #         final1 = d1[1][1]+"/"+d1[2][1]+"/"+d1[0]
    #     end_date = self.request.data["to_date"]
    #     date2 = end_date.split("T")
    #     d2 = date2[0].split("-")
    #     if d2[1][0] != "0" and d2[2][0] != "0":
    #         final2 = d2[1]+"/"+d2[2]+"/"+d2[0]
    #     elif d2[1][0] == "0" and d2[2][0] != "0":
    #         final2 = d2[1][1]+"/"+d2[2]+"/"+d2[0]
    #     elif d2[1][0] != "0" and d2[2][0] == "0":
    #         final2 = d2[1]+"/"+d2[2][1]+"/"+d2[0]
    #     else:
    #         final2 = d2[1][1]+"/"+d2[2][1]+"/"+d2[0]

    #     start_date = str(final1+" "+date1[1])
    #     end_date = str(final2+" "+date2[1])
    #     print(start_date, end_date)
    #     # start_date = "2/20/2020 10:15"
    #     # end_date = "5/20/2020 10:15"
    #     mask = (self.df2_nifty_CE['Date'] > start_date) & (
    #         self.df2_nifty_CE['Date'] <= end_date)
    #     # print(mask)
    #     self.df2_nifty_CE = self.df2_nifty_CE.loc[mask]
    #     print(self.df2_nifty_CE)
    #     no_of_trades = list()
    #     order = list()
    #     buy_sell = list()
    #     Entry_price = list()
    #     Exit_price = list()
    #     profit = list()
    #     mtm = list()

    #     # lot_size = 75  # quantity
    #     pro = 0
    #     trade = 0
    #     buying_price = 0
    #     selling_price = 0

    #     len_df = self.df2_nifty_CE["close"].size
    #     # len_df = 2324

    #     buy_flag = False
    #     sell_flag = True

    #     buy_flag1 = False

    #     date = ""
    #     prv_trade_date = ""

    #     self.df2_nifty_CE["Position"] = 0
    #     print(self.df2_nifty_CE)
    #     # print(location_index(1))
    #     # print(time_index(1, "9:45"))
    #     # print(location_index(2324) > time_index(2324, "9:45"))
    #     # print(prv_trade_date != today(2324))
    #     for x in self.df2_nifty_CE.index:
    #         pro = 0
    #         # print(x)

    #         if(self.location_index(x) > self.time_index(x, "9:45")) and (not buy_flag) and (prv_trade_date != self.today(x) or trade == 0):
    #             trade += 1
    #             buying_price = self.location_ohlcv("close", x)

    #             order.append(-1)
    #             buy_sell.append("Buy")
    #             Entry_price.append(buying_price)
    #             Exit_price.append("")
    #             mtm.append("Position Taken")
    #             self.df2_nifty_CE["Position"][x] = 1

    #             buy_flag1 = True
    #             buy_flag = True
    #             sell_flag = False

    #         elif(((self.location_ohlcv("close", x) - buying_price) * self.lot_size <= -500) or ((self.location_ohlcv("close", x) - buying_price) * self.lot_size >= 1500) or (self.location_index(x) >= self.time_index(x, "15:00:00"))) and (not sell_flag):
    #             date = str(self.df2_nifty_CE.index[x]).split(' ')
    #             prv_trade_date = date[0]
    #             pro = self.location_ohlcv("close", x) - buying_price
    #             trade += 1
    #             selling_price = self.location_ohlcv("close", x)

    #             order.append(1)
    #             buy_sell.append("Sell")
    #             Entry_price.append("")
    #             Exit_price.append(selling_price)
    #             mtm.append("Position closed")

    #             if buy_flag1 == True:
    #                 buy_flag1 = False
    #             buy_flag = False
    #             sell_flag = True
    #         else:
    #             if (buy_flag == True):
    #                 yy = (self.location_ohlcv("close", x) -
    #                       buying_price) * self.lot_size
    #             else:
    #                 yy = "0"

    #             order.append(0)
    #             buy_sell.append("No Trade")
    #             Entry_price.append("")
    #             Exit_price.append("")
    #             mtm.append(yy)

    #             if buy_flag1 == True:
    #                 self.df2_nifty_CE["Position"][x] = 1

    #         no_of_trades.append(trade)
    #         profit.append(pro)

    #     initial_capital = int(self.request.data["Initial_Capital"])
    #     self.df2_nifty_CE['Returns'] = np.log(
    #         self.df2_nifty_CE["close"] / self.df2_nifty_CE["close"].shift(1))
    #     self.df2_nifty_CE['Strategy_Return'] = self.df2_nifty_CE['Position'].shift(
    #         1) * self.df2_nifty_CE['Returns']
    #     self.df2_nifty_CE["placed_order"] = order
    #     self.df2_nifty_CE["buy_sell"] = buy_sell
    #     self.df2_nifty_CE["Entry"] = Entry_price
    #     self.df2_nifty_CE["Exit"] = Exit_price
    #     self.df2_nifty_CE['profit'] = profit
    #     self.df2_nifty_CE['profit'] = (
    #         self.df2_nifty_CE['profit']) * self.lot_size
    #     self.df2_nifty_CE["mtm"] = mtm
    #     self.df2_nifty_CE["cost"] = (self.df2_nifty_CE["placed_order"].multiply(
    #         self.df2_nifty_CE["close"])) * self.lot_size
    #     self.df2_nifty_CE["Account"] = initial_capital + \
    #         self.df2_nifty_CE["cost"].cumsum()
    #     self.df2_nifty_CE["Trades"] = no_of_trades

    #     risk_free_rate = 0.06/252
    #     if np.std(self.df2_nifty_CE.Strategy_Return) != 0:
    #         sharpe = np.sqrt(252)*(np.mean(self.df2_nifty_CE.Strategy_Return) -
    #                                (risk_free_rate))/np.std(self.df2_nifty_CE.Strategy_Return)
    #     else:
    #         sharpe = "undefined"

    #     cumulative_returns = self.df2_nifty_CE.Strategy_Return.cumsum(
    #     ).iloc[-1]
    #     period_in_days = len(self.df2_nifty_CE.Strategy_Return)
    #     CAGR = 100*((cumulative_returns+1)**(252.0/period_in_days)-1)

    #     self.df2_nifty_CE.dropna(inplace=True)
    #     cum_ret = self.df2_nifty_CE.Strategy_Return.cumsum()

    #     peak = (np.maximum.accumulate(cum_ret) - cum_ret).idxmax()
    #     trough = cum_ret[:peak].idxmax()
    #     drawdown = (cum_ret[trough] - cum_ret[peak]) * 100

    #     buy_records = self.df2_nifty_CE[self.df2_nifty_CE["buy_sell"] == "Buy"]
    #     sell_records = self.df2_nifty_CE[self.df2_nifty_CE["buy_sell"] == "Sell"]

    #     trade_details = pd.DataFrame(0, index=range(len(buy_records)),
    #                                  columns=["Entry", "Date",
    #                                           "Price", "Exit",
    #                                           "ExDate", "ExPrice"])
    #     trade_details["Entry"] = buy_records["buy_sell"].values
    #     trade_details["Date"] = buy_records.index.values  # buy date
    #     trade_details["Price"] = buy_records["close"].values  # buy price
    #     trade_details["Exit"] = sell_records["buy_sell"].values
    #     trade_details["ExDate"] = sell_records.index.values  # sell date
    #     trade_details["ExPrice"] = sell_records["close"].values  # sell price
    #     trade_details['% Change'] = (
    #         trade_details['ExPrice'] / trade_details['Price']) - 1
    #     trade_details['Profit'] = trade_details['ExPrice'] - \
    #         trade_details['Price']
    #     trade_details['% Profit'] = (
    #         trade_details['ExPrice'] / trade_details['Price']) - 1
    #     trade_details['Position value'] = trade_details['Price']
    #     trade_details['Cumm Profit'] = trade_details['Profit'].cumsum()
    #     trade_details['MAE'] = 0
    #     trade_details['MFE'] = 0
    #     trade_details['Scale In / Scale Out'] = 0
    #     output = {}

    #     profit = trade_details[trade_details["Profit"] >= 1]
    #     loss = trade_details[trade_details["Profit"] <= -1]

    #     # table = BeautifulTable()
    #     # table.column_headers = ['PERFORMANCE METRICS', 'VALUES']
    #     output["request"] = self.request.data["symbol"]
    #     print(request.data)
    #     # table.append_row(["Trade start date", self.df2_nifty_CE.index[0]])
    #     output["Trade start date"] = self.df2_nifty_CE.index[0]
    #     # table.append_row(['Trade end date', self.df2_nifty_CE.index[-1]])
    #     output['Trade end date'] = self.df2_nifty_CE.index[-1]
    #     # table.append_row(
    #     #     ['Initial_Capital', self.df2_nifty_CE["Account"].iloc[0]])
    #     output['Initial_Capital'] = self.df2_nifty_CE["Account"].iloc[0]
    #     # table.append_row(
    #     #     ['Ending_Capital', self.df2_nifty_CE["Account"].iloc[-1]])
    #     output['Ending_Capital'] = self.df2_nifty_CE["Account"].iloc[-1]
    #     # table.append_row(['Total no trades', len(buy_records)])
    #     output['Total no trades'] = len(buy_records)
    #     # table.append_row(['Positive_trades', len(
    #     #     self.df2_nifty_CE[self.df2_nifty_CE["profit"] >= 1])])
    #     output['Positive_trades'] = len(
    #         self.df2_nifty_CE[self.df2_nifty_CE["profit"] >= 1])
    #     # table.append_row(['Negative_trades', len(
    #     #     self.df2_nifty_CE[self.df2_nifty_CE["profit"] <= -1])])
    #     output['Negative_trades'] = len(
    #         self.df2_nifty_CE[self.df2_nifty_CE["profit"] <= -1])
    #     # table.append_row(
    #     #     ['Total_profit', self.df2_nifty_CE[self.df2_nifty_CE["profit"] >= 1]["profit"].sum()])
    #     output['Negative_trades'] = self.df2_nifty_CE[self.df2_nifty_CE["profit"]
    #                                                   >= 1]["profit"].sum()
    #     # table.append_row(
    #     #     ['Total_loss', self.df2_nifty_CE[self.df2_nifty_CE["profit"] <= -1]["profit"].sum()])
    #     output['Total_loss'] = self.df2_nifty_CE[self.df2_nifty_CE["profit"]
    #                                              <= -1]["profit"].sum()
    #     # table.append_row(
    #     #     ['Net Profit', self.df2_nifty_CE["Account"].iloc[-1] - self.df2_nifty_CE["Account"].iloc[0]])
    #     output['Net Profit'] = self.df2_nifty_CE["Account"].iloc[-1] - \
    #         self.df2_nifty_CE["Account"].iloc[0]
    #     # table.append_row(['Net Profit (%)', ((
    #     #     self.df2_nifty_CE["Account"].iloc[-1] / self.df2_nifty_CE["Account"].iloc[0]) - 1) * 100])
    #     output['Net Profit (%)'] = (self.df2_nifty_CE["Account"].iloc[-1] /
    #                                 (self.df2_nifty_CE["Account"].iloc[0]) - 1) * 100
    #     # table.append_row(['Avg. Profit / Loss',
    #     #                   np.mean(profit["Profit"].values) / np.mean(loss["Profit"].values)])
    #     # output['Avg. Profit / Loss'] = np.mean(
    #     #     profit["Profit"].values) / np.mean(loss["Profit"].values)
    #     # table.append_row(['Sharpe ratio', sharpe])
    #     output['Sharpe ratio'] = sharpe
    #     # table.append_row(['CAGR (%)', CAGR])
    #     output['CAGR (%)'] = CAGR
    #     # table.append_row(['Maximum Drawdown (%)', drawdown])
    #     output['Maximum Drawdown (%)'] = drawdown
    #     # table.append_row(['CAGR / MDD (%)', CAGR / drawdown])
    #     # output['CAGR / MDD (%)'] = CAGR / drawdown
    #     # table.set_style(BeautifulTable.STYLE_GRID)
    #     # table.column_alignments['PERFORMANCE METRICS'] = BeautifulTable.ALIGN_LEFT
    #     # table.column_alignments['VALUES'] = BeautifulTable.ALIGN_RIGHT
    #     # table.left_padding_widths['VALUES'] = 10
    #     print(output)
    #     # x = {"hello": "123"}
    #     return Response(output)

    #     # return Response(x)
    #     # print(self.request.data, "request")

    # def location_index(self, bar):
    #     # id_loc = self.df2_nifty_CE.index[bar]
    #     id_loc = self.df2_nifty_CE['Date'][bar]
    #     return id_loc

    # def time_index(self, bar, time):
    #     # today_date = str(df2_nifty_CE.index[bar]).split(' ')
    #     today_date = str(self.df2_nifty_CE['Date'][bar]).split(' ')
    #     today_date_time = today_date[0] + " " + time  # "09:45:00"
    #     return today_date_time

    # def location_ohlcv(self, col, bar):
    #     # col_val = self.df2_nifty_CE[col].iloc[bar]
    #     col_val = self.df2_nifty_CE[col][bar]
    #     return col_val

    # def today(self, bar):
    #     # today = str(df2_nifty_CE.index[bar]).split(' ')
    #     today = str(self.df2_nifty_CE['Date'][bar]).split(' ')
    #     today_date = today[0]
    #     return today_date
