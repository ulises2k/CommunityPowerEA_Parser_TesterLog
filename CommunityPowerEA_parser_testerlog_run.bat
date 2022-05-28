set DATENOW=20220209
c:\Python38\python.exe CommunityPowerEA_parser_testerlog.py -mt5_visual_mode_checked off > %DATENOW%.csv 
c:\Python38\python.exe CommunityPowerEA_convert_CSV_To_Excel.py -i %DATENOW%.csv -o %DATENOW%.xlsx
