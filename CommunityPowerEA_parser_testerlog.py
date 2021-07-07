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
# https://realpython.com/python-gui-tkinter/
#window = tk.Tk()
#window.title("Community Power Parser Log Tester - @Ulises2k for CommunityPower EA")
#window.rowconfigure(0, minsize=800, weight=1)
#window.columnconfigure(1, minsize=800, weight=1)
#text_box = tk.Text()
# text_box.pack()

# Variables Clean
SignalRow = ""
SignalRow2 = ""
SignalRow3 = ""
OrderSendRow = ""
OrderCloseRow = ""
TrailingStopRow = ""
OrderModifyRow = ""

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
print("Time;Action;Type;Martingale;Price;Signal;Symbol;Type;Volume;PriceAction;ValueX;Price1;Price2;Comment;MagicID;Status;Ticket #")

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
            # QM	0	02:50:15.116	Core 1	2020.09.21 17:40:00   Signal to open buy #2 at 1885.770!
            # OE	0	02:50:15.116	Core 1	2020.09.21 17:40:00   market buy 0.19 XAUUSD (1885.400 / 1885.770)
            # GQ	0	02:50:15.116	Core 1	2020.09.21 17:40:00   deal #97 buy 0.19 XAUUSD at 1885.770 done (based on order #97)
            # EO	0	02:50:15.116	Core 1	2020.09.21 17:40:00   deal performed [#97 buy 0.19 XAUUSD at 1885.770]
            # HR	0	02:50:15.116	Core 1	2020.09.21 17:40:00   order performed buy 0.19 at 1885.770 [#97 buy 0.19 XAUUSD at 1885.770]
            # KH	0	02:50:15.116	Core 1	2020.09.21 17:40:00   |  OrderSend( XAUUSD, buy, 0.19, 1885.770, 50, 0.000, 0.000, "CP18.06.2021.21:03 #2", 234 ) - OK! Ticket #97.

            # Signal to open buy #1 at 1490.790 (BigCandle + IdentifyTrend + TDI)!
            SignalRegex = re.compile(r'Signal to ([a-zA-Z ]+) ([a-zA-Z ]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*) \(([a-zA-Z+ ]+)\)!')
            SignalMatch = SignalRegex.search(mensaje)
            if SignalMatch is not None:
                # print(mensaje)
                # print(SignalMatch.groups())
                flag_Signal = 1
                SignalRow = linea.split("   ")[0] + ";" + "Signal to " + SignalMatch.group(1) + ";" + SignalMatch.group(2) + ";" + SignalMatch.group(3) + ";" + SignalMatch.group(4) + ";" + SignalMatch.group(5)
                #print(SignalRow)

            # Signal to open buy #2 at 1885.770!
            SignalRegex2 = re.compile(r'Signal to ([a-zA-Z]+) ([a-zA-Z ]+) \#([0-9]+) at ([0-9]*[.]?[0-9]*)!')
            SignalMatch2 = SignalRegex2.search(mensaje)
            if SignalMatch2 is not None:
                # print(mensaje)
                # print(SignalMatch.groups())
                flag_Signal2 = 1
                SignalRow2 = linea.split("   ")[0] + ";" + "Signal to " + SignalMatch2.group(1) + ";" + SignalMatch2.group(2) + ";" + SignalMatch2.group(3) + ";" + SignalMatch2.group(4)
                #print(SignalRow2)

            # Signal to close sell (FIBO )!
            SignalRegex3 = re.compile(r'Signal to ([a-zA-Z]+) ([a-zA-Z ]+) \(([a-zA-Z ]+) \)!')
            SignalMatch3 = SignalRegex3.search(mensaje)
            if SignalMatch3 is not None:
                # print(mensaje)
                # print(SignalMatch3.groups())
                flag_Signal3 = 1
                SignalRow3 = linea.split("   ")[0] + ";" + "Signal to " + SignalMatch3.group(1) + ";" + SignalMatch3.group(2) + ";;;" + SignalMatch3.group(3)
                #print(SignalRow3)

            # |  OrderSend( XAUUSD, buy, 0.10, 1592.750, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - OK! Ticket #2.
            OrderSendRegex = re.compile(r'\|  OrderSend\( ([a-zA-Z\.]+), ([a-zA-Z ]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), \"([a-zA-Z0-9\.\#: ]+)\", ([0-9]*) \) - ([a-zA-Z\!]+)! Ticket \#([0-9]*).')
            OrderSendMatch = OrderSendRegex.search(mensaje)
            if OrderSendMatch is not None:
                # print(mensaje)
                #print(OrderSendMatch.groups())
                flag_OrderSend = 1
                OrderSendRow = linea.split("   ")[0] + ";" + OrderSendMatch.group(1) + ";" + OrderSendMatch.group(2) + ";" + OrderSendMatch.group(3) + ";" + OrderSendMatch.group(4) + ";" + OrderSendMatch.group(5) + ";" + OrderSendMatch.group(6) + ";" + OrderSendMatch.group(7) + ";" + OrderSendMatch.group(8) + ";" + OrderSendMatch.group(9) + ";" + OrderSendMatch.group(10) + ";" + OrderSendMatch.group(11)
                #print(OrderSendRow)

            # |  OrderSend( XAUUSD, buy stop, 0.10, 1501.680, 50, 0.000, 0.000, "CP18.06.2021.21:03 #1", 234 ) - ERROR #10018 (Market is closed)!
            # FALTA TERMINAR


            #GE	0	09:33:09.610	Core 1	2020.03.23 00:05:08   Signal to close sell (FIBO )!
            #MN	0	09:33:09.610	Core 1	2020.03.23 00:05:08   market buy 1.48 EURUSD, close #272 (1.06935 / 1.06957)
            #OM	0	09:33:09.610	Core 1	2020.03.23 00:05:08   deal #273 buy 1.48 EURUSD at 1.06957 done (based on order #273)
            #CD	0	09:33:09.610	Core 1	2020.03.23 00:05:08   deal performed [#273 buy 1.48 EURUSD at 1.06957]
            #MJ	0	09:33:09.610	Core 1	2020.03.23 00:05:08   order performed buy 1.48 at 1.06957 [#273 buy 1.48 EURUSD at 1.06957]
            #LD	0	09:33:09.610	Core 1	2020.03.23 00:05:08   |  OrderClose( 272, 1.48, 1.06957, 50 ) - OK!
            # |  OrderClose( 272, 1.48, 1.06957, 50 ) - OK!
            OrderCloseRegex = re.compile(r'\|  OrderClose\( ([0-9]+), ([0-9]*[.]?[0-9]*), ([0-9]*[.]?[0-9]*), ([0-9]*) \) - ([a-zA-Z]+)!')
            OrderCloseMatch = OrderCloseRegex.search(mensaje)
            if OrderCloseMatch is not None:
                # print(mensaje)
                #print(OrderCloseMatch.groups())
                flag_OrderClose = 1
                OrderCloseRow = linea.split("   ")[0] + ";" + ";" + OrderCloseMatch.group(2) + ";" + OrderCloseMatch.group(3) + ";" + OrderCloseMatch.group(4) + ";;;;;" + OrderCloseMatch.group(5) + ";" + OrderCloseMatch.group(1)
                #print(OrderCloseRow)


            #Juntar la señal junto con la orden
            if (SignalRow.split(";")[0] == OrderSendRow.split(";")[0]):
                if ((flag_Signal) and (flag_OrderSend)):
                    OrderSendRow=OrderSendRow.replace(SignalRow.split(";")[0], '')
                    print(SignalRow +  OrderSendRow)
                    SignalRow = ""
                    OrderSendRow = ""
                    flag_Signal = 0
                    flag_OrderSend = 0
                    #continue

            if (SignalRow2.split(";")[0] == OrderSendRow.split(";")[0]):
                if ((flag_Signal2) and (flag_OrderSend)):
                    OrderSendRow=OrderSendRow.replace(SignalRow2.split(";")[0], '')
                    print(SignalRow2 + ";" + OrderSendRow)
                    SignalRow2 = ""
                    OrderSendRow = ""
                    flag_Signal2 = 0
                    flag_OrderSend = 0
                    #continue

            if (SignalRow3.split(";")[0] == OrderCloseRow.split(";")[0]):
                if ((flag_Signal3) and (flag_OrderClose)):
                    OrderCloseRow=OrderCloseRow.replace(SignalRow3.split(";")[0], '')
                    print(SignalRow3 + ";" + OrderCloseRow)
                    SignalRow3 = ""
                    OrderCloseRow = ""
                    flag_Signal3 = 0
                    flag_OrderClose = 0
                    #continue




            #FALTA TERMINAR
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
                print(TrailingStopRow)

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
                    print(TrailingStopRow + ";" + OrderModifyRow)
                    OrderModifyRow = ""
                    flag_OrderModify = 0
                    continue


#text_box.insert(tk.INSERT , match.groups())
# window.mainloop()
