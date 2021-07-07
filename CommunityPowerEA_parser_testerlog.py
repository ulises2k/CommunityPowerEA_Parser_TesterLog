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


# Flags
flag_Signal = 0
flag_Signal2 = 0
flag_Signal3 = 0
flag_OrderSend = 0
flag_OrderClose = 0
flag_TrailingStop = 0
flag_market = 0
flag_market2 = 0
# https://realpython.com/python-gui-tkinter/
#window = tk.Tk()
#window.title("Community Power Parser Log Tester - @Ulises2k for CommunityPower EA")
#window.rowconfigure(0, minsize=800, weight=1)
#window.columnconfigure(1, minsize=800, weight=1)
#text_box = tk.Text()
# text_box.pack()

# Variables Clean
SignalRow = ()
SignalRow2 = ()
SignalRow3 = ()
OrderSendRow = ()
OrderCloseRow = ()
TrailingStopRow = ()
OrderModifyRow = ()
marketRow = ()
marketRow2 = ()
#CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DATA_FOLDER="9EB2973C469D24060397BB5158EA73A5"
#CUSTOM THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#LOG FILE
LogDirectory=expanduser("~") + "\\AppData\\Roaming\\MetaQuotes\\Terminal\\" + DATA_FOLDER + "\\Tester\\logs"
#LogToday="20210705.log"
now = datetime.now()
LogToday=now.strftime('%Y%m%d') + ".log"
LogFile=os.path.join(LogDirectory, LogToday)
if not (os.path.isfile(LogFile)):
    print("Not found file: " + os.path.join(LogDirectory, LogToday))
    exit()


#HEADER CSV
print("Time;Action;Type;Martingale;Signal;Symbol;Volume;PriceAction;Slippage;Ask;Bid;Comment;MagicID;Status;Ticket #")

#Interate Log
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
            #Example 1
            # QM	0	02:50:15.116	Core 1	2020.09.21 17:40:00   Signal to open buy #2 at 1885.770!
            # OE	0	02:50:15.116	Core 1	2020.09.21 17:40:00   market buy 0.19 XAUUSD (1885.400 / 1885.770)
            # GQ	0	02:50:15.116	Core 1	2020.09.21 17:40:00   deal #97 buy 0.19 XAUUSD at 1885.770 done (based on order #97)
            # EO	0	02:50:15.116	Core 1	2020.09.21 17:40:00   deal performed [#97 buy 0.19 XAUUSD at 1885.770]
            # HR	0	02:50:15.116	Core 1	2020.09.21 17:40:00   order performed buy 0.19 at 1885.770 [#97 buy 0.19 XAUUSD at 1885.770]
            # KH	0	02:50:15.116	Core 1	2020.09.21 17:40:00   |  OrderSend( XAUUSD, buy, 0.19, 1885.770, 50, 0.000, 0.000, "CP18.06.2021.21:03 #2", 234 ) - OK! Ticket #97.

            #Example 2
            #JR	0	21:48:46.343	Core 1	2021.01.06 14:43:36   Signal to open buy #1 at 1935.010 (BigCandle)!
            #DJ	0	21:48:46.343	Core 1	2021.01.06 14:43:36   market buy 0.1 XAUUSD (1934.050 / 1935.010)
            #DF	0	21:48:46.343	Core 1	2021.01.06 14:43:36   deal #2 buy 0.1 XAUUSD at 1935.010 done (based on order #2)
            #DK	0	21:48:46.343	Core 1	2021.01.06 14:43:36   deal performed [#2 buy 0.1 XAUUSD at 1935.010]
            #CM	0	21:48:46.343	Core 1	2021.01.06 14:43:36   order performed buy 0.1 at 1935.010 [#2 buy 0.1 XAUUSD at 1935.010]
            #IN	0	21:48:46.343	Core 1	2021.01.06 14:43:36   |  OrderSend( XAUUSD, buy, 0.10, 1935.010, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
            #KP	0	21:48:46.343	Core 1	2021.01.06 14:43:36   Signal to open sell #1 at 1934.050 (BigCandle)!
            #LP	0	21:48:46.343	Core 1	2021.01.06 14:43:36   market sell 0.1 XAUUSD (1934.050 / 1935.010)
            #QF	0	21:48:46.343	Core 1	2021.01.06 14:43:36   deal #3 sell 0.1 XAUUSD at 1934.050 done (based on order #3)
            #DG	0	21:48:46.343	Core 1	2021.01.06 14:43:36   deal performed [#3 sell 0.1 XAUUSD at 1934.050]
            #NN	0	21:48:46.343	Core 1	2021.01.06 14:43:36   order performed sell 0.1 at 1934.050 [#3 sell 0.1 XAUUSD at 1934.050]
            #GM	0	21:48:46.343	Core 1	2021.01.06 14:43:36   |  OrderSend( XAUUSD, sell, 0.10, 1934.050, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #3.
            #HF	0	21:48:46.343	Core 1	2021.01.06 14:43:36   Signal to close buy (IdentifyTrend)!
            #LR	0	21:48:46.343	Core 1	2021.01.06 14:43:36   market sell 0.1 XAUUSD, close #2 (1937.140 / 1937.630)
            #NR	0	21:48:46.343	Core 1	2021.01.06 14:43:36   deal #4 sell 0.1 XAUUSD at 1937.140 done (based on order #4)
            #RK	0	21:48:46.343	Core 1	2021.01.06 14:43:36   deal performed [#4 sell 0.1 XAUUSD at 1937.140]
            #IJ	0	21:48:46.343	Core 1	2021.01.06 14:43:36   order performed sell 0.1 at 1937.140 [#4 sell 0.1 XAUUSD at 1937.140]
            #HG	0	21:48:46.343	Core 1	2021.01.06 14:43:36   |  OrderClose( 2, 0.10, 1937.140, 50 ) - OK!


            # Signal to open buy #1 at 1490.790 (BigCandle + IdentifyTrend + TDI)!
            SignalRegex = re.compile(r'Signal to ([a-zA-Z ]+) ([a-zA-Z ]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*) \(([a-zA-Z+ ]+)\)!')
            SignalMatch = SignalRegex.search(mensaje)
            if SignalMatch is not None:
                #print(mensaje)
                #print(SignalMatch.groups())
                flag_Signal = 1
                SignalRow = (linea.split("   ")[0],) + SignalMatch.groups()
                #print(SignalRow)

            # Signal to open buy #2 at 1885.770!
            SignalRegex2 = re.compile(r'Signal to ([a-zA-Z]+) ([a-zA-Z ]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch2 = SignalRegex2.search(mensaje)
            if SignalMatch2 is not None:
                # print(mensaje)
                # print(SignalMatch.groups())
                flag_Signal2 = 1
                SignalRow2 = (linea.split("   ")[0],) + SignalMatch2.groups()
                #print(SignalRow2)

            # Signal to close sell (FIBO )!
            SignalRegex3 = re.compile(r'Signal to ([a-zA-Z]+) ([a-zA-Z ]+) \(([a-zA-Z ]+) \)!')
            SignalMatch3 = SignalRegex3.search(mensaje)
            if SignalMatch3 is not None:
                # print(mensaje)
                # print(SignalMatch3.groups())
                flag_Signal3 = 1
                SignalRow3 = (linea.split("   ")[0],) + SignalMatch3.groups()
                #print(SignalRow3)

            # |  OrderSend( XAUUSD, buy, 0.10, 1592.750, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
            OrderSendRegex = re.compile(r'\|  OrderSend\( ([a-zA-Z\.]+), ([a-zA-Z ]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), \"([a-zA-Z0-9\.\#: ]+)\", ([0-9]*) \) - ([a-zA-Z\!]+)! Ticket \#([0-9]*).')
            OrderSendMatch = OrderSendRegex.search(mensaje)
            if OrderSendMatch is not None:
                # print(mensaje)
                # print(OrderSendMatch.groups())
                flag_OrderSend = 1
                OrderSendRow = (linea.split("   ")[0],) + OrderSendMatch.groups()
                #print(OrderSendRow)


            # its MISSING
            # |  OrderSend( XAUUSD, buy stop, 0.10, 1501.680, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - ERROR #10018 (Market is closed)!



            #market buy 0.1 XAUUSD (1934.050 / 1935.010)
            marketRegex = re.compile(r'market ([a-zA-Z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z]+) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch = marketRegex.search(mensaje)
            if marketRegexMatch is not None:
                #print(mensaje)
                #print(marketRegexMatch.groups())
                flag_market = 1
                marketRow = (linea.split("   ")[0],) + marketRegexMatch.groups()
                #print(marketRow)

            #market buy 0.1 EURUSD, close #10 (1.13411 / 1.13414)
            marketRegex2 = re.compile(r'market ([a-zA-Z]+) ([0-9]*[.]?[0-9]*) ([a-zA-Z]+), ([a-zA-Z]+) #([0-9]*) \(([0-9]*[.]?[0-9]*) \/ ([0-9]*[.]?[0-9]*)\)')
            marketRegexMatch2 = marketRegex2.search(mensaje)
            if marketRegexMatch2 is not None:
                #print(mensaje)
                #print(marketRegexMatch2.groups())
                flag_market2 = 1
                marketRow2 = (linea.split("   ")[0],) + marketRegexMatch2.groups()
                #print(marketRow2)



            # |  OrderClose( 272, 1.48, 1.06957, 50 ) - OK!
            OrderCloseRegex = re.compile(r'\|  OrderClose\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*) \) - ([a-zA-Z]+)!')
            OrderCloseMatch = OrderCloseRegex.search(mensaje)
            if OrderCloseMatch is not None:
                # print(mensaje)
                #print(OrderCloseMatch.groups())
                flag_OrderClose = 1
                OrderCloseRow = (linea.split("   ")[0],) + OrderCloseMatch.groups()
                #print(OrderCloseRow)





            #Join the signal together with the order and market
            if (len(SignalRow)) and (len(marketRow)) and (len(OrderSendRow) and (SignalRow[0] == marketRow[0]) and (SignalRow[0] == OrderSendRow[0])):
                if ((flag_Signal == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #Signal to open buy #1 at 1935.010 (BigCandle)!
                    #mar
                    # ket buy 0.1 XAUUSD (1934.050 / 1935.010)
                    #|  OrderSend( XAUUSD, buy, 0.10, 1935.010, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
                    if (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        print(SignalRow[0] + ";Signal to " + SignalRow[1] + ";" + SignalRow[2] + ";" + SignalRow[3] + ";" + SignalRow[5] + ";" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";" + OrderSendRow[5] + ";" + marketRow[4] + ";" + marketRow[5] + ";" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow[10] + ";" + OrderSendRow[11])
                        SignalRow = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal = 0
                        flag_market = 0
                        flag_OrderSend = 0
                    else:
                        print("Error in EA. Check Please!! Critical error-1")
                        exit()

            if (len(SignalRow2)) and (len(marketRow)) and (len(OrderSendRow) and (SignalRow2[0] == marketRow[0]) and (SignalRow2[0] == OrderSendRow[0])):
                if ((flag_Signal2 == 1) and (flag_market == 1) and (flag_OrderSend == 1)):
                    #Signal to open buy #2 at 1843.330!
                    #market buy 0.12 XAUUSD (1842.830 / 1843.330)
                    #|  OrderSend( XAUUSD, buy, 0.12, 1843.330, 50, 0.000, 0.000, "CP18.06.2021.21:03 #2", 234 ) - OK! Ticket #17.
                    if (marketRow[1] == OrderSendRow[2]) and (marketRow[3] == OrderSendRow[1]):
                        print(SignalRow2[0] + ";Signal to " + SignalRow2[1] + ";" + SignalRow2[2] + ";" + SignalRow2[3] + ";;" + OrderSendRow[1] + ";" + OrderSendRow[3] + ";" + OrderSendRow[4] + ";" + OrderSendRow[5] + ";" + marketRow[4] + ";" + marketRow[5] + ";" + OrderSendRow[8] + ";" + OrderSendRow[9] + ";" + OrderSendRow[10] + ";" + OrderSendRow[11])
                        SignalRow2 = tuple()
                        marketRow = tuple()
                        OrderSendRow = tuple()
                        flag_Signal = 0
                        flag_market = 0
                        flag_OrderSend = 0
                    else:
                        print("Error in EA. Check Please!! Critical error-2")
                        exit()

            if (len(SignalRow3)) and (len(marketRow2)) and (len(OrderCloseRow) and (SignalRow3[0] == marketRow2[0]) and (SignalRow3[0] == OrderCloseRow[0])):
                if ((flag_Signal3 == 1) and (flag_market2 == 1) and (flag_OrderClose == 1)):
                    #Signal to close sell (FIBO )!
                    #market buy 0.1 EURUSD, close #10 (1.13411 / 1.13414)
                    #|  OrderClose( 10, 0.10, 1.13414, 50 ) - OK!
                    if (marketRow2[5] == OrderCloseRow[1]):
                        print(SignalRow3[0] + ";Signal to " + SignalRow3[1] + ";" + SignalRow3[2] + ";;" + SignalRow3[3] + ";" + marketRow2[3] + ";" + OrderCloseRow[2] + ";" + OrderCloseRow[3] + ";" + OrderCloseRow[4] + ";" + marketRow2[6] + ";" + marketRow2[7] + ";;;" + OrderCloseRow[5]+ ";" + OrderCloseRow[1])
                        SignalRow3 = tuple()
                        marketRow2 = tuple()
                        OrderCloseRow = tuple()
                        flag_Signal = 0
                        flag_market = 0
                        flag_OrderClose = 0
                    else:
                        print("Error in EA. Check Please!! Critical error-3")
                        exit()
            continue


            # its MISSING
            #--------------------------------------------------------------------------------------------
            #TrailingStop
            #--------------------------------------------------------------------------------------------
            #MS	0	02:50:27.323	Core 1	2020.10.09 17:02:50   TrailingStop for BUY: 0 -> 1920.37
            #JD	0	02:50:27.323	Core 1	2020.10.09 17:02:50   Modifying SL for buy-order #97: 0.000 -> 1920.370...
            #IG	0	02:50:27.323	Core 1	2020.10.09 17:02:50   position modified [#97 buy 0.19 XAUUSD 1885.770 sl: 1920.370]
            #PI	0	02:50:27.323	Core 1	2020.10.09 17:02:50   |  OrderModify( 97, 1885.770, 1920.370, 0.000 ) - OK!
            #KL	0	02:50:27.323	Core 1	2020.10.09 17:02:50   Modifying SL for buy-order #96: 0.000 -> 1920.370...
            #OL	0	02:50:27.323	Core 1	2020.10.09 17:02:50   position modified [#96 buy 0.11 XAUUSD 1969.460 sl: 1920.370]
            #RF	0	02:50:27.323	Core 1	2020.10.09 17:02:50   |  OrderModify( 96, 1969.460, 1920.370, 0.000 ) - OK!
            #FALTA TERMINAR
            #"Time;Action;Type;Martingale;Price;Signal;Symbol;Type;Volume;Price;ValorX;Precio1;Precio2;Comment;MagicID;Status;Ticket #"
            #TrailingStop for BUY: 0 -> 1920.37
            TrailingStopRegex = re.compile(r'TrailingStop for ([a-zA-Z]+): ([0-9]+) -> ([0-9]*[.]?[0-9]*)')
            TrailingStopMatch = TrailingStopRegex.search(mensaje)
            if TrailingStopMatch is not None:
                # print(mensaje)
                #print(TrailingStopMatch.groups())
                flag_TrailingStop = 1
                TrailingStopRow = linea.split("   ")[0] + "TrailingStop for;" +  TrailingStopMatch.group(1) + ";;"  + TrailingStopMatch.group(2) + ";" + TrailingStopMatch.group(3)
                #print(TrailingStopRow)

            #PI	0	02:50:27.323	Core 1	2020.10.09 17:02:50   |  OrderModify( 97, 1885.770, 1920.370, 0.000 ) - OK!
            #RF	0	02:50:27.323	Core 1	2020.10.09 17:02:50   |  OrderModify( 96, 1969.460, 1920.370, 0.000 ) - OK!
            OrderModifyRegex = re.compile(r'\|  OrderModify\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*) \) - ([a-zA-Z]+)!')
            OrderModifyMatch = OrderModifyRegex.search(mensaje)
            if OrderModifyMatch is not None:
                # print(mensaje)
                #print(OrderModifyMatch.groups())
                flag_OrderModify = 1
                OrderModifyRow = linea.split("   ")[0] + ";;;;;" + OrderModifyMatch.group(2) + ";" + OrderModifyMatch.group(3) + ";;" + OrderModifyMatch.group(4) + ";" + OrderModifyMatch.group(5) + ";" + OrderModifyMatch.group(1)
                #print(OrderModifyRow)

            #FALTA TERMINAR
            if (TrailingStopRow.split(";")[0] == OrderModifyRow.split(";")[0]):
                if ((flag_TrailingStop) and (flag_OrderModify)):
                    OrderModifyRow=OrderModifyRow.replace(TrailingStopRow.split(";")[0], '')
                    #print(TrailingStopRow + ";" + OrderModifyRow)
                    OrderModifyRow = ""
                    flag_OrderModify = 0
                    continue


#text_box.insert(tk.INSERT , match.groups())
# window.mainloop()
