# Script to parser Tester Logs from CommunityPower EA
#
# Install Python 3.10.x
#
# Install module:
# pip install pandas
# pip install openpyxl
#
#
#
import sys
import csv
import codecs
import re
from datetime import datetime
import time
import os
from os.path import expanduser

import pandas as pd
import getopt

#Contar la cantidad de Trades al final
#Results with less trades might be overfitted.
#You need at least 200 trades to make statistically significant conclusions
#
# CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DATA_FOLDER = "9EB2973C469D24060397BB5158EA73A5"
# CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#WARNING
#
#Do not use the # character as a comment in EA Config Parameter
#
# LOG FILE
args = sys.argv[1:]
if len(args) == 2 and args[0] == '-mt5_visual_mode_checked':
    if args[1] == 'off':
        LogDirectory = expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\Logs"
    if args[1] == 'on':
        LogDirectory=expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Tester\\" + DATA_FOLDER + "\\Agent-127.0.0.1-3000\\Logs"
    else:
        LogDirectory = expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\Logs"
else:
    # MT5 change this:
    # LogDirectory = expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\Logs"
    LogDirectory=expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Tester\\" + DATA_FOLDER + "\\Agent-127.0.0.1-3000\\Logs"

now = datetime.now()
LogToday = now.strftime('%Y%m%d') + ".log"
#LogToday="20220531.log"
LogFile = os.path.join(LogDirectory, LogToday)
if not (os.path.isfile(LogFile)):
    print(f"File Not Found : {LogFile}")
    exit()

print("Reading file...")
print(LogFile)


# HEADER CSV
csv_columns = ['Time','Action','Type','Martingale','Signal','Symbol','Volume','PriceAction','NewValue','Profit','Slippage','Value1','Value2','StopLoss','TakeProfit','Expiration','Comment','MagicID','Status','Ticket #']
csv_row = [{}]
file_uniqe = datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S')
csv_file = file_uniqe + ".csv"
excel_file = file_uniqe + ".xlsx"

# Flags Initialization
flag_Signal = 0
flag_Signal2 = 0
flag_Signal3 = 0
flag_Signal4 = 0
flag_Signal5 = 0
flag_Signal6 = 0
flag_Signal7 = 0
flag_OrderSend = 0
flag_OrderClose = 0
flag_OrderModify = 0
flag_OrderModify2 = 0
flag_OrderDelete = 0
flag_TrailingStop = 0
flag_Sum_TakeProfit = 0
flag_Modifying = 0
flag_Moving = 0
flag_position_modified = 0
flag_position_modified2 = 0
flag_order_modified = 0
flag_order_canceled = 0
flag_stop_loss_triggered = 0
flag_stop_loss_triggered2 = 0
flag_market = 0
flag_market2 = 0
flag_buy_sell_stop = 0
flag_Global_TakeProfit = 0
flag_Partial_close = 0
flag_Partial_close2 = 0
flag_Partial_close3 = 0
flag_Slippages = 0
# Variables Clean
SignalRow = ()
SignalRow2 = ()
SignalRow3 = ()
SignalRow4 = ()
SignalRow5 = ()
SignalRow6 = ()
SignalRow7 = ()
SignalRow8 = ()
OrderSendRow = ()
OrderCloseRow = ()
OrderModifyRow = ()
OrderModifyRow2 = ()
OrderDeleteRow = ()
TrailingStopRow = ()
Sum_TakeProfitRow = ()
ModifyingRow = ()
MovingRow = ()
position_modifiedRow = ()
position_modifiedRow2 = ()
order_modifiedRow = ()
order_canceledRow = ()
stop_loss_triggeredRow = ()
stop_loss_triggeredRow2 = ()
marketRow = ()
marketRow2 = ()
buy_sell_stopRow = ()
Global_TakeProfitRow = ()
calculate_profitRow = ()
Partial_closeRow = ()
Partial_closeRow2 = ()
Partial_closeRow3 = ()
SlippagesRow = ()
close_order = 0
close_order2 = 0
close_order3 = 0
# Variables Clean ERROR
count_OrderModify = 0
flag_Magic = 0

# Iterate Log
for line in csv.reader(codecs.open(LogFile, 'rU',  'utf-16'), delimiter="\t"):

    if not (len(line) >= 4):
        continue

    # print(', '.join(line))
    linea = line[4]
    # print(linea)
    # linea = line[4]
    # ticks synchronization started


    # calculate profit in pips, initial deposit 10000, leverage 1:2000
    calculate_profitRegex = re.compile(r'calculate profit in pips, initial deposit ([0-9]+), leverage ([0-9]*[:]?[0-9]*)')
    calculate_profitMatch = calculate_profitRegex.search(linea)
    if calculate_profitMatch is not None:
        flag_Magic = 0
        # print(calculate_profitMatch.groups())
        calculate_profitRow = calculate_profitMatch.groups() + ("calculate_profitRow",)

    # Overwrite si existe este valor
    # initial deposit 500.00 USD, leverage 1:500
    calculate_profitRegex = re.compile(r'initial deposit ([0-9]*[.]?[0-9]*) ([A-Z]+), leverage ([0-9]*[:]?[0-9]*)')
    calculate_profitMatch = calculate_profitRegex.search(linea)
    if calculate_profitMatch is not None:
        flag_Magic = 0
        # print(calculate_profitMatch.groups())
        calculate_profitRow = (calculate_profitMatch.group(1),) + (calculate_profitMatch.group(3),) + ("calculate_profitRow",)


    fecha = linea.split(" ")[0]
    # print(fecha)
    match = re.search(r'^\d{4}\.\d{2}\.\d{2}', fecha)
    if match is not None:
        year = fecha.split(".")[0]
        # print(year)
        if (int(year) >= 2000):
            mensaje = linea.split("   ")[1]
            # print (mensaje)

            if not flag_Magic:
                # 2019.01.01 00:00:00   Magic v2020.07.22 launched...
                MagicRegex = re.compile(r'Magic v([0-9]*[.][0-9]*[.][0-9]*) launched...')
                MagicMatch = MagicRegex.search(mensaje)
                if MagicMatch is not None:
                    # print(MagicMatch.groups())
                    flag_Magic = 1
                    MagicRow = (linea.split("   ")[0],) + ("MagicRow",)
                    # print(MagicRow)
                    csv_row.append({'Time': MagicRow[0],'Action': f'Initial Deposit {calculate_profitRow[0]} - leverage {calculate_profitRow[1]}'})

                    # Flags Initialization
                    flag_Signal = 0
                    flag_Signal2 = 0
                    flag_Signal3 = 0
                    flag_Signal4 = 0
                    flag_Signal5 = 0
                    flag_Signal6 = 0
                    flag_Signal7 = 0
                    flag_OrderSend = 0
                    flag_OrderClose = 0
                    flag_OrderModify = 0
                    flag_OrderModify2 = 0
                    flag_OrderDelete = 0
                    flag_TrailingStop = 0
                    flag_Sum_TakeProfit = 0
                    flag_Modifying = 0
                    flag_Moving = 0
                    flag_position_modified = 0
                    flag_position_modified2 = 0
                    flag_order_modified = 0
                    flag_order_canceled = 0
                    flag_stop_loss_triggered = 0
                    flag_stop_loss_triggered2 = 0
                    flag_market = 0
                    flag_market2 = 0
                    flag_buy_sell_stop = 0
                    flag_Global_TakeProfit = 0
                    flag_Partial_close = 0
                    flag_Partial_close2 = 0
                    flag_Partial_close3 = 0
                    flag_Slippages = 0
                    # Variables Clean
                    SignalRow = ()
                    SignalRow2 = ()
                    SignalRow3 = ()
                    SignalRow4 = ()
                    SignalRow5 = ()
                    SignalRow6 = ()
                    SignalRow7 = ()
                    OrderSendRow = ()
                    OrderCloseRow = ()
                    OrderModifyRow = ()
                    OrderModifyRow2 = ()
                    OrderDeleteRow = ()
                    TrailingStopRow = ()
                    Sum_TakeProfitRow = ()
                    ModifyingRow = ()
                    MovingRow = ()
                    position_modifiedRow = ()
                    position_modifiedRow2 = ()
                    order_modifiedRow = ()
                    order_canceledRow = ()
                    stop_loss_triggeredRow = ()
                    stop_loss_triggeredRow2 = ()
                    marketRow = ()
                    marketRow2 = ()
                    buy_sell_stopRow = ()
                    Global_TakeProfitRow = ()
                    calculate_profitRow = ()
                    Partial_closeRow = ()
                    Partial_closeRow2 = ()
                    Partial_closeRow3 = ()
                    SlippagesRow = ()
                    close_order = 0
                    close_order2 = 0
                    # Variables Clean ERROR
                    count_OrderModify = 0


            # --------------------------------------------------------------------------------------------
            # SIGNAL BEGIN
            # --------------------------------------------------------------------------------------------
            # Signal to open buy #1 at 1490.790 (BigCandle + IdentifyTrend + TDI)!
            # Signal to open sell #1 at 1.14156 (Stochastic K + IdentifyTrend + TDI)!
            SignalRegex = re.compile(r'Signal to (open|close) (buy|sell) \#([0-9]+) at ([0-9]*[.]?[0-9]*) \(([a-zA-Z+ ]+)\)!')
            SignalMatch = SignalRegex.search(mensaje)
            if SignalMatch is not None:
                # print(SignalMatch.groups())
                flag_Signal = 1
                SignalRow = (linea.split("   ")[0],) + SignalMatch.groups() + ("SignalRow",)
                # print(SignalRow)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit =0

            # Signal to open buy #2 at 1885.770!
            SignalRegex2 = re.compile(r'Signal to (open|close) (buy|sell) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch2 = SignalRegex2.search(mensaje)
            if SignalMatch2 is not None:
                # print(SignalMatch.groups())
                flag_Signal2 = 1
                SignalRow2 = (linea.split("   ")[0],) + SignalMatch2.groups() + ("SignalRow2",)
                # print(SignalRow2)
                flag_Signal = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0

            # Signal to close sell (FIBO )!
            # Signal to close sell (Stochastic K)!
            SignalRegex3 = re.compile(r'Signal to (open|close) (buy|sell) \(([a-zA-Z+ ]+)\)!')
            SignalMatch3 = SignalRegex3.search(mensaje)
            if SignalMatch3 is not None:
                # print(SignalMatch3.groups())
                flag_Signal3 = 1
                SignalRow3 = (linea.split("   ")[0],) + SignalMatch3.groups() + ("SignalRow3",)
                # print(SignalRow3)
                flag_Signal2 = flag_Signal = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0

            # Signal to open AutoHedge for buy-order #6 at 1.14407!
            SignalRegex4 = re.compile(r'Signal to (open|close) AutoHedge for (buy\-order|sell\-order) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch4 = SignalRegex4.search(mensaje)
            if SignalMatch4 is not None:
                # print(SignalMatch4.groups())
                flag_Signal4 = 1
                SignalRow4 = (linea.split("   ")[0],) + SignalMatch4.groups() + ("SignalRow4",)
                # print(SignalRow4)
                flag_Signal2 = flag_Signal3 = flag_Signal = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0

            # Signal to open anti-martingale buy #2 at 1.22464!
            SignalRegex5 = re.compile(r'Signal to (open|close) anti-martingale (buy|sell) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch5 = SignalRegex5.search(mensaje)
            if SignalMatch5 is not None:
                # print(SignalMatch5.groups())
                flag_Signal5 = 1
                SignalRow5 = (linea.split("   ")[0],) + SignalMatch5.groups() + ("SignalRow5",)
                # print(SignalRow5)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0

            #Signal to close buy (BreakEven after order #4 reached: Bid = 1.18534, op = 1.18524, MinProfit = 1.0)!
            #Signal to close sell (BreakEven after order #3 reached: Ask = 1.20893, op = 1.20904, MinProfit = 1.0)!
            SignalRegex6 = re.compile(r'Signal to (open|close) (buy|sell) \(BreakEven after order \#([0-9]+) reached: ([a-zA-Z]+) = ([0-9]*[.]?[0-9]*), op = ([0-9]*[.]?[0-9]*), MinProfit = ([0-9]*[.]?[0-9]*)\)!')
            SignalMatch6 = SignalRegex6.search(mensaje)
            if SignalMatch6 is not None:
                # print(SignalMatch6.groups())
                flag_Signal6 = 1
                SignalRow6 = (linea.split("   ")[0],) + SignalMatch6.groups() + ("SignalRow6",)
                # print(SignalRow6)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0

            #Signal to open AutoHedge for buy-order #1!
            SignalRegex7 = re.compile(r'Signal to (open|close) AutoHedge for (buy\-order|sell\-order) \#([0-9]+)!')
            SignalMatch7 = SignalRegex7.search(mensaje)
            if SignalMatch7 is not None:
                # print(SignalMatch7.groups())
                flag_Signal7 = 1
                SignalRow7 = (linea.split("   ")[0],) + SignalMatch7.groups() + ("SignalRow7",)
                # print(SignalRow7)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal8 = flag_Signal = flag_Sum_TakeProfit = 0

            # Signal to delete pending buy-order (indicator)!
            SignalRegex8 = re.compile(r'Signal to delete pending (buy|sell)\-order \(indicator\)!')
            SignalMatch8 = SignalRegex8.search(mensaje)
            if SignalMatch8 is not None:
                # print(SignalMatch8.groups())
                flag_Signal8 = 1
                SignalRow8 = (linea.split("   ")[0],) + SignalMatch8.groups() + ("SignalRow8",)
                # print(SignalRow8)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal = flag_Sum_TakeProfit = 0

            # order canceled [#15 buy stop 1 EURUSD at 1.14479]
            # |  OrderDelete( 15 ) - OK!

            # --------------------------------------------------------------------------------------------
            # SIGNAL END
            # --------------------------------------------------------------------------------------------


            # TrailingStop for BUY: 0 -> 1920.37
            TrailingStopRegex = re.compile(r'TrailingStop for (BUY|SELL): ([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)')
            TrailingStopMatch = TrailingStopRegex.search(mensaje)
            if TrailingStopMatch is not None:
                # print(TrailingStopMatch.groups())
                flag_TrailingStop = 1
                TrailingStopRow = (linea.split("   ")[0],) + TrailingStopMatch.groups() + ("TrailingStopRow",)
                # print(TrailingStopRow)

            # Modifying TP for buy-order #18: 2154.566 -> 2175.994...
            # Modifying SL for sell-order #86: 0.00000 -> 1.17551...
            ModifyingRegex = re.compile(r'Modifying (TP|SL) for (buy\-order|sell\-order) \#([0-9]+): ([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)...')
            ModifyingMatch = ModifyingRegex.search(mensaje)
            if ModifyingMatch is not None:
                # print(ModifyingMatch.groups())
                flag_Modifying = 1
                ModifyingRow = (linea.split("   ")[0],) + ModifyingMatch.groups() + ("ModifyingRow",)
                # print(ModifyingRow)

            # position modified [#18 buy 0.99 XAUUSD 1856.780 tp: 2175.994]
            # position modified [#27 sell 1.7 EURUSDm# 1.11919 tp: 1.11375]
            position_modifiedRegex = re.compile(r'position modified \[\#([0-9]+) (buy|sell) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) tp: ([0-9]*[.]?[0-9]*)\]')
            position_modifiedMatch = position_modifiedRegex.search(mensaje)
            if position_modifiedMatch is not None:
                # print(position_modifiedMatch.groups())
                flag_position_modified = 1
                position_modifiedRow = (linea.split("   ")[0],) + position_modifiedMatch.groups() + ("position_modifiedRow",)
                # print(position_modifiedRow)

            # position modified [#7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326]
            position_modifiedRegex2 = re.compile(r'position modified \[\#([0-9]+) (buy|sell) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) sl: ([0-9]*[.]?[0-9]*) tp: ([0-9]*[.]?[0-9]*)\]')
            position_modifiedMatch2 = position_modifiedRegex2.search(mensaje)
            if position_modifiedMatch2 is not None:
                # print(position_modifiedMatch2.groups())
                flag_position_modified2 = 1
                position_modifiedRow2 = (linea.split("   ")[0],) + position_modifiedMatch2.groups() + ("position_modifiedRow2",)
                # print(position_modifiedRow2)

            # order modified [#10 buy stop 1.01 EURUSD at 1.15179]
            order_modifiedRegex = re.compile(r'order modified \[\#([0-9]+) (buy|sell) stop ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*)\]')
            order_modifiedMatch = order_modifiedRegex.search(mensaje)
            if order_modifiedMatch is not None:
                # print(order_modifiedMatch.groups())
                flag_order_modified = 1
                order_modifiedRow = (linea.split("   ")[0],) + order_modifiedMatch.groups() + ("order_modifiedRow",)
                # print(order_modifiedRow)

            # order canceled [#2 buy stop 0.1 EURUSD at 1.13532]
            order_canceledRegex = re.compile(r'order canceled \[\#([0-9]+) (buy|sell) stop ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*)\]')
            order_canceledMatch = order_canceledRegex.search(mensaje)
            if order_canceledMatch is not None:
                # print(order_canceledMatch.groups())
                flag_order_canceled = 1
                order_canceledRow = (linea.split("   ")[0],) + order_canceledMatch.groups() + ("order_canceledRow",)
                # print(order_canceledRow)

            # buy stop 1 EURUSD at 1.14301 (1.14029 / 1.14034)
            # sell stop 1 EURUSD at 1.13248 (1.13415 / 1.13420)
            buy_sell_stopRegex = re.compile(r'(buy|sell) stop ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            buy_sell_stopMatch = buy_sell_stopRegex.search(mensaje)
            if buy_sell_stopMatch is not None:
                # print(buy_sell_stopMatch.groups())
                flag_buy_sell_stop = 1
                buy_sell_stopRow = (linea.split("   ")[0],) + buy_sell_stopMatch.groups() + ("buy_sell_stopRow",)
                # print(buy_sell_stopRow)

            # |  OrderSend( EURUSD, buy stop, 0.1, 1.13538, 50, 0.00000, 0.00000, "CP #1", 3040 ) - OK! Ticket #3.
            # |  OrderSend( XAUUSD, buy, 0.10, 1592.750, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
            OrderSendRegex = re.compile(r'\|  OrderSend\( ([a-zA-Z\#\.]+), (buy|sell|buy stop|sell stop), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), \"([a-zA-Z0-9\.\#:\- ]+)\", ([0-9]*) \) - ([a-zA-Z\!]+)! Ticket \#([0-9]*).')
            OrderSendMatch = OrderSendRegex.search(mensaje)
            if OrderSendMatch is not None:
                # print(OrderSendMatch.groups())
                flag_OrderSend = 1
                OrderSendRow = (linea.split("   ")[0],) + OrderSendMatch.groups() + ("OrderSendRow",)
                # print(OrderSendRow)
                # https://docs.mql4.com/trading/ordersend

            # Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
            # Moving sell-stop order #3 to the new level (1.13281 -> 1.13286)...
            MovingRegex = re.compile(r'Moving (buy\-stop|sell\-stop) order \#([0-9]+) to the new level \(([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)\)...')
            MovingMatch = MovingRegex.search(mensaje)
            if MovingMatch is not None:
                # print(MovingMatch.groups())
                flag_Moving = 1
                MovingRow = (linea.split("   ")[0],) + MovingMatch.groups() + ("MovingRow",)
                # print(MovingRow)

            # PENDING TO DO
            # |  OrderSend( XAUUSD, buy stop, 0.10, 1501.680, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - ERROR #10018 (Market is closed)!

            # PENDING TO DO
            # Signal to open buy #6 at 1.09278 (BigCandle)!
            #  Not enough money to open 16.40 lots EURUSDm#! 

            # PENDING TO DO
            # Signal to open sell #6 at 1.09220!
            # Alert:  Not enough money to open 0.07 lots EURUSD! 

            # PENDING TO DO
            #Signal to open sell #1 at 1.16428 (Stochastic K + IdentifyTrend + FIBO )!
            #Alert: Can't calculate lot for SELL (RiskOnSL): OP = 1.16428, SL = 0.00000!


            # market buy 0.1 XAUUSD (1934.050 / 1935.010)
            marketRegex = re.compile(r'market (buy|sell) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch = marketRegex.search(mensaje)
            if marketRegexMatch is not None:
                # print(marketRegexMatch.groups())
                flag_market = 1
                marketRow = (linea.split("   ")[0],) + marketRegexMatch.groups() + ("marketRow",)
                # print(marketRow)

            # market buy 0.1 EURUSD, close #10 (1.13411 / 1.13414)
            marketRegex2 = re.compile(r'market (buy|sell) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+), ([a-z]+) \#([0-9]*) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch2 = marketRegex2.search(mensaje)
            if marketRegexMatch2 is not None:
                # print(marketRegexMatch2.groups())
                flag_market2 = 1
                marketRow2 = (linea.split("   ")[0],) + marketRegexMatch2.groups() + ("marketRow2",)
                # print(marketRow2)


            # https://docs.mql4.com/trading/orderclose
            # |  OrderClose( 272, 1.48, 1.06957, 50 ) - OK!
            OrderCloseRegex = re.compile(r'\|  OrderClose\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*) \) - ([A-Z]+)!')
            OrderCloseMatch = OrderCloseRegex.search(mensaje)
            if OrderCloseMatch is not None:
                # print(OrderCloseMatch.groups())
                flag_OrderClose = 1
                OrderCloseRow = (linea.split("   ")[0],) + OrderCloseMatch.groups() + ("OrderCloseRow",)
                # print(OrderCloseRow)

            # https://docs.mql4.com/trading/ordermodify
            # |  OrderModify( 18, 1856.780, 0.000, 2175.994 ) - OK!
            # |  OrderModify( 86, 1.14135, 1.17551, 0.00000 ) - OK!
            OrderModifyRegex = re.compile(r'\|  OrderModify\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*) \) - ([A-Z]+)!')
            OrderModifyMatch = OrderModifyRegex.search(mensaje)
            if OrderModifyMatch is not None:
                # print(OrderModifyMatch.groups())
                flag_OrderModify = 1
                OrderModifyRow = (linea.split("   ")[0],) + OrderModifyMatch.groups() + ("OrderModifyRow",)
                # print(OrderModifyRow)

            # https://docs.mql4.com/trading/orderdelete
            # |  OrderDelete( 15 ) - OK!
            OrderDeleteRegex = re.compile(r'\|  OrderDelete\( ([0-9]+) \) - ([A-Z]+)!')
            OrderDeleteMatch = OrderDeleteRegex.search(mensaje)
            if OrderDeleteMatch is not None:
                # print(OrderDeleteMatch.groups())
                flag_OrderDelete = 1
                OrderDeleteRow = (linea.split("   ")[0],) + OrderDeleteMatch.groups() + ("OrderDeleteRow",)
                # print(OrderDeleteRow)


            # PENDING TO DO
            # ERROR ONLY. Use only to count
            # |  OrderModify( 743, 1.10723, 0.00000, 1.10993 ) - ERROR #10018 (Market is closed)!

            # stop loss triggered #7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326 [#8 buy 1 XAUUSD at 1881.920]
            stop_loss_triggeredRegex = re.compile(r'stop loss triggered \#([0-9]*) (buy|sell) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) sl: ([0-9]*[.]?[0-9]*) tp: ([0-9]*[.]?[0-9]*) \[\#([0-9]*) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*)\]')
            stop_loss_triggeredRegexMatch = stop_loss_triggeredRegex.search(mensaje)
            if stop_loss_triggeredRegexMatch is not None:
                # print(stop_loss_triggeredRegexMatch.groups())
                flag_stop_loss_triggered = 1
                stop_loss_triggeredRow = (linea.split("   ")[0],) + stop_loss_triggeredRegexMatch.groups() + ("stop_loss_triggeredRow",)
                # print(stop_loss_triggeredRow)

            # stop loss triggered #3 sell 0.1 EURUSD 1.13731 sl: 1.13475 [#4 buy 0.1 EURUSD at 1.13475]
            stop_loss_triggeredRegex2 = re.compile(r'stop loss triggered \#([0-9]*) (buy|sell) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) sl: ([0-9]*[.]?[0-9]*) \[\#([0-9]*) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*)\]')
            stop_loss_triggeredRegexMatch2 = stop_loss_triggeredRegex2.search(mensaje)
            if stop_loss_triggeredRegexMatch2 is not None:
                # print(stop_loss_triggeredRegexMatch2.groups())
                flag_stop_loss_triggered2 = 1
                stop_loss_triggeredRow2 = (linea.split("   ")[0],) + stop_loss_triggeredRegexMatch2.groups() + ("stop_loss_triggeredRow2",)
                # print(stop_loss_triggeredRow2)


            #FALTA COMPROBAR SI ANDA. PENDING TO DO
            # Global TakeProfit (1.0%) has been reached ($111.64 >= $100.00)
            Global_TakeProfitRegex = re.compile(r'Global TakeProfit \(([0-9]*[.]?[0-9]*)\%\) has been reached \(\$([0-9]*[.]?[0-9]*) >= \$([0-9]*[.]?[0-9]*)\)')
            Global_TakeProfitRegexMatch = Global_TakeProfitRegex.search(mensaje)
            if Global_TakeProfitRegexMatch is not None:
                # print(Global_TakeProfitRegexMatch.groups())
                flag_Global_TakeProfit = 1
                Global_TakeProfitRow = (linea.split("   ")[0],) + Global_TakeProfitRegexMatch.groups() + ("Global_TakeProfitRow",)
                # print(Global_TakeProfitRow)


            #FALTA COMPROBAR SI ANDA. PENDING TO DO
            #Global Account TakeProfit has been reached ($10.93 >= $10.00)!
            Global_AccountRegex = re.compile(r'Global Account TakeProfit has been reached \(\$([0-9]*[.]?[0-9]*) >= \$([0-9]*[.]?[0-9]*)\)!')
            Global_AccountRegexMatch = Global_AccountRegex.search(mensaje)
            if Global_AccountRegexMatch is not None:
                # print(Global_AccountRegexMatch.groups())
                flag_Global_Account = 1
                Global_AccountRow = (linea.split("   ")[0],) + Global_AccountRegexMatch.groups() + ("Global_AccountRow",)
                # print(Global_AccountRow)


            # ClosePartialHedge_20210727.log
            #Partial close hedge: closing 1 profit order ($+76.85) + 1 opposite loss order ($-75.77) with total profit $+1.08!
            Partial_closeRegex = re.compile(r'Partial close hedge: closing ([0-9]+) profit order \(\$([\+\-0-9]*[.]?[0-9]*)\) \+ ([0-9]+) opposite loss order \(\$([\+\-0-9]*[.]?[0-9]*)\) with total profit \$([\+\-0-9]*[.]?[0-9]*)!')
            Partial_closeRegexMatch = Partial_closeRegex.search(mensaje)
            if Partial_closeRegexMatch is not None:
                # print(Partial_closeRegexMatch.groups())
                flag_Partial_close = 1
                Partial_closeRow = (linea.split("   ")[0],) + Partial_closeRegexMatch.groups() + ("Partial_closeRow",)
                # print(Partial_closeRow)
                # Reset all signal
                flag_Signal = flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0


            #Partial close any: closing 2 profit orders ($+266.05) + 1 loss order ($-166.00) with total profit $+100.05!
            Partial_closeRegex2 = re.compile(r'Partial close any: closing ([0-9]+) profit orders \(\$([\+\-0-9]*[.]?[0-9]*)\) \+ ([0-9]+) loss order \(\$([\+\-0-9]*[.]?[0-9]*)\) with total profit \$([\+\-0-9]*[.]?[0-9]*)!')
            Partial_closeRegexMatch2 = Partial_closeRegex2.search(mensaje)
            if Partial_closeRegexMatch2 is not None:
                # print(Partial_closeRegexMatch2.groups())
                flag_Partial_close2 = 1
                Partial_closeRow2 = (linea.split("   ")[0],) + Partial_closeRegexMatch2.groups() + ("Partial_closeRow2",)
                # print(Partial_closeRow2)
                # Reset all signal
                flag_Signal = flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0


            #Partial close for SELL-series: closing 3 profit orders ($+110.17) + 1 loss order ($-104.10) with total profit $+6.07!
            Partial_closeRegex3 = re.compile(r'Partial close for (BUY|SELL)-series: closing ([0-9]+) profit orders \(\$([\+\-0-9]*[.]?[0-9]*)\) \+ ([0-9]+) loss order \(\$([\+\-0-9]*[.]?[0-9]*)\) with total profit \$([\+\-0-9]*[.]?[0-9]*)!')
            Partial_closeRegexMatch3 = Partial_closeRegex3.search(mensaje)
            if Partial_closeRegexMatch3 is not None:
                # print(Partial_closeRegexMatch3.groups())
                flag_Partial_close3 = 1
                Partial_closeRow3 = (linea.split("   ")[0],) + Partial_closeRegexMatch3.groups() + ("Partial_closeRow3",)
                # print(Partial_closeRow3)
                # Reset all signal
                flag_Signal = flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0


            #Slippages: order #8 (0.02 lots): Market Enter at 1.09587 executed at 1.09587, slippage = -0.0 p, spread = 0.50 p, last ping = 0.0 ms, latency = 1.8 ms!
            #Slippages: order #9 (0.04 lots): Market Exit at 1.09592 executed at 1.09592, slippage = -0.0 p, spread = 0.50 p, last ping = 0.0 ms, latency = 1.9 ms!
            #Slippages: order #3 (0.09 lots): Market Enter at 1.11752 executed at 1.11752, slippage = 0.0 p, spread = 0.30 p, last ping = 0.0 ms, latency = 1.8 ms!
            SlippagesRegex = re.compile(r'Slippages: order \#([0-9]*) \(([0-9]*[.]?[0-9]*) lots\): Market (Enter|Exit) at ([0-9]*[.]?[0-9]*) executed at ([0-9]*[.]?[0-9]*), slippage = ([\+\-0-9]*[.]?[0-9]*) p, spread = ([0-9]*[.]?[0-9]*) p, last ping = ([0-9]*[.]?[0-9]*) ms, latency = ([0-9]*[.]?[0-9]*) ms!')
            SlippagesRegexMatch = SlippagesRegex.search(mensaje)
            if SlippagesRegexMatch is not None:
                # print(SlippagesRegexMatch.groups())
                flag_Slippages = 1
                SlippagesRow = (linea.split("   ")[0],) + SlippagesRegexMatch.groups() + ("SlippagesRow",)
                # print(SlippagesRow)


            #Sum TakeProfit ($1.00) has been reached ($1.52 >= $1.00)!
            Sum_TakeProfitRegex = re.compile(r'Sum TakeProfit \(\$([\+\-0-9]*[.]?[0-9]*)\) has been reached \(\$([\+\-0-9]*[.]?[0-9]*) >= \$([\+\-0-9]*[.]?[0-9]*)\)!')
            Sum_TakeProfitRegexMatch = Sum_TakeProfitRegex.search(mensaje)
            if Sum_TakeProfitRegexMatch is not None:
                # print(Sum_TakeProfitRegexMatch.groups())
                flag_Sum_TakeProfit = 1
                Sum_TakeProfitRow = (linea.split("   ")[0],) + Sum_TakeProfitRegexMatch.groups() + ("Sum_TakeProfitRow",)
                # Reset all signal
                flag_Signal = flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = 0
                # print(Sum_TakeProfitRow)


            # ---------------------------------------------------------------------------------------------------------------------------------------
            # Join the signal together with the order and market and position and etc.
            # ---------------------------------------------------------------------------------------------------------------------------------------
            # Don't Touch. Working
            # Signal to open buy #1 at 1.14301 (Stochastic K + IdentifyTrend + TDI)!
            if ((len(SignalRow) and len(buy_sell_stopRow) and len(OrderSendRow)) and (SignalRow[0] == buy_sell_stopRow[0]) and (buy_sell_stopRow[0] == OrderSendRow[0])):
                if ((flag_Signal == 1) and (flag_buy_sell_stop == 1) and (flag_OrderSend == 1)):
                    #SignalRow          # Signal to open buy #1 at 1.14301 (Stochastic K + IdentifyTrend + TDI)!
                    #buy_sell_stopRow   # buy stop 1 EURUSD at 1.14301 (1.14029 / 1.14034)
                    #OrderSendRow       # |  OrderSend( EURUSD, buy stop, 1.00, 1.14301, 50, 0.00000, 0.00000, "CP #1", 3047 ) - OK! Ticket #2.

                    #SignalRow          # Signal to open sell #1 at 1.14156 (Stochastic K + IdentifyTrend + TDI)!
                    #buy_sell_stopRow   # sell stop 1.02 EURUSD at 1.14156 (1.14297 / 1.14301)
                    #OrderSendRow       # |  OrderSend( EURUSD, sell stop, 1.02, 1.14156, 50, 0.00000, 0.00000, "CP #1", 3047 ) - OK! Ticket #50.

                    #SignalRow          #Signal to open buy #1 at 1.13538 (Stochastic K + IdentifyTrend + TDI)!
                    #buy_sell_stopRow   #buy stop 0.1 EURUSD at 1.13538 (1.13399 / 1.13414)
                    #OrderSendRow       #|  OrderSend( EURUSD, buy stop, 0.1, 1.13538, 50, 0.00000, 0.00000, "CP #1", 3040 ) - OK! Ticket #3.
                    if (SignalRow[4] == buy_sell_stopRow[4]) and (buy_sell_stopRow[4] == OrderSendRow[4]) and (SignalRow[3] == OrderSendRow[8].split("#")[1]):
                        csv_row.append({'Time': SignalRow[0],
                            'Action': f'Signal1 to {SignalRow[1]}',
                            'Type': SignalRow[2],
                            'Martingale': SignalRow[3],
                            'Signal': SignalRow[5],
                            'Symbol': OrderSendRow[1],
                            'Volume': OrderSendRow[3],
                            'PriceAction': OrderSendRow[4],
                            'Slippage': OrderSendRow[5],
                            'Value1': buy_sell_stopRow[4],
                            'Value2': buy_sell_stopRow[5],
                            'Comment': OrderSendRow[8],
                            'MagicID': OrderSendRow[9],
                            'Status': OrderSendRow[10],
                            'Ticket #': OrderSendRow[11]})
                        SignalRow = tuple()
                        buy_sell_stopRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal = 0
                        flag_buy_sell_stop = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-1")
                        exit()

            #Signal to open buy #1 at 1.14034 (Stochastic K + IdentifyTrend + TDI)!
            if ((len(SignalRow) and len(marketRow) and len(OrderSendRow)) and (SignalRow[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    # CommunityPower MT5 (EURUSD,M5)	2019.01.02 14:30:00   Signal to open buy #1 at 1.14034 (Stochastic K + IdentifyTrend + TDI)!
                    # Trade	2019.01.02 14:30:00   market buy 0.1 EURUSD (1.14029 / 1.14034)
                    # Trades	2019.01.02 14:30:00   deal #2 buy 0.1 EURUSD at 1.14034 done (based on order #2)
                    # Trade	2019.01.02 14:30:00   deal performed [#2 buy 0.1 EURUSD at 1.14034]
                    # Trade	2019.01.02 14:30:00   order performed buy 0.1 at 1.14034 [#2 buy 0.1 EURUSD at 1.14034]
                    # CommunityPower MT5 (EURUSD,M5)	2019.01.02 14:30:00   |  OrderSend( EURUSD, buy, 0.10, 1.14034, 50, 0.00000, 0.00000, "CP #1", 3047 ) - OK! Ticket #2.
                    # https://docs.mql4.com/trading/ordersend
                    if (SignalRow[3] == OrderSendRow[8].split("#")[1]) and (SignalRow[2] == marketRow[1]) and (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        csv_row.append({'Time': SignalRow[0],
                            'Action': f'Signal2 to {SignalRow[1]}',
                            'Type': SignalRow[2],
                            'Martingale': SignalRow[3],
                            'Signal': SignalRow[5],
                            'Symbol': OrderSendRow[1],
                            'Volume': OrderSendRow[3],
                            'PriceAction': OrderSendRow[4],
                            'Slippage': OrderSendRow[5],
                            'Value1': marketRow[4],
                            'Value2': marketRow[5],
                            'Comment': OrderSendRow[8],
                            'MagicID': OrderSendRow[9],
                            'Status': OrderSendRow[10],
                            'Ticket #': OrderSendRow[11]})
                        SignalRow = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal = 0
                        flag_market = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-2")
                        exit()

            #Signal to open buy #2 at 1.11817!
            if ((len(SignalRow2) and len(marketRow) and len(OrderSendRow)) and (SignalRow2[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal2 == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #Example 1(1er example. Not completed)
                    # Signal to open buy #2 at 1843.330!
                    # market buy 0.12 XAUUSD (1842.830 / 1843.330)
                    # |  OrderSend( XAUUSD, buy, 0.12, 1843.330, 50, 0.000, 0.000, "CP18.06.2021.21:03 #2", 234 ) - OK! Ticket #17.
                    # https://docs.mql4.com/trading/ordersend

                    #Example2 (Real Example)
                    #SignalRow2     #2021.07.27 20:09:48.870	2020.01.07 13:52:31   Signal to open buy #2 at 1.11817!
                    #marketRow      #2021.07.27 20:09:48.870	2020.01.07 13:52:31   market buy 0.08 EURUSD (1.11811 / 1.11817)
                    #               #2021.07.27 20:09:48.870	2020.01.07 13:52:31   deal #111 buy 0.08 EURUSD at 1.11817 done (based on order #111)
                    #               #2021.07.27 20:09:48.870	2020.01.07 13:52:31   deal performed [#111 buy 0.08 EURUSD at 1.11817]
                    #               #2021.07.27 20:09:48.870	2020.01.07 13:52:31   order performed buy 0.08 at 1.11817 [#111 buy 0.08 EURUSD at 1.11817]
                    #OrderSendRow   #2021.07.27 20:09:48.872	2020.01.07 13:52:31   |  OrderSend( EURUSD, buy, 0.08, 1.11817, 50, 0.00000, 0.00000, "CP19.07.2021.00:25 #2", 235 ) - OK! Ticket #111.
                    if (SignalRow2[1] == "open") and (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        csv_row.append({'Time': SignalRow2[0],
                            'Action': 'Signal3 to ' + SignalRow2[1],
                            'Type': SignalRow2[2],
                            'Martingale': SignalRow2[3],
                            'Symbol': OrderSendRow[1],
                            'Volume': OrderSendRow[3],
                            'PriceAction': OrderSendRow[4],
                            'Slippage': OrderSendRow[5],
                            'Value1': marketRow[4],
                            'Value2': marketRow[5],
                            'Comment': OrderSendRow[8],
                            'MagicID': OrderSendRow[9],
                            'Status': OrderSendRow[10],
                            'Ticket #': OrderSendRow[11]})
                        SignalRow2 = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        # flag_Signal2 = 0 (not reset flag)
                        flag_market = 0
                        flag_OrderSend = 0

                        # Reset other signal
                        flag_Signal3 = 0
                        SignalRow3 = tuple()

                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-3")
                        exit()

            # Signal to close sell (Stochastic K)!
            if ((len(SignalRow3) and len(marketRow2) and len(OrderCloseRow)) and (SignalRow3[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_Signal3 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    # Signal to close buy (Stochastic K + MACD )!
                    # market sell 0.15 EURUSD, close #251 (1.12740 / 1.12746)
                    # deal #252 sell 0.15 EURUSD at 1.12740 done (based on order #252)
                    # deal performed [#252 sell 0.15 EURUSD at 1.12740]
                    # order performed sell 0.15 at 1.12740 [#252 sell 0.15 EURUSD at 1.12740]
                    # |  OrderClose( 251, 0.15, 1.12740, 50 ) - OK!
                    # https://docs.mql4.com/trading/orderclose

                    # Other Options. Close 3 orders
                    #SignalRow3     # 2021.07.19 15:33:45.003	2019.01.03 13:50:00   Signal to close sell (Stochastic K)!
                    #marketRow2     # 2021.07.19 15:33:45.003	2019.01.03 13:50:00   market buy 0.15 EURUSD, close #30 (1.13429 / 1.13435)
                    #               # 2021.07.19 15:33:45.003	2019.01.03 13:50:00   deal #31 buy 0.15 EURUSD at 1.13435 done (based on order #31)
                    #               # 2021.07.19 15:33:45.003	2019.01.03 13:50:00   deal performed [#31 buy 0.15 EURUSD at 1.13435]
                    #               # 2021.07.19 15:33:45.003	2019.01.03 13:50:00   order performed buy 0.15 at 1.13435 [#31 buy 0.15 EURUSD at 1.13435]
                    #OrderCloseRow  # 2021.07.19 15:33:45.005	2019.01.03 13:50:00   |  OrderClose( 30, 0.15, 1.13435, 50 ) - OK!
                    #marketRow2     # 2021.07.19 15:33:45.005	2019.01.03 13:50:00   market buy 0.1 EURUSD, close #29 (1.13429 / 1.13435)
                    #               # 2021.07.19 15:33:45.005	2019.01.03 13:50:00   deal #32 buy 0.1 EURUSD at 1.13435 done (based on order #32)
                    #               # 2021.07.19 15:33:45.005	2019.01.03 13:50:00   deal performed [#32 buy 0.1 EURUSD at 1.13435]
                    #               # 2021.07.19 15:33:45.005	2019.01.03 13:50:00   order performed buy 0.1 at 1.13435 [#32 buy 0.1 EURUSD at 1.13435]
                    #OrderCloseRow  # 2021.07.19 15:33:45.007	2019.01.03 13:50:00   |  OrderClose( 29, 0.10, 1.13435, 50 ) - OK!
                    #marketRow2     # 2021.07.19 15:33:45.007	2019.01.03 13:50:00   market buy 0.07 EURUSD, close #18 (1.13429 / 1.13435)
                    #               # 2021.07.19 15:33:45.007	2019.01.03 13:50:00   deal #33 buy 0.07 EURUSD at 1.13435 done (based on order #33)
                    #               # 2021.07.19 15:33:45.007	2019.01.03 13:50:00   deal performed [#33 buy 0.07 EURUSD at 1.13435]
                    #               # 2021.07.19 15:33:45.007	2019.01.03 13:50:00   order performed buy 0.07 at 1.13435 [#33 buy 0.07 EURUSD at 1.13435]
                    #OrderCloseRow  # 2021.07.19 15:33:45.029	2019.01.03 13:50:00   |  OrderClose( 18, 0.07, 1.13435, 50 ) - OK!
                    #               # https://docs.mql4.com/trading/orderclose
                    if (SignalRow3[1] == "close") and (marketRow2[5] == OrderCloseRow[1]):
                        csv_row.append({'Time': SignalRow3[0],
                            'Action': f'Signal4 to {SignalRow3[1]}',
                            'Type':  SignalRow3[2],
                            'Signal': SignalRow3[3],
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        # SignalRow3 = tuple()
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        # flag_Signal3 = 0 (not reset flag)
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-4")
                        continue
                        # exit()

            #Signal to open AutoHedge for buy-order #6 at 1.14407!
            if ((len(SignalRow4) and len(marketRow) and len(OrderSendRow)) and (SignalRow4[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal4 == 1) and (flag_market2 == 1) and (flag_OrderSend == 1)):
                    #SignalRow4    #2021.06.01 10:30:16   Signal to open AutoHedge for sell-order #1!
                    #marketRow     #2021.06.01 10:30:16   market buy 1 USDCAD (1.20365 / 1.20384)
                    #              #2021.06.01 10:30:16   deal #3 buy 1 USDCAD at 1.20384 done (based on order #3)
                    #              #2021.06.01 10:30:16   deal performed [#3 buy 1 USDCAD at 1.20384]
                    #              #2021.06.01 10:30:16   order performed buy 1 at 1.20384 [#3 buy 1 USDCAD at 1.20384]
                    #OrderSendRow  #2021.06.01 10:30:16   |  OrderSend( USDCAD, buy, 1.0, 1.20384, 50, 0.00000, 0.00000, "ZIGZAG #H1", 2431 ) - OK! Ticket #3.
                    if (SignalRow4[3] == OrderSendRow[8].split("#H")[1]) and (SignalRow4[4] == OrderSendRow[4]) and (marketRow[3] == OrderSendRow[1]):
                        csv_row.append({'Time': SignalRow4[0],
                            'Action': f'Signal5 to {SignalRow4[1]}',
                            'Type': OrderSendRow[2],
                            'Martingale': SignalRow4[3],
                            'Signal': 'AutoHedge',
                            'Symbol': OrderSendRow[1],
                            'Volume': OrderSendRow[3],
                            'PriceAction': OrderSendRow[4],
                            'Slippage': OrderSendRow[5],
                            'Comment': OrderSendRow[8],
                            'MagicID': OrderSendRow[9],
                            'Status': OrderSendRow[10],
                            'Ticket #': OrderSendRow[11]})
                        SignalRow4 = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal4 = 0
                        flag_market2 = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-5")
                        exit()

            #Signal to open anti-martingale buy #2 at 1.22464!
            if ((len(SignalRow5) and len(marketRow) and len(OrderSendRow)) and (SignalRow5[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal5 == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    # Signal to open anti-martingale buy #2 at 1.22464!
                    # market buy 0.15 EURUSD (1.22450 / 1.22464)
                    # deal #13 buy 0.15 EURUSD at 1.22464 done (based on order #13)
                    # deal performed [#13 buy 0.15 EURUSD at 1.22464]
                    # order performed buy 0.15 at 1.22464 [#13 buy 0.15 EURUSD at 1.22464]
                    # |  OrderSend( EURUSD, buy, 0.15, 1.22464, 50, 0.00000, 0.00000, "CP16.07.2021.16:19 #-2", 234 ) - OK! Ticket #13.
                    # https://docs.mql4.com/trading/ordersend
                    if (SignalRow5[3] == OrderSendRow[8].split("#-")[1]) and (SignalRow5[4] == OrderSendRow[4]) and (marketRow[3] == OrderSendRow[1]):
                        csv_row.append({'Time': SignalRow5[0],
                            'Action': f'Signal6 to {SignalRow5[1]}',
                            'Type': OrderSendRow[2],
                            'Martingale': SignalRow5[3],
                            'Signal': 'anti-martingale',
                            'Symbol': OrderSendRow[1],
                            'Volume': OrderSendRow[3],
                            'PriceAction': OrderSendRow[4],
                            'Slippage': OrderSendRow[5],
                            'Comment': OrderSendRow[8],
                            'MagicID': OrderSendRow[9],
                            'Status': OrderSendRow[10],
                            'Ticket #': OrderSendRow[11]})
                        SignalRow5 = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal5 = 0
                        flag_market = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-6")
                        exit()

            #Signal to close buy (BreakEven after order #4 reached: Bid = 1.18534, op = 1.18524, MinProfit = 1.0)!
            #Signal to close sell (BreakEven after order #3 reached: Ask = 1.20893, op = 1.20904, MinProfit = 1.0)!
            if ((len(SignalRow6) and len(marketRow2) and len(OrderCloseRow)) and (SignalRow6[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_Signal6 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #SignalRow6         #Signal to close buy (BreakEven after order #4 reached: Bid = 1.18534, op = 1.18524, MinProfit = 1.0)!
                    #marketRow2         #market sell 0.13 EURUSD, close #26 (1.18534 / 1.18555)
                    #                   #deal #30 sell 0.13 EURUSD at 1.18534 done (based on order #30)
                    #                   #deal performed [#30 sell 0.13 EURUSD at 1.18534]
                    #                   #order performed sell 0.13 at 1.18534 [#30 sell 0.13 EURUSD at 1.18534]
                    #OrderCloseRow      #|  OrderClose( 26, 0.13, 1.18534, 50 ) - OK!
                    #marketRow2         #market sell 0.11 EURUSD, close #14 (1.18534 / 1.18555)
                    #                   #deal #31 sell 0.11 EURUSD at 1.18534 done (based on order #31)
                    #                   #deal performed [#31 sell 0.11 EURUSD at 1.18534]
                    #                   #order performed sell 0.11 at 1.18534 [#31 sell 0.11 EURUSD at 1.18534]
                    #OrderCloseRow      #|  OrderClose( 14, 0.11, 1.18534, 50 ) - OK!
                    #marketRow2         #market sell 0.09 EURUSD, close #13 (1.18534 / 1.18555)
                    #                   #deal #32 sell 0.09 EURUSD at 1.18534 done (based on order #32)
                    #                   #deal performed [#32 sell 0.09 EURUSD at 1.18534]
                    #                   #order performed sell 0.09 at 1.18534 [#32 sell 0.09 EURUSD at 1.18534]
                    #OrderCloseRow      #|  OrderClose( 13, 0.09, 1.18534, 50 ) - OK!
                    #marketRow2         #market sell 0.08 EURUSD, close #12 (1.18534 / 1.18555)
                    #                   #deal #33 sell 0.08 EURUSD at 1.18534 done (based on order #33)
                    #                   #deal performed [#33 sell 0.08 EURUSD at 1.18534]
                    #                   #order performed sell 0.08 at 1.18534 [#33 sell 0.08 EURUSD at 1.18534]
                    #OrderCloseRow      #|  OrderClose( 12, 0.08, 1.18534, 50 ) - OK!
                    #marketRow2         #market buy 3.93 EURUSD, close #27 (1.18534 / 1.18555)
                    #                   #deal #34 buy 3.93 EURUSD at 1.18555 done (based on order #34)
                    #                   #deal performed [#34 buy 3.93 EURUSD at 1.18555]
                    #                   #order performed buy 3.93 at 1.18555 [#34 buy 3.93 EURUSD at 1.18555]
                    #OrderCloseRow      #|  OrderClose( 27, 3.93, 1.18555, 50 ) - OK!
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]):
                        csv_row.append({'Time': SignalRow6[0],
                            'Action': f'Signal7 to {SignalRow6[1]}',
                            'Type': SignalRow6[2],
                            'Signal': 'BreakEven',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'Profit': f'MinProfit: {SignalRow6[7]}',
                            'Slippage': OrderCloseRow[4],
                            'TakeProfit': SignalRow6[5],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        flag_market2 = 0
                        flag_OrderClose = 0
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-7")
                        exit()


            #Signal to open AutoHedge for buy-order #1!
            #Signal to open AutoHedge for sell-order #1!
            if ((len(SignalRow7) and len(marketRow) and len(OrderSendRow)) and (SignalRow7[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal7 == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #SignalRow7         #Signal to open AutoHedge for buy-order #1!
                    #marketRow          #market sell 0.65 EURUSD (1.11845 / 1.11848)
                    #                   #deal #17 sell 0.65 EURUSD at 1.11845 done (based on order #17)
                    #                   #deal performed [#17 sell 0.65 EURUSD at 1.11845]
                    #                   #order performed sell 0.65 at 1.11845 [#17 sell 0.65 EURUSD at 1.11845]
                    #OrderSendRow       #|  OrderSend( EURUSD, sell, 0.65, 1.11845, 50, 0.00000, 0.00000, "CP28.01.2022.09:58 #H1", 2421 ) - OK! Ticket #17.

                    #SignalRow7         #2021.06.01 10:30:16   Signal to open AutoHedge for sell-order #1!
                    #marketRow          #2021.06.01 10:30:16   market buy 1 USDCAD (1.20365 / 1.20384)
                    #                   #2021.06.01 10:30:16   deal #3 buy 1 USDCAD at 1.20384 done (based on order #3)
                    #                   #2021.06.01 10:30:16   deal performed [#3 buy 1 USDCAD at 1.20384]
                    #                   #2021.06.01 10:30:16   order performed buy 1 at 1.20384 [#3 buy 1 USDCAD at 1.20384]
                    #OrderSendRow       #2021.06.01 10:30:16   |  OrderSend( USDCAD, buy, 1.0, 1.20384, 50, 0.00000, 0.00000, "ZIGZAG #H1", 2431 ) - OK! Ticket #3.
                    if (SignalRow7[3] == OrderSendRow[8].split("#H")[1]) and (marketRow[3] == OrderSendRow[1]):
                        csv_row.append({'Time': SignalRow7[0],
                            'Action': f'Signal8 to {SignalRow7[1]}',
                            'Type': OrderSendRow[2],
                            'Martingale': SignalRow7[3],
                            'Signal': 'AutoHedge',
                            'Symbol': OrderSendRow[1],
                            'Volume': OrderSendRow[3],
                            'PriceAction': OrderSendRow[4],
                            'Slippage': OrderSendRow[5],
                            'Comment': OrderSendRow[8],
                            'MagicID': OrderSendRow[9],
                            'Status': OrderSendRow[10],
                            'Ticket #': OrderSendRow[11]})
                        SignalRow7 = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal7 = 0
                        flag_market = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-8")
                        exit()

            #Signal to delete pending buy-order (indicator)!
            if ((len(SignalRow8) and len(order_canceledRow) and len(OrderDeleteRow)) and (SignalRow8[0] == order_canceledRow[0]) and (order_canceledRow[0] == OrderDeleteRow[0])):
                if ((flag_Signal8 == 1) and (flag_order_canceled == 1) and (flag_OrderDelete == 1)):
                #SignalRow8         #Signal to delete pending buy-order (indicator)!
                #order_canceledRow  #order canceled [#2 buy stop 0.1 EURUSD at 1.13532]
                #OrderDeleteRow     #|  OrderDelete( 2 ) - OK!
                    if (SignalRow8[1] == order_canceledRow[2]) and (order_canceledRow[1] == OrderDeleteRow[1]):
                        csv_row.append({'Time': SignalRow8[0],
                            'Action': f'Signal9 to delete pending',
                            'Type': SignalRow8[1],
                            'Signal': 'delete',
                            'Symbol': order_canceledRow[4],
                            'Volume': order_canceledRow[3],
                            'PriceAction': order_canceledRow[5],
                            'Status': OrderDeleteRow[2],
                            'Ticket #': OrderDeleteRow[1]})
                        SignalRow8 = tuple()
                        order_canceledRow = tuple()
                        OrderDeleteRow = tuple()
                        flag_Signal8 = 0
                        flag_order_canceled = 0
                        flag_OrderDelete = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-8.1")
                        exit()

            #Global TakeProfit (1.0%) has been reached ($111.64 >= $100.00)!
            if ((len(Global_TakeProfitRow) and len(marketRow2) and len(OrderCloseRow)) and (Global_TakeProfitRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_Global_TakeProfit == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #Global_TakeProfitRow       # Global TakeProfit (1.0%) has been reached ($111.64 >= $100.00)!
                    #marketRow2                 # market buy 0.13 EURUSD, close #5 (1.22325 / 1.22340)
                    #                           # deal #8 buy 0.13 EURUSD at 1.22340 done (based on order #8)
                    #                           # deal performed [#8 buy 0.13 EURUSD at 1.22340]
                    #                           # order performed buy 0.13 at 1.22340 [#8 buy 0.13 EURUSD at 1.22340]
                    #OrderCloseRow              # |  OrderClose( 5, 0.13, 1.22340, 50 ) - OK!
                    # <----->buy<----->
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[7] == OrderCloseRow[3]):
                        csv_row.append({'Time': Global_TakeProfitRow[0],
                            'Action': f'Global TakeProfit {Global_TakeProfitRow[1]}% -> ${Global_TakeProfitRow[3]}',
                            'Type': marketRow2[1],
                            'Signal': 'Global TakeProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'Profit': Global_TakeProfitRow[2],
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        Global_TakeProfitRow = tuple()
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_Global_TakeProfit = 0
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    # Global TakeProfit (1.0%) has been reached ($111.64 >= $100.00)!
                    # market sell 0.17 EURUSD, close #6 (1.22325 / 1.22340)
                    # deal #7 sell 0.17 EURUSD at 1.22325 done (based on order #7)
                    # deal performed [#7 sell 0.17 EURUSD at 1.22325]
                    # order performed sell 0.17 at 1.22325 [#7 sell 0.17 EURUSD at 1.22325]
                    # |  OrderClose( 6, 0.17, 1.22325, 50 ) - OK!
                    # <----->sell<----->
                    elif (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[6] == OrderCloseRow[3]):
                        csv_row.append({'Time': Global_TakeProfitRow[0],
                            'Action': f'Global TakeProfit {Global_TakeProfitRow[1]}% -> $ {Global_TakeProfitRow[3]}',
                            'Type': marketRow2[1],
                            'Signal': 'Global TakeProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'Profit': Global_TakeProfitRow[2],
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        Global_TakeProfitRow = tuple()
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_Global_TakeProfit = 0
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-9")
                        exit()


            # Modifying SL for sell-order #86: 0.00000 -> 1.17551...
            # Modifying TP for sell-order #437: 0.00000 -> 1.19366...
            if ((len(ModifyingRow) and len(position_modifiedRow) and len(OrderModifyRow)) and (ModifyingRow[0] == position_modifiedRow[0]) and (position_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_Modifying == 1) and (flag_position_modified == 1) and (flag_OrderModify == 1)):
                    # Modifying SL for sell-order #86: 0.00000 -> 1.17551...
                    # position modified [#86 sell 0.1 EURUSD 1.14135 sl: 1.17551]
                    # |  OrderModify( 86, 1.14135, 1.17551, 0.00000 ) - OK!
                    # https://docs.mql4.com/trading/ordermodify

                    #2021.07.27 20:09:48.874	2020.01.07 13:52:31   Modifying TP for buy-order #111: 0.00000 -> 1.12231...
                    #2021.07.27 20:09:48.874	2020.01.07 13:52:31   position modified [#111 buy 0.08 EURUSD 1.11817 sl: 1.08607 tp: 1.12231]
                    #2021.07.27 20:09:48.876	2020.01.07 13:52:31   |  OrderModify( 111, 1.11817, 1.08607, 1.12231 ) - OK!
                    if (ModifyingRow[3] == position_modifiedRow[1]) and (position_modifiedRow[1] == OrderModifyRow[1]) and (ModifyingRow[3] == OrderModifyRow[1]):
                        csv_row.append({'Time': ModifyingRow[0],
                            'Action': f'Modifying {ModifyingRow[1]}',
                            'Type': position_modifiedRow[2],
                            'Symbol': position_modifiedRow[4],
                            'Volume': position_modifiedRow[3],
                            'PriceAction': OrderModifyRow[2],
                            'NewValue': ModifyingRow[5],
                            'StopLoss': OrderModifyRow[3],
                            'TakeProfit': OrderModifyRow[4],
                            'Status': OrderModifyRow[5],
                            'Ticket #': OrderModifyRow[1]})
                        ModifyingRow = tuple()
                        position_modifiedRow = tuple()
                        OrderModifyRow = tuple()
                        flag_Modifying = 0
                        flag_position_modified = 0
                        flag_OrderModify = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-10")
                        continue
                        # exit()


            #Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
            if ((len(MovingRow) and len(order_modifiedRow) and len(OrderModifyRow)) and (MovingRow[0] == order_modifiedRow[0]) and (order_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_Moving == 1) and (flag_order_modified == 1) and (flag_OrderModify == 1)):
                    # Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
                    # order modified [#10 buy stop 1.01 EURUSD at 1.15179]
                    # |  OrderModify( 10, 1.15179, 0.00000, 0.00000 ) - OK!
                    # https://docs.mql4.com/trading/ordermodify
                    if (MovingRow[2] == order_modifiedRow[1]) and (order_modifiedRow[1] == OrderModifyRow[1]) and (MovingRow[4] == order_modifiedRow[5]) and (order_modifiedRow[5] == OrderModifyRow[2]):
                        csv_row.append({'Time': MovingRow[0],
                            'Action': f'Moving {MovingRow[1]}',
                            'Type': order_modifiedRow[2],
                            'Symbol': order_modifiedRow[4],
                            'Volume': order_modifiedRow[3],
                            'PriceAction': MovingRow[3],
                            'NewValue': MovingRow[4],
                            'StopLoss': OrderModifyRow[3],
                            'TakeProfit': OrderModifyRow[4],
                            'Status': OrderModifyRow[5],
                            'Ticket #': OrderModifyRow[1]})
                        MovingRow = tuple()
                        order_modifiedRow = tuple()
                        OrderModifyRow = tuple()
                        flag_Moving = 0
                        flag_order_modified = 0
                        flag_OrderModify = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-11")
                        exit()

            # Partial close hedge: closing 1 profit order ($+76.85) + 1 opposite loss order ($-75.77) with total profit $+1.08!
            if ((len(Partial_closeRow) and len(marketRow2) and len(OrderCloseRow)) and ( (Partial_closeRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0]))):
                if ((flag_Partial_close == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    total_close_order=int(Partial_closeRow[1]) + int(Partial_closeRow[3])
                    #Example Partial Close hedge
                    #Partial_closeRow    #2021.07.27 22:03:08.905	2020.01.10 11:21:12   Partial close hedge: closing 1 profit order ($+76.85) + 1 opposite loss order ($-75.77) with total profit $+1.08!
                    #marketRow2          #2021.07.27 22:03:08.905	2020.01.10 11:21:12   market sell 0.08 EURUSD, close #24 (1.10916 / 1.10920)
                    #                    #2021.07.27 22:03:08.905	2020.01.10 11:21:12   deal #28 sell 0.08 EURUSD at 1.10916 done (based on order #28)
                    #                    #2021.07.27 22:03:08.905	2020.01.10 11:21:12   deal performed [#28 sell 0.08 EURUSD at 1.10916]
                    #                    #2021.07.27 22:03:08.905	2020.01.10 11:21:12   order performed sell 0.08 at 1.10916 [#28 sell 0.08 EURUSD at 1.10916]
                    #OrderCloseRow       #2021.07.27 22:03:08.907	2020.01.10 11:21:12   |  OrderClose( 24, 0.08, 1.10916, 50 ) - OK!
                    #marketRow2          #2021.07.27 22:03:08.907	2020.01.10 11:21:12   market buy 0.26 EURUSD, close #27 (1.10916 / 1.10920)
                    #                    #2021.07.27 22:03:08.907	2020.01.10 11:21:12   deal #29 buy 0.26 EURUSD at 1.10920 done (based on order #29)
                    #                    #2021.07.27 22:03:08.907	2020.01.10 11:21:12   deal performed [#29 buy 0.26 EURUSD at 1.10920]
                    #                    #2021.07.27 22:03:08.907	2020.01.10 11:21:12   order performed buy 0.26 at 1.10920 [#29 buy 0.26 EURUSD at 1.10920]
                    #OrderCloseRow       #2021.07.27 22:03:08.909	2020.01.10 11:21:12   |  OrderClose( 27, 0.26, 1.10920, 50 ) - OK!

                    #Partial_closeRow    #2020.02.07 10:59:29   Partial close hedge: closing 1 profit order ($+15.84) + 1 opposite loss order ($-0.04) with total profit $+15.80!
                    #marketRow2          #2020.02.07 10:59:29   market sell 0.04 EURUSD, close #9 (1.09592 / 1.09597)
                    #                    #2020.02.07 10:59:29   deal #10 sell 0.04 EURUSD at 1.09592 done (based on order #10)
                    #                    #2020.02.07 10:59:29   deal performed [#10 sell 0.04 EURUSD at 1.09592]
                    #                    #2020.02.07 10:59:29   order performed sell 0.04 at 1.09592 [#10 sell 0.04 EURUSD at 1.09592]
                    #OrderCloseRow       #2020.02.07 10:59:29   |  OrderClose( 9, 0.04, 1.09592, 50 ) - OK!
                    #marketRow2          #2020.02.07 10:59:29   market buy 0.08 EURUSD, close #6 (1.09592 / 1.09597)
                    #                    #2020.02.07 10:59:29   deal #11 buy 0.08 EURUSD at 1.09597 done (based on order #11)
                    #                    #2020.02.07 10:59:29   deal performed [#11 buy 0.08 EURUSD at 1.09597]
                    #                    #2020.02.07 10:59:29   order performed buy 0.08 at 1.09597 [#11 buy 0.08 EURUSD at 1.09597]
                    #OrderCloseRow       #2020.02.07 10:59:29   |  OrderClose( 6, 0.08, 1.09597, 50 ) - OK!
                    if close_order < total_close_order:
                        close_order = close_order + 1
                        if (marketRow2[5] == OrderCloseRow[1]):
                            csv_row.append({'Time': Partial_closeRow[0],
                                'Action': f'Partial close hedge profit {Partial_closeRow[1]} + loss {Partial_closeRow[3]}',
                                'Type': marketRow2[1],
                                'Symbol': marketRow2[3],
                                'Volume': marketRow2[2],
                                'PriceAction': OrderCloseRow[3],
                                'Profit': Partial_closeRow[5],
                                'Slippage': OrderCloseRow[4],
                                'Value1': marketRow2[6],
                                'Value2': marketRow2[7],
                                'Status': OrderCloseRow[5],
                                'Ticket #': OrderCloseRow[1]})
                            flag_market2 = 0
                            flag_OrderClose = 0
                            marketRow2 = tuple()
                            OrderCloseRow = tuple()
                            continue
                        else:
                            print("Error in Script. Check Log!! Critical error-12")
                            continue
                            # exit()
                    if close_order >= total_close_order:
                        close_order = 0
                        flag_Partial_close = 0
                        flag_market2 = 0
                        flag_OrderClose = 0
                        Partial_closeRow = tuple()
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                    continue




            #Partial close any: closing 2 profit orders ($+266.05) + 1 loss order ($-166.00) with total profit $+100.05!
            if ((len(Partial_closeRow2) and len(marketRow2) and len(OrderCloseRow)) and ((Partial_closeRow2[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0]) and (marketRow2[5] == OrderCloseRow[1]))):
                if ((flag_Partial_close2 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    total_close_order2=int(Partial_closeRow2[1]) + int(Partial_closeRow2[3])
                    #Example Partial Close any
                    #Partial_closeRow2      #2022.01.04 18:25:39   Partial close any: closing 2 profit orders ($+266.05) + 1 loss order ($-166.00) with total profit $+100.05!
                    #marketRow2             #2022.01.04 18:25:39   market buy 1.33 EURUSD, close #21 (1.12973 / 1.12990)
                    #                       #2022.01.04 18:25:39    deal #22 buy 1.33 EURUSD at 1.12990 done (based on order #22)
                    #                       #2022.01.04 18:25:39   deal performed [#22 buy 1.33 EURUSD at 1.12990]
                    #                       #2022.01.04 18:25:39   order performed buy 1.33 at 1.12990 [#22 buy 1.33 EURUSD at 1.12990]
                    #OrderCloseRow          #2022.01.04 18:25:39   |  OrderClose( 21, 1.3300000000000001, 1.12990, 50 ) - OK!
                    #marketRow2             #2022.01.04 18:25:39   market buy 1.21 EURUSD, close #20 (1.12973 / 1.12990)
                    #                       #2022.01.04 18:25:39   deal #23 buy 1.21 EURUSD at 1.12990 done (based on order #23)
                    #                       #2022.01.04 18:25:39   deal performed [#23 buy 1.21 EURUSD at 1.12990]
                    #                       #2022.01.04 18:25:39   order performed buy 1.21 at 1.12990 [#23 buy 1.21 EURUSD at 1.12990]
                    #OrderCloseRow          #2022.01.04 18:25:39   |  OrderClose( 20, 1.21, 1.12990, 50 ) - OK!
                    #marketRow2             #2022.01.04 18:25:39   market buy 1 EURUSD, close #18 (1.12973 / 1.12990)
                    #                       #2022.01.04 18:25:39   deal #24 buy 1 EURUSD at 1.12990 done (based on order #24)
                    #                       #2022.01.04 18:25:39   deal performed [#24 buy 1 EURUSD at 1.12990]
                    #                       #2022.01.04 18:25:39   order performed buy 1 at 1.12990 [#24 buy 1 EURUSD at 1.12990]
                    #OrderCloseRow          #2022.01.04 18:25:39   |  OrderClose( 18, 1.0, 1.12990, 50 ) - OK!
                    if (marketRow2[5] == OrderCloseRow[1]):
                        csv_row.append({'Time': Partial_closeRow2[0],
                            'Action': f'Partial close any profit {Partial_closeRow2[1]} + loss {Partial_closeRow2[3]}',
                            'Type': marketRow2[1],
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'Profit': Partial_closeRow2[5],
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        if close_order2 < total_close_order2:
                            close_order2 = close_order2 + 1
                        if close_order2 >= total_close_order2:
                            close_order2 = 0
                            flag_Partial_close2 = 0
                            flag_market2 = 0
                            flag_OrderClose = 0
                            Partial_closeRow2 = tuple()
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-13")
                        exit()


            #Partial close for SELL-series: closing 3 profit orders ($+110.17) + 1 loss order ($-104.10) with total profit $+6.07!
            if ((len(Partial_closeRow3) and len(marketRow2) and len(OrderCloseRow)) and ((Partial_closeRow3[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0]) and (marketRow2[5] == OrderCloseRow[1]))):
                if ((flag_Partial_close3 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    total_close_order3=int(Partial_closeRow3[2]) + int(Partial_closeRow3[4])
                    #Example
                    #Partial_closeRow3  #Partial close for SELL-series: closing 3 profit orders ($+110.17) + 1 loss order ($-104.10) with total profit $+6.07!
                    #marketRow2         #market buy 0.41 EURUSD, close #743 (1.13748 / 1.13767)
                    #                   #deal #744 buy 0.41 EURUSD at 1.13767 done (based on order #744)
                    #                   #deal performed [#744 buy 0.41 EURUSD at 1.13767]
                    #                   #order performed buy 0.41 at 1.13767 [#744 buy 0.41 EURUSD at 1.13767]
                    #OrderCloseRow      #|  OrderClose( 743, 0.41, 1.13767, 50 ) - OK!
                    #marketRow2         #market buy 0.37 EURUSD, close #742 (1.13748 / 1.13767)
                    #                   #deal #745 buy 0.37 EURUSD at 1.13767 done (based on order #745)
                    #                   #deal performed [#745 buy 0.37 EURUSD at 1.13767]
                    #                   #order performed buy 0.37 at 1.13767 [#745 buy 0.37 EURUSD at 1.13767]
                    #OrderCloseRow      #|  OrderClose( 742, 0.37, 1.13767, 50 ) - OK!
                    #marketRow2         #market buy 0.34 EURUSD, close #741 (1.13748 / 1.13767)
                    #                   #deal #746 buy 0.34 EURUSD at 1.13767 done (based on order #746)
                    #                   #deal performed [#746 buy 0.34 EURUSD at 1.13767]
                    #                   #order performed buy 0.34 at 1.13767 [#746 buy 0.34 EURUSD at 1.13767]
                    #OrderCloseRow      #|  OrderClose( 741, 0.34, 1.13767, 50 ) - OK!
                    #marketRow2         #market buy 0.1 EURUSD, close #728 (1.13748 / 1.13767)
                    #                   #deal #747 buy 0.1 EURUSD at 1.13767 done (based on order #747)
                    #                   #deal performed [#747 buy 0.1 EURUSD at 1.13767]
                    #                   #order performed buy 0.1 at 1.13767 [#747 buy 0.1 EURUSD at 1.13767]
                    #OrderCloseRow      #|  OrderClose( 728, 0.1, 1.13767, 50 ) - OK!
                    if (marketRow2[5] == OrderCloseRow[1]):
                        csv_row.append({'Time': Partial_closeRow3[0],
                            'Action': f'Partial close for {Partial_closeRow3[1]}-series {Partial_closeRow3[2]} + loss {Partial_closeRow3[4]}',
                            'Type': marketRow2[1],
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'Profit': Partial_closeRow3[6],
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        if close_order3 < total_close_order3:
                            close_order3 = close_order3 + 1
                        if close_order3 >= total_close_order3:
                            close_order3 = 0
                            flag_Partial_close3 = 0
                            flag_market3 = 0
                            flag_OrderClose = 0
                            Partial_closeRow3 = tuple()
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-14")
                        exit()


            #Sum TakeProfit ($1.00) has been reached ($1.52 >= $1.00)!
            if ((len(Sum_TakeProfitRow) and len(marketRow2) and len(OrderCloseRow)) and ((Sum_TakeProfitRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0]) and (marketRow2[5] == OrderCloseRow[1]))):
                if ((flag_Sum_TakeProfit == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #Sum_TakeProfitRow  #Sum TakeProfit ($1.00) has been reached ($1.52 >= $1.00)!
                    #marketRow2         #market sell 0.3 XAUUSD, close #28 (1921.370 / 1921.780)
                                        #deal #29 sell 0.3 XAUUSD at 1921.370 done (based on order #29)
                                        #deal performed [#29 sell 0.3 XAUUSD at 1921.370]
                                        #order performed sell 0.3 at 1921.370 [#29 sell 0.3 XAUUSD at 1921.370]
                    #OrderCloseRow      #|  OrderClose( 28, 0.3, 1921.370, 50 ) - OK!
                    #marketRow2         #market sell 0.17 XAUUSD, close #27 (1921.370 / 1921.780)
                                        #deal #30 sell 0.17 XAUUSD at 1921.370 done (based on order #30)
                                        #deal performed [#30 sell 0.17 XAUUSD at 1921.370]
                                        #order performed sell 0.17 at 1921.370 [#30 sell 0.17 XAUUSD at 1921.370]
                    #OrderCloseRow      #|  OrderClose( 27, 0.17, 1921.370, 50 ) - OK!
                    #marketRow2         #market sell 0.1 XAUUSD, close #26 (1921.370 / 1921.780)
                                        #deal #31 sell 0.1 XAUUSD at 1921.370 done (based on order #31)
                                        #deal performed [#31 sell 0.1 XAUUSD at 1921.370]
                                        #order performed sell 0.1 at 1921.370 [#31 sell 0.1 XAUUSD at 1921.370]
                    #OrderCloseRow      #|  OrderClose( 26, 0.1, 1921.370, 50 ) - OK!
                    if (marketRow2[5] == OrderCloseRow[1]):
                        csv_row.append({'Time': Sum_TakeProfitRow[0],
                            'Action': f'Sum TakeProfit {Sum_TakeProfitRow[1]} has been reached {Sum_TakeProfitRow[2]} >= {Sum_TakeProfitRow[3]}',
                            'Type': marketRow2[1],
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'Profit': Sum_TakeProfitRow[2],
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-15")
                        exit()

                #FALTA TERMINAR
                #Global Account TakeProfit has been reached ($10.93 >= $10.00)!
                #market buy 1.34 EURUSD, close #19 (1.11413 / 1.11416)
                #deal #20 buy 1.34 EURUSD at 1.11416 done (based on order #20)
                #deal performed [#20 buy 1.34 EURUSD at 1.11416]
                #order performed buy 1.34 at 1.11416 [#20 buy 1.34 EURUSD at 1.11416]
                #|  OrderClose( 19, 1.34, 1.11416, 50 ) - OK!
                #market sell 0.24 EURUSD, close #18 (1.11413 / 1.11416)
                #deal #21 sell 0.24 EURUSD at 1.11413 done (based on order #21)
                #deal performed [#21 sell 0.24 EURUSD at 1.11413]
                #order performed sell 0.24 at 1.11413 [#21 sell 0.24 EURUSD at 1.11413]
                #|  OrderClose( 18, 0.24, 1.11413, 50 ) - OK!
                #market sell 0.15 EURUSD, close #17 (1.11413 / 1.11416)
                #deal #22 sell 0.15 EURUSD at 1.11413 done (based on order #22)
                #deal performed [#22 sell 0.15 EURUSD at 1.11413]
                #order performed sell 0.15 at 1.11413 [#22 sell 0.15 EURUSD at 1.11413]
                #|  OrderClose( 17, 0.15, 1.11413, 50 ) - OK!
                #market buy 0.07 EURUSD, close #16 (1.11413 / 1.11416)
                #deal #23 buy 0.07 EURUSD at 1.11416 done (based on order #23)
                #deal performed [#23 buy 0.07 EURUSD at 1.11416]
                #order performed buy 0.07 at 1.11416 [#23 buy 0.07 EURUSD at 1.11416]
                #|  OrderClose( 16, 0.07, 1.11416, 50 ) - OK!
                #market sell 0.1 EURUSD, close #15 (1.11413 / 1.11416)
                #deal #24 sell 0.1 EURUSD at 1.11413 done (based on order #24)
                #deal performed [#24 sell 0.1 EURUSD at 1.11413]
                #order performed sell 0.1 at 1.11413 [#24 sell 0.1 EURUSD at 1.11413]
                #|  OrderClose( 15, 0.10, 1.11413, 50 ) - OK!
                #market sell 0.07 EURUSD, close #14 (1.11413 / 1.11416)
                #deal #25 sell 0.07 EURUSD at 1.11413 done (based on order #25)
                #deal performed [#25 sell 0.07 EURUSD at 1.11413]
                #order performed sell 0.07 at 1.11413 [#25 sell 0.07 EURUSD at 1.11413]
                #|  OrderClose( 14, 0.07, 1.11413, 50 ) - OK!
                #
                #
            if (len(TrailingStopRow)):
                if (flag_TrailingStop == 1):
                    # 2019.01.24 16:14:15   TrailingStop for BUY: 1.13446 -> 1.13553
                    # 2019.01.03 10:06:34   TrailingStop for SELL: 0 -> 1.13679
                    # https://www.metatrader4.com/es/trading-platform/help/positions/trailing
                    csv_row.append({'Time': TrailingStopRow[0],
                        'Action': 'TrailingStop for ' + TrailingStopRow[1].lower(),
                        'Type': TrailingStopRow[1].lower(),
                        'PriceAction': TrailingStopRow[2],
                        'StopLoss': TrailingStopRow[3]})
                    TrailingStopRow = tuple()
                    flag_TrailingStop = 0
                    continue

            # https://www.metatrader4.com/en/trading-platform/help/positions/orders
            # CHECK THIS IF WORKING
            if (len(stop_loss_triggeredRow)):
                if (flag_stop_loss_triggered == 1):
                    # stop loss triggered #7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326 [#8 buy 1 XAUUSD at 1881.920]
                    # deal #8 buy 1 XAUUSD at 1902.500 done (based on order #8)
                    # deal performed [#8 buy 1 XAUUSD at 1902.500]
                    # order performed buy 1 at 1902.500 [#8 buy 1 XAUUSD at 1881.920]
                    csv_row.append({'Time': stop_loss_triggeredRow[0],
                        'Action': f'stop loss triggered' ,
                        'Type': stop_loss_triggeredRow[2],
                        'Symbol': stop_loss_triggeredRow[4],
                        'Volume': stop_loss_triggeredRow[3],
                        'PriceAction': stop_loss_triggeredRow[12],
                        'Value1': stop_loss_triggeredRow[6],
                        'Value2': stop_loss_triggeredRow[7],
                        'Ticket #': stop_loss_triggeredRow[1]})
                    stop_loss_triggeredRow = tuple()
                    flag_stop_loss_triggered = 0
                    continue
                else:
                    print("Error in Script. Check Log!! Critical error-16")
                    exit()


            # stop loss triggered #3 sell 0.1 EURUSD 1.13731 sl: 1.13475 [#4 buy 0.1 EURUSD at 1.13475]
            if ((len(stop_loss_triggeredRow2)) and ((stop_loss_triggeredRow2[3] == stop_loss_triggeredRow2[9]) and (stop_loss_triggeredRow2[4] == stop_loss_triggeredRow2[10]) and (stop_loss_triggeredRow2[6] == stop_loss_triggeredRow2[11]))):
                if (flag_stop_loss_triggered2 == 1):
                    #stop_loss_triggeredRow2    #stop_loss_triggeredRow2    #stop loss triggered #3 sell 0.1 EURUSD 1.13731 sl: 1.13475 [#4 buy 0.1 EURUSD at 1.13475]
                    #                           #deal #4 buy 0.1 EURUSD at 1.13475 done (based on order #4)
                    #                           #deal performed [#4 buy 0.1 EURUSD at 1.13475]
                    #                           #order performed buy 0.1 at 1.13475 [#4 buy 0.1 EURUSD at 1.13475]
                    csv_row.append({'Time': stop_loss_triggeredRow2[0],
                        'Action': f'stop loss triggered' ,
                        'Type': stop_loss_triggeredRow2[2],
                        'Symbol': stop_loss_triggeredRow2[4],
                        'Volume': stop_loss_triggeredRow2[3],
                        'PriceAction': stop_loss_triggeredRow2[11],
                        'Value1': stop_loss_triggeredRow2[5],
                        'Value2': stop_loss_triggeredRow2[6],
                        'Ticket #': stop_loss_triggeredRow2[1]})
                    stop_loss_triggeredRow2 = tuple()
                    flag_stop_loss_triggered2 = 0
                    continue
                else:
                    print("Error in Script. Check Log!! Critical error-17")
                    exit()


            if (len(SlippagesRow)):
                if (flag_Slippages == 1):
                    csv_row.append({'Time': SlippagesRow[0],
                        'Action': 'Slippages',
                        'Type' : SlippagesRow[3],
                        'Volume': SlippagesRow[2],
                        'PriceAction': SlippagesRow[4],
                        'NewValue': SlippagesRow[5],
                        'Slippage': SlippagesRow[6],
                        'Ticket #': SlippagesRow[1]})
                    SlippagesRow = tuple()
                    flag_Slippages = 0
                    # Flags Initialization
                    flag_Signal = 0
                    flag_Signal2 = 0
                    flag_Signal3 = 0
                    flag_Signal4 = 0
                    flag_Signal5 = 0
                    flag_Signal6 = 0
                    flag_Signal7 = 0
                    flag_OrderSend = 0
                    flag_OrderClose = 0
                    flag_OrderModify = 0
                    flag_OrderModify2 = 0
                    flag_OrderDelete = 0
                    flag_TrailingStop = 0
                    flag_Modifying = 0
                    flag_Moving = 0
                    flag_position_modified = 0
                    flag_position_modified2 = 0
                    flag_order_modified = 0
                    flag_stop_loss_triggered = 0
                    flag_market = 0
                    flag_market2 = 0
                    flag_buy_sell_stop = 0
                    flag_Global_TakeProfit = 0
                    flag_Partial_close = 0
                    flag_Partial_close2 = 0
                    flag_Slippages = 0
                    # Variables Clean
                    SignalRow = ()
                    SignalRow2 = ()
                    SignalRow3 = ()
                    SignalRow4 = ()
                    SignalRow5 = ()
                    SignalRow6 = ()
                    SignalRow7 = ()
                    SignalRow8 = ()
                    OrderSendRow = ()
                    OrderCloseRow = ()
                    OrderModifyRow = ()
                    OrderModifyRow2 = ()
                    TrailingStopRow = ()
                    ModifyingRow = ()
                    MovingRow = ()
                    position_modifiedRow = ()
                    position_modifiedRow2 = ()
                    order_modifiedRow = ()
                    order_canceledRow = ()
                    stop_loss_triggeredRow = ()
                    stop_loss_triggeredRow2 = ()
                    marketRow = ()
                    marketRow2 = ()
                    buy_sell_stopRow = ()
                    Global_TakeProfitRow = ()
                    calculate_profitRow = ()
                    Partial_closeRow = ()
                    Partial_closeRow2 = ()
                    SlippagesRow = ()
                else:
                    print("Error in Script. Check Log!! Critical error-17")
                    exit()
            # Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
            # order modified [#10 buy stop 1.01 EURUSD at 1.15179]
            # |  OrderModify( 10, 1.15179, 0.00000, 0.00000 ) - OK!
    else:
        #if (flag_Signal) or (flag_Signal2) or (flag_Signal3) or (flag_Signal4) or (flag_Signal5):
        if flag_Magic:
            if (linea.split(" ")[0] == "final") and (linea.split(" ")[1] == "balance"):
                # final balance 4.99 USD
                csv_row.append({'Time': linea.split(" ")[0] + " " + linea.split(" ")[1] + " " + linea.split(" ")[2] + " " + linea.split(" ")[3]})
                flag_Magic = 0
            if (linea.split(" ")[0] == "stop") and (linea.split(" ")[1] == "out") and (linea.split(" ")[2] == "occurred"):
                # stop out occurred on 0% of testing interval
                csv_row.append({'Time': linea.split(" ")[0] + " " + linea.split(" ")[1] + " " + linea.split(" ")[2]})
                flag_Magic = 0


# print("OrderModify() - ERROR # (Market is closed);" + str(count_OrderModify)
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns, delimiter=';', extrasaction='raise', dialect='unix', quoting = csv.QUOTE_NONE)
        writer.writeheader()
        i=1
        for data in csv_row:
            if i:
                i=0
                continue
            writer.writerow(data)
except IOError:
    print("I/O error")
read_file = pd.read_csv (csv_file,delimiter=";")
read_file.to_excel (excel_file, index = None, header=True)
print("Finish. Opening file...")
print(excel_file)
os.startfile(excel_file)