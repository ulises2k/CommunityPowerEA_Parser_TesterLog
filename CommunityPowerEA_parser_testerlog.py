#Script to parser Tester Logs from CommunityPower EA
#
#import tkinter as tk
import csv
import codecs
import re
from datetime import datetime
import time
import os
from os.path import expanduser

# https://realpython.com/python-gui-tkinter/
#window = tk.Tk()
#window.title("Community Power Parser Log Tester - @Ulises2k for CommunityPower EA")
#window.rowconfigure(0, minsize=800, weight=1)
#window.columnconfigure(1, minsize=800, weight=1)
#text_box = tk.Text()
# text_box.pack()


# Flags
flag_Signal = 0
flag_Signal2 = 0
flag_Signal3 = 0
flag_Signal4 = 0
flag_OrderSend = 0
flag_OrderClose = 0
flag_OrderModify = 0
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

# Variables Clean
SignalRow = ()
SignalRow2 = ()
SignalRow3 = ()
SignalRow4 = ()
OrderSendRow = ()
OrderCloseRow = ()
OrderModifyRow = ()
TrailingStopRow = ()
ModifyingRow = ()
MovingRow = ()
position_modifiedRow = ()
position_modifiedRow2 = ()
order_modifiedRow = ()
stop_loss_triggeredRow = ()
marketRow = ()
marketRow2 = ()
buy_sell_stopRow = ()

#CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DATA_FOLDER="9EB2973C469D24060397BB5158EA73A5"
#CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#LOG FILE
#LogDirectory=expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\logs"
LogDirectory=expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Tester\\" + DATA_FOLDER + "\\Agent-127.0.0.1-3000\\Logs"
now = datetime.now()
LogToday=now.strftime('%Y%m%d') + ".log"
LogToday="20210709.log"
LogFile=os.path.join(LogDirectory, LogToday)
if not (os.path.isfile(LogFile)):
    print("File Not Found : " + os.path.join(LogDirectory, LogToday))
    exit()


#HEADER CSV
print("Time;Action;Type;Martingale;Signal;Symbol;Volume;PriceAction;NewValue;Slippage;Bid;Ask;StopLoss;TakeProfit;Expiration;Comment;MagicID;Status;Ticket #")

#Iterate Log
for line in csv.reader(codecs.open(LogFile, 'rU',  'utf-16'), delimiter="\t"):
    #print(', '.join(line))
    linea = line[4]
    # print(linea)
    fecha = linea.split(" ")[0]
    # print(fecha)
    match = re.search(r'^\d{4}\.\d{2}\.\d{2}', fecha)
    if match is not None:
        year = fecha.split(".")[0]
        # print(year)
        if (int(year) >= 2000):
            mensaje = linea.split("   ")[1]
            #print (mensaje)

            #--------------------------------------------------------------------------------------------
            #SIGNAL
            #--------------------------------------------------------------------------------------------
            # Signal to open buy #1 at 1490.790 (BigCandle + IdentifyTrend + TDI)!
            SignalRegex = re.compile(r'Signal to (open|close) ([a-z]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*) \(([a-zA-Z+ ]+)\)!')
            SignalMatch = SignalRegex.search(mensaje)
            if SignalMatch is not None:
                #print(SignalMatch.groups())
                flag_Signal = 1
                SignalRow = (linea.split("   ")[0],) + SignalMatch.groups() + ("SignalRow",)
                #print(SignalRow)

            # Signal to open buy #2 at 1885.770!
            SignalRegex2 = re.compile(r'Signal to (open|close) ([a-z]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch2 = SignalRegex2.search(mensaje)
            if SignalMatch2 is not None:
                # print(SignalMatch.groups())
                flag_Signal2 = 1
                SignalRow2 = (linea.split("   ")[0],) + SignalMatch2.groups() + ("SignalRow2",)
                #print(SignalRow2)

            # Signal to close sell (FIBO )!
            SignalRegex3 = re.compile(r'Signal to (open|close) ([a-z]+) \(([a-zA-Z+ ]+) \)!')
            SignalMatch3 = SignalRegex3.search(mensaje)
            if SignalMatch3 is not None:
                # print(SignalMatch3.groups())
                flag_Signal3 = 1
                SignalRow3 = (linea.split("   ")[0],) + SignalMatch3.groups() + ("SignalRow3",)
                #print(SignalRow3)

            #Signal to open AutoHedge for buy-order #6 at 1.14407!
            SignalRegex4 = re.compile(r'Signal to (open|close) ([a-zA-Z]+) for ([a-z-]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch4 = SignalRegex4.search(mensaje)
            if SignalMatch4 is not None:
                # print(SignalMatch4.groups())
                flag_Signal4 = 1
                SignalRow4 = (linea.split("   ")[0],) + SignalMatch4.groups() + ("SignalRow4",)
                #print(SignalRow4)


            #Signal to delete pending buy-order (indicator)!
            #order canceled [#15 buy stop 1 EURUSD at 1.14479]
            #|  OrderDelete( 15 ) - OK!


            #TrailingStop for BUY: 0 -> 1920.37
            TrailingStopRegex = re.compile(r'TrailingStop for ([A-Z]+): ([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)')
            TrailingStopMatch = TrailingStopRegex.search(mensaje)
            if TrailingStopMatch is not None:
                # print(TrailingStopMatch.groups())
                flag_TrailingStop = 1
                TrailingStopRow = (linea.split("   ")[0],) + TrailingStopMatch.groups() + ("TrailingStopRow",)
                #print(TrailingStopRow)

            #Modifying TP for buy-order #18: 2154.566 -> 2175.994...
            #Modifying SL for sell-order #86: 0.00000 -> 1.17551...
            ModifyingRegex = re.compile(r'Modifying ([A-Z]+) for ([a-z-]+) \#([0-9]+): ([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)...')
            ModifyingMatch = ModifyingRegex.search(mensaje)
            if ModifyingMatch is not None:
                # print(ModifyingMatch.groups())
                flag_Modifying = 1
                ModifyingRow = (linea.split("   ")[0],) + ModifyingMatch.groups() + ("ModifyingRow",)
                #print(ModifyingRow)

            #position modified [#18 buy 0.99 XAUUSD 1856.780 tp: 2175.994]
            position_modifiedRegex = re.compile(r'position modified \[\#([0-9]+) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) tp: ([0-9]*[.]?[0-9]*)\]')
            position_modifiedMatch = position_modifiedRegex.search(mensaje)
            if position_modifiedMatch is not None:
                # print(position_modifiedMatch.groups())
                flag_position_modified = 1
                position_modifiedRow = (linea.split("   ")[0],) + position_modifiedMatch.groups() + ("position_modifiedRow",)
                #print(position_modifiedRow)

            #position modified [#7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326]
            position_modifiedRegex2 = re.compile(r'position modified \[\#([0-9]+) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) sl: ([0-9]*[.]?[0-9]*) tp: ([0-9]*[.]?[0-9]*)\]')
            position_modifiedMatch2 = position_modifiedRegex2.search(mensaje)
            if position_modifiedMatch2 is not None:
                # print(position_modifiedMatch2.groups())
                flag_position_modified2 = 1
                position_modifiedRow2 = (linea.split("   ")[0],) + position_modifiedMatch2.groups() + ("position_modifiedRow2",)
                #print(position_modifiedRow2)

            #order modified [#10 buy stop 1.01 EURUSD at 1.15179]
            order_modifiedRegex = re.compile(r'order modified \[\#([0-9]+) ([a-z ]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*)\]')
            order_modifiedMatch = order_modifiedRegex.search(mensaje)
            if order_modifiedMatch is not None:
                # print(order_modifiedMatch.groups())
                flag_order_modified = 1
                order_modifiedRow = (linea.split("   ")[0],) + order_modifiedMatch.groups() + ("order_modifiedRow",)
                #print(order_modifiedRow)

            #buy stop 1 EURUSD at 1.14301 (1.14029 / 1.14034)
            #sell stop 1 EURUSD at 1.13248 (1.13415 / 1.13420)
            buy_sell_stopRegex = re.compile(r'(buy|sell) stop ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            buy_sell_stopMatch = buy_sell_stopRegex.search(mensaje)
            if buy_sell_stopMatch is not None:
                # print(buy_sell_stopMatch.groups())
                flag_buy_sell_stop = 1
                buy_sell_stopRow = (linea.split("   ")[0],) + buy_sell_stopMatch.groups() + ("buy_sell_stopRow",)
                #print(buy_sell_stopRow)

            # |  OrderSend( XAUUSD, buy, 0.10, 1592.750, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
            OrderSendRegex = re.compile(r'\|  OrderSend\( ([a-zA-Z\#\.]+), ([a-z ]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), \"([a-zA-Z0-9\.\#: ]+)\", ([0-9]*) \) - ([a-zA-Z\!]+)! Ticket \#([0-9]*).')
            OrderSendMatch = OrderSendRegex.search(mensaje)
            if OrderSendMatch is not None:
                # print(OrderSendMatch.groups())
                flag_OrderSend = 1
                OrderSendRow = (linea.split("   ")[0],) + OrderSendMatch.groups() + ("OrderSendRow",)
                #print(OrderSendRow)

            # PENDING TO DO
            #Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
            MovingRegex = re.compile(r'Moving ([a-z-]+) order \#([0-9]+) to the new level \(([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)\)...')
            MovingMatch = MovingRegex.search(mensaje)
            if MovingMatch is not None:
                # print(MovingMatch.groups())
                flag_Moving = 1
                MovingRow = (linea.split("   ")[0],) + MovingMatch.groups() + ("MovingRow",)
                #print(MovingRow)

            # PENDING TO DO
            #failed modify #681 buy 0.54 EURUSD sl: 0.00000, tp: 1.14993 -> sl: 0.00000, tp: 1.15021 [Market closed]

            # PENDING TO DO
            # |  OrderSend( XAUUSD, buy stop, 0.10, 1501.680, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - ERROR #10018 (Market is closed)!

            # PENDING TO DO
            #Modifying TP for buy-order #743: 1.10987 -> 1.10993...
            #failed modify #743 buy 1.7 EURUSDm# sl: 0.00000, tp: 1.10987 -> sl: 0.00000, tp: 1.10993 [Market closed]
            #|  OrderModify( 743, 1.10723, 0.00000, 1.10993 ) - ERROR #10018 (Market is closed)!

            # PENDING TO DO
            #Signal to open buy #6 at 1.09278 (BigCandle)!
            # Not enough money to open 16.40 lots EURUSDm#! 

            # PENDING TO DO
            #|  OrderModify( 681, 1.14788, 0.00000, 1.15021 ) - ERROR #10018 (Market is closed)!

            #market buy 0.1 XAUUSD (1934.050 / 1935.010)
            marketRegex = re.compile(r'market ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch = marketRegex.search(mensaje)
            if marketRegexMatch is not None:
                #print(marketRegexMatch.groups())
                flag_market = 1
                marketRow = (linea.split("   ")[0],) + marketRegexMatch.groups() + ("marketRow",)
                #print(marketRow)

            #market buy 0.1 EURUSD, close #10 (1.13411 / 1.13414)
            marketRegex2 = re.compile(r'market ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+), ([a-z]+) \#([0-9]*) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch2 = marketRegex2.search(mensaje)
            if marketRegexMatch2 is not None:
                #print(marketRegexMatch2.groups())
                flag_market2 = 1
                marketRow2 = (linea.split("   ")[0],) + marketRegexMatch2.groups() + ("marketRow2",)
                #print(marketRow2)

            # |  OrderClose( 272, 1.48, 1.06957, 50 ) - OK!
            OrderCloseRegex = re.compile(r'\|  OrderClose\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*) \) - ([A-Z]+)!')
            OrderCloseMatch = OrderCloseRegex.search(mensaje)
            if OrderCloseMatch is not None:
                #print(OrderCloseMatch.groups())
                flag_OrderClose = 1
                OrderCloseRow = (linea.split("   ")[0],) + OrderCloseMatch.groups() + ("OrderCloseRow",)
                #print(OrderCloseRow)

            #|  OrderModify( 18, 1856.780, 0.000, 2175.994 ) - OK!
            #|  OrderModify( 86, 1.14135, 1.17551, 0.00000 ) - OK!
            OrderModifyRegex = re.compile(r'\|  OrderModify\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*) \) - ([A-Z]+)!')
            OrderModifyMatch = OrderModifyRegex.search(mensaje)
            if OrderModifyMatch is not None:
                #print(OrderModifyMatch.groups())
                flag_OrderModify = 1
                OrderModifyRow = (linea.split("   ")[0],) + OrderModifyMatch.groups() + ("OrderModifyRow",)
                #print(OrderModifyRow)

            #stop loss triggered #7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326 [#8 buy 1 XAUUSD at 1881.920]
            stop_loss_triggeredRegex = re.compile(r'stop loss triggered \#([0-9]*) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) sl: ([0-9]*[.]?[0-9]*) tp: ([0-9]*[.]?[0-9]*) \[\#([0-9]*) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*)\]')
            stop_loss_triggeredRegexMatch = stop_loss_triggeredRegex.search(mensaje)
            if stop_loss_triggeredRegexMatch is not None:
                #print(stop_loss_triggeredRegexMatch.groups())
                flag_stop_loss_triggered = 1
                stop_loss_triggeredRow = (linea.split("   ")[0],) + stop_loss_triggeredRegexMatch.groups() + ("stop_loss_triggeredRow",)
                #print(stop_loss_triggeredRow)






            #---------------------------------------------------------------------------------------------------------------------------------------
            #Join the signal together with the order and market and position and etc.
            #---------------------------------------------------------------------------------------------------------------------------------------
            #Don't Touch. Working
            if ((len(SignalRow) and len(buy_sell_stopRow) and len(OrderSendRow)) and (SignalRow[0] == buy_sell_stopRow[0]) and (buy_sell_stopRow[0] == OrderSendRow[0])):
                if ((flag_Signal == 1) and (flag_buy_sell_stop == 1) and (flag_OrderSend == 1)):
                    #Complete
                    #Signal to open buy #1 at 1.14301 (Stochastic K + IdentifyTrend + TDI)!
                    #buy stop 1 EURUSD at 1.14301 (1.14029 / 1.14034)
                    #|  OrderSend( EURUSD, buy stop, 1.00, 1.14301, 50, 0.00000, 0.00000, "CP #1", 3047 ) - OK! Ticket #2.
                    if (SignalRow[4] == buy_sell_stopRow[3]) and (buy_sell_stopRow[3] == OrderSendRow[4]) and (SignalRow[3] == OrderSendRow[8].split("#")[1]):
                        print(SignalRow[0] + ";Signal1 to " + SignalRow[1] + ";" + SignalRow[2] + ";" + SignalRow[3] + ";" + SignalRow[5] + ";" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";;" + OrderSendRow[5] + ";" + buy_sell_stopRow[4] + ";" + buy_sell_stopRow[5] + ";;;;" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow[10] + ";" + OrderSendRow[11])
                        SignalRow = tuple()
                        buy_sell_stopRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal = 0
                        flag_buy_sell_stop = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in EA. Check Please!! Critical error-1")
                        exit()

            if ((len(SignalRow) and len(marketRow) and len(OrderSendRow)) and (SignalRow[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #CommunityPower MT5 (EURUSD,M5)	2019.01.02 14:30:00   Signal to open buy #1 at 1.14034 (Stochastic K + IdentifyTrend + TDI)!
                    #Trade	2019.01.02 14:30:00   market buy 0.1 EURUSD (1.14029 / 1.14034)
                    #Trades	2019.01.02 14:30:00   deal #2 buy 0.1 EURUSD at 1.14034 done (based on order #2)
                    #Trade	2019.01.02 14:30:00   deal performed [#2 buy 0.1 EURUSD at 1.14034]
                    #Trade	2019.01.02 14:30:00   order performed buy 0.1 at 1.14034 [#2 buy 0.1 EURUSD at 1.14034]
                    #CommunityPower MT5 (EURUSD,M5)	2019.01.02 14:30:00   |  OrderSend( EURUSD, buy, 0.10, 1.14034, 50, 0.00000, 0.00000, "CP #1", 3047 ) - OK! Ticket #2.
                    #https://docs.mql4.com/trading/ordersend
                    if (SignalRow[3] == OrderSendRow[8].split("#")[1]) and (SignalRow[2] == marketRow[1]) and (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        print(SignalRow[0] + ";Signal2 to " + SignalRow[1] + ";" + SignalRow[2] + ";" + SignalRow[3] + ";" + SignalRow[5] + ";" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";;" + OrderSendRow[5] + ";" + marketRow[4] + ";" + marketRow[5] + ";;;;" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow[10] + ";" + OrderSendRow[11])
                        SignalRow = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal = 0
                        flag_market = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in EA. Check Please!! Critical error-2")
                        exit()




            #Signal to open sell #1 at 1.14156 (Stochastic K + IdentifyTrend + TDI)!
            #sell stop 1.02 EURUSD at 1.14156 (1.14297 / 1.14301)
            #|  OrderSend( EURUSD, sell stop, 1.02, 1.14156, 50, 0.00000, 0.00000, "CP #1", 3047 ) - OK! Ticket #50.


            if ((len(SignalRow2) and len(marketRow) and len(OrderSendRow)) and (SignalRow2[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal2 == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #Signal to open buy #2 at 1843.330!
                    #market buy 0.12 XAUUSD (1842.830 / 1843.330)
                    #|  OrderSend( XAUUSD, buy, 0.12, 1843.330, 50, 0.000, 0.000, "CP18.06.2021.21:03 #2", 234 ) - OK! Ticket #17.
                    #https://docs.mql4.com/trading/ordersend
                    if (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        print(SignalRow2[0] + ";Signal3 to " + SignalRow2[1] + ";" + SignalRow2[2] + ";" + SignalRow2[3] + ";;" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";" + OrderSendRow[5] + ";" + marketRow[4] + ";" + marketRow[5] + ";;;;" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow[10] + ";" + OrderSendRow[11])
                        SignalRow2 = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal2 = 0
                        flag_market = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in EA. Check Please!! Critical error-3")
                        exit()

            if ((len(SignalRow3) and len(marketRow2) and len(OrderCloseRow)) and (SignalRow3[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_Signal3 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #Signal to close sell (FIBO )!
                    #market buy 0.1 EURUSD, close #10 (1.13411 / 1.13414)
                    #|  OrderClose( 10, 0.10, 1.13414, 50 ) - OK!
                    #https://docs.mql4.com/trading/orderclose
                    if (marketRow2[5] == OrderCloseRow[1]):
                        print(SignalRow3[0] + ";Signal4 to " + SignalRow3[1] + ";" + SignalRow3[2] + ";;" + SignalRow3[3] + ";" + marketRow2[3] + ";" + OrderCloseRow[2] + ";" + OrderCloseRow[3] + ";" + OrderCloseRow[4] + ";" + marketRow2[6] + ";" + marketRow2[7] + ";;;" + OrderCloseRow[5]+ ";" + OrderCloseRow[1])
                        SignalRow3 = tuple()
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_Signal3 = 0
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue
                    else:
                        print("Error in EA. Check Please!! Critical error-4")
                        exit()

            #Falta Chequear MEJOR
            if ((len(SignalRow4) and len(marketRow2) and len(OrderSendRow)) and (SignalRow4[0] == marketRow2[0]) and (marketRow2[0] == OrderSendRow[0])):
                if ((flag_Signal4 == 1) and (flag_market2 == 1) and (flag_OrderSend == 1)):
                    #Signal to open AutoHedge for buy-order #6 at 1.14407!
                    #market sell 10.98 EURUSD (1.14407 / 1.14410)
                    #deal #162 sell 10.98 EURUSD at 1.14407 done (based on order #191)
                    #deal performed [#162 sell 10.98 EURUSD at 1.14407]
                    #order performed sell 10.98 at 1.14407 [#191 sell 10.98 EURUSD at 1.14407]
                    #|  OrderSend( EURUSD, sell, 10.98, 1.14407, 50, 0.00000, 0.00000, "CP H6", 30471 ) - OK! Ticket #191.
                    #https://docs.mql4.com/trading/ordersend
                    if (marketRow2[5] == OrderCloseRow[1]):
                        print(SignalRow4[0] + ";Signal5 to " + SignalRow4[1] + ";" + OrderSendRow[2] + ";;" + SignalRow4[2] + ";" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";;" + OrderSendRow[5] + ";;;;;;" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow [10] + ";" + OrderSendRow[11])
                        SignalRow4 = tuple()
                        marketRow2 = tuple()
                        OrderSendRow = tuple()
                        flag_Signal4 = 0
                        flag_market2 = 0
                        flag_OrderSend = 0
                        continue
                    else:
                        print("Error in EA. Check Please!! Critical error-5")
                        exit()

            if ((len(ModifyingRow) and len(position_modifiedRow) and len(OrderModifyRow)) and (ModifyingRow[0] == position_modifiedRow[0]) and (position_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_Modifying == 1) and (flag_position_modified == 1) and (flag_OrderModify == 1)):
                    #Modifying SL for sell-order #86: 0.00000 -> 1.17551...
                    #position modified [#86 sell 0.1 EURUSD 1.14135 sl: 1.17551]
                    #|  OrderModify( 86, 1.14135, 1.17551, 0.00000 ) - OK!
                    #https://docs.mql4.com/trading/ordermodify
                    if (ModifyingRow[3] == position_modifiedRow[1]) and (position_modifiedRow[1] == OrderModifyRow[1]) and (ModifyingRow[3] == OrderModifyRow[1]):
                        print(ModifyingRow[0] + ";Modifying " + ModifyingRow[1] + ";" + position_modifiedRow[2] + ";;;" + position_modifiedRow[4] + ";" + position_modifiedRow[3] + ";" + OrderModifyRow[2] + ";" + ModifyingRow[5] + ";;;;" + OrderModifyRow[3] + ";" + OrderModifyRow[4] + ";;;;" + OrderModifyRow[5] + ";" + OrderModifyRow[1])
                        ModifyingRow = tuple()
                        position_modifiedRow = tuple()
                        OrderModifyRow = tuple()
                        flag_Modifying = 0
                        flag_position_modified = 0
                        flag_OrderModify = 0
                        continue
                    else:
                        print("Error in EA. Check Please!! Critical error-6")
                        exit()

            if ((len(MovingRow) and len(order_modifiedRow) and len(OrderModifyRow)) and (MovingRow[0] == order_modifiedRow[0]) and (order_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_Moving == 1) and (flag_order_modified == 1) and (flag_OrderModify == 1)):
                    #Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
                    #order modified [#10 buy stop 1.01 EURUSD at 1.15179]
                    #|  OrderModify( 10, 1.15179, 0.00000, 0.00000 ) - OK!
                    #https://docs.mql4.com/trading/ordermodify
                    if (MovingRow[2] == order_modifiedRow[1]) and (order_modifiedRow[1] == OrderModifyRow[1]) and (MovingRow[4] == order_modifiedRow[5]) and (order_modifiedRow[5] == OrderModifyRow[2]):
                        print(MovingRow[0] + ";Moving " + MovingRow[1] + ";" + order_modifiedRow[2] + ";;;" + order_modifiedRow[4] + ";" + order_modifiedRow[3] + ";" + MovingRow[3] + ";" + MovingRow[4] + ";;;;" + OrderModifyRow[3] + ";" + OrderModifyRow[4] + ";;;;" + OrderModifyRow[5] + ";" + OrderModifyRow[1])
                        MovingRow = tuple()
                        order_modifiedRow = tuple()
                        OrderModifyRow = tuple()
                        flag_Moving = 0
                        flag_order_modified = 0
                        flag_OrderModify = 0
                        continue
                    else:
                        print("Error in EA. Check Please!! Critical error-7")
                        exit()


            if (len(TrailingStopRow)):
                if (flag_TrailingStop == 1):
                    #2019.01.24 16:14:15   TrailingStop for BUY: 1.13446 -> 1.13553
                    #https://www.metatrader4.com/es/trading-platform/help/positions/trailing
                    print(TrailingStopRow[0] + ";TrailingStop for " + TrailingStopRow[1].lower() + ";" + TrailingStopRow[1].lower() + ";;;;;" + TrailingStopRow[2] + ";" + TrailingStopRow[3])
                    TrailingStopRow = tuple()
                    flag_TrailingStop = 0
                    continue


            #https://www.metatrader4.com/en/trading-platform/help/positions/orders
            #MMMM Esto hay que chequearlo bien en el tester porque no estoy seguro que este bien
            if (len(stop_loss_triggeredRow)):
                if (flag_stop_loss_triggered == 1):
                #stop loss triggered #7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326 [#8 buy 1 XAUUSD at 1881.920]
                #deal #8 buy 1 XAUUSD at 1902.500 done (based on order #8)
                #deal performed [#8 buy 1 XAUUSD at 1902.500]
                #order performed buy 1 at 1902.500 [#8 buy 1 XAUUSD at 1881.920]
                    print(stop_loss_triggeredRow[0] + ";stop loss triggered " + stop_loss_triggeredRow[2] + ";" + stop_loss_triggeredRow[2] + ";;;" + stop_loss_triggeredRow[4] + ";" + stop_loss_triggeredRow[3] + ";" + stop_loss_triggeredRow[12] + ";;;;" + stop_loss_triggeredRow[6] + ";" + stop_loss_triggeredRow[7] + ";;;;;" + stop_loss_triggeredRow[1])
                    stop_loss_triggeredRow = tuple()
                    flag_stop_loss_triggered = 0
                    continue
                else:
                    print("Error in EA. Check Please!! Critical error-8")
                    exit()

            #Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
            #order modified [#10 buy stop 1.01 EURUSD at 1.15179]
            #|  OrderModify( 10, 1.15179, 0.00000, 0.00000 ) - OK!



#text_box.insert(tk.INSERT , match.groups())
# window.mainloop()
