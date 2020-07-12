import cv2
import matplotlib.pyplot as plt
import struct
import os
import random
import math
from core.BWR_Error_List import Error_List as BWR_Error_List

#This class contains compression functions of BWR
class Compress():
    # To get the data of the input file
    # And init the output file
    def Getfile(self,inputfile,outputfile):
        input_file = cv2.imread(inputfile)
        if input_file==None:
            return ERROR_2 # the input file is not a valid image
        output_file = open(outputfile, 'wb')
        return input_file,output_file
    # A simple implementation of DPCM.
    # This function can be replaced by
    # other DPCM function if it would
    # give much redundance in high bits
    # between bytes.
    def DPCM_Filter(self,filedata):
        sp = filedata.shape
        sz1 = sp[0]#height(rows) of image
        sz2 = sp[1]#width(colums) of image
        sz3 = sp[2]#the amount of color channels
        if sz3 != 3:
            return ERROR_1 # the input file is not a RGB image
        totalpixels=sz1*sz2
        imgdif=[]
        for i in range(0,sz1):
            imgdif.append([])
        for i in imgdif:
            for j in range(0,sz2):
                i.append([])
        for i in imgdif:
            for j in i:
                for k in range(0,3):
                    j.append(None)
        previousr=0
        previousg=0
        previousb=0
        for i in range(0,sz1):
            for j in range(0,sz2):
                imgdif[i][j][0]=int(int(filedata[i,j,0])-int(previousr))
                imgdif[i][j][1]=int(int(filedata[i,j,1])-int(previousg))
                imgdif[i][j][2]=int(int(filedata[i,j,2])-int(previousb))
                previousr=filedata[i,j,0]
                previousg=filedata[i,j,1]
                previousb=filedata[i,j,2]
            diftogether=[]
        for i in range(0,sz1):
            for j in range(0,sz2):
                diftogether.append(imgdif[i][j][0])
                diftogether.append(imgdif[i][j][1])
                diftogether.append(imgdif[i][j][2])
        return imgdif,diftogether,sz1,sz2
    # To change the negative number to
    # "positive" with adding a flag bit
    def Flagconvert(self,difarr):
        output=[] # To save the converted data
        for i in difarr:
            if i<0:
                temp=((~i)<<1)|0x1
                output.append(temp)
            else:
                temp=i<<1
                output.append(temp)
        return output
    # Main function of the BWR encoder
    def BWR_Encode(self,imgdif,totalbytes):
        tempoutputbyte=0 # Store the byte generated now 0..255
        tempoutputbit=7 # The bit number of tempoutputbyte handled now
        currentbyte=0 # Store the byte handled now 0..(totalbytes-1)
        currentbit=8 # The bit number handled now 0..8
        outputarr=[] # The array for output
        while currentbit>=0:
            while currentbyte<=totalbytes-1:   
                tempoutputbyte|=((imgdif[currentbyte]&int(math.pow(2,currentbit)))>>currentbit)<<tempoutputbit
                tempoutputbit-=1
                if tempoutputbit<0:
                    outputarr.append(tempoutputbyte)
                    tempoutputbyte=0
                    tempoutputbit=7
                currentbyte+=1
            currentbit-=1
            currentbyte=0
        if tempoutputbit!=7: # Flush the tempoutputbyte if it had data left
            outputarr.append(tempoutputbyte)
        return outputarr
    # The version handling per 4 bits 
    def BWR_Encode_4(self,imgdif,totalbytes):
        tempoutputbyte=0 # Store the byte generated now 0..255
        tempoutputbit=4 # The bit number of tempoutputbyte handled now 
        currentbyte=0 # Store the byte handled now 0..(totalbytes-1)
        currentbit=5 # The bit number handled now 0,1,5
        outputarr=[] # The array for output
        while currentbit>=1:
            while currentbyte<=totalbytes-1:
                tempoutputbyte|=((imgdif[currentbyte]&int(15*math.pow(2,currentbit)))>>currentbit)<<tempoutputbit
                tempoutputbit-=4
                if tempoutputbit<0:
                    outputarr.append(tempoutputbyte)
                    tempoutputbyte=0
                    tempoutputbit=4
                currentbyte+=1
            currentbit-=4
            currentbyte=0
        if tempoutputbit!=4: # Flush the tempoutputbyte if it had data left
            outputarr.append(tempoutputbyte)
        tempoutputbyte=0 
        tempoutputbit=7 
        currentbyte=0 
        currentbit=0 
        while currentbit>=0:
            while currentbyte<=totalbytes-1:   
                tempoutputbyte|=((imgdif[currentbyte]&int(math.pow(2,currentbit)))>>currentbit)<<tempoutputbit
                tempoutputbit-=1
                if tempoutputbit<0:
                    outputarr.append(tempoutputbyte)
                    tempoutputbyte=0
                    tempoutputbit=7
                currentbyte+=1
            currentbit-=1
            currentbyte=0
        if tempoutputbit!=7: # Flush the tempoutputbyte if it had data left
            outputarr.append(tempoutputbyte)
        return outputarr
        # Run this function to convert data in
        # DPCM and BWR way.
        # Argvs:
        # @filedata: data got by function 'cv2.imread'
        # @bitsunit: Bits unit of BWR, which can be 1 or 4
        # in this library
    def Run_DPCM_BWR_Compress(self,filedata,bitsunit):
        imgdif,diftogether,sz1,sz2=self.DPCM_Filter(filedata)
        totalbytes=sz1*sz2*3
        dataconverted=self.Flagconvert(diftogether)
        outputarr=[]
        if bitsunit==1:
            outputarr=self.BWR_Encode(dataconverted,totalbytes)
        elif bitsunit==4:
            outputarr=self.BWR_Encode_4(dataconverted,totalbytes)
        else:
            return BWR_Error_List.ERROR_3 # Invalid bitsunit argv
        return outputarr
        
