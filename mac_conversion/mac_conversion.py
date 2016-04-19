#!/usr/bin/evn python
# -*- coding: utf-8 -*-
__author__ = "Riyan Setiadji"
__date__ = "March 13, 2016"

"""
MAC Conversion:

The purpose of this task is to write code that performs the MAC conversion based on the following usage specification and input/output scheme.
This conversion MUST follow the procedure that we discussed in the lecture note #6. We assume a little endian ordering is applied.


mac_conversion -T|-D [-f filename | -h hex value]
-T Use time conversion module. Either -f or -h must be given.
-D Use date conversion module. Either -f or -h must be given.
-f filename
	This specifies the path to the filenamethat includes a hex value of time or date.
	Note that the hex value should follow this notation: 0x1234.
	For the multiple hex values in either a file or a command line input, we consider only one hex value so the recursive mode for MAC conversion is optimal.
-h hex value
	This  specifies the hex value for converting to the either date or time value.
	Note that the hex value should follow this notation: 0x1234. 
	For the multiple hex value in either a file or a command line input, we consider only one hex value so the recursive mode for MAC conversion is optimal.
"""

from argparse import ArgumentParser
from datetime import datetime
import calendar

def int_to_month(number_month):
	"""
	Convert integer to month
	"""
	if number_month <=0 or number_month >= 13:
		print "Error: Month has to be 1 - 12"
	else:
		try:
			return calendar.month_name[number_month][0:3]
		except IndexError:
			return "Error: Calendar return IndexError"


def calculate_time(text_file=None, hex_val=None):
	"""
	If the arguments is to get time
	"""

	#If text file is given
	if text_file:
		#Read the input file
		#Get the first line and convert it to binary
	    input_file  = open(text_file,"r").readlines()[0].strip()
	    binary_rep = bin(int(input_file, 16))[2:].zfill(16)
	    return main_conversion_function(binary_rep)
	#if the hex value is given
	elif hex_val:
	    #Convert the hex into binary
	    binary_rep = bin(int(hex_val, 16))[2:].zfill(16)
	    return main_conversion_function(binary_rep)
	else:
	    return "Error: Invalid Arguments"


def calculate_date(text_file=None, hex_val=None):
	"""
	If the arguments is to get date
	"""
	if text_file:
	    # If a text file is given as input, then read only one hex value and convert it into binary.
	    input_file = open(text_file,"r").readlines()[0].strip()
	    binary_rep = bin(int(input_file, 16))[2:].zfill(16)
	    return main_conversion_function(binary_rep, False)
	elif hex_val:
	    # If a hex value is given as input, send it to main_conversion_function. No need to read from a file.
	    binary_rep = bin(int(hex_val, 16))[2:].zfill(16)
	    return main_conversion_function(binary_rep, False)
	else:
	    return 'Invalid arguments. Must provide either -f or -x.'


def main_conversion_function(binary_string=None, is_time=True):
	"""
	Convert the binary into little endian
	Apply appropriate conversion: time or date
	"""

	#Little endian
	little_endian = binary_string[8:16] + binary_string[0:8]

	# Time
	if is_time:
	    # Get the hour, minute, and second from the little endian
	    second = int(little_endian[11:16], 2)*2
	    minute = int(little_endian[5:11], 2)
	    hour = int(little_endian[0:5], 2)

	    if hour >= 24 or minute >= 60 or second >= 60:
	        print 'Error: Invalid Time Format'
	    else:
	    	date_format =  datetime.strptime(str(hour)+":"+str(minute)+":"+str(second), "%H:%M:%S")
	    	return "Time: " + str(date_format.strftime("%I:%M:%S %p"))
	#Date
	else:
		#Get the day, month, and year from the little endian
	    day = int(little_endian[11:16], 2)
	    month = int(little_endian[7:11], 2)
	    year = int(little_endian[0:7], 2) + 1980

	    if day > 31 or month > 12 or year > 127+1980:
	        return 'Error: Invalid Date Format'
	    else:
	        return 'Date: ' + str(int_to_month(month)) + ' ' + str(day) + ', ' + str(year)


def mac_conversion(arguments):
	"""
	Given the arguments, 
	Call the correct function
	"""
	if arguments.time:
	    print(calculate_time(arguments.filename, arguments.hex_value))
	elif arguments.date:
	    print(calculate_date(arguments.filename, arguments.hex_value))
	else:
	    print('Error: Invalid Arguments')

if __name__ == '__main__':
	"""
	Main function

	1. Getting the arguments from the user
	2. Insert the given arguments into mac_conversion function
	"""
	parser = ArgumentParser(add_help=False)
	time_or_date = parser.add_mutually_exclusive_group()
	time_or_date.add_argument('-T', '--time', action='store_true')
	time_or_date.add_argument('-D', '--date', action='store_true')
	input_format = parser.add_mutually_exclusive_group()
	input_format.add_argument('-f', '--filename', type=None)
	input_format.add_argument('-h', '--hex-value', type=None)
	arguments = parser.parse_args()
	mac_conversion(arguments)


