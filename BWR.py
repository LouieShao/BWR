
import sys, getopt
from core.BWR_Compress import Compress as BWR_Compress
from core.BWR_Decompress import Decompress as BWR_Decompress
import struct
import cv2
def main(argv):
    inputfile=0
    outputfile=0
    bitsunit=1
    mode=0 # 0: Compress mode; 1: Decompress mode
    try:
        
        opts, args = getopt.getopt(argv, "cdhi:o:u:r",[])
    except getopt.GetoptError:
        print('argv Error!\nUsage: test_arg.py -i <inputfile> -o <outputfile>\n')
        print('Arguments:\n')
        print('-i# : Set input file as #\n')
        print('-o# : Set output file as #\n')
        print('-h  : Display help form\n')
        print('-u# : Set the bit unit as #\n')
        print('-c  : Use compression mode\n')
        print('-d  : Use decompression mode\n')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print('Usage:test_arg.py -i <inputfile> -o <outputfile>\n')
            print('Arguments:\n')
            print('-i# : Set input file as #\n')
            print('-o# : Set output file as #\n')
            print('-h  : Display help form\n')
            print('-u# : Set the bit unit as #\n')
            print('-c  : Use compression mode\n')
            print('-d  : Use decompression mode\n')
            sys.exit(0)
        elif opt in ("-c"):
            mode=0
        elif opt in ("-d"):
            mode=1
        elif opt in ("-i", "--infile"):
            inputfile = arg
        elif opt in ("-o", "--outfile"):
            outputfile = arg
        elif opt in ("-u"):
            #arg=4
            if arg in (1,4,'1','4'):
                bitsunit=int(arg)
            else:
                print('Invalid bit unit! Try 1 or 4 instead.')
                sys.exit(2)
    Compress=BWR_Compress()
    Decompress=BWR_Decompress()
    
    if mode==0:
        rawdata=cv2.imread(inputfile)
        outputdata=Compress.Run_DPCM_BWR_Compress(rawdata,bitsunit)
    elif mode==1:
        data=open(inputfile,'rb').read()
        data_int=[]
        for i in data:
            data_int.append(int(i))
        outputdata=Decompress.Run_DPCM_BWR_Deompress(data_int,bitsunit)
    fp=open(outputfile, 'wb')
    for x in outputdata:
        x&=255
        a=struct.pack('B', x)
        fp.write(a)
    fp.close()
    print('Finish. Output file is in '+outputfile+'.')
    exit(0)




if __name__ == '__main__':
    main(sys.argv[1:])