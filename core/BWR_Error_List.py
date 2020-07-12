import cv2
import matplotlib.pyplot as plt
import struct
import os
import random
class Error_List():
    ERROR_1 = 1 # The input file is not a RGB image
    ERROR_2 = 2 # The input file is not a valid image
    ERROR_3 = 3 # Invalid bitsunit argv