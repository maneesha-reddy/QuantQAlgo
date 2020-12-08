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
import itertools
# from aiohttp import web
# from aiohttp import WSMsgType
from rest_framework.decorators import api_view
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


def EMA(df, base, target, period, alpha=False):

    con = pd.concat([df[:period][base].rolling(
        window=period).mean(), df[period:][base]])

    if (alpha == True):
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df


def ATR(df, period, ohlc=['Open', 'High', 'Low', 'Close']):

    atr = 'ATR_' + str(period)
    df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
    df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
    df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())
    df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)
    df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)
    EMA(df, 'TR', atr, period, alpha=True)

    return df


def SuperTrend(df, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close']):
    ATR(df, period, ohlc=ohlc)
    atr = 'ATR_' + str(period)
    st = 'ST_' + str(period) + '_' + str(multiplier)
    stx = 'STX_' + str(period) + '_' + str(multiplier)

    df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
    df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

    df['final_ub'] = 0.00
    df['final_lb'] = 0.00
    for i in range(period, len(df)):
        df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i -
                                                                                                    1] or df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else df['final_ub'].iat[i - 1]
        df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i -
                                                                                                    1] or df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else df['final_lb'].iat[i - 1]

    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] <= df['final_ub'].iat[i] else \
            df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] > df['final_ub'].iat[i] else \
            df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= df['final_lb'].iat[i] else \
            df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i -
                                                                             1] and df[ohlc[3]].iat[i] < df['final_lb'].iat[i] else 0.00

    df[stx] = np.where((df[st] > 0.00), np.where(
        (df[ohlc[3]] < df[st]), 'down',  'up'), np.NaN)

    df.drop(['basic_ub', 'basic_lb', 'final_ub',
             'final_lb'], inplace=True, axis=1)

    df.fillna(0, inplace=True)

    return df


def RSI(series, rsi_period):
    chg = series.diff(1)
    gain = chg.mask(chg < 0, 0)
    data = pd.DataFrame()
    data['gain'] = gain
    loss = chg.mask(chg > 0, 0)
    data['loss'] = loss
    avg_gain = data['gain'].mean(axis=0, skipna=True)
    avg_loss = data['loss'].mean(axis=0, skipna=True)
    rs = abs(avg_gain/avg_loss)
    rsi = 100-(100/(1+rs))
    return rsi


def macd(df, m1, m2, s1):
    df.reset_index(level=0, inplace=True)
    df.columns = ['ds', 'y']
    exp1 = df.y.ewm(span=m1, adjust=False).mean()
    exp2 = df.y.ewm(span=m2, adjust=False).mean()
    macd2 = exp1-exp2
    exp3 = macd2.ewm(span=s1, adjust=False).mean()
    return macd2, exp3


def indicator(tk, ltp, ohlc, ltp_df):
    global ltp_f
    global le_t
    global se_t
    global Rmin1
    global Rhr1
    global Shr1
    global Smin1
    global Mhr1
    global Mmin1
    global data1
    global data2
    global data3
    global signal
    global dict1
    global dict2
    global leflag
    global lxflag
    global seflag
    global sxflag
    global flag4
    global chtime
    global lsigflag
    global ssigflag
    global sigmin
    global Rlen
    global Slen
    global Mlen
    T2 = datetime.now()
    hr2 = int(T2.hour)
    min2 = int(T2.minute)
    # tk=ticks[i]['instrument_token']
    code = dict1[tk]
    loop = dict2[tk]
    # print(loop, "loop")
    ltp_f[loop] = ltp

    if(Rlen == 60):
        if(Rhr1[loop]+1 == hr2 and Rmin1[loop] == min2):
            print("RSI of "+str(code)+" updated at "+str(T2))
            data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
            Rhr1[loop] = Rhr1[loop]+1

    elif(Rlen == 30):
        if(Rmin1[loop] == 15):
            if(Rhr1[loop] == hr2 and min2 == 45):
                print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rmin1[loop] = 45
        elif(Rmin1[loop] == 45):
            if(Rhr1[loop]+1 == hr2 and min2 == 15):
                print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rhr1[loop] = Rhr1[loop]+1
                Rmin1[loop] = 15

    elif(Rlen == 15):
        if(Rmin1[loop] == 15):
            if(Rhr1[loop] == hr2 and min2 == 30):
                print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rmin1[loop] = 30
        elif(Rmin1[loop] == 30):
            if(Rhr1[loop] == hr2 and min2 == 45):
                print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rmin1[loop] = 45
        elif(Rmin1[loop] == 45):
            if(Rhr1[loop]+1 == hr2 and min2 == 0):
                print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rhr1[loop] = Rhr1[loop]+1
                Rmin1[loop] = 0
        elif(Rmin1[loop] == 0):
            if(Rhr1[loop] == hr2 and min2 == 15):
                print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rmin1[loop] = 15
    elif(Rlen == 5):
        if(Rhr1[loop] == hr2):
            if(Rmin1[loop]+5 <= min2):
                #                 print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rmin1[loop] = Rmin1[loop]+5
        else:
            if(min2 >= 0):
                #                 print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rmin1[loop] = Rmin1[loop]+5

    # cc=data1[loop][-25:]
    # print(cc)
    close1 = data1[loop][['Close']][-26:-1]
    # print(close1)
    close1 = close1.append(ltp_df, ignore_index=True)
    close2 = close1['Close']
    # print(close2)
    RSI1 = RSI(close2, 25)
    # print(RSI)
    v1 = RSI1
    close11 = data1[loop]['Close'][-27:-1]
    close12 = data1[loop]['Close'][-28:-2]
    close13 = data1[loop]['Close'][-29:-3]
    close14 = data1[loop]['Close'][-30:-4]
    close15 = data1[loop]['Close'][-31:-5]
    v11 = RSI(close11, 25)
    v12 = RSI(close12, 25)
    v13 = RSI(close13, 25)
    v14 = RSI(close14, 25)
    v15 = RSI(close15, 25)
#     print(v1)

    if(Mlen == 60):
        if(Mhr1[loop]+1 == hr2 and Mmin1[loop] == min2):
            print("MACD of "+str(code)+" updated at "+str(T2))
            data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
            Mhr1[loop] = Mhr1[loop]+1

    elif(Mlen == 30):
        if(Mmin1[loop] == 15):
            if(Mhr1[loop] == hr2 and min2 == 45):
                print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mmin1[loop] = 45
        elif(Mmin1[loop] == 45):
            if(Mhr1[loop]+1 == hr2 and min2 == 15):
                print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mhr1[loop] = Mhr1[loop]+1
                Mmin1[loop] = 15

    elif(Mlen == 15):
        if(Mmin1[loop] == 15):
            if(Mhr1[loop] == hr2 and min2 == 30):
                print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mmin1[loop] = 30
        elif(Mmin1[loop] == 30):
            if(Mhr1[loop] == hr2 and min2 == 45):
                print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mmin1[loop] = 45
        elif(Mmin1[loop] == 45):
            if(Mhr1[loop]+1 == hr2 and min2 == 0):
                print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mhr1[loop] = Mhr1[loop]+1
                Mmin1[loop] = 0
        elif(Mmin1[loop] == 0):
            if(Mhr1[loop] == hr2 and min2 == 15):
                print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mmin1[loop] = 15

    elif(Mlen == 5):
        if(Mhr1[loop] == hr2):
            if(Mmin1[loop]+5 <= min2):
                #                 print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mmin1[loop] = Mmin1[loop]+5
        else:
            if(min2 >= 0):
                #                 print("MACD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                Mmin1[loop] = Mmin1[loop]+5

    dff = data3[loop][['Close']]
    dff = dff.append(ltp_df, ignore_index=True)
    macd3, sig3 = macd(dff, 12, 26, 9)
    vm1 = macd3.iloc[-1]
    vm2 = macd3.iloc[-2]
    vm3 = macd3.iloc[-3]
    vm4 = macd3.iloc[-4]
    vm5 = macd3.iloc[-5]
    vm6 = macd3.iloc[-6]
    vs1 = sig3.iloc[-1]
    vs2 = sig3.iloc[-2]
    vs3 = sig3.iloc[-3]
    vs4 = sig3.iloc[-4]
    vs5 = sig3.iloc[-5]
    vs6 = sig3.iloc[-6]
#     print(vmt,vst,vmy,vsy)
    v5 = 'No Cross-Over'
    v21 = 0
    v22 = 0
    v23 = 0
    v24 = 0
    v25 = 0
    if vm1 > 0 and vs1 > 0:
        if vm1 > vs1 and vm2 < vs2:
            v21 = 1
            v5 = "Cross-Over above line"
    if vm2 > 0 and vs2 > 0:
        if vm2 > vs2 and vm3 < vs3:
            v22 = 1
            v5 = "Cross-Over above line"
    if vm3 > 0 and vs3 > 0:
        if vm3 > vs3 and vm4 < vs4:
            v23 = 1
            v5 = "Cross-Over above line"
    if vm4 > 0 and vs4 > 0:
        if vm4 > vs4 and vm5 < vs5:
            v24 = 1
            v5 = "Cross-Over above line"
    if vm5 > 0 and vs5 > 0:
        if vm5 > vs5 and vm6 < vs6:
            v25 = 1
            v5 = "Cross-Over above line"

    v61 = 0
    v62 = 0
    v63 = 0
    v64 = 0
    v65 = 0
    if vm1 < 0 and vs1 < 0:
        if vm1 > vs1 and vm2 < vs2:
            v61 = 1
            v5 = "Cross-Over below line"
    if vm2 < 0 and vs2 < 0:
        if vm2 > vs2 and vm3 < vs3:
            v62 = 1
            v5 = "Cross-Over below line"
    if vm3 < 0 and vs3 < 0:
        if vm3 > vs3 and vm4 < vs4:
            v63 = 1
            v5 = "Cross-Over below line"
    if vm4 < 0 and vs4 < 0:
        if vm4 > vs4 and vm5 < vs5:
            v64 = 1
            v5 = "Cross-Over below line"
    if vm5 < 0 and vs5 < 0:
        if vm5 > vs5 and vm6 < vs6:
            v65 = 1
            v5 = "Cross-Over below line"

    ohlc2 = {}
    ohlc2['Open'] = ohlc['open']
    ohlc2['High'] = ohlc['high']
    ohlc2['Low'] = ohlc['low']
    ohlc2['Close'] = ohlc['close']

    if(Slen == 60):
        if(Shr1[loop]+1 == hr2 and Smin1[loop] == min2):
            print("STRD of "+str(code)+" updated at "+str(T2))
            data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
            Shr1[loop] = Shr1[loop]+1

    elif(Slen == 30):
        if(Smin1[loop] == 15):
            if(Shr1[loop] == hr2 and min2 == 45):
                print("STRD of "+str(code)+" updated at "+str(T2))
                data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                Smin1[loop] = 45
        elif(Smin1[loop] == 45):
            if(Shr1[loop]+1 == hr2 and min2 == 15):
                print("STRD of "+str(code)+" updated at "+str(T2))
                data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                Shr1[loop] = Shr1[loop]+1
                Smin1[loop] = 15

    elif(Slen == 15):
        if(Smin1[loop] == 15):
            if(Shr1[loop] == hr2 and min2 == 30):
                print("STRDof "+str(code)+" updated at "+str(T2))
                data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                Smin1[loop] = 30
        elif(Smin1[loop] == 30):
            if(Shr1[loop] == hr2 and min2 == 45):
                print("STRD of "+str(code)+" updated at "+str(T2))
                data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                Smin1[loop] = 45
        elif(Smin1[loop] == 45):
            if(Shr1[loop]+1 == hr2 and min2 == 0):
                print("STRD of "+str(code)+" updated at "+str(T2))
                data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                Shr1[loop] = Shr1[loop]+1
                Smin1[loop] = 0
        elif(Smin1[loop] == 0):
            if(Shr1[loop] == hr2 and min2 == 15):
                print("STRD of "+str(code)+" updated at "+str(T2))
                data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                Smin1[loop] = 15

    elif(Slen == 5):
        if(Shr1[loop] == hr2):
            if(Smin1[loop]+5 <= min2):
                #                 print("STRD of "+str(code)+" updated at "+str(T2))
                data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                Smin1[loop] = Smin1[loop]+5
        else:
            if(min2 >= 0):
                #                 print("STRD of "+str(code)+" updated at "+str(T2))
                data3[loop] = data3[loop].append(ohlc2, ignore_index=True)
                Mmin1[loop] = Mmin1[loop]+5

    strd = data2[loop].iloc[-24:]
    strd = strd.append(ohlc2, ignore_index=True)
    ans2 = SuperTrend(strd, 15, 1.5)
    # print(ans2)
    v3 = ans2['STX_15_1.5'].iloc[-1]
    v4 = ans2['ST_15_1.5'].iloc[-1]
    # print(v3)
    v31 = ans2['STX_15_1.5'].iloc[-2]
    v32 = ans2['STX_15_1.5'].iloc[-3]
    v33 = ans2['STX_15_1.5'].iloc[-4]
    v34 = ans2['STX_15_1.5'].iloc[-5]
    v35 = ans2['STX_15_1.5'].iloc[-6]
    val = ''
    if (v3 == "up" and v1 > 55 and (not leflag[loop]) and (not seflag[loop])) or lsigflag[loop] == 1:
        val = 'In-LE-For-A-While'
        val = 'LE'
        if((v31 == "down" or v32 == "down" or v33 == "down" or v34 == "down" or v35 == "down") and (v11 <= 55 or v12 <= 55 or v13 <= 55 or v14 <= 55 or v15 <= 55)) or lsigflag[loop] == 1:
            print("check-1", v3, v1, v5,
                  ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
            if lsigflag[loop] == 0:
                sigmin[loop] = int(min2)
                lsigflag[loop] = 1
                val = "Might-Give-A-LE-Signal"
                print("LE-flag value at might= ",
                      lsigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
            elif lsigflag[loop] == 1 and sigmin[loop]+chtime <= int(min2):
                print("check-2", v3, v1, v5,
                      ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                if (v3 == "up" and v1 > 55 and (not leflag[loop]) and (not seflag[loop])):
                    val = "LE"
                    leflag[loop] = True
                    lxflag[loop] = False
                    le_t.append(loop)
                    lsigflag[loop] = 0
                    sigmin[loop] = 0
                else:
                    val = "LE-failed"
                    lsigflag[loop] = 0
                    sigmin[loop] = 0
            else:
                val = "Waiting-for-LE"
                print("LE-flag value at wait= ",
                      lsigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)

    elif v3 == "down" and (not lxflag[loop]):
        val = "LX"
        # leflag[loop] = False
        # lxflag[loop] = True
    elif (v3 == "down" and v1 < 45 and (not leflag[loop]) and (not seflag[loop])) or ssigflag[loop] == 1:
        val = 'In-SE-For-A-While'
        val = 'SE'
        if ((v31 == "up" or v32 == "up" or v33 == "up" or v34 == "up" or v35 == "up") and (v11 >= 45 or v12 >= 45 or v13 >= 45 or v14 >= 45 or v15 >= 45)) or ssigflag[loop] == 1:
            print("check-1", v3, v1, v5,
                  ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
            if ssigflag[loop] == 0:
                sigmin[loop] = int(min2)
                ssigflag[loop] = 1
                val = "Might-Give-A-SE-Signal"
                print("SE-flag value at might= ",
                      ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
            if ssigflag[loop] == 1 and sigmin[loop]+chtime <= int(min2):
                print("check-2", v3, v1, v5,
                      ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                if (v3 == "down" and v1 < 45 and (not leflag[loop]) and (not seflag[loop])):
                    val = "SE"
                    seflag[loop] = True
                    sxflag[loop] = False
                    se_t.append(loop)
                    ssigflag[loop] = 0
                    sigmin[loop] = 0
                else:
                    val = "SE-Failed"
                    ssigflag[loop] = 0
                    sigmin[loop] = 0
            else:
                val = "Waiting-for-SE"
                print("SE-flag value at wait= ",
                      ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
    elif v3 == "up" and (not sxflag[loop]):
        val = "SX"
        seflag[loop] = False
        sxflag[loop] = True
    else:
        if (leflag[loop] == True):
            # print(code,end=' ')
            val = "buy already"

        elif (seflag[loop] == True):
            # print(code,end=' ')
            val = "short already"
        else:
            # print(code,end=' ')
            val = "NO-TRADE"

    if(val != signal[loop] and val != "NO-TRADE") or (val == "LE") or (val == "SE"):
        signal[loop] = val
#         res=str(code)+" "+str(val)+" "+"LTP="+str(ltp)+" "+" RSI="+str(v1)+" "+" SUPERTEND="+str(v4)+" "+str(v3)+" "+"MACD= "+v5+" TIMESTAMP="+str(T2)+"\n"
#         print(res)
#         print(code,val,ltp,v1,v4,v3,T2)
        file1 = open("MACD_Added_LiveTest_Results.txt", "a+")
    # print(code,val,ltp,v1,v4,v3,T2)
        res = str(code)+" "+str(val)+" "+"LTP="+str(ltp)+" "+" RSI="+str(v1)+" " + \
            " SUPERTEND="+str(v4)+" "+str(v3)+" "+"MACD= " + \
            v5+" TIMESTAMP="+str(T2)+"\n"
#             print(res)
        file1.write(res)
        file1.close()
#     res=str(code)+" "+str(val)+" "+"LTP="+str(ltp)+" "+" RSI="+str(v1)+" "+" SUPERTEND="+str(v4)+" "+str(v3)+" "+"MACD= "+v5+" TIMESTAMP="+str(T2)+"\n"
#     print(res)

    for j in range(len(dict3)):
        if lsigflag[j] == 1:
            if sigmin[j]+chtime < int(min2):
                print("Flag of "+str(dict1[dict3[j]]) +
                      " is made 0 ", sigmin[j], min2)
                lsigflag[j] = 0
                sigmin[j] = 0
        if ssigflag[j] == 1:
            if sigmin[j]+chtime < int(min2):
                print("Flag of "+str(dict1[dict3[j]]) +
                      " is made 0", sigmin[j], min2)
                ssigflag[j] = 0
                sigmin[j] = 0
    # print("ticker completed")


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
    global allltp
    for i in range(len(ticks)):
        # print(i, end=" ")
        c = close[ticks[i]['instrument_token']]
        allltp[ticks[i]['instrument_token']] = [ticks[i]['last_price'], c]
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
            logging.debug("Ticks: {}".format(ticks))

        ltp = ticks[i]['last_price']
        ohlc = ticks[i]['ohlc']
        ltp_df = {'Close': ltp}
        tk = ticks[i]['instrument_token']
        indicator(tk, ltp, ohlc, ltp_df)

    s = {k: v for k, v in sorted(s.items(), key=lambda item: item[1])}
    global le_t

    print("\n", le_t, "le_t")
    for i in le_t:
        print(dict3[i])
        paperNames.append(dict1[dict3[i]])
    global papercapital
    invst = papercapital/4

    if 0 in trade_flag:
        pos = trade_flag.index(0)
        if len(le_t) > 0:
            token1 = dict3[le_t[-1]]
#             print("token1 taken")
        if len(se_t) > 0:
            token2 = dict3[se_t[-1]]
            print(token2)
#             print("token2 taken")

        if len(le_t) > 0 or len(se_t) > 0:
            if token1 not in trade_tokens:
                sizep = invst//ltp_f[le_t[-1]]
                if sizep >= 1:
                    trade_flag[pos] = 1
                    trade_tokens[pos] = token1
                    trade_name[pos] = dict1[token1]
                    entry_val[pos] = ltp_f[le_t[-1]]
                    size[pos] = invst//entry_val[pos]
                    print("trade opened")
                    print(trade_name[pos], trade_flag[pos],
                          entry_val[pos], size[pos])
                    le_t.pop()
            elif token2 not in trade_tokens:
                sizep = invst//ltp_f[le_t[-1]]
                if sizep >= 1:
                    trade_flag[pos] = 2
                    trade_tokens[pos] = token2
                    trade_name[pos] = dict1[token2]
                    entry_val[pos] = ltp_f[se_t[-1]]
                    size[pos] = invst//entry_val[pos]
                    print("trade opened")
                    print(trade_name[pos], trade_flag[pos],
                          entry_val[pos], size[pos])
                    se_t.pop()

    for i in range(4):
        if trade_flag[i] != 0:
            if trade_flag[i] == 1:
                loop = dict2[trade_tokens[i]]
                if lxflag[loop] == False:
                    trade_ltp[i] = ltp_f[loop]
                    pnl1 = (ltp_f[loop]-entry_val[i])*size[i]
                    if pnl1 != pnl[i]:
                        papercapital = papercapital-pnl[i]
                        pnl[i] = pnl1
                        papercapital = papercapital+pnl[i]
                        print("trade updated")
                        print(trade_name[i], trade_flag[i], entry_val[i],
                              size[i], trade_ltp[i], pnl[i], papercapital)
                else:
                    trade_flag[i] = 0
                    print("trade closed")
                    print(trade_name[i], pnl[i])
            elif trade_flag[i] == 2:
                loop = dict2[trade_tokens[i]]
                if sxflag[loop] == False:
                    trade_ltp[i] = ltp_f[loop]
                    pnl1 = (entry_val[i]-ltp_f[loop])*size[i]
                    if pnl1 != pnl[i]:
                        papercapital = papercapital-pnl[i]
                        pnl[i] = pnl1
                        papercapital = papercapital+pnl[i]
                        print("trade updated")
                        print(trade_name[i], trade_flag[i], entry_val[i],
                              size[i], trade_ltp[i], pnl[i], papercapital)
                else:
                    trade_flag[i] = 0
                    print("trade closed")
                    print(trade_name[i], pnl[i])
    print(papercapital)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    print("hi")
    kws.connect(threaded=True, disable_ssl_verification=False)
    while True:
        if count % 120 == 1:
            print(count)
            # print(datetime.now())
            if(len(nltp) != 0):
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
        # trade_tokens = [0 for i in range(4)]

        sio.emit('paper', papercapital)
        sio.emit('size', size)
        sio.emit('tradename', trade_name)
        sio.emit('pnl', pnl)
        sio.emit('entryval', entry_val)
        sio.emit('tradeltp', trade_ltp)
        sio.emit('tradetoken', trade_tokens)
        # print(s)
        if k != []:
            loosersName = []
            loosersltp = []
            # print(k, "k")
            for i in range(5):
                loosersName.append(dict1[k[i]])
                loosersltp.append(
                    [round(s[k[i]], 2), allltp[k[i]][0], allltp[k[i]][1]])

                # print(dict1[k[i]])
                # x = str(dict1[k[i]]).split('"')

            gainersName = []
            gainersltp = []
            g = k[-5:]
            for i in range(5):
                gainersName.append(dict1[g[i]])
                gainersltp.append(
                    [round(s[g[i]], 2), allltp[g[i]][0], allltp[g[i]][1]])
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
    if str(t1.time()) < "09:15:00":
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        t1 = str(yesterday)+"+"+"09:15:00"
        t2 = str(yesterday)+"+"+"22:30:00"
    else:
        today = datetime.utcnow().date()
        t1 = str(today)+"+"+"09:15:00"
        t2 = str(today)+"+"+str(t2.time())

    # if str(t2.time()) > '15:30:00':
    #     t2 = str(t2.date())+' '+'15:30:00'
    #     print(t2)
    # t1 = str(t1)
    # t2 = str(t2)
    # t1 = t1.split(" ")
    # t3 = t1[1].split(':')
    # t3[0] = '09'
    # t3[1] = '15'
    # t3 = t3[0]+':'+t3[1]+':'+t3[2]
    # t1 = t1[0]+"+"+t3
    # t2 = t2.split(" ")
    # t2 = t2[0]+"+"+t2[1]
    print(t1)
    print(t2)
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(token)+"/15minute?from="+t1+"&to="+t2
    print(url2)
    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
    res2 = requests.get(url2, headers=HEADERS)
    dat2 = res2.json()
    dat2 = dat2["data"]["candles"]

    # print(data2)
    # print(data2)
    timestamp = []
    close1 = []
    for i in range(len(dat2)):
        # print(dat2[i][0])
        d = dat2[i][0].split("T")
        d = d[1].split("+")
        timestamp.append(d[0])
        close1.append(dat2[i][4])
    return timestamp, close1


# with open('app/tokens.p', 'rb') as fp:
#     dict3 = pickle.load(fp)
# with open('app/instruments.p', 'rb') as fp:
#     dict1 = pickle.load(fp)


# dict3[137] = 256265
# dict3[138] = 265
# dict3[139] = 260105
# dict3[140] = 264969
# dict1[256265] = '"NIFTI"'
# dict1[265] = '"SENSEX"'
# dict1[260105] = '"NIFTI BANK"'
# dict1[264969] = '"INDIA VIX"'
# dict1={57648135:'GOLD-21JAN' ,56744455: 'CRUDEOIL21JAN', 57445383 : 'ZINC21JAN'  }
# dict2={57648135 : 0 , 56744455:1 , 2:57445383}
# dict3={0 : 57648135 , 1:56744455, 57445383:2}
dict3 = {}
dict1 = {}
dict3[0] = 256265
dict3[1] = 265
dict3[2] = 260105
dict3[3] = 264969
dict3[4] = 56407303
dict3[5] = 56551687
dict3[6] = 57062151
dict3[7] = 57059847
dict1[256265] = '"NIFTY"'
dict1[265] = '"SENSEX"'
dict1[260105] = '"NIFTY BANK"'
dict1[264969] = '"INDIA VIX"'
dict1[56407303] = '"COTTON"'
dict1[56551687] = '"CRUDEOIL21JAN"'
dict1[57062151] = '"ZINC21JAN"'
dict1[57059847] = '"ALUMINIUM"'


# dict3 = dict(itertools.islice(dict3.items(), 100))
# dict1 = dict(itertools.islice(dict1.items(), 100))
dict2 = {v: k for k, v in dict3.items()}

acc_key = accesskey()
niftiltp = []
niftitime = []
nltp = []
ntime = ''
paperNames = []

sensexltp = []
sensextime = []
sltp = []
stime = ''

bankltp = []
banktime = []
bltp = []
btime = ''

indialtp = []
indiatime = []
iltp = []
itime = ''

close = {}
s = {}
allltp = {}

ltp_f = [0 for i in range(len(dict3))]
le_t = [4, 5, 6, 7]
se_t = []

keys = list(dict1)
close = {}
s = {}
papercapital = 0
trade_tokens = [0 for i in range(4)]
trade_flag = [0 for i in range(4)]
trade_name = ['' for i in range(4)]
entry_val = [0 for i in range(4)]
pnl = [0 for i in range(4)]
size = [0 for i in range(4)]
trade_ltp = [0 for i in range(4)]
token1 = 0
token2 = 0

today = datetime.utcnow().date()
# print(today)
yesterday = today - timedelta(days=3)
t1 = str(yesterday)+"+"+"14:15:00"
t2 = str(today)+"+"+"04:30:00"

print(t1)
print(t2)
for i in range(len(dict3)):
    print(i)
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(dict3[i])+"/15minute?from="+t1+"&to="+t2

    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
    res2 = requests.get(url2, headers=HEADERS)
    data2 = res2.json()
    # print(data2)
    data2 = data2["data"]["candles"]

    # if i == 137:
    #     # print(data2)
    # global close
    close[keys[i]] = data2[-1][4]

data1 = ['' for i in range(len(dict3))]
data2 = ['' for i in range(len(dict3))]
data3 = ['' for i in range(len(dict3))]
leflag = [True for i in range(len(dict3))]
seflag = [False for i in range(len(dict3))]
lxflag = [False for i in range(len(dict3))]
sxflag = [True for i in range(len(dict3))]
signal = ['' for i in range(len(dict3))]
flag4 = [1 for i in range(len(dict3))]
sigmin = [0 for i in range(len(dict3))]
lsigflag = [0 for i in range(len(dict3))]
ssigflag = [0 for i in range(len(dict3))]
chtime = 0  # check-time for a signal in minutes
Rlen = 30  # RSI time-period : Allowed - 15,30,60(in minutes)
Slen = 30  # SuperTrend time-period : Allowed - 15,30,60(in minutes)
Mlen = 30  # MACD time-period : Allowed - 15,30,60(in minutes)

for i in range(len(dict3)):
    # print(i)
    t2 = (datetime.now())
    t1 = (datetime.now() - timedelta(days=10))
    # print(t1)
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
#     print(t1)
#     print(t2)
    url1 = "https://api.kite.trade/instruments/historical/" + \
        str(dict3[i])+"/" + str(Rlen)+"minute?from="+t1+"&to="+t2
    print(url1)
    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
    res1 = requests.get(url1, headers=HEADERS)
    data1[i] = res1.json()
#     print(data1[i])
    data1[i] = data1[i]["data"]["candles"]
    data1[i] = pd.DataFrame(data1[i])
    data1[i] = data1[i].rename(
        columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    t2 = (datetime.now())
    t1 = (datetime.now() - timedelta(days=10))
    # print(t1)
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
    # print(t1)
    # print(t2)
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(dict3[i])+"/" + str(Slen)+"minute?from="+t1+"&to="+t2
    print(url2)
    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}

    res2 = requests.get(url2, headers=HEADERS)
    data2[i] = res2.json()
    data2[i] = data2[i]["data"]["candles"]
    data2[i] = pd.DataFrame(data2[i])
    data2[i] = data2[i].rename(
        columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    t2 = (datetime.now())
    t1 = (datetime.now() - timedelta(days=10))
    print(t1)
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
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(dict3[i])+"/" + str(Mlen)+"minute?from="+t1+"&to="+t2
    print(url2)
    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}

    res2 = requests.get(url2, headers=HEADERS)
    data3[i] = res2.json()
#     print(data3[i])
    data3[i] = data3[i]["data"]["candles"]
    data3[i] = pd.DataFrame(data3[i])
    data3[i] = data3[i].rename(
        columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})

# print(data2, "daaataaa")


TR1 = data1[0]['Time'].iloc[-1]
# print(T1)
Rhr1 = ['' for i in range(len(dict3))]
Rmin1 = ['' for i in range(len(dict3))]
Shr1 = ['' for i in range(len(dict3))]
Smin1 = ['' for i in range(len(dict3))]
Mhr1 = ['' for i in range(len(dict3))]
Mmin1 = ['' for i in range(len(dict3))]
TR1 = TR1.split('T')[1]
for i in range(len(dict3)):
    Rhr1[i] = int(TR1.split(':')[0])
    Rmin1[i] = int(TR1.split(':')[1])

TS1 = data2[0]['Time'].iloc[-1]
# print(TS1)
TS1 = TS1.split('T')[1]
for i in range(len(dict3)):
    Shr1[i] = int(TS1.split(':')[0])
    Smin1[i] = int(TS1.split(':')[1])

TM1 = data3[0]['Time'].iloc[-1]
# print(TS1)
TM1 = TM1.split('T')[1]
for i in range(len(dict3)):
    Mhr1[i] = int(TM1.split(':')[0])
    Mmin1[i] = int(TM1.split(':')[1])


niftitime, niftiltp = prevdata(256265, acc_key)
# print(niftiltp)
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


@api_view(['GET', 'POST'])
def papertrade(request):
    global papercapital
    print(request.data)
    # global trade_flag, trade_tokens, trade_name, pnl, size, trade_ltp, token1, token2,entry_val
    papercapital = 0
    # trade_tokens = [0 for i in range(4)]
    # trade_flag = [0 for i in range(4)]
    # trade_name = ['' for i in range(4)]
    # entry_val = [0 for i in range(4)]
    # pnl = [0 for i in range(4)]
    # size = [0 for i in range(4)]
    # trade_ltp = [0 for i in range(4)]
    # token1 = 0
    # token2 = 0

    papercapital = request.data['capital']
    print(papercapital, "feuh")
    sio.emit('paper', paperNames)

    return Response({"message": papercapital, "Names": paperNames})


class ImageCreateView(CreateAPIView):
    queryset = BackTest.objects.all()
    serializer_class = ImageSerializer

    def __init__(self):
        # self.df2_nifty_CE = pd.read_csv(
        #     "C:/Users/Dell/Desktop/quant-app/Server/app//acc_15min.csv")
        self.df1 = pd.read_csv(
            "app//SBIN_15_min.csv")
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
