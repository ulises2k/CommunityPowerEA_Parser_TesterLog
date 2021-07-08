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
flag_OrderSend = 0
flag_OrderClose = 0
flag_OrderModify = 0
flag_TrailingStop = 0
flag_Modifying = 0
flag_position_modified = 0
flag_position_modified2 = 0
flag_stop_loss_triggered = 0
flag_market = 0
flag_market2 = 0

# Variables Clean
SignalRow = ()
SignalRow2 = ()
SignalRow3 = ()
OrderSendRow = ()
OrderCloseRow = ()
OrderModifyRow = ()
TrailingStopRow = ()
ModifyingRow = ()
position_modifiedRow = ()
position_modifiedRow2 = ()
stop_loss_triggeredRow = ()
marketRow = ()
marketRow2 = ()


#CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DATA_FOLDER="9EB2973C469D24060397BB5158EA73A5"
#CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#LOG FILE
LogDirectory=expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\logs"
now = datetime.now()
LogToday=now.strftime('%Y%m%d') + ".log"
#LogToday="20210705.log"
LogFile=os.path.join(LogDirectory, LogToday)
if not (os.path.isfile(LogFile)):
    print("Not found file: " + os.path.join(LogDirectory, LogToday))
    exit()


#HEADER CSV
print("Time;Action;Type;Martingale;Signal;Symbol;Volume;PriceAction;Slippage;Ask;Bid;StopLoss;TakeProfit;Expiration;Comment;MagicID;Status;Ticket #")

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
            SignalRegex = re.compile(r'Signal to ([a-z]+) ([a-z]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*) \(([a-zA-Z+ ]+)\)!')
            SignalMatch = SignalRegex.search(mensaje)
            if SignalMatch is not None:
                #print(mensaje)
                #print(SignalMatch.groups())
                flag_Signal = 1
                SignalRow = (linea.split("   ")[0],) + SignalMatch.groups() + ("SignalRow",)
                #print(SignalRow)

            # Signal to open buy #2 at 1885.770!
            SignalRegex2 = re.compile(r'Signal to ([a-z]+) ([a-z]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch2 = SignalRegex2.search(mensaje)
            if SignalMatch2 is not None:
                # print(mensaje)
                # print(SignalMatch.groups())
                flag_Signal2 = 1
                SignalRow2 = (linea.split("   ")[0],) + SignalMatch2.groups() + ("SignalRow2",)
                #print(SignalRow2)

            # Signal to close sell (FIBO )!
            SignalRegex3 = re.compile(r'Signal to ([a-z]+) ([a-z]+) \(([a-zA-Z+ ]+) \)!')
            SignalMatch3 = SignalRegex3.search(mensaje)
            if SignalMatch3 is not None:
                # print(mensaje)
                # print(SignalMatch3.groups())
                flag_Signal3 = 1
                SignalRow3 = (linea.split("   ")[0],) + SignalMatch3.groups() + ("SignalRow3",)
                #print(SignalRow3)

            #TrailingStop for BUY: 0 -> 1920.37
            TrailingStopRegex = re.compile(r'TrailingStop for ([A-Z]+): ([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)')
            TrailingStopMatch = TrailingStopRegex.search(mensaje)
            if TrailingStopMatch is not None:
                # print(mensaje)
                # print(TrailingStopMatch.groups())
                flag_TrailingStop = 1
                TrailingStopRow = (linea.split("   ")[0],) + TrailingStopMatch.groups() + ("TrailingStopRow",)
                #print(TrailingStopRow)

            #Modifying TP for buy-order #18: 2154.566 -> 2175.994...
            #Modifying SL for sell-order #86: 0.00000 -> 1.17551...
            ModifyingRegex = re.compile(r'Modifying ([A-Z]+) for ([a-z-]+) \#([0-9]+): ([0-9]*[.]?[0-9]*) -> ([0-9]*[.]?[0-9]*)...')
            ModifyingMatch = ModifyingRegex.search(mensaje)
            if ModifyingMatch is not None:
                # print(mensaje)
                # print(ModifyingMatch.groups())
                flag_Modifying = 1
                ModifyingRow = (linea.split("   ")[0],) + ModifyingMatch.groups() + ("ModifyingRow",)
                #print(ModifyingRow)

            # PENDING TO DO
            #Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...

            # PENDING TO DO
            #failed modify #681 buy 0.54 EURUSD sl: 0.00000, tp: 1.14993 -> sl: 0.00000, tp: 1.15021 [Market closed]

            #position modified [#18 buy 0.99 XAUUSD 1856.780 tp: 2175.994]
            position_modifiedRegex = re.compile(r'position modified \[\#([0-9]+) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) ([a-z]+): ([0-9]*[.]?[0-9]*)\]')
            position_modifiedMatch = position_modifiedRegex.search(mensaje)
            if position_modifiedMatch is not None:
                # print(mensaje)
                # print(position_modifiedMatch.groups())
                flag_position_modified = 1
                position_modifiedRow = (linea.split("   ")[0],) + position_modifiedMatch.groups() + ("position_modifiedRow",)
                #print(position_modifiedRow)

            #position modified [#7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326]
            position_modifiedRegex2 = re.compile(r'position modified \[\#([0-9]+) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) ([a-z]+): ([0-9]*[.]?[0-9]*) ([a-z]+): ([0-9]*[.]?[0-9]*)\]')
            position_modifiedMatch2 = position_modifiedRegex2.search(mensaje)
            if position_modifiedMatch2 is not None:
                # print(mensaje)
                # print(position_modifiedMatch2.groups())
                flag_position_modified2 = 1
                position_modifiedRow2 = (linea.split("   ")[0],) + position_modifiedMatch2.groups() + ("position_modifiedRow2",)
                #print(position_modifiedRow2)


            # |  OrderSend( XAUUSD, buy, 0.10, 1592.750, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
            OrderSendRegex = re.compile(r'\|  OrderSend\( ([a-zA-Z\#\.]+), ([a-z ]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), \"([a-zA-Z0-9\.\#: ]+)\", ([0-9]*) \) - ([a-zA-Z\!]+)! Ticket \#([0-9]*).')
            OrderSendMatch = OrderSendRegex.search(mensaje)
            if OrderSendMatch is not None:
                # print(mensaje)
                # print(OrderSendMatch.groups())
                flag_OrderSend = 1
                OrderSendRow = (linea.split("   ")[0],) + OrderSendMatch.groups() + ("OrderSendRow",)
                #print(OrderSendRow)


            # # PENDING TO DO
            # |  OrderSend( XAUUSD, buy stop, 0.10, 1501.680, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - ERROR #10018 (Market is closed)!



            #market buy 0.1 XAUUSD (1934.050 / 1935.010)
            marketRegex = re.compile(r'market ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch = marketRegex.search(mensaje)
            if marketRegexMatch is not None:
                #print(mensaje)
                #print(marketRegexMatch.groups())
                flag_market = 1
                marketRow = (linea.split("   ")[0],) + marketRegexMatch.groups() + ("marketRow",)
                #print(marketRow)

            #market buy 0.1 EURUSD, close #10 (1.13411 / 1.13414)
            marketRegex2 = re.compile(r'market ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+), ([a-z]+) \#([0-9]*) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch2 = marketRegex2.search(mensaje)
            if marketRegexMatch2 is not None:
                #print(mensaje)
                #print(marketRegexMatch2.groups())
                flag_market2 = 1
                marketRow2 = (linea.split("   ")[0],) + marketRegexMatch2.groups() + ("marketRow2",)
                #print(marketRow2)

            # |  OrderClose( 272, 1.48, 1.06957, 50 ) - OK!
            OrderCloseRegex = re.compile(r'\|  OrderClose\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*) \) - ([a-zA-Z]+)!')
            OrderCloseMatch = OrderCloseRegex.search(mensaje)
            if OrderCloseMatch is not None:
                # print(mensaje)
                #print(OrderCloseMatch.groups())
                flag_OrderClose = 1
                OrderCloseRow = (linea.split("   ")[0],) + OrderCloseMatch.groups() + ("OrderCloseRow",)
                #print(OrderCloseRow)

            # PENDING TO DO
            #|  OrderModify( 681, 1.14788, 0.00000, 1.15021 ) - ERROR #10018 (Market is closed)!


            #|  OrderModify( 18, 1856.780, 0.000, 2175.994 ) - OK!
            #|  OrderModify( 86, 1.14135, 1.17551, 0.00000 ) - OK!
            OrderModifyRegex = re.compile(r'\|  OrderModify\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*) \) - ([a-zA-Z]+)!')
            OrderModifyMatch = OrderModifyRegex.search(mensaje)
            if OrderModifyMatch is not None:
                # print(mensaje)
                #print(OrderModifyMatch.groups())
                flag_OrderModify = 1
                OrderModifyRow = (linea.split("   ")[0],) + OrderModifyMatch.groups() + ("OrderModifyRow",)
                #print(OrderModifyRow)


            #stop loss triggered #7 sell 1 XAUUSD 1889.540 sl: 1881.920 tp: 1732.326 [#8 buy 1 XAUUSD at 1881.920]
            stop_loss_triggeredRegex = re.compile(r'stop loss triggered \#([0-9]*) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) ([0-9]*[.]?[0-9]*) sl: ([0-9]*[.]?[0-9]*) tp: ([0-9]*[.]?[0-9]*) \[\#([0-9]*) ([a-z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z\#\.]+) at ([0-9]*[.]?[0-9]*)\]')
            stop_loss_triggeredRegexMatch = stop_loss_triggeredRegex.search(mensaje)
            if stop_loss_triggeredRegexMatch is not None:
                #print(mensaje)
                #print(stop_loss_triggeredRegexMatch.groups())
                flag_stop_loss_triggered = 1
                stop_loss_triggeredRow = (linea.split("   ")[0],) + stop_loss_triggeredRegexMatch.groups() + ("stop_loss_triggeredRow",)
                #print(stop_loss_triggeredRow)


            ########################################################################################################################################
            #Join the signal together with the order and market and position and etc.
            if ((len(SignalRow) and len(marketRow) and len(OrderSendRow)) and (SignalRow[0] == marketRow[0]) and (SignalRow[0] == OrderSendRow[0])):
                if ((flag_Signal == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #Signal to open buy #1 at 1935.010 (BigCandle)!
                    #market buy 0.1 XAUUSD (1934.050 / 1935.010)
                    #|  OrderSend( XAUUSD, buy, 0.10, 1935.010, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
                    #https://docs.mql4.com/trading/ordersend
                    if (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        print(SignalRow[0] + ";Signal to " + SignalRow[1] + ";" + SignalRow[2] + ";" + SignalRow[3] + ";" + SignalRow[5] + ";" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";" + OrderSendRow[5] + ";" + marketRow[4] + ";" + marketRow[5] + ";;;;" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow[10] + ";" + OrderSendRow[11])
                        SignalRow = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal = 0
                        flag_market = 0
                        flag_OrderSend = 0
                        continue

            if ((len(SignalRow2) and len(marketRow) and len(OrderSendRow)) and (SignalRow2[0] == marketRow[0]) and (marketRow[0] == OrderSendRow[0])):
                if ((flag_Signal2 == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #Signal to open buy #2 at 1843.330!
                    #market buy 0.12 XAUUSD (1842.830 / 1843.330)
                    #|  OrderSend( XAUUSD, buy, 0.12, 1843.330, 50, 0.000, 0.000, "CP18.06.2021.21:03 #2", 234 ) - OK! Ticket #17.
                    #https://docs.mql4.com/trading/ordersend
                    if (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        print(SignalRow2[0] + ";Signal to " + SignalRow2[1] + ";" + SignalRow2[2] + ";" + SignalRow2[3] + ";;" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";" + OrderSendRow[5] + ";" + marketRow[4] + ";;;;" + marketRow[5] + ";" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow[10] + ";" + OrderSendRow[11])
                        SignalRow2 = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal2 = 0
                        flag_market = 0
                        flag_OrderSend = 0
                        continue

            if ((len(SignalRow3) and len(marketRow2) and len(OrderCloseRow)) and (SignalRow3[0] == marketRow2[0]) and (marketRow2[0] == OrderCloseRow[0])):
                if ((flag_Signal3 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #Signal to close sell (FIBO )!
                    #market buy 0.1 EURUSD, close #10 (1.13411 / 1.13414)
                    #|  OrderClose( 10, 0.10, 1.13414, 50 ) - OK!
                    #https://docs.mql4.com/trading/orderclose
                    if (marketRow2[5] == OrderCloseRow[1]):
                        print(SignalRow3[0] + ";Signal to " + SignalRow3[1] + ";" + SignalRow3[2] + ";;" + SignalRow3[3] + ";" + marketRow2[3] + ";" + OrderCloseRow[2] + ";" + OrderCloseRow[3] + ";" + OrderCloseRow[4] + ";" + marketRow2[6] + ";" + marketRow2[7] + ";;;" + OrderCloseRow[5]+ ";" + OrderCloseRow[1])
                        SignalRow3 = tuple()
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_Signal3 = 0
                        flag_market2 = 0
                        flag_OrderClose = 0
                        continue

            if ((len(ModifyingRow) and len(position_modifiedRow) and len(OrderModifyRow)) and (ModifyingRow[0] == position_modifiedRow[0]) and (position_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_Modifying == 1) and (flag_position_modified == 1) and (flag_OrderModify == 1)):
                    #Modifying SL for sell-order #86: 0.00000 -> 1.17551...
                    #position modified [#86 sell 0.1 EURUSD 1.14135 sl: 1.17551]
                    #|  OrderModify( 86, 1.14135, 1.17551, 0.00000 ) - OK!
                    #https://docs.mql4.com/trading/ordermodify
                    if (ModifyingRow[3] == position_modifiedRow[1]) and (position_modifiedRow[1] == OrderModifyRow[1]) and (ModifyingRow[3] == OrderModifyRow[1]):
                        print(ModifyingRow[0] + ";Modifying " + ModifyingRow[1] + ";" + position_modifiedRow[2] + ";;;" + position_modifiedRow[4] + ";" + position_modifiedRow[3] + ";" + OrderModifyRow[2] + ";;;;" + OrderModifyRow[3] + ";" + OrderModifyRow[4] + ";;;;" + OrderModifyRow[5] + ";" + OrderModifyRow[1])
                        ModifyingRow = tuple()
                        position_modifiedRow = tuple()
                        OrderModifyRow = tuple()
                        flag_Modifying = 0
                        flag_position_modified = 0
                        flag_OrderModify = 0
                        continue

            if (len(TrailingStopRow) and (len(ModifyingRow) and len(position_modifiedRow) and len(OrderModifyRow)) and (ModifyingRow[0] == position_modifiedRow[0]) and (position_modifiedRow[0] == OrderModifyRow[0])):
                if ((flag_TrailingStop == 1) and (flag_Modifying == 1) and (flag_position_modified == 1) and (flag_OrderModify == 1)):
                    #TrailingStop for SELL: 0 -> 1881.92
                    #Modifying SL for sell-order #7: 0.000 -> 1881.920...
                    #position modified [#7 sell 1 XAUUSD 1889.540 sl: 1881.920]
                    #|  OrderModify( 7, 1889.540, 1881.920, 0.000 ) - OK!
                    if (ModifyingRow[3] == position_modifiedRow[1]) and (position_modifiedRow[1] == OrderModifyRow[1]) and (ModifyingRow[3] == OrderModifyRow[1]):
                        print(ModifyingRow[0] + ";TrailingStop for " + ModifyingRow[1] + ";" + position_modifiedRow[2] + ";;;" + position_modifiedRow[4] + ";" + position_modifiedRow[3] + ";" + OrderModifyRow[2] + ";;;;" + OrderModifyRow[3] + ";" + OrderModifyRow[4] + ";;;;" + OrderModifyRow[5] + ";" + OrderModifyRow[1])
                        TrailingStopRow = tuple()
                        ModifyingRow = tuple()
                        position_modifiedRow = tuple()
                        OrderModifyRow = tuple()
                        flag_TrailingStop = 0
                        flag_Modifying = 0
                        flag_position_modified = 0
                        flag_OrderModify = 0
                        continue

            #https://www.metatrader4.com/en/trading-platform/help/positions/orders
            #MMMM Estoy hay que chequearlo bien en el tester porque no estoy seguro que este bien
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

            #Moving buy-stop order #10 to the new level (1.15191 -> 1.15179)...
            #order modified [#10 buy stop 1.01 EURUSD at 1.15179]
            #|  OrderModify( 10, 1.15179, 0.00000, 0.00000 ) - OK!


            #Modifying TP for sell-order #27: 1.11378 -> 1.11376...
            #failed modify #27 sell 1.7 EURUSDm# sl: 0.00000, tp: 1.11378 -> sl: 0.00000, tp: 1.11376 [Market closed]
            #|  OrderModify( 27, 1.11919, 0.00000, 1.11376 ) - ERROR #10018 (Market is closed)!


#text_box.insert(tk.INSERT , match.groups())
# window.mainloop()
