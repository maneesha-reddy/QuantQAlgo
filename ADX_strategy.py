# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 11:52:15 2020

@author: HP
"""

import pandas as pd
from pandas import json_normalize
import numpy as np
import talib as ta
from beautifultable import BeautifulTable
from itertools import product
# import pymongo
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# mydb                            = myclient["SBIN_eq"]
# mycol                           = mydb["SBIN_15_minute"]
# start_date                      = 
# end_date                        = "2020-10-30 15:30:00"
class Financialdf1(object):
    def __init__(self, symbol, interval, start_date, end_date,timeperiod,diff):
        self.symbol                     = symbol
        self.interval                   = interval
        self.start_date                 = start_date
        self.end_date                   = end_date
        self.tf                        = timeperiod
        self.diff                      = diff
        # print(self.tf)
        self.fetch_df1()
        
    def fetch_df1(self):
        self.df1= pd.read_csv("SBIN_15_min.csv")
        # self.df1.set_index('Date', inplace = True)
        # self.df1.dropna(inplace = True)
        mask = (self.df1["Date"] > self.start_date) & (self.df1["Date"] <= self.end_date)
        # print(mask)
        self.df1 = self.df1.loc[mask]
        self.df1['PLUS_DI']                                         = ta.PLUS_DI(np.asarray(self.df1['high'], dtype='f8'), np.asarray(self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=self.tf)
        self.df1['MINUS_DI']                                        = ta.MINUS_DI(np.asarray(self.df1['high'], dtype='f8'), np.asarray(self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=self.tf)

        self.df1['ADX']                                             = ta.ADX(np.asarray(self.df1['high'], dtype='f8'), np.asarray(self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=self.tf)
        self.df1['macd'], self.df1['signal'], self.df1['macdhist']            = ta.MACD(np.asarray(self.df1['close'], dtype='f8'), fastperiod = 12 , slowperiod = 26, signalperiod = 9)
        self.df1['EMA_S']                                           = ta.EMA(np.asarray(self.df1['close'], dtype='f8'), timeperiod=self.tf-self.diff)
        self.df1['EMA_L']                                           = ta.EMA(np.asarray(self.df1['close'], dtype='f8'), timeperiod=self.tf+self.diff)
        self.df1['UPPERBAND'], self.df1['MIDDLEBAND'], self.df1['LOWERBAND']  = ta.BBANDS(np.asarray(self.df1['close'], dtype='f8'), timeperiod = self.tf+self.diff, nbdevup = 2, nbdevdn = 2, matype = 0)


             
# print(FD_df1.head())
# cursor                          = mycol.find({"trade_candle_type": "15minute", "stock_name": {'$in':['SBIN']}, 'trade_time': {'$lt': end_date, '$gte': start_date}})
# df                              = json_normalize(cursor)
# df1                             = df[["trade_time", "open", "high", "low","close" ,"volume", "stock_name"]]
# df1                             = df1.rename(columns = {'trade_time':'Date'})
# df1.to_csv('SBIN_15_min.csv')


#calculation of indicators.
class BacktestingBase(Financialdf1):
    def __init__(self, symbol, interval, start_date, end_date, sl_limit, tgt_limit,timeperiod,diff):
        super(BacktestingBase, self).__init__(symbol, interval, start_date, end_date,timeperiod,diff)
        self.symbol                     = symbol
        self.sl_limit                   = sl_limit
        self.tgt_limit                  = tgt_limit
        
        self.strategy()   
        self.backtest_results()
    def location_ohlcv(self,col, bar):
            self.col_val  = self.df1[col].loc[bar]
            return self.col_val
    def strategy(self):
        # some variables.
        no_of_trades               = []
        order                      = []
        buy_sell                   = []
        Entry_price                = []
        Exit_price                 = []
        profit                     = []
        mtm                        = []
           
        lot_size                   = 1300 
        pro                        = 0
        trade                      = 0
        buying_price               = 0
        selling_price              = 0

        # len_df1                    = self.df1["close"].size
        
        buy_flag                   = False
        sell_flag                  = True
        buy_flag1                  = False

        self.df1["Position"]            = 0
        # print(self.df1)
        len_df1                    = len(self.df1)
        # print(len_df1)
        stoploss                   = 0
        target                     = 0

        self.df1["ADX_COMP"]            = 0
        self.df1["EMA_COMP"]            = 0
        self.df1["MACD_COMP"]           = 0
        #df1.dropna(inplace = True)
        # print(self.df1.index)
        # for i in self.df1.index:
        for i in self.df1.index:
            # print(self.df1.index[0],i)
            # print(self.df1['PLUS_DI'].iloc[i],i)
            if (i > self.df1.index[0]) and (self.df1['PLUS_DI'].loc[i] > self.df1['MINUS_DI'].loc[i]) and (self.df1['ADX'].loc[i] > self.df1['MINUS_DI'].loc[i]) and (self.df1['ADX'].loc[i-1] < self.df1['MINUS_DI'].loc[i-1]):
                self.df1.loc[i, "ADX_COMP"]  = 1
                # print(self.df1.loc[i])
                # print(len(self.df1))
            else:
                self.df1.loc[i, "ADX_COMP"]  = 0
                # print(len(self.df1))
                
            if (i > 1) and (self.df1['EMA_S'].loc[i] > self.df1['EMA_L'].loc[i]) and (self.df1['EMA_S'].loc[i-1] < self.df1['EMA_L'].loc[i-1]):
                self.df1.loc[i, "EMA_COMP"]  = 1
                # print(len(self.df1))
            else:
                self.df1.loc[i, "EMA_COMP"]  = 0
                # print(len(self.df1))

            if (i > 1) and (self.df1['macd'].loc[i] > self.df1['signal'].loc[i]) and (self.df1['macd'].loc[i-1] < self.df1['signal'].loc[i-1]):
                self.df1.loc[i, "MACD_COMP"] = 1
                # print(len(self.df1))
            else:
                self.df1.loc[i, "MACD_COMP"] = 0
                # print(len(self.df1))
        
        k=1
        for x in self.df1.index:
            pro  = 0
            # print(x)
            if((self.df1['PLUS_DI'].loc[x] > self.df1['MINUS_DI'].loc[x]) and (self.df1['ADX'].loc[x] > self.df1['MINUS_DI'].loc[x]) and (self.df1['ADX'].loc[x-1] < self.df1['MINUS_DI'].loc[x-1]) or (1 in self.df1['ADX_COMP'].loc[x-7:x].values)) and ((self.df1['macd'].loc[x] > self.df1['signal'].loc[x]) and (self.df1['macd'].loc[x-1] < self.df1['signal'].loc[x-1]) or (1 in self.df1['MACD_COMP'].loc[x-5:x].values)) and ((self.df1['EMA_S'].loc[x] > self.df1['EMA_L'].loc[x]) and (self.df1['EMA_S'].loc[x-1] < self.df1['EMA_L'].loc[x-1]) or (1 in self.df1['EMA_COMP'].loc[x-5:x].values)) and (not buy_flag):
                trade              += 1
                buying_price       = self.df1['close'].loc[x]
                
                order.append(-1)
                # print(len(self.df1),-1)
                buy_sell.append("Buy")
                Entry_price.append(buying_price)
                Exit_price.append("")
                mtm.append("Position Taken")
                # print(self.df1["Position"][x+1])
                
                self.df1["Position"][x+1]     = 1
               
                buy_flag1          = True
                buy_flag           = True
                sell_flag          = False    

                
            elif(((self.location_ohlcv("close", x) - buying_price) * lot_size  <= -(self.sl_limit)) or ((self.location_ohlcv("close", x) - buying_price) * lot_size  >= self.tgt_limit) or (x > self.df1.index[0]) and ((self.df1['UPPERBAND'].loc[x-1] < self.df1['close'].loc[x-1]) and (self.df1['UPPERBAND'].loc[x] > self.df1['close'].loc[x]) and (self.df1['ADX'].loc[x] > self.df1['PLUS_DI'].loc[x])) or (self.df1['close'].loc[x] < (0.99 * buying_price))) and (not sell_flag):
                trade              += 1
                selling_price      = self.df1['close'].loc[x]
                pro                = selling_price - buying_price
                
                order.append(1)
                # print(len(self.df1),1)
                buy_sell.append("Sell")
                Entry_price.append("")
                Exit_price.append(selling_price)
                mtm.append("Position closed") 
                
                if buy_flag1 == True:
                    buy_flag1 = False
                buy_flag           = False
                sell_flag          = True
                
            else:
                if (buy_flag == True):
                    yy = (self.df1['close'].loc[x] - buying_price) * lot_size
                else:
                    yy = "0"

                order.append(0)
                # print(len(self.df1),0)
                buy_sell.append("No Trade")
                Entry_price.append("")
                Exit_price.append("")
                mtm.append(yy)
                
                if buy_flag1 == True:
                    self.df1["Position"][x]     = 1 
                    # print(self.df1["Position"][x+1])
                
            k=k+1  
            no_of_trades.append(trade)
            profit.append(pro)
        # print(len_df1,len(order))
        # print(len(self.df1))
        initial_capital            = 20000
        self.df1['Returns']             = np.log(self.df1["close"] / self.df1["close"].shift(1))
        self.df1['Strategy_Return']     = self.df1['Position'].shift(1) * self.df1['Returns']
        self.df1["placed_order"]        = order
        self.df1["buy_sell"]            = buy_sell
        self.df1["Entry"]               = Entry_price
        self.df1["Exit"]                = Exit_price
        self.df1['profit']              = profit
        self.df1['profit']              = (self.df1['profit']) * lot_size
        self.df1["mtm"]                 = mtm
        self.df1["cost"]                = (self.df1["placed_order"].multiply(self.df1["close"])) * lot_size
        self.df1["Account"]             = initial_capital + self.df1["cost"].cumsum()
        self.df1["Trades"]              = no_of_trades

        # df1.set_index('Date', inplace=True)

        risk_free_rate = 0.061/252
        self.sharpe = np.sqrt(252)*(np.mean(self.df1.Strategy_Return) - (risk_free_rate))/np.std(self.df1.Strategy_Return)

        cumulative_returns = self.df1.Strategy_Return.cumsum().iloc[-1]   
        period_in_days = len(self.df1.Strategy_Return)
        self.CAGR = 100*((cumulative_returns+1)**(252.0/period_in_days)-1)

        self.df1.dropna(inplace = True)
        cum_ret = self.df1.Strategy_Return.cumsum()

        peak = (np.maximum.accumulate(cum_ret) - cum_ret).idxmax() 
        trough = cum_ret[:peak].idxmax()
        self.drawdown =  (cum_ret[trough] - cum_ret[peak]) * 100
    def trade_log(self):
        self.buy_records                         = self.df1[self.df1["buy_sell"]=="Buy"]
        self.sell_records                        = self.df1[self.df1["buy_sell"]=="Sell"]


        self.trade_details                       = pd.DataFrame(0,index=range(len(self.buy_records)),
                                                                   columns=["Entry", "Date", \
                                                                            "Price", "Exit", \
                                                                                "ExDate", "ExPrice"])
                    
        self.trade_details["Entry"]              = self.buy_records["buy_sell"].values
        self.trade_details["Date"]               = self.buy_records.index.values # buy date
        self.trade_details["Price"]              = self.buy_records["close"].values # buy price
        self.trade_details["Exit"]               = self.sell_records["buy_sell"].values
        self.trade_details["ExDate"]             = self.sell_records.index.values# sell date
        self.trade_details["ExPrice"]            = self.sell_records["close"].values # sell price
        self.trade_details['% Change']           = (self.trade_details['ExPrice'] / self.trade_details['Price']) - 1
        self.trade_details['Profit']             = self.trade_details['ExPrice'] - self.trade_details['Price']
        self.trade_details['% Profit']           = (self.trade_details['ExPrice'] / self.trade_details['Price']) - 1
        self.trade_details['Position value']     = self.trade_details['Price']
        self.trade_details['Cumm Profit']        = self.trade_details['Profit'].cumsum()
        self.trade_details['MAE']                     = 0
        self.trade_details['MFE']                     = 0
        self.trade_details['Scale In / Scale Out']    = 0
        self.profit                                   = self.trade_details[self.trade_details["Profit"] >= 1]
        self.loss                                     = self.trade_details[self.trade_details["Profit"] <= -1]

    def backtest_results(self):
        self.trade_log()
        table = BeautifulTable()
        table.column_headers = ['PERFORMANCE METRICS', 'VALUES']
        table.append_row(["Trade start date", self.df1.index[0]])
        table.append_row(['Trade end date', self.df1.index[-1]])
        table.append_row(['Initial_Capital', self.df1["Account"].iloc[0]])
        table.append_row(['Ending_Capital', self.df1["Account"].iloc[-1]])
        table.append_row(['Total no trades', len(self.buy_records)])
        table.append_row(['Positive_trades', len(self.df1[self.df1["profit"] >= 1])])
        table.append_row(['Negative_trades', len(self.df1[self.df1["profit"] <= -1])])
        table.append_row(['Total_profit', self.df1[self.df1["profit"] >= 1]["profit"].sum()])
        table.append_row(['Total_loss', self.df1[self.df1["profit"] <= -1]["profit"].sum()])
        table.append_row(['Net Profit', self.df1["Account"].iloc[-1] - self.df1["Account"].iloc[0]])
        table.append_row(['Net Profit (%)', ((self.df1["Account"].iloc[-1] / self.df1["Account"].iloc[0]) - 1) * 100])
        table.append_row(['Avg. Profit / Loss', np.mean(self.profit["Profit"].values) / np.mean(self.loss["Profit"].values)])
        table.append_row(['Sharpe ratio', self.sharpe])
        table.append_row(['CAGR (%)', self.CAGR])
        table.append_row(['Maximum Drawdown (%)', self.drawdown])
        table.append_row(['CAGR / MDD (%)', self.CAGR / self.drawdown])
        table.set_style(BeautifulTable.STYLE_GRID)
        table.column_alignments['PERFORMANCE METRICS'] = BeautifulTable.ALIGN_LEFT
        table.column_alignments['VALUES'] = BeautifulTable.ALIGN_RIGHT
        table.left_padding_widths['VALUES'] = 10
        # print(table)
        return table,((self.df1["Account"].iloc[-1] / self.df1["Account"].iloc[0]) - 1) * 100
fd = BacktestingBase('NIFTY20JUN10000CE', 15, "2020-06-02 09:15:00", "2020-06-15 15:30:00", 350, 1775,8,2)
Df_CE = fd.df1

bt_report = fd.backtest_results()      
log_sheet = fd.trade_details 

sl_limit  = range(300, 451, 25)
tgt_limit = range(1100, 2400, 25)
# sl_limit  = range(300, 401, 25)
# tgt_limit = range(1800, 2400, 25)
pro=[]
ind=[]
time=range(14,26)
difference=range(2,12)              
# for i in range(14,21):
for s in product(time, difference):
    # print(s)
    fd = Financialdf1('NIFTY20JUN10000CE', 15, "2020-06-02 09:15:00", "2020-06-15 15:30:00",s[0],s[1])
    FD_df1  = fd.df1 
    fd = BacktestingBase('NIFTY20JUN10000CE', 15, "2020-06-02 09:15:00", "2020-06-15 15:30:00", 350, 1775,s[0],s[1])
    print(50 * '=')
    print(s[0],s[1])
    table,profit=fd.backtest_results()
    print(table)
    pro.append(profit)
    ind.append([s[0],s[1]])
minimum=max(pro)
index=pro.index(minimum)
print(minimum)
print(ind[index])
print(pro)
          
