# Script to parser Tester Logs from CommunityPower EA
#
# Install Python 3.10.x
#
# Install module:
# pip install pandas
# pip install XlsxWriter
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
import xlsxwriter

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
        LogDirectory = expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Tester\\" + DATA_FOLDER + "\\Agent-127.0.0.1-3000\\Logs"
    else:
        LogDirectory = expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\Logs"
else:
    LogDirectory = expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\Logs"

now = datetime.now()
LogToday = now.strftime('%Y%m%d') + ".log"
#LogToday="20220611.log"
LogFile = os.path.join(LogDirectory, LogToday)
if not (os.path.isfile(LogFile)):
    print(f"File Not Found : {LogFile}")
    exit()

print("Reading file...")
print(LogFile)


# HEADER CSV
csv_columns = ['Time','Action','Type','Martingale','Signal','Symbol','Volume','PriceAction','NewValue','Profit','StartEquity','CurrentEquity','Slippage','Value1','Value2','StopLoss','TakeProfit','Expiration','Comment','MagicID','Status','Ticket #']
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
flag_Signal8 = 0
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
flag_GA_TakeProfit = 0
flag_GA_TakeProfit2 = 0
flag_GA_TargetProfit = 0
flag_GA_TargetProfit2 = 0
flag_GA_TrailingStopActivated = 0
flag_GA_TrailingStopActivated2 = 0
flag_GA_TrailingStop = 0
flag_GA_TrailingStop2 = 0
flag_Partial_close = 0
flag_Partial_close2 = 0
flag_Partial_close3 = 0
flag_Slippages = 0
flag_TesterWithdrawal = 0
flag_orders_reached_BreakEven = 0
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
TesterWithdrawalRow = ()
orders_reached_BreakEvenRow = ()
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
GA_TakeProfitRow = ()
GA_TakeProfitRow2 = ()
GA_TargetProfitRow = ()
GA_TargetProfitRow2 = ()
GA_TrailingStopActivatedRow = ()
GA_TrailingStopRow = ()
GA_TrailingStopRow2 = ()
GA_TrailingStopActivatedRow2 = ()
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
                    flag_Signal8 = 0
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
                    flag_GA_TakeProfit = 0
                    flag_GA_TakeProfit2 = 0
                    flag_GA_TargetProfit = 0
                    flag_GA_TargetProfit2 = 0
                    flag_GA_TrailingStopActivated = 0
                    flag_GA_TrailingStopActivated2 = 0
                    flag_GA_TrailingStop = 0
                    flag_GA_TrailingStop2 = 0
                    flag_Partial_close = 0
                    flag_Partial_close2 = 0
                    flag_Partial_close3 = 0
                    flag_Slippages = 0
                    flag_TesterWithdrawal = 0
                    flag_orders_reached_BreakEven = 0
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
                    TesterWithdrawalRow = ()
                    orders_reached_BreakEvenRow = ()
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
                    GA_TakeProfitRow = ()
                    GA_TakeProfitRow2 = ()
                    GA_TargetProfitRow = ()
                    GA_TargetProfitRow2 = ()
                    GA_TrailingStopActivatedRow = ()
                    GA_TrailingStopRow = ()
                    GA_TrailingStopRow2 = ()
                    GA_TrailingStopActivatedRow2 = ()
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
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0

            # Signal to open buy #2 at 1885.770!
            SignalRegex2 = re.compile(r'Signal to (open|close) (buy|sell) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch2 = SignalRegex2.search(mensaje)
            if SignalMatch2 is not None:
                # print(SignalMatch.groups())
                flag_Signal2 = 1
                SignalRow2 = (linea.split("   ")[0],) + SignalMatch2.groups() + ("SignalRow2",)
                # print(SignalRow2)
                flag_Signal = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0

            # Signal to close sell (FIBO )!
            # Signal to close sell (Stochastic K)!
            SignalRegex3 = re.compile(r'Signal to (open|close) (buy|sell) \(([a-zA-Z+ ]+)\)!')
            SignalMatch3 = SignalRegex3.search(mensaje)
            if SignalMatch3 is not None:
                # print(SignalMatch3.groups())
                flag_Signal3 = 1
                SignalRow3 = (linea.split("   ")[0],) + SignalMatch3.groups() + ("SignalRow3",)
                # print(SignalRow3)
                flag_Signal2 = flag_Signal = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0

            # Signal to open AutoHedge for buy-order #6 at 1.14407!
            SignalRegex4 = re.compile(r'Signal to (open|close) AutoHedge for (buy\-order|sell\-order) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch4 = SignalRegex4.search(mensaje)
            if SignalMatch4 is not None:
                # print(SignalMatch4.groups())
                flag_Signal4 = 1
                SignalRow4 = (linea.split("   ")[0],) + SignalMatch4.groups() + ("SignalRow4",)
                # print(SignalRow4)
                flag_Signal2 = flag_Signal3 = flag_Signal = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0

            # Signal to open anti-martingale buy #2 at 1.22464!
            SignalRegex5 = re.compile(r'Signal to (open|close) anti-martingale (buy|sell) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch5 = SignalRegex5.search(mensaje)
            if SignalMatch5 is not None:
                # print(SignalMatch5.groups())
                flag_Signal5 = 1
                SignalRow5 = (linea.split("   ")[0],) + SignalMatch5.groups() + ("SignalRow5",)
                # print(SignalRow5)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0

            #Signal to close buy (BreakEven after order #4 reached: Bid = 1.18534, op = 1.18524, MinProfit = 1.0)!
            #Signal to close sell (BreakEven after order #3 reached: Ask = 1.20893, op = 1.20904, MinProfit = 1.0)!
            SignalRegex6 = re.compile(r'Signal to (open|close) (buy|sell) \(BreakEven after order \#([0-9]+) reached: ([a-zA-Z]+) = ([0-9]*[.]?[0-9]*), op = ([0-9]*[.]?[0-9]*), MinProfit = ([0-9]*[.]?[0-9]*)\)!')
            SignalMatch6 = SignalRegex6.search(mensaje)
            if SignalMatch6 is not None:
                # print(SignalMatch6.groups())
                flag_Signal6 = 1
                SignalRow6 = (linea.split("   ")[0],) + SignalMatch6.groups() + ("SignalRow6",)
                # print(SignalRow6)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0

            #Signal to open AutoHedge for buy-order #1!
            SignalRegex7 = re.compile(r'Signal to (open|close) AutoHedge for (buy\-order|sell\-order) \#([0-9]+)!')
            SignalMatch7 = SignalRegex7.search(mensaje)
            if SignalMatch7 is not None:
                # print(SignalMatch7.groups())
                flag_Signal7 = 1
                SignalRow7 = (linea.split("   ")[0],) + SignalMatch7.groups() + ("SignalRow7",)
                # print(SignalRow7)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal8 = flag_Signal = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0

            # Signal to delete pending buy-order (indicator)!
            SignalRegex8 = re.compile(r'Signal to delete pending (buy|sell)\-order \(indicator\)!')
            SignalMatch8 = SignalRegex8.search(mensaje)
            if SignalMatch8 is not None:
                # print(SignalMatch8.groups())
                flag_Signal8 = 1
                SignalRow8 = (linea.split("   ")[0],) + SignalMatch8.groups() + ("SignalRow8",)
                # print(SignalRow8)
                flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal = flag_Sum_TakeProfit = flag_GA_TakeProfit = flag_GA_TakeProfit2 = flag_GA_TargetProfit = flag_GA_TargetProfit2 = flag_GA_TrailingStop = 0
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

            # --------------------------------------------------------------------------------------------
            # Global Account BEGIN
            # --------------------------------------------------------------------------------------------
            #Global Account TakeProfit has been reached ($10.93 >= $10.00)!
            GA_TakeProfitRegex = re.compile(r'Global Account TakeProfit has been reached \(\$([\+\-\ 0-9]*[.]?[0-9]*) >= \$([\+\-\ 0-9]*[.]?[0-9]*)\)!')
            GA_TakeProfitRegexMatch = GA_TakeProfitRegex.search(mensaje)
            if GA_TakeProfitRegexMatch is not None:
                # print(GA_TakeProfitRegexMatch.groups())
                flag_GA_TakeProfit = 1
                GA_TakeProfitRow = (linea.split("   ")[0],) + GA_TakeProfitRegexMatch.groups() + ("GA_TakeProfitRow",)
                # print(GA_TakeProfitRow)

            #CP < 2.47 Version(Maybe)(CHECK IT)
            # Global TakeProfit (1.0%) has been reached ($111.64 >= $100.00)
            GA_TakeProfitRegex2 = re.compile(r'Global TakeProfit \(([0-9]*[.]?[0-9]*)\%\) has been reached \(\$([\+\-\ 0-9]*[.]?[0-9]*) >= \$([\+\-\ 0-9]*[.]?[0-9]*)\)')

            #CP = 2.47 Version
            #Global Account TakeProfit (1.00%) has been reached ($518.16 >= $503.97)!
            GA_TakeProfitRegex2 = re.compile(r'Global Account TakeProfit \(([0-9]*[.]?[0-9]*)\%\) has been reached \(\$([\+\-\ 0-9]*[.]?[0-9]*) >= \$([\+\-\ 0-9]*[.]?[0-9]*)\)!')
            GA_TakeProfitRegexMatch2 = GA_TakeProfitRegex2.search(mensaje)
            if GA_TakeProfitRegexMatch2 is not None:
                # print(GA_TakeProfitRegexMatch2.groups())
                flag_GA_TakeProfit2 = 1
                GA_TakeProfitRow2 = (linea.split("   ")[0],) + GA_TakeProfitRegexMatch2.groups() + ("GA_TakeProfit2",)
                # print(GA_TakeProfitRow2)

            #Global Account TargetProfit ($1.00) has been reached ($50 592.19 -> $50 594.69)!
            GA_TargetProfitRegex = re.compile(r'Global Account TargetProfit \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) has been reached \(\$([\+\-\ 0-9]*[.]?[0-9]*) -> \$([\+\-\ 0-9]*[.]?[0-9]*)\)!')
            GA_TargetProfitRegexMatch = GA_TargetProfitRegex.search(mensaje)
            if GA_TargetProfitRegexMatch is not None:
                # print(GA_TargetProfitRegexMatch.groups())
                flag_GA_TargetProfit = 1
                GA_TargetProfitRow = (linea.split("   ")[0],) + GA_TargetProfitRegexMatch.groups() + ("GA_TargetProfit",)
                # print(GA_TargetProfitRow)

            #Global Account TargetProfit (1.00%) has been reached ($51 005.85 -> $51 516.26)!
            GA_TargetProfitRegex2 = re.compile(r'Global Account TargetProfit \(([0-9]*[.]?[0-9]*)\%\) has been reached \(\$([\+\-\ 0-9]*[.]?[0-9]*) -> \$([\+\-\ 0-9]*[.]?[0-9]*)\)!')
            GA_TargetProfitRegexMatch2 = GA_TargetProfitRegex2.search(mensaje)
            if GA_TargetProfitRegexMatch2 is not None:
                # print(GA_TargetProfitRegexMatch2.groups())
                flag_GA_TargetProfit2 = 1
                GA_TargetProfitRow2 = (linea.split("   ")[0],) + GA_TargetProfitRegexMatch2.groups() + ("GA_TargetProfit2",)
                # print(GA_TargetProfitRow2)

            #GlobalAccount TrailingStop ($10.00) activated, start equity = $50 001.85, current equity = $50 011.85...
            GA_TrailingStopActivatedRegex = re.compile(r'GlobalAccount TrailingStop \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) activated, start equity = \$([\+\-\ 0-9]*[.]?[0-9]*), current equity = \$([\+\-\ 0-9]*[.]?[0-9]*)...')
            GA_TrailingStopActivatedRegexMatch = GA_TrailingStopActivatedRegex.search(mensaje)
            if GA_TrailingStopActivatedRegexMatch is not None:
                # print(GA_TrailingStopActivatedRegexMatch.groups())
                flag_GA_TrailingStopActivated = 1
                GA_TrailingStopActivatedRow = (linea.split("   ")[0],) + GA_TrailingStopActivatedRegexMatch.groups() + ("GA_TrailingStopActivated",)
                # print(GA_TrailingStopActivatedRow)

            #GlobalAccount TrailingStop (1.00%) activated, start equity = $90 936.95, current equity = $91 889.20...
            GA_TrailingStopActivatedRegex2 = re.compile(r'GlobalAccount TrailingStop \(([\+\-\ 0-9]*[.]?[0-9]*)\%\) activated, start equity = \$([\+\-\ 0-9]*[.]?[0-9]*), current equity = \$([\+\-\ 0-9]*[.]?[0-9]*)...')
            GA_TrailingStopActivatedRegexMatch2 = GA_TrailingStopActivatedRegex2.search(mensaje)
            if GA_TrailingStopActivatedRegexMatch2 is not None:
                # print(GA_TrailingStopActivatedRegexMatch2.groups())
                flag_GA_TrailingStopActivated2 = 1
                GA_TrailingStopActivatedRow2 = (linea.split("   ")[0],) + GA_TrailingStopActivatedRegexMatch2.groups() + ("GA_TrailingStopActivated2",)
                # print(GA_TrailingStopActivatedRow2)

            #Global Account TrailingStop ($10.00) has been reached (max equity = $50 012.85, current equity = $50 002.85)!
            GA_TrailingStopRegex = re.compile(r'Global Account TrailingStop \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) has been reached \(max equity = \$([\+\-\ 0-9]*[.]?[0-9]*), current equity = \$([\+\-\ 0-9]*[.]?[0-9]*)\)!')
            GA_TrailingStopRegexMatch = GA_TrailingStopRegex.search(mensaje)
            if GA_TrailingStopRegexMatch is not None:
                # print(GA_TrailingStopRegexMatch.groups())
                flag_GA_TrailingStop = 1
                GA_TrailingStopRow = (linea.split("   ")[0],) + GA_TrailingStopRegexMatch.groups() + ("GA_TrailingStop",)
                # print(GA_TrailingStopRow)

            #Global Account TrailingStop (1.00%) has been reached (max equity = $51 486.68, current equity = $50 951.63)!
            GA_TrailingStopRegex2 = re.compile(r'Global Account TrailingStop \(([\+\-\ 0-9]*[.]?[0-9]*)\%\) has been reached \(max equity = \$([\+\-\ 0-9]*[.]?[0-9]*), current equity = \$([\+\-\ 0-9]*[.]?[0-9]*)\)!')
            GA_TrailingStopRegexMatch2 = GA_TrailingStopRegex2.search(mensaje)
            if GA_TrailingStopRegexMatch2 is not None:
                # print(GA_TrailingStopRegexMatch2.groups())
                flag_GA_TrailingStop2 = 1
                GA_TrailingStopRow2 = (linea.split("   ")[0],) + GA_TrailingStopRegexMatch2.groups() + ("GA_TrailingStop2",)
                # print(GA_TrailingStopRow2)

            # --------------------------------------------------------------------------------------------
            # Global Account END
            # --------------------------------------------------------------------------------------------


            #Partial close hedge: closing 1 profit order ($+76.85) + 1 opposite loss order ($-75.77) with total profit $+1.08!
            Partial_closeRegex = re.compile(r'Partial close hedge: closing ([0-9]+) profit order \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) \+ ([0-9]+) opposite loss order \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) with total profit \$([\+\-\ 0-9]*[.]?[0-9]*)!')
            Partial_closeRegexMatch = Partial_closeRegex.search(mensaje)
            if Partial_closeRegexMatch is not None:
                # print(Partial_closeRegexMatch.groups())
                flag_Partial_close = 1
                Partial_closeRow = (linea.split("   ")[0],) + Partial_closeRegexMatch.groups() + ("Partial_closeRow",)
                # print(Partial_closeRow)
                # Reset all signal
                flag_Signal = flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0

            #Partial close any: closing 2 profit orders ($+266.05) + 1 loss order ($-166.00) with total profit $+100.05!
            Partial_closeRegex2 = re.compile(r'Partial close any: closing ([0-9]+) profit orders \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) \+ ([0-9]+) loss order \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) with total profit \$([\+\-\ 0-9]*[.]?[0-9]*)!')
            Partial_closeRegexMatch2 = Partial_closeRegex2.search(mensaje)
            if Partial_closeRegexMatch2 is not None:
                # print(Partial_closeRegexMatch2.groups())
                flag_Partial_close2 = 1
                Partial_closeRow2 = (linea.split("   ")[0],) + Partial_closeRegexMatch2.groups() + ("Partial_closeRow2",)
                # print(Partial_closeRow2)
                # Reset all signal
                flag_Signal = flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = flag_Sum_TakeProfit = 0

            #Partial close for SELL-series: closing 3 profit orders ($+110.17) + 1 loss order ($-104.10) with total profit $+6.07!
            Partial_closeRegex3 = re.compile(r'Partial close for (BUY|SELL)-series: closing ([0-9]+) profit orders \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) \+ ([0-9]+) loss order \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) with total profit \$([\+\-\ 0-9]*[.]?[0-9]*)!')
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
            Sum_TakeProfitRegex = re.compile(r'Sum TakeProfit \(\$([\+\-\ 0-9]*[.]?[0-9]*)\) has been reached \(\$([\+\-\ 0-9]*[.]?[0-9]*) >= \$([\+\-\ 0-9]*[.]?[0-9]*)\)!')
            Sum_TakeProfitRegexMatch = Sum_TakeProfitRegex.search(mensaje)
            if Sum_TakeProfitRegexMatch is not None:
                # print(Sum_TakeProfitRegexMatch.groups())
                flag_Sum_TakeProfit = 1
                Sum_TakeProfitRow = (linea.split("   ")[0],) + Sum_TakeProfitRegexMatch.groups() + ("Sum_TakeProfitRow",)
                # Reset all signal
                flag_Signal = flag_Signal2 = flag_Signal3 = flag_Signal4 = flag_Signal5 = flag_Signal6 = flag_Signal7 = flag_Signal8 = 0
                # print(Sum_TakeProfitRow)

            #TesterWithdrawal: previous balance = $14 959.35, current profit = $+6 669.68, withdrawal amount = $3 334.84! Next withdrawal is scheduled for 2022.07.01
            TesterWithdrawalRegex = re.compile(r'TesterWithdrawal: previous balance = \$([\+\-\ 0-9]*[.]?[0-9]*), current profit = \$([\+\-\ 0-9]*[.]?[0-9]*), withdrawal amount = \$([\+\-\ 0-9]*[.]?[0-9]*)! Next withdrawal is scheduled for (\d{4}\.\d{2}\.\d{2})')
            TesterWithdrawalRegexMatch = TesterWithdrawalRegex.search(mensaje)
            if TesterWithdrawalRegexMatch is not None:
                # print(TesterWithdrawalRegexMatch.groups())
                flag_TesterWithdrawal = 1
                TesterWithdrawalRow = (linea.split("   ")[0],) + TesterWithdrawalRegexMatch.groups() + ("TesterWithdrawalRow",)
                # print(TesterWithdrawalRow)

            #Buy-series with 3 orders reached BreakEven (1.07368 >= 1.07368)!
            #Sell-series with 4 orders reached BreakEven (1.08801 <= 1.08805)!
            orders_reached_BreakEvenRegex = re.compile(r'(Buy|Sell)-series with ([0-9]*) orders reached BreakEven \(([\+\-0-9]*[.]?[0-9]*) >= ([\+\-0-9]*[.]?[0-9]*)\)!')
            orders_reached_BreakEvenRegexMatch = orders_reached_BreakEvenRegex.search(mensaje)
            if orders_reached_BreakEvenRegexMatch is not None:
                # print(orders_reached_BreakEvenRegexMatch.groups())
                flag_orders_reached_BreakEven = 1
                orders_reached_BreakEvenRow = (linea.split("   ")[0],) + orders_reached_BreakEvenRegexMatch.groups() + ("orders_reached_BreakEvenRow",)
                # print(orders_reached_BreakEvenRow)

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
                    #SignalRow      #Signal to open buy #1 at 1.14034 (Stochastic K + IdentifyTrend + TDI)!
                    #marketRow      #market buy 0.1 EURUSD (1.14029 / 1.14034)
                    #               # deal #2 buy 0.1 EURUSD at 1.14034 done (based on order #2)
                    #               # deal performed [#2 buy 0.1 EURUSD at 1.14034]
                    #               # order performed buy 0.1 at 1.14034 [#2 buy 0.1 EURUSD at 1.14034]
                    #OrderSendRow   # |  OrderSend( EURUSD, buy, 0.10, 1.14034, 50, 0.00000, 0.00000, "CP #1", 3047 ) - OK! Ticket #2.
                    #               # https://docs.mql4.com/trading/ordersend
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
                    #Example 1 (1er example. Not completed)
                    #SignalRow2     # Signal to open buy #2 at 1843.330!
                    #marketRow      # market buy 0.12 XAUUSD (1842.830 / 1843.330)
                    #OrderSendRow   # |  OrderSend( XAUUSD, buy, 0.12, 1843.330, 50, 0.000, 0.000, "CP18.06.2021.21:03 #2", 234 ) - OK! Ticket #17.
                    #               # https://docs.mql4.com/trading/ordersend

                    #Example 2 (Real Example)
                    #SignalRow2     #Signal to open buy #2 at 1.11817!
                    #marketRow      #market buy 0.08 EURUSD (1.11811 / 1.11817)
                    #               #deal #111 buy 0.08 EURUSD at 1.11817 done (based on order #111)
                    #               #deal performed [#111 buy 0.08 EURUSD at 1.11817]
                    #               #order performed buy 0.08 at 1.11817 [#111 buy 0.08 EURUSD at 1.11817]
                    #OrderSendRow   #|  OrderSend( EURUSD, buy, 0.08, 1.11817, 50, 0.00000, 0.00000, "CP19.07.2021.00:25 #2", 235 ) - OK! Ticket #111.
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
                    #SignalRow3     # Signal to close buy (Stochastic K + MACD )!
                    #marketRow2     # market sell 0.15 EURUSD, close #251 (1.12740 / 1.12746)
                    #               # deal #252 sell 0.15 EURUSD at 1.12740 done (based on order #252)
                    #               # deal performed [#252 sell 0.15 EURUSD at 1.12740]
                    #               # order performed sell 0.15 at 1.12740 [#252 sell 0.15 EURUSD at 1.12740]
                    #OrderCloseRow  # |  OrderClose( 251, 0.15, 1.12740, 50 ) - OK!
                    #               # https://docs.mql4.com/trading/orderclose

                    #Other Options. Close 3 orders
                    #SignalRow3     # Signal to close sell (Stochastic K)!
                    #marketRow2     # market buy 0.15 EURUSD, close #30 (1.13429 / 1.13435)
                    #               # deal #31 buy 0.15 EURUSD at 1.13435 done (based on order #31)
                    #               # deal performed [#31 buy 0.15 EURUSD at 1.13435]
                    #               # order performed buy 0.15 at 1.13435 [#31 buy 0.15 EURUSD at 1.13435]
                    #OrderCloseRow  # |  OrderClose( 30, 0.15, 1.13435, 50 ) - OK!
                    #marketRow2     # market buy 0.1 EURUSD, close #29 (1.13429 / 1.13435)
                    #               # deal #32 buy 0.1 EURUSD at 1.13435 done (based on order #32)
                    #               # deal performed [#32 buy 0.1 EURUSD at 1.13435]
                    #               # order performed buy 0.1 at 1.13435 [#32 buy 0.1 EURUSD at 1.13435]
                    #OrderCloseRow  # |  OrderClose( 29, 0.10, 1.13435, 50 ) - OK!
                    #marketRow2     # market buy 0.07 EURUSD, close #18 (1.13429 / 1.13435)
                    #               # deal #33 buy 0.07 EURUSD at 1.13435 done (based on order #33)
                    #               # deal performed [#33 buy 0.07 EURUSD at 1.13435]
                    #               # order performed buy 0.07 at 1.13435 [#33 buy 0.07 EURUSD at 1.13435]
                    #OrderCloseRow  # |  OrderClose( 18, 0.07, 1.13435, 50 ) - OK!
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
                    #SignalRow4    #Signal to open AutoHedge for sell-order #1!
                    #marketRow     #market buy 1 USDCAD (1.20365 / 1.20384)
                    #              #deal #3 buy 1 USDCAD at 1.20384 done (based on order #3)
                    #              #deal performed [#3 buy 1 USDCAD at 1.20384]
                    #              #order performed buy 1 at 1.20384 [#3 buy 1 USDCAD at 1.20384]
                    #OrderSendRow  #|  OrderSend( USDCAD, buy, 1.0, 1.20384, 50, 0.00000, 0.00000, "ZIGZAG #H1", 2431 ) - OK! Ticket #3.
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
                    #SignalRow5     #Signal to open anti-martingale buy #2 at 1.22464!
                    #marketRow      #market buy 0.15 EURUSD (1.22450 / 1.22464)
                    #               #deal #13 buy 0.15 EURUSD at 1.22464 done (based on order #13)
                    #               #deal performed [#13 buy 0.15 EURUSD at 1.22464]
                    #               #order performed buy 0.15 at 1.22464 [#13 buy 0.15 EURUSD at 1.22464]
                    #OrderSendRow   # |  OrderSend( EURUSD, buy, 0.15, 1.22464, 50, 0.00000, 0.00000, "CP16.07.2021.16:19 #-2", 234 ) - OK! Ticket #13.
                    #               #https://docs.mql4.com/trading/ordersend
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

                    #SignalRow7         #Signal to open AutoHedge for sell-order #1!
                    #marketRow          #market buy 1 USDCAD (1.20365 / 1.20384)
                    #                   #deal #3 buy 1 USDCAD at 1.20384 done (based on order #3)
                    #                   #deal performed [#3 buy 1 USDCAD at 1.20384]
                    #                   #order performed buy 1 at 1.20384 [#3 buy 1 USDCAD at 1.20384]
                    #OrderSendRow       #|  OrderSend( USDCAD, buy, 1.0, 1.20384, 50, 0.00000, 0.00000, "ZIGZAG #H1", 2431 ) - OK! Ticket #3.
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
                    #SignalRow8             # Signal to delete pending buy-order (indicator)!
                    #order_canceledRow      # order canceled [#2 buy stop 0.1 EURUSD at 1.13532]
                    #OrderDeleteRow         # |  OrderDelete( 2 ) - OK!
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
                        print("Error in Script. Check Log!! Critical error-9")
                        exit()

            #Global Account TakeProfit has been reached ($10.93 >= $10.00)!
            if ((len(GA_TakeProfitRow) and len(marketRow2) and len(OrderCloseRow)) and (GA_TakeProfitRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_GA_TakeProfit == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #GA_TakeProfitRow      #Global Account TakeProfit has been reached ($10.93 >= $10.00)!
                    #marketRow2             #market buy 1.34 EURUSD, close #19 (1.11413 / 1.11416)
                    #                       #deal #20 buy 1.34 EURUSD at 1.11416 done (based on order #20)
                    #                       #deal performed [#20 buy 1.34 EURUSD at 1.11416]
                    #                       #order performed buy 1.34 at 1.11416 [#20 buy 1.34 EURUSD at 1.11416]
                    #OrderCloseRow          #|  OrderClose( 19, 1.34, 1.11416, 50 ) - OK!
                    #marketRow2             #market sell 0.24 EURUSD, close #18 (1.11413 / 1.11416)
                    #                       #deal #21 sell 0.24 EURUSD at 1.11413 done (based on order #21)
                    #                       #deal performed [#21 sell 0.24 EURUSD at 1.11413]
                    #                       #order performed sell 0.24 at 1.11413 [#21 sell 0.24 EURUSD at 1.11413]
                    #OrderCloseRow          #|  OrderClose( 18, 0.24, 1.11413, 50 ) - OK!
                    #marketRow2             #market sell 0.15 EURUSD, close #17 (1.11413 / 1.11416)
                    #                       #deal #22 sell 0.15 EURUSD at 1.11413 done (based on order #22)
                    #                       #deal performed [#22 sell 0.15 EURUSD at 1.11413]
                    #                       #order performed sell 0.15 at 1.11413 [#22 sell 0.15 EURUSD at 1.11413]
                    #OrderCloseRow          #|  OrderClose( 17, 0.15, 1.11413, 50 ) - OK!
                    #marketRow2             #market buy 0.07 EURUSD, close #16 (1.11413 / 1.11416)
                    #                       #deal #23 buy 0.07 EURUSD at 1.11416 done (based on order #23)
                    #                       #deal performed [#23 buy 0.07 EURUSD at 1.11416]
                    #                       #order performed buy 0.07 at 1.11416 [#23 buy 0.07 EURUSD at 1.11416]
                    #OrderCloseRow          #|  OrderClose( 16, 0.07, 1.11416, 50 ) - OK!
                    #marketRow2             #market sell 0.1 EURUSD, close #15 (1.11413 / 1.11416)
                    #                       #deal #24 sell 0.1 EURUSD at 1.11413 done (based on order #24)
                    #                       #deal performed [#24 sell 0.1 EURUSD at 1.11413]
                    #                       #order performed sell 0.1 at 1.11413 [#24 sell 0.1 EURUSD at 1.11413]
                    #OrderCloseRow          #|  OrderClose( 15, 0.10, 1.11413, 50 ) - OK!
                    #marketRow2             #market sell 0.07 EURUSD, close #14 (1.11413 / 1.11416)
                    #                       #deal #25 sell 0.07 EURUSD at 1.11413 done (based on order #25)
                    #                       #deal performed [#25 sell 0.07 EURUSD at 1.11413]
                    #                       #order performed sell 0.07 at 1.11413 [#25 sell 0.07 EURUSD at 1.11413]
                    #OrderCloseRow          #|  OrderClose( 14, 0.07, 1.11413, 50 ) - OK!
                    # <----->buy<----->
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[7] == OrderCloseRow[3]):
                        StartEquity=GA_TakeProfitRow[1]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TakeProfitRow[2]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TakeProfitRow[0],
                            'Action': 'Global Account TakeProfit',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TakeProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    # <----->sell<----->
                    elif (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[6] == OrderCloseRow[3]):
                        StartEquity=GA_TakeProfitRow[1]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TakeProfitRow[2]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TakeProfitRow[0],
                            'Action': 'Global Account TakeProfit',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TakeProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-10")
                        exit()

            #Global Account TakeProfit (1.00%) has been reached ($518.16 >= $503.97)!
            if ((len(GA_TakeProfitRow2) and len(marketRow2) and len(OrderCloseRow)) and (GA_TakeProfitRow2[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_GA_TakeProfit2 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #GA_TakeProfitRow2     #Global Account TakeProfit (1.00%) has been reached ($518.16 >= $503.97)!
                    #marketRow2             #market sell 8.2 EURUSD, close #36 (1.13011 / 1.13027)
                    #                       #deal #28 sell 8.2 EURUSD at 1.13011 done (based on order #37)
                    #                       #deal performed [#28 sell 8.2 EURUSD at 1.13011]
                    #                       #order performed sell 8.2 at 1.13011 [#37 sell 8.2 EURUSD at 1.13011]
                    #OrderCloseRow          #|  OrderClose( 36, 8.2, 1.13011, 50 ) - OK!
                    #marketRow2             #market sell 4.68 EURUSD, close #35 (1.13011 / 1.13027)
                    #                       #deal #29 sell 4.68 EURUSD at 1.13011 done (based on order #38)
                    #                       #deal performed [#29 sell 4.68 EURUSD at 1.13011]
                    #                       #order performed sell 4.68 at 1.13011 [#38 sell 4.68 EURUSD at 1.13011]
                    #OrderCloseRow          #|  OrderClose( 35, 4.68, 1.13011, 50 ) - OK!
                    #marketRow2             #market sell 2.67 EURUSD, close #34 (1.13011 / 1.13027)
                    #                       #deal #30 sell 2.67 EURUSD at 1.13011 done (based on order #39)
                    #                       #deal performed [#30 sell 2.67 EURUSD at 1.13011]
                    #                       #order performed sell 2.67 at 1.13011 [#39 sell 2.67 EURUSD at 1.13011]
                    #OrderCloseRow          #|  OrderClose( 34, 2.67, 1.13011, 50 ) - OK!
                    #marketRow2             #market sell 1.53 EURUSD, close #33 (1.13011 / 1.13027)
                    #                       #deal #31 sell 1.53 EURUSD at 1.13011 done (based on order #40)
                    #                       #deal performed [#31 sell 1.53 EURUSD at 1.13011]
                    #                       #order performed sell 1.53 at 1.13011 [#40 sell 1.53 EURUSD at 1.13011]
                    #OrderCloseRow          #|  OrderClose( 33, 1.53, 1.13011, 50 ) - OK!
                    #marketRow2             #market sell 0.87 EURUSD, close #32 (1.13011 / 1.13027)
                    #                       #deal #32 sell 0.87 EURUSD at 1.13011 done (based on order #41)
                    #                       #deal performed [#32 sell 0.87 EURUSD at 1.13011]
                    #                       #order performed sell 0.87 at 1.13011 [#41 sell 0.87 EURUSD at 1.13011]
                    #OrderCloseRow          #|  OrderClose( 32, 0.87, 1.13011, 50 ) - OK!
                    #marketRow2             #market sell 0.5 EURUSD, close #31 (1.13011 / 1.13027)
                    #                       #deal #33 sell 0.5 EURUSD at 1.13011 done (based on order #42)
                    #                       #deal performed [#33 sell 0.5 EURUSD at 1.13011]
                    #                       #order performed sell 0.5 at 1.13011 [#42 sell 0.5 EURUSD at 1.13011]
                    #OrderCloseRow          #|  OrderClose( 31, 0.5, 1.13011, 50 ) - OK!
                    # <----->buy<----->
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[7] == OrderCloseRow[3]):
                        StartEquity=GA_TakeProfitRow2[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TakeProfitRow2[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TakeProfitRow2[0],
                            'Action': f'Global Account TakeProfit {GA_TakeProfitRow2[1]}%',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    # <----->sell<----->
                    elif (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[6] == OrderCloseRow[3]):
                        StartEquity=GA_TakeProfitRow2[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TakeProfitRow2[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TakeProfitRow2[0],
                            'Action': f'Global Account TakeProfit {GA_TakeProfitRow2[1]}%',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-11")
                        exit()


            #Global Account TargetProfit ($1.00) has been reached ($50 592.19 -> $50 594.69)!
            if ((len(GA_TargetProfitRow) and len(marketRow2) and len(OrderCloseRow)) and (GA_TargetProfitRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_GA_TargetProfit == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #GA_TargetProfitRow     #Global Account TargetProfit ($1.00) has been reached ($50 592.19 -> $50 594.69)!
                    #marketRow2             #market buy 0.5 EURUSD, close #887 (1.07284 / 1.07300)
                    #                       #deal #747 buy 0.5 EURUSD at 1.07300 done (based on order #888)
                    #                       #deal performed [#747 buy 0.5 EURUSD at 1.07300]
                    #                       #order performed buy 0.5 at 1.07300 [#888 buy 0.5 EURUSD at 1.07300]
                    #OrderCloseRow          #|  OrderClose( 887, 0.5, 1.07300, 50 ) - OK!
                    # <----->buy<----->
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[7] == OrderCloseRow[3]):
                        StartEquity=GA_TargetProfitRow[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TargetProfitRow[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TargetProfitRow[0],
                            'Action': f'Global Account TargetProfit ${GA_TargetProfitRow[1]}',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    # <----->sell<----->
                    elif (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[6] == OrderCloseRow[3]):
                        StartEquity=GA_TargetProfitRow[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TargetProfitRow[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TargetProfitRow[0],
                            'Action': f'Global Account TargetProfit ${GA_TargetProfitRow[1]}',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-12")
                        exit()

            #Global Account TargetProfit (1.00%) has been reached ($92 541.58 -> $93 513.54)!
            if ((len(GA_TargetProfitRow2) and len(marketRow2) and len(OrderCloseRow)) and (GA_TargetProfitRow2[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_GA_TargetProfit2 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #GA_TargetProfitRow2    #Global Account TargetProfit ($1.00) has been reached ($50 592.19 -> $50 594.69)!
                    #marketRow2             #market buy 0.5 EURUSD, close #887 (1.07284 / 1.07300)
                    #                       #deal #747 buy 0.5 EURUSD at 1.07300 done (based on order #888)
                    #                       #deal performed [#747 buy 0.5 EURUSD at 1.07300]
                    #                       #order performed buy 0.5 at 1.07300 [#888 buy 0.5 EURUSD at 1.07300]
                    #OrderCloseRow          #|  OrderClose( 887, 0.5, 1.07300, 50 ) - OK!
                    # <----->buy<----->
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[7] == OrderCloseRow[3]):
                        StartEquity=GA_TargetProfitRow2[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TargetProfitRow2[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TargetProfitRow2[0],
                            'Action': f'Global Account TargetProfit {GA_TargetProfitRow2}%',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    # <----->sell<----->
                    elif (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[6] == OrderCloseRow[3]):
                        StartEquity=GA_TargetProfitRow2[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TargetProfitRow2[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TargetProfitRow2[0],
                            'Action': f'Global Account TargetProfit {GA_TargetProfitRow2}%',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-13")
                        exit()

            #GlobalAccount TrailingStop ($10.00) activated, start equity = $50 001.85, current equity = $50 011.85...
            if (len(GA_TrailingStopActivatedRow)):
                if (flag_GA_TrailingStopActivated == 1):

                    StartEquity=GA_TrailingStopActivatedRow[2]
                    StartEquity=StartEquity.replace("+", "")
                    StartEquity=StartEquity.replace(" ", "")

                    CurrentEquity=GA_TrailingStopActivatedRow[3]
                    CurrentEquity=CurrentEquity.replace("+", "")
                    CurrentEquity=CurrentEquity.replace(" ", "")

                    csv_row.append({'Time': GA_TrailingStopActivatedRow[0],
                        'Action': f'Global Account TrailingStop ${GA_TrailingStopActivatedRow2[1]} activated',
                        'StartEquity': StartEquity,
                        'CurrentEquity': CurrentEquity})
                    GA_TrailingStopActivatedRow = tuple()
                    flag_GA_TrailingStopActivated = 0
                    continue

            #GlobalAccount TrailingStop (1.00%) activated, start equity = $90 936.95, current equity = $91 889.20...
            if (len(GA_TrailingStopActivatedRow2)):
                if (flag_GA_TrailingStopActivated2 == 1):

                    StartEquity=GA_TrailingStopActivatedRow2[2]
                    StartEquity=StartEquity.replace("+", "")
                    StartEquity=StartEquity.replace(" ", "")

                    CurrentEquity=GA_TrailingStopActivatedRow2[3]
                    CurrentEquity=CurrentEquity.replace("+", "")
                    CurrentEquity=CurrentEquity.replace(" ", "")

                    csv_row.append({'Time': GA_TrailingStopActivatedRow2[0],
                        'Action': f'Global Account TrailingStop {GA_TrailingStopActivatedRow2[1]}% activated',
                        'StartEquity': StartEquity,
                        'CurrentEquity': CurrentEquity})
                    GA_TrailingStopActivatedRow2 = tuple()
                    flag_GA_TrailingStopActivated2 = 0
                    continue

            #Global Account TrailingStop ($10.00) has been reached (max equity = $50 012.85, current equity = $50 002.85)!
            if ((len(GA_TrailingStopRow) and len(marketRow2) and len(OrderCloseRow)) and (GA_TrailingStopRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_GA_TrailingStop == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #GA_TrailingStopRow     #Global Account TrailingStop ($1.00) has been reached (max equity = $50 221.18, current equity = $50 218.68)!
                    #marketRow2             #market buy 0.5 EURUSD, close #885 (1.07215 / 1.07240)
                    #                       #deal #745 buy 0.5 EURUSD at 1.07240 done (based on order #886)
                    #                       #deal performed [#745 buy 0.5 EURUSD at 1.07240]
                    #                       #order performed buy 0.5 at 1.07240 [#886 buy 0.5 EURUSD at 1.07240]
                    #OrderCloseRow          #|  OrderClose( 885, 0.5, 1.07240, 50 ) - OK!
                    # <----->buy<----->
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[7] == OrderCloseRow[3]):
                        StartEquity=GA_TrailingStopRow[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TrailingStopRow[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TrailingStopRow[0],
                            'Action': f'Global Account TrailingStop ${GA_TrailingStopRow[1]}',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TrailingStop',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    # <----->sell<----->
                    elif (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[6] == OrderCloseRow[3]):
                        StartEquity=GA_TrailingStopRow[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TrailingStopRow[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TrailingStopRow[0],
                            'Action': f'Global Account TargetProfit ${GA_TrailingStopRow[1]})',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in Script. Check Log!! Critical error-14")
                        exit()

            #Global Account TrailingStop (1.00%) has been reached (max equity = $51 486.68, current equity = $50 951.63)!
            if ((len(GA_TrailingStopRow2) and len(marketRow2) and len(OrderCloseRow)) and (GA_TrailingStopRow2[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_GA_TrailingStop2 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #GA_TrailingStopRow2    #Global Account TrailingStop (1.00%) has been reached (max equity = $92 074.00, current equity = $91 131.52)!
                    #marketRow2             #market buy 8.44 EURUSD, close #1071 (1.07091 / 1.07116)
                    #                       #deal #951 buy 8.44 EURUSD at 1.07116 done (based on order #1072)
                    #                       #deal performed [#951 buy 8.44 EURUSD at 1.07116]
                    #                       #order performed buy 8.44 at 1.07116 [#1072 buy 8.44 EURUSD at 1.07116]
                    #OrderCloseRow          #|  OrderClose( 1071, 8.44, 1.07116, 50 ) - OK!
                    # <----->buy<----->
                    if (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[7] == OrderCloseRow[3]):
                        StartEquity=GA_TrailingStopRow2[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TrailingStopRow2[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TrailingStopRow2[0],
                            'Action': f'Global Account TrailingStop {GA_TrailingStopRow2[1]}%',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TrailingStop',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
                            'Status': OrderCloseRow[5],
                            'Ticket #': OrderCloseRow[1]})
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    # <----->sell<----->
                    elif (str(round(float(marketRow2[2]),2)) == str(round(float(OrderCloseRow[2]),2))) and (marketRow2[5] == OrderCloseRow[1]) and (marketRow2[6] == OrderCloseRow[3]):
                        StartEquity=GA_TrailingStopRow2[2]
                        StartEquity=StartEquity.replace("+", "")
                        StartEquity=StartEquity.replace(" ", "")

                        CurrentEquity=GA_TrailingStopRow2[3]
                        CurrentEquity=CurrentEquity.replace("+", "")
                        CurrentEquity=CurrentEquity.replace(" ", "")

                        csv_row.append({'Time': GA_TrailingStopRow2[0],
                            'Action': f'Global Account TargetProfit {GA_TrailingStopRow2[1]}%',
                            'Type': marketRow2[1],
                            'Signal': 'Global Account TargetProfit',
                            'Symbol': marketRow2[3],
                            'Volume': marketRow2[2],
                            'PriceAction': OrderCloseRow[3],
                            'StartEquity': StartEquity,
                            'CurrentEquity': CurrentEquity,
                            'Slippage': OrderCloseRow[4],
                            'Value1': marketRow2[6],
                            'Value2': marketRow2[7],
                            'TakeProfit': OrderCloseRow[3],
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


            # Modifying SL for sell-order #86: 0.00000 -> 1.17551...
            # Modifying TP for sell-order #437: 0.00000 -> 1.19366...
            if ((len(ModifyingRow) and len(position_modifiedRow) and len(OrderModifyRow)) and (ModifyingRow[0] == position_modifiedRow[0]) and (position_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_Modifying == 1) and (flag_position_modified == 1) and (flag_OrderModify == 1)):
                    #ModifyingRow           # Modifying SL for sell-order #86: 0.00000 -> 1.17551...
                    #position_modifiedRow   # position modified [#86 sell 0.1 EURUSD 1.14135 sl: 1.17551]
                    #OrderModifyRow         # |  OrderModify( 86, 1.14135, 1.17551, 0.00000 ) - OK!
                    #                       # https://docs.mql4.com/trading/ordermodify

                    #ModifyingRow           # Modifying TP for buy-order #111: 0.00000 -> 1.12231...
                    #position_modifiedRow   # position modified [#111 buy 0.08 EURUSD 1.11817 sl: 1.08607 tp: 1.12231]
                    #OrderModifyRow         # |  OrderModify( 111, 1.11817, 1.08607, 1.12231 ) - OK!
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
                        print("Error in Script. Check Log!! Critical error-16")
                        continue
                        # exit()


            #Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
            if ((len(MovingRow) and len(order_modifiedRow) and len(OrderModifyRow)) and (MovingRow[0] == order_modifiedRow[0]) and (order_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_Moving == 1) and (flag_order_modified == 1) and (flag_OrderModify == 1)):
                    #MovingRow              # Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
                    #order_modifiedRow      # order modified [#10 buy stop 1.01 EURUSD at 1.15179]
                    #OrderModifyRow         # |  OrderModify( 10, 1.15179, 0.00000, 0.00000 ) - OK!
                    #                       # https://docs.mql4.com/trading/ordermodify
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
                        print("Error in Script. Check Log!! Critical error-17")
                        exit()

            # Partial close hedge: closing 1 profit order ($+76.85) + 1 opposite loss order ($-75.77) with total profit $+1.08!
            if ((len(Partial_closeRow) and len(marketRow2) and len(OrderCloseRow)) and ( (Partial_closeRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0]))):
                if ((flag_Partial_close == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    total_close_order=int(Partial_closeRow[1]) + int(Partial_closeRow[3])
                    #Example Partial Close hedge
                    #Partial_closeRow    #Partial close hedge: closing 1 profit order ($+76.85) + 1 opposite loss order ($-75.77) with total profit $+1.08!
                    #marketRow2          #market sell 0.08 EURUSD, close #24 (1.10916 / 1.10920)
                    #                    #deal #28 sell 0.08 EURUSD at 1.10916 done (based on order #28)
                    #                    #deal performed [#28 sell 0.08 EURUSD at 1.10916]
                    #                    #order performed sell 0.08 at 1.10916 [#28 sell 0.08 EURUSD at 1.10916]
                    #OrderCloseRow       #|  OrderClose( 24, 0.08, 1.10916, 50 ) - OK!
                    #marketRow2          #market buy 0.26 EURUSD, close #27 (1.10916 / 1.10920)
                    #                    #deal #29 buy 0.26 EURUSD at 1.10920 done (based on order #29)
                    #                    #deal performed [#29 buy 0.26 EURUSD at 1.10920]
                    #                    #order performed buy 0.26 at 1.10920 [#29 buy 0.26 EURUSD at 1.10920]
                    #OrderCloseRow       #|  OrderClose( 27, 0.26, 1.10920, 50 ) - OK!

                    #Partial_closeRow    #Partial close hedge: closing 1 profit order ($+15.84) + 1 opposite loss order ($-0.04) with total profit $+15.80!
                    #marketRow2          #market sell 0.04 EURUSD, close #9 (1.09592 / 1.09597)
                    #                    #deal #10 sell 0.04 EURUSD at 1.09592 done (based on order #10)
                    #                    #deal performed [#10 sell 0.04 EURUSD at 1.09592]
                    #                    #order performed sell 0.04 at 1.09592 [#10 sell 0.04 EURUSD at 1.09592]
                    #OrderCloseRow       #|  OrderClose( 9, 0.04, 1.09592, 50 ) - OK!
                    #marketRow2          #market buy 0.08 EURUSD, close #6 (1.09592 / 1.09597)
                    #                    #deal #11 buy 0.08 EURUSD at 1.09597 done (based on order #11)
                    #                    #deal performed [#11 buy 0.08 EURUSD at 1.09597]
                    #                    #order performed buy 0.08 at 1.09597 [#11 buy 0.08 EURUSD at 1.09597]
                    #OrderCloseRow       #|  OrderClose( 6, 0.08, 1.09597, 50 ) - OK!
                    if close_order < total_close_order:
                        close_order = close_order + 1
                        if (marketRow2[5] == OrderCloseRow[1]):
                            csv_row.append({'Time': Partial_closeRow[0],
                                'Action': f'Partial close hedge profit {Partial_closeRow[1]} + loss {Partial_closeRow[3]}',
                                'Type': marketRow2[1],
                                'Signal': 'Partial close hedge',
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
                            print("Error in Script. Check Log!! Critical error-18")
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
                    #Partial_closeRow2      #Partial close any: closing 2 profit orders ($+266.05) + 1 loss order ($-166.00) with total profit $+100.05!
                    #marketRow2             #market buy 1.33 EURUSD, close #21 (1.12973 / 1.12990)
                    #                       # deal #22 buy 1.33 EURUSD at 1.12990 done (based on order #22)
                    #                       #deal performed [#22 buy 1.33 EURUSD at 1.12990]
                    #                       #order performed buy 1.33 at 1.12990 [#22 buy 1.33 EURUSD at 1.12990]
                    #OrderCloseRow          #|  OrderClose( 21, 1.3300000000000001, 1.12990, 50 ) - OK!
                    #marketRow2             #market buy 1.21 EURUSD, close #20 (1.12973 / 1.12990)
                    #                       #deal #23 buy 1.21 EURUSD at 1.12990 done (based on order #23)
                    #                       #deal performed [#23 buy 1.21 EURUSD at 1.12990]
                    #                       #order performed buy 1.21 at 1.12990 [#23 buy 1.21 EURUSD at 1.12990]
                    #OrderCloseRow          #|  OrderClose( 20, 1.21, 1.12990, 50 ) - OK!
                    #marketRow2             #market buy 1 EURUSD, close #18 (1.12973 / 1.12990)
                    #                       #deal #24 buy 1 EURUSD at 1.12990 done (based on order #24)
                    #                       #deal performed [#24 buy 1 EURUSD at 1.12990]
                    #                       #order performed buy 1 at 1.12990 [#24 buy 1 EURUSD at 1.12990]
                    #OrderCloseRow          #|  OrderClose( 18, 1.0, 1.12990, 50 ) - OK!
                    if (marketRow2[5] == OrderCloseRow[1]):
                        csv_row.append({'Time': Partial_closeRow2[0],
                            'Action': f'Partial close any profit {Partial_closeRow2[1]} + loss {Partial_closeRow2[3]}',
                            'Type': marketRow2[1],
                            'Signal': 'Partial close',
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
                        print("Error in Script. Check Log!! Critical error-19")
                        exit()


            #Partial close for SELL-series: closing 3 profit orders ($+110.17) + 1 loss order ($-104.10) with total profit $+6.07!
            if ((len(Partial_closeRow3) and len(marketRow2) and len(OrderCloseRow)) and ((Partial_closeRow3[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0]) and (marketRow2[5] == OrderCloseRow[1]))):
                if ((flag_Partial_close3 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    total_close_order3=int(Partial_closeRow3[2]) + int(Partial_closeRow3[4])
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
                            'Signal': 'Partial close',
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
                        print("Error in Script. Check Log!! Critical error-20")
                        exit()


            #Sum TakeProfit ($1.00) has been reached ($1.52 >= $1.00)!
            if ((len(Sum_TakeProfitRow) and len(marketRow2) and len(OrderCloseRow)) and ((Sum_TakeProfitRow[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0]) and (marketRow2[5] == OrderCloseRow[1]))):
                if ((flag_Sum_TakeProfit == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #Sum_TakeProfitRow  #Sum TakeProfit ($1.00) has been reached ($1.52 >= $1.00)!
                    #marketRow2         #market sell 0.3 XAUUSD, close #28 (1921.370 / 1921.780)
                    #                   #deal #29 sell 0.3 XAUUSD at 1921.370 done (based on order #29)
                    #                   #deal performed [#29 sell 0.3 XAUUSD at 1921.370]
                    #                   #order performed sell 0.3 at 1921.370 [#29 sell 0.3 XAUUSD at 1921.370]
                    #OrderCloseRow      #|  OrderClose( 28, 0.3, 1921.370, 50 ) - OK!
                    #marketRow2         #market sell 0.17 XAUUSD, close #27 (1921.370 / 1921.780)
                    #                   #deal #30 sell 0.17 XAUUSD at 1921.370 done (based on order #30)
                    #                   #deal performed [#30 sell 0.17 XAUUSD at 1921.370]
                    #                   #order performed sell 0.17 at 1921.370 [#30 sell 0.17 XAUUSD at 1921.370]
                    #OrderCloseRow      #|  OrderClose( 27, 0.17, 1921.370, 50 ) - OK!
                    #marketRow2         #market sell 0.1 XAUUSD, close #26 (1921.370 / 1921.780)
                    #                   #deal #31 sell 0.1 XAUUSD at 1921.370 done (based on order #31)
                    #                   #deal performed [#31 sell 0.1 XAUUSD at 1921.370]
                    #                   #order performed sell 0.1 at 1921.370 [#31 sell 0.1 XAUUSD at 1921.370]
                    #OrderCloseRow      #|  OrderClose( 26, 0.1, 1921.370, 50 ) - OK!
                    if (marketRow2[5] == OrderCloseRow[1]):
                        csv_row.append({'Time': Sum_TakeProfitRow[0],
                            'Action': f'Sum TakeProfit {Sum_TakeProfitRow[1]} has been reached {Sum_TakeProfitRow[2]} >= {Sum_TakeProfitRow[3]}',
                            'Type': marketRow2[1],
                            'Signal': 'Sum TakeProfit',
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
                        print("Error in Script. Check Log!! Critical error-21")
                        exit()

            if (len(TrailingStopRow)):
                if (flag_TrailingStop == 1):
                    #GA_TakeProfitRow   # TrailingStop for BUY: 1.13446 -> 1.13553

                    #GA_TakeProfitRow   # TrailingStop for SELL: 0 -> 1.13679
                    # https://www.metatrader4.com/es/trading-platform/help/positions/trailing
                    csv_row.append({'Time': TrailingStopRow[0],
                        'Action': f'TrailingStop for {TrailingStopRow[1].lower()}',
                        'Type': TrailingStopRow[1].lower(),
                        'PriceAction': TrailingStopRow[2],
                        'StopLoss': TrailingStopRow[3]})
                    TrailingStopRow = tuple()
                    flag_TrailingStop = 0
                    continue

            #TesterWithdrawal: previous balance = $14 959.35, current profit = $+6 669.68, withdrawal amount = $3 334.84! Next withdrawal is scheduled for 2022.07.01
            if (len(TesterWithdrawalRow)):
                if (flag_TesterWithdrawal == 1):
                    #TesterWithdrawalRow    #TesterWithdrawal: previous balance = $14 959.35, current profit = $+6 669.68, withdrawal amount = $3 334.84! Next withdrawal is scheduled for 2022.07.01
                    #                       #deal #838 balance -3334.84 [withdrawal] done
                    profit=TesterWithdrawalRow[2]
                    profit=profit.replace("+", "")
                    profit=profit.replace(" ", "")

                    value1=TesterWithdrawalRow[1]
                    value1=value1.replace("+", "")
                    value1=value1.replace(" ", "")

                    value2=TesterWithdrawalRow[3]
                    value2=value2.replace("+", "")
                    value2=value2.replace(" ", "")

                    csv_row.append({'Time': TesterWithdrawalRow[0],
                        'Action': 'TesterWithdrawal',
                        'Profit': profit,
                        'Value1': value1,
                        'Value2': value2})
                    TesterWithdrawalRow = tuple()
                    flag_TesterWithdrawal = 0
                    continue

            #Buy-series with 3 orders reached BreakEven (1.07368 >= 1.07368)!
            #Sell-series with 4 orders reached BreakEven (1.08801 <= 1.08805)!
            if (len(orders_reached_BreakEvenRow)):
                if (flag_orders_reached_BreakEven == 1):
                    #orders_reached_BreakEvenRow    #Sell-series with 4 orders reached BreakEven (1.10217 <= 1.10221)!

                    #orders_reached_BreakEvenRow    #Buy-series with 3 orders reached BreakEven (1.07368 >= 1.07368)!
                    csv_row.append({'Time': orders_reached_BreakEvenRow[0],
                        'Action': f'{orders_reached_BreakEvenRow[2]} orders reached BreakEven',
                        'Type': orders_reached_BreakEvenRow[1].lower(),
                        'Value1': orders_reached_BreakEvenRow[3],
                        'Value2': orders_reached_BreakEvenRow[4]})
                    orders_reached_BreakEvenRow = tuple()
                    flag_orders_reached_BreakEven = 0
                    continue


            # https://www.metatrader4.com/en/trading-platform/help/positions/orders
            # CHECK THIS IF WORKING
            if (len(stop_loss_triggeredRow)):
                if (flag_stop_loss_triggered == 1):
                    #stop_loss_triggeredRow  # stop loss triggered #7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326 [#8 buy 1 XAUUSD at 1881.920]
                    #                        # deal #8 buy 1 XAUUSD at 1902.500 done (based on order #8)
                    #                        # deal performed [#8 buy 1 XAUUSD at 1902.500]
                    #                        # order performed buy 1 at 1902.500 [#8 buy 1 XAUUSD at 1881.920]
                    csv_row.append({'Time': stop_loss_triggeredRow[0],
                        'Action': f'stop loss triggered1' ,
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
                    print("Error in Script. Check Log!! Critical error-18")
                    exit()


            # stop loss triggered #3 sell 0.1 EURUSD 1.13731 sl: 1.13475 [#4 buy 0.1 EURUSD at 1.13475]
            if ((len(stop_loss_triggeredRow2)) and ((stop_loss_triggeredRow2[3] == stop_loss_triggeredRow2[9]) and (stop_loss_triggeredRow2[4] == stop_loss_triggeredRow2[10]) and (stop_loss_triggeredRow2[6] == stop_loss_triggeredRow2[11]))):
                if (flag_stop_loss_triggered2 == 1):
                    #stop_loss_triggeredRow2    #stop loss triggered #3 sell 0.1 EURUSD 1.13731 sl: 1.13475 [#4 buy 0.1 EURUSD at 1.13475]
                    #                           #deal #4 buy 0.1 EURUSD at 1.13475 done (based on order #4)
                    #                           #deal performed [#4 buy 0.1 EURUSD at 1.13475]
                    #                           #order performed buy 0.1 at 1.13475 [#4 buy 0.1 EURUSD at 1.13475]
                    csv_row.append({'Time': stop_loss_triggeredRow2[0],
                        'Action': f'stop loss triggered2' ,
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
                    print("Error in Script. Check Log!! Critical error-19")
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

                    flag_Signal = 0
                    flag_Signal2 = 0
                    flag_Signal3 = 0
                    flag_Signal4 = 0
                    flag_Signal5 = 0
                    flag_Signal6 = 0
                    flag_Signal7 = 0
                    flag_Signal8 = 0
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
                    flag_GA_TakeProfit = 0
                    flag_Partial_close = 0
                    flag_Partial_close2 = 0
                    flag_Partial_close3 = 0
                    flag_Slippages = 0
                    flag_TesterWithdrawal = 0
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
                    TesterWithdrawalRow = ()
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
                    GA_TakeProfitRow = ()
                    calculate_profitRow = ()
                    Partial_closeRow = ()
                    Partial_closeRow2 = ()
                    Partial_closeRow3 = ()
                    SlippagesRow = ()
                    close_order = 0
                    close_order2 = 0
                    close_order3 = 0
                else:
                    print("Error in Script. Check Log!! Critical error-20")
                    exit()
    else:
        if flag_Magic:
            if (linea.split(" ")[0] == "final") and (linea.split(" ")[1] == "balance"):
                # final balance 4.99 USD
                csv_row.append({'Time': linea.split(" ")[0] + " " + linea.split(" ")[1] + " " + linea.split(" ")[2] + " " + linea.split(" ")[3]})
                flag_Magic = 0
            if (linea.split(" ")[0] == "stop") and (linea.split(" ")[1] == "out") and (linea.split(" ")[2] == "occurred"):
                # stop out occurred on 0% of testing interval
                csv_row.append({'Time': linea.split(" ")[0] + " " + linea.split(" ")[1] + " " + linea.split(" ")[2]})
                flag_Magic = 0


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
    exit()

read_file = pd.read_csv (csv_file, delimiter=";")
writer = pd.ExcelWriter (excel_file, engine='xlsxwriter')
read_file.to_excel (writer, sheet_name='Sheet1', index = None, header = True)

workbook = writer.book
worksheet = workbook.add_worksheet()
worksheet = workbook.get_worksheet_by_name('Sheet2')

worksheet1 = workbook.get_worksheet_by_name('Sheet1')
worksheet1.autofilter('A1:V1')
worksheet1.freeze_panes(1, 0)

rowCount = worksheet1.dim_rowmax

bold = workbook.add_format({'bold': True})

worksheet.write('B1', 'Sum', bold)
worksheet.write('C1', 'Min', bold)
worksheet.write('D1', 'Max', bold)
worksheet.write('E1', 'Count', bold)
worksheet.write('F1', 'Average', bold)
worksheet.write('G1', 'Count #1', bold)
worksheet.write('H1', 'Count #2', bold)
worksheet.write('I1', 'Count #3', bold)
worksheet.write('J1', 'Count #4', bold)
worksheet.write('K1', 'Count #5', bold)
worksheet.write('L1', 'Count #6', bold)
worksheet.write('M1', 'Count #7', bold)
worksheet.write('N1', 'Count #8', bold)
worksheet.write('O1', 'Count #9', bold)
worksheet.write('P1', 'Count #10', bold)


worksheet.write('A2', 'Martingale', bold)
worksheet.write('A3', 'Volume', bold)

#Martingale
worksheet.write_formula('B2', '=SUM(Sheet1!D3:D' + str(rowCount) + ')')
worksheet.write_formula('C2', '=MIN(Sheet1!D3:D' + str(rowCount) + ')')
worksheet.write_formula('D2', '=MAX(Sheet1!D3:D' + str(rowCount) + ')')
worksheet.write_formula('E2', '=COUNT(Sheet1!D3:D' + str(rowCount) + ')')
worksheet.write_formula('F2', '=AVERAGE(Sheet1!D3:D' + str(rowCount) + ')')
worksheet.write_formula('G2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',1)')
worksheet.write_formula('H2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',2)')
worksheet.write_formula('I2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',3)')
worksheet.write_formula('J2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',4)')
worksheet.write_formula('K2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',5)')
worksheet.write_formula('L2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',6)')
worksheet.write_formula('M2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',7)')
worksheet.write_formula('N2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',8)')
worksheet.write_formula('O2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',9)')
worksheet.write_formula('P2', '=COUNTIF(Sheet1!D3:D' + str(rowCount) + ',10)')



#Volume
worksheet.write_formula('B3', '=SUM(Sheet1!G3:G' + str(rowCount) + ')')
worksheet.write_formula('C3', '=MIN(Sheet1!G3:G' + str(rowCount) + ')')
worksheet.write_formula('D3', '=MAX(Sheet1!G3:G' + str(rowCount) + ')')
worksheet.write_formula('E3', '=COUNT(Sheet1!G3:G' + str(rowCount) + ')')
worksheet.write_formula('F3', '=AVERAGE(Sheet1!G3:G' + str(rowCount) + ')')

workbook.close()

print("Finish. Opening file...")
print(excel_file)
os.startfile(excel_file)
