#Convert CSV File to Excel File.
import pandas as pd
import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('CommunityPowerEA_convert_CSV_To_Excel.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('CommunityPowerEA_convert_CSV_To_Excel.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    #print 'Input file is "', inputfile
    #print 'Output file is "', outputfile
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    read_file = pd.read_csv (inputfile,delimiter=";")
    read_file.to_excel (outputfile, index = None, header=True)

if __name__ == "__main__":
    main(sys.argv[1:])
