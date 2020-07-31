# BWR
BWR is a pre-compression algorithm (or called filtering algorithm). It can rearrange the bits of the data, in different ways, to make the redundance of data utilized.  After using BWR to filter the data of images, you can use various compression algorithm to compress the data, from which, you can get a better compression ratio than compress without BWR. This repository provides both a compressor and a decompressor. It is written in python for showing the compression ratio we can get, but can be less efficient than a C/C++ version which will be released in the future.

Notice: BWR "CAN NOT DIRECTLY" compress data. Instead, it is a filtering algorithm for compression algorithm better compress it. For instance, try python BWR.py -c -i your_image -o output, then, lz4 output. You will get improvements in most cases.

## Usage

Try python BWR.py -arguments

arguments:

-i# : Set input file as #

-o# : Set output file as #

-h  : Display help form

-u# : Set the bit unit as #

-c  : Use compression mode

-d  : Use decompression mode

### Liscence

This work is under BSD-3-Clause License. 
 
