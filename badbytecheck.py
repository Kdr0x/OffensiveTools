#!/usr/bin/python3

########################################################################

"""
Author: 	Gary "kd" Contreras
Title:		Bad Byte Check
Purpose:	For use when doing exploit development
Original Test:	Tested against "vulnserver" application
Python Engine:	Python 3

Instructions to configure this tool:

*	Configure line 63 to automatically skip over any known "bad" bytes/chars
*	Configure line 67 to the dumpedbytefile path or just pass it on the command line, which will overwrite the default

Usage:
	./badbytecheck.py [/path/to/dumpedbytes.bin]

Notes:
	Generally the way I use this is to set up a SMB server with anonymous read/write permissions and mount it from my 
	Windows exploit dev VM. This is so that I can export a binary file from my debugging session with the bytes I want 
	to check. It's easiest to automate this bad byte checking process so that you don't accidentally miss anything. I 
	am just trying to raise the percentage chance that we are going to have an excellent and successful exploit development 
	adventure. :)
	
	The tool works by reading in the dumped bytes binary file first. Then it creates an array of binary byte values 0-255. 
	From there, it starts going through the binary values 0-255, skipping the "bad" bytes that were already defined, as they 
	should not be detected in the dumped file (in order) if we already knew about them, right? Well, even though we are skipping 
	their "order" within the range of 0-255, they will still be detected if the tool finds them as a result of truncation or 
	mangling. The "skip" functionality is simply in regards to their "order" in the check, not whether they exist in the dumped 
	output. The allbytes and dumpedbytes values are checked against each other in order and when a mismatch is detected, it gets 
	reported as output so you know where the problem is. Verify it with hexdump! It will look like the following:
	
	# ./badbytecheck.py /opt/writable/bytes.bin
	[*] Detected byte mismatch on allbytes value 21 (0x15) when compared to dumpedbytes value 0 (0x0) at file offset 0x12 inside /opt/writable/bytes.bin
	[*] Detected byte mismatch on allbytes value 26 (0x1a) when compared to dumpedbytes value 47 (0x2f) at file offset 0x17 inside /opt/writable/bytes.bin
		                                                                                                                                                                          
	# hexdump -C /opt/writable/bytes.bin 
	00000000  01 02 03 04 05 06 07 08  09 0b 0c 0e 0f 10 11 12  |................|
	00000010  13 14 00 16 17 18 19 2f  1b 1c 1d 1e 1f 20 21 22  |......./..... !"|
	00000020  23 24 25 26 27 28 29 2a  2b 2c 2d 2e 2f 30 31 32  |#$%&'()*+,-./012|
	00000030  33 34 35 36 37 38 39 3a  3b 3c 3d 3e 3f 40 41 42  |3456789:;<=>?@AB|
	00000040  43 44 45 46 47 48 49 4a  4b 4c 4d 4e 4f 50 51 52  |CDEFGHIJKLMNOPQR|
	00000050  53 54 55 56 57 58 59 5a  5b 5c 5d 5e 5f 60 61 62  |STUVWXYZ[\]^_`ab|
	00000060  63 64 65 66 67 68 69 6a  6b 6c 6d 6e 6f 70 71 72  |cdefghijklmnopqr|
	00000070  73 74 75 76 77 78 79 7a  7b 7c 7d 7e 7f 80 81 82  |stuvwxyz{|}~....|
	00000080  83 84 85 86 87 88 89 8a  8b 8c 8d 8e 8f 90 91 92  |................|
	00000090  93 94 95 96 97 98 99 9a  9b 9c 9d 9e 9f a0 a1 a2  |................|
	000000a0  a3 a4 a5 a6 a7 a8 a9 aa  ab ac ad ae af b0 b1 b2  |................|
	000000b0  b3 b4 b5 b6 b7 b8 b9 ba  bb bc bd be bf c0 c1 c2  |................|
	000000c0  c3 c4 c5 c6 c7 c8 c9 ca  cb cc cd ce cf d0 d1 d2  |................|
	000000d0  d3 d4 d5 d6 d7 d8 d9 da  db dc dd de df e0 e1 e2  |................|
	000000e0  e3 e4 e5 e6 e7 e8 e9 ea  eb ec ed ee ef f0 f1 f2  |................|
	000000f0  f3 f4 f5 f6 f7 f8 f9 fa  fb fc fd fe ff           |.............|
"""

########################################################################

import sys

# Define all "bad" bytes/chars here
badbytes = b'\x00\x0a\x0d'

# Ingest the dumped byte file
dumpedbytes = b''
dumpedbytefile = '/home/kali/Desktop/dumpedbytes.bin'

if len(sys.argv) == 2:
	dumpedbytefile = sys.argv[1]

with open(dumpedbytefile,'rb') as infile:
	dumpedbytes += infile.read()

# Create a range of bytes from 0-255, inclusive
allbytes = b''
for i in range(0,256):
	allbytes += i.to_bytes(1,'little')

# Don't touch these :)
skip = False			# This is used to know when to skip bytes that are known bad
dc = 0				# This is the array index counter for dumpedbytes

# Compare the bytes in the dumped byte file with those in the allbytes range, excluding the bad bytes indicated on the first line
# Report any bytes that don't match
for i in range(0,256):

	# Check whether each byte is a known "bad" char/byte, and skip it within the "allbytes" range
	for b in badbytes:
		if allbytes[i] == b:
			skip = True
			break
	
	# Continue to the next byte within "allbytes" if there's a byte we need to skip
	if skip == True:
		skip = False
		continue
	
	# Check if the current allbytes value is the same as the current dumpedbytes value; report if they are mismatched!
	if allbytes[i] == dumpedbytes[dc]:
		dc += 1
	else:
		print('[*] Detected byte mismatch on allbytes value {0} ({1}) when compared to dumpedbytes value {2} ({3}) at file offset {4} inside {5}'.format(allbytes[i], hex(allbytes[i]), dumpedbytes[dc], hex(dumpedbytes[dc]), hex(dc), dumpedbytefile))
		dc += 1