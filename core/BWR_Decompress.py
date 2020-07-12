import cv2
import matplotlib.pyplot as plt
import struct
import os
import random
import math
from core.BWR_Error_List import Error_List as BWR_Error_List

class Decompress():
    def BWR_Figure_out_size(self,BWRdata):
        oribytes=int(len(BWRdata)/9)*8
        codingbytes=len(BWRdata)
        return oribytes,codingbytes
    def BWR_Decode_4(self,BWRdata,oribytes,codingbytes):
        outputarr=[] # To save the decoded data
        coding_bit_handled=4 # The bit handled in coding data 
        #let decoding_bit_handled=8
        #let decoding_index=0 # The index of decoding array, ranging [0,oribytes) 
        coding_index=0 # The index of coding array, ranging [0,codingbytes)
        # Init the output array
        for i in range(0,oribytes):
            outputarr.append(0)
        for decoding_bit_handled in range(5,-1,-4):
            for decoding_index in range(0,oribytes):
                outputarr[decoding_index]|=((BWRdata[coding_index]&int(0xF*math.pow(2,coding_bit_handled)))>>coding_bit_handled)<<decoding_bit_handled
                coding_bit_handled-=4
                if coding_bit_handled<0:
                    coding_bit_handled=4
                    coding_index+=1
        coding_bit_handled=7
        for decoding_bit_handled in range(0,-1,-1):
            for decoding_index in range(0,oribytes):
                outputarr[decoding_index]|=((BWRdata[coding_index]&int(math.pow(2,coding_bit_handled)))>>coding_bit_handled)<<decoding_bit_handled
                coding_bit_handled-=1
                if coding_bit_handled<0:
                    coding_bit_handled=7
                    coding_index+=1
        return outputarr
    def BWR_Decode(self,BWRdata,oribytes,codingbytes):
        outputarr=[] # To save the decoded data
        coding_bit_handled=7 # The bit handled in coding data 
        #let decoding_bit_handled=8
        #let decoding_index=0 # The index of decoding array, ranging [0,oribytes) 
        coding_index=0 # The index of coding array, ranging [0,codingbytes)
        # Init the output array
        for i in range(0,oribytes):
            outputarr.append(0)
        for decoding_bit_handled in range(8,-1,-1):
            for decoding_index in range(0,oribytes):
                outputarr[decoding_index]|=(BWRdata[coding_index]&int(math.pow(2,coding_bit_handled))>>coding_bit_handled)<<decoding_bit_handled
                coding_bit_handled-=1
                if coding_bit_handled<0:
                    coding_bit_handled=7
                    coding_index+=1
        return outputarr
    def Flagreconvert(self,difarr):
        outputarr=[] 
        for i in difarr:
            if i&1==1:
                outputarr.append(~(i>>1))
            else:
                outputarr.append(i>>1)
        return outputarr
    def DPCM_Refilter(self,filtereddata):
        outputarr=[]
        outputarr.append(filtereddata[0])
        outputarr.append(filtereddata[1])
        outputarr.append(filtereddata[2])
        for i in range(3,len(filtereddata)):
            outputarr.append(filtereddata[i]+outputarr[i-3])
        return outputarr
    def Run_DPCM_BWR_Deompress(self,compresseddata,bitsunit):
        temp1=0
        temp2=0
        temp3=0
        oribytes,codingbytes=self.BWR_Figure_out_size(compresseddata)
        if bitsunit==4:
            temp1=self.BWR_Decode_4(compresseddata,oribytes,codingbytes)
        elif bitsunit==1:
            
            temp1=self.BWR_Decode(compresseddata,oribytes,codingbytes)
        else:
            return BWR_Error_List.ERROR_3
        temp2=self.Flagreconvert(temp1)
        temp3=self.DPCM_Refilter(temp2)
        return temp3
        

