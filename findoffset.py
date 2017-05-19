'''
Script Name: findoffset.py
Version: 1
Revised Date: 07/13/2015
Python Version: 3
Description: A module for finding the highest potentially matched record size for structured data.
Copyright: 2015 Mike Felch <mike@linux.edu> 
URL: http://www.forensicpy.com/
--
- ChangeLog -
v1 - [11-05-2014]: Original code
'''

from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.filedialog

import os
import sys

filesize = 0

def offsetcount(filename, recordsize):
	global filesize,maxsize
	"""
	Tally non-0x00/FF bytes at each offset of the provided record size.
	"""

	# Open the filename for binary read only access.
	hfile = open(filename, 'rb')

	# Display file size.
	filesize = os.fstat(hfile.fileno()).st_size

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

	hfile.close()

	return record

def main():
	global filesize
	"""
	Usage: findoffset.py <minsize> <maxsize> <filename>
	"""
	filename = tkinter.filedialog.askopenfilename()
	minsize = tkinter.simpledialog.askstring('Minimum Record Size','Please enter the minimum record size to check:')
	maxsize = tkinter.simpledialog.askstring('Maximum Record Size','Please enter the maximum record size to check:')
	minsize = int(minsize)
	maxsize = int(maxsize)

	# Record the accuracy of each offset between min and max
	accuracy = {}

	# For each offset between min and max
	for offset in range(minsize, maxsize+1):
		recordsize = offset

		# Retrieve offset match counts
		accuracy[offset] = offsetcount(filename, offset)

		# Record total 100%'s'
		total = 0

		# For each match at offset
		for k, v in accuracy[offset].items():
			# If value exists
			if v:
				# Get percentage of matches at offset
				maxval = round(v / (filesize//offset),4)

				# If percentage is 100%, record it
				if maxval == 1.0:
					total += 1

		# Update offset total in master accuracy record
		accuracy[offset] = total

	# Should we check for max?
	check = False

	# For each offset
	for offset in accuracy:
		# If offset has a 100% match
		if accuracy[offset] >= 1:
			# Check for max value
			check = True
			print('Offset: {}\nCount: {}\r\n'.format(offset, accuracy[offset]))

	# Check for matches
	if check:
		
		# Get the highest matched offset
		maxval = max(accuracy, key=accuracy.get)
		print('-- Highest Matched Offset: {} --'.format(maxval))
	else:
		print('-- No Exact Matches Found --')
	
if __name__ == "__main__": main ( )
