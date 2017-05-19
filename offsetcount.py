'''
Script Name: offsetcount.py
Version: 1
Revised Date: 11/06/2014
Python Version: 3
Description: A module for visualizing how accurate a record size matches the structured file.
A potentially valid record size will have at least one 100% at the start of the each field.
Copyright: 2014 Mike Felch <mike@linux.edu> 
URL: http://www.forensicpy.com/
--
- ChangeLog -
v1 - [11-06-2014]: Original code
'''

from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.filedialog

import os
import sys

def offsetcount(filename, recordsize):
	"""
	Tally non-0x00/FF bytes at each offset of the provided record size.
	"""

	# Open the filename for binary read only access.
	hfile = open(filename, 'rb')

	# Display file size.
	filesize = os.fstat(hfile.fileno()).st_size
	print('Size: ', filesize)

	# Create a dictionary to store the count of each byte.
	record = {}

	# Initialize the dictionary (create an entry for each offset in the record and set it to zero).
	for offset in range(recordsize):
		record[offset] = 0

	# Infinite loop terminated within.
	while True:

		# Read one record at a time.
		data = hfile.read(recordsize)

		# Stop if we are unable to get an entire record.
		if len(data) != recordsize:
			break

		# Check each offset within the record.
		offset = 0
		for byte in data:
			if byte not in (0, 255): 
				record[offset] += 1
			offset += 1

	for k, v in record.items():
		if v:
			print(k, v, '{:.2%}'.format(round(v / (filesize//recordsize),4)), sep='\t')

	hfile.close()

def main():
	"""
	Usage: offsetcount.py <recordsize> <filename>
	"""
	file_name = tkinter.filedialog.askopenfilename()
	offset = tkinter.simpledialog.askstring('Record Size','Please enter a record size to see the results:')
	offset = int(offset)
	offsetcount(file_name, offset)

if __name__ == "__main__": main ( )
