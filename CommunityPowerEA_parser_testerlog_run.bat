set DATENOW=20210808
c:\Python38\python.exe CommunityPowerEA_parser_testerlog.py > %DATENOW%.csv
c:\Python38\python.exe CommunityPowerEA_convert_CSV_To_Excel.py -i %DATENOW%.csv -o %DATENOW%.xlsx
