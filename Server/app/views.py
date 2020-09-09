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


class ImageCreateView(CreateAPIView):
    queryset = BackTest.objects.all()
    serializer_class = ImageSerializer

    def __init__(self):
        self.df2_nifty_CE = pd.read_csv(
            "C:/Users/Dell/Desktop/quant-app/Server/app//acc_15min.csv")
        self.lot_size = 0
        self.request = ""

    def post(self, request):
        self.request = request
        x = {"hello": request.data["symbol"]}
        print(self.request.data["symbol"], "helllooo")
        self.lot_size = int(self.request.data["Quantity"])

        start_date = self.request.data["from_date"]
        date1 = start_date.split("T")
        d1 = date1[0].split("-")
        if d1[1][0] != "0" and d1[2][0] != "0":
            final1 = d1[1]+"/"+d1[2]+"/"+d1[0]
        elif d1[1][0] == "0" and d1[2][0] != "0":
            final1 = d1[1][1]+"/"+d1[2]+"/"+d1[0]
        elif d1[1][0] != "0" and d1[2][0] == "0":
            final1 = d1[1]+"/"+d1[2][1]+"/"+d1[0]
        else:
            final1 = d1[1][1]+"/"+d1[2][1]+"/"+d1[0]
        end_date = self.request.data["to_date"]
        date2 = end_date.split("T")
        d2 = date2[0].split("-")
        if d2[1][0] != "0" and d2[2][0] != "0":
            final2 = d2[1]+"/"+d2[2]+"/"+d2[0]
        elif d2[1][0] == "0" and d2[2][0] != "0":
            final2 = d2[1][1]+"/"+d2[2]+"/"+d2[0]
        elif d2[1][0] != "0" and d2[2][0] == "0":
            final2 = d2[1]+"/"+d2[2][1]+"/"+d2[0]
        else:
            final2 = d2[1][1]+"/"+d2[2][1]+"/"+d2[0]

        start_date = str(final1+" "+date1[1])
        end_date = str(final2+" "+date2[1])
        print(start_date, end_date)
        # start_date = "2/20/2020 10:15"
        # end_date = "5/20/2020 10:15"
        mask = (self.df2_nifty_CE['Date'] > start_date) & (
            self.df2_nifty_CE['Date'] <= end_date)
        # print(mask)
        self.df2_nifty_CE = self.df2_nifty_CE.loc[mask]
        print(self.df2_nifty_CE)
        no_of_trades = list()
        order = list()
        buy_sell = list()
        Entry_price = list()
        Exit_price = list()
        profit = list()
        mtm = list()

        # lot_size = 75  # quantity
        pro = 0
        trade = 0
        buying_price = 0
        selling_price = 0

        len_df = self.df2_nifty_CE["close"].size
        # len_df = 2324

        buy_flag = False
        sell_flag = True

        buy_flag1 = False

        date = ""
        prv_trade_date = ""

        self.df2_nifty_CE["Position"] = 0
        print(self.df2_nifty_CE)
        # print(location_index(1))
        # print(time_index(1, "9:45"))
        # print(location_index(2324) > time_index(2324, "9:45"))
        # print(prv_trade_date != today(2324))
        for x in self.df2_nifty_CE.index:
            pro = 0
            # print(x)

            if(self.location_index(x) > self.time_index(x, "9:45")) and (not buy_flag) and (prv_trade_date != self.today(x) or trade == 0):
                trade += 1
                buying_price = self.location_ohlcv("close", x)

                order.append(-1)
                buy_sell.append("Buy")
                Entry_price.append(buying_price)
                Exit_price.append("")
                mtm.append("Position Taken")
                self.df2_nifty_CE["Position"][x] = 1

                buy_flag1 = True
                buy_flag = True
                sell_flag = False

            elif(((self.location_ohlcv("close", x) - buying_price) * self.lot_size <= -500) or ((self.location_ohlcv("close", x) - buying_price) * self.lot_size >= 1500) or (self.location_index(x) >= self.time_index(x, "15:00:00"))) and (not sell_flag):
                date = str(self.df2_nifty_CE.index[x]).split(' ')
                prv_trade_date = date[0]
                pro = self.location_ohlcv("close", x) - buying_price
                trade += 1
                selling_price = self.location_ohlcv("close", x)

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
                    yy = (self.location_ohlcv("close", x) -
                          buying_price) * self.lot_size
                else:
                    yy = "0"

                order.append(0)
                buy_sell.append("No Trade")
                Entry_price.append("")
                Exit_price.append("")
                mtm.append(yy)

                if buy_flag1 == True:
                    self.df2_nifty_CE["Position"][x] = 1

            no_of_trades.append(trade)
            profit.append(pro)

        initial_capital = int(self.request.data["Initial_Capital"])
        self.df2_nifty_CE['Returns'] = np.log(
            self.df2_nifty_CE["close"] / self.df2_nifty_CE["close"].shift(1))
        self.df2_nifty_CE['Strategy_Return'] = self.df2_nifty_CE['Position'].shift(
            1) * self.df2_nifty_CE['Returns']
        self.df2_nifty_CE["placed_order"] = order
        self.df2_nifty_CE["buy_sell"] = buy_sell
        self.df2_nifty_CE["Entry"] = Entry_price
        self.df2_nifty_CE["Exit"] = Exit_price
        self.df2_nifty_CE['profit'] = profit
        self.df2_nifty_CE['profit'] = (
            self.df2_nifty_CE['profit']) * self.lot_size
        self.df2_nifty_CE["mtm"] = mtm
        self.df2_nifty_CE["cost"] = (self.df2_nifty_CE["placed_order"].multiply(
            self.df2_nifty_CE["close"])) * self.lot_size
        self.df2_nifty_CE["Account"] = initial_capital + \
            self.df2_nifty_CE["cost"].cumsum()
        self.df2_nifty_CE["Trades"] = no_of_trades

        risk_free_rate = 0.06/252
        if np.std(self.df2_nifty_CE.Strategy_Return) != 0:
            sharpe = np.sqrt(252)*(np.mean(self.df2_nifty_CE.Strategy_Return) -
                                   (risk_free_rate))/np.std(self.df2_nifty_CE.Strategy_Return)
        else:
            sharpe = "undefined"

        cumulative_returns = self.df2_nifty_CE.Strategy_Return.cumsum(
        ).iloc[-1]
        period_in_days = len(self.df2_nifty_CE.Strategy_Return)
        CAGR = 100*((cumulative_returns+1)**(252.0/period_in_days)-1)

        self.df2_nifty_CE.dropna(inplace=True)
        cum_ret = self.df2_nifty_CE.Strategy_Return.cumsum()

        peak = (np.maximum.accumulate(cum_ret) - cum_ret).idxmax()
        trough = cum_ret[:peak].idxmax()
        drawdown = (cum_ret[trough] - cum_ret[peak]) * 100

        buy_records = self.df2_nifty_CE[self.df2_nifty_CE["buy_sell"] == "Buy"]
        sell_records = self.df2_nifty_CE[self.df2_nifty_CE["buy_sell"] == "Sell"]

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
        output = {}

        profit = trade_details[trade_details["Profit"] >= 1]
        loss = trade_details[trade_details["Profit"] <= -1]

        # table = BeautifulTable()
        # table.column_headers = ['PERFORMANCE METRICS', 'VALUES']
        output["request"] = self.request.data["symbol"]
        print(request.data)
        # table.append_row(["Trade start date", self.df2_nifty_CE.index[0]])
        output["Trade start date"] = self.df2_nifty_CE.index[0]
        # table.append_row(['Trade end date', self.df2_nifty_CE.index[-1]])
        output['Trade end date'] = self.df2_nifty_CE.index[-1]
        # table.append_row(
        #     ['Initial_Capital', self.df2_nifty_CE["Account"].iloc[0]])
        output['Initial_Capital'] = self.df2_nifty_CE["Account"].iloc[0]
        # table.append_row(
        #     ['Ending_Capital', self.df2_nifty_CE["Account"].iloc[-1]])
        output['Ending_Capital'] = self.df2_nifty_CE["Account"].iloc[-1]
        # table.append_row(['Total no trades', len(buy_records)])
        output['Total no trades'] = len(buy_records)
        # table.append_row(['Positive_trades', len(
        #     self.df2_nifty_CE[self.df2_nifty_CE["profit"] >= 1])])
        output['Positive_trades'] = len(
            self.df2_nifty_CE[self.df2_nifty_CE["profit"] >= 1])
        # table.append_row(['Negative_trades', len(
        #     self.df2_nifty_CE[self.df2_nifty_CE["profit"] <= -1])])
        output['Negative_trades'] = len(
            self.df2_nifty_CE[self.df2_nifty_CE["profit"] <= -1])
        # table.append_row(
        #     ['Total_profit', self.df2_nifty_CE[self.df2_nifty_CE["profit"] >= 1]["profit"].sum()])
        output['Negative_trades'] = self.df2_nifty_CE[self.df2_nifty_CE["profit"]
                                                      >= 1]["profit"].sum()
        # table.append_row(
        #     ['Total_loss', self.df2_nifty_CE[self.df2_nifty_CE["profit"] <= -1]["profit"].sum()])
        output['Total_loss'] = self.df2_nifty_CE[self.df2_nifty_CE["profit"]
                                                 <= -1]["profit"].sum()
        # table.append_row(
        #     ['Net Profit', self.df2_nifty_CE["Account"].iloc[-1] - self.df2_nifty_CE["Account"].iloc[0]])
        output['Net Profit'] = self.df2_nifty_CE["Account"].iloc[-1] - \
            self.df2_nifty_CE["Account"].iloc[0]
        # table.append_row(['Net Profit (%)', ((
        #     self.df2_nifty_CE["Account"].iloc[-1] / self.df2_nifty_CE["Account"].iloc[0]) - 1) * 100])
        output['Net Profit (%)'] = (self.df2_nifty_CE["Account"].iloc[-1] /
                                    (self.df2_nifty_CE["Account"].iloc[0]) - 1) * 100
        # table.append_row(['Avg. Profit / Loss',
        #                   np.mean(profit["Profit"].values) / np.mean(loss["Profit"].values)])
        # output['Avg. Profit / Loss'] = np.mean(
        #     profit["Profit"].values) / np.mean(loss["Profit"].values)
        # table.append_row(['Sharpe ratio', sharpe])
        output['Sharpe ratio'] = sharpe
        # table.append_row(['CAGR (%)', CAGR])
        output['CAGR (%)'] = CAGR
        # table.append_row(['Maximum Drawdown (%)', drawdown])
        output['Maximum Drawdown (%)'] = drawdown
        # table.append_row(['CAGR / MDD (%)', CAGR / drawdown])
        # output['CAGR / MDD (%)'] = CAGR / drawdown
        # table.set_style(BeautifulTable.STYLE_GRID)
        # table.column_alignments['PERFORMANCE METRICS'] = BeautifulTable.ALIGN_LEFT
        # table.column_alignments['VALUES'] = BeautifulTable.ALIGN_RIGHT
        # table.left_padding_widths['VALUES'] = 10
        print(output)
        # x = {"hello": "123"}
        return Response(output)

        # return Response(x)
        # print(self.request.data, "request")

    def location_index(self, bar):
        # id_loc = self.df2_nifty_CE.index[bar]
        id_loc = self.df2_nifty_CE['Date'][bar]
        return id_loc

    def time_index(self, bar, time):
        # today_date = str(df2_nifty_CE.index[bar]).split(' ')
        today_date = str(self.df2_nifty_CE['Date'][bar]).split(' ')
        today_date_time = today_date[0] + " " + time  # "09:45:00"
        return today_date_time

    def location_ohlcv(self, col, bar):
        # col_val = self.df2_nifty_CE[col].iloc[bar]
        col_val = self.df2_nifty_CE[col][bar]
        return col_val

    def today(self, bar):
        # today = str(df2_nifty_CE.index[bar]).split(' ')
        today = str(self.df2_nifty_CE['Date'][bar]).split(' ')
        today_date = today[0]
        return today_date
