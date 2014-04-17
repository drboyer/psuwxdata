# prepareVal.py
#
# This simple module contains one function which prepares the values scraped
#    from the SC historical records page for database entry, which includes
#    changing trace values to (very small) numeric values and changing N/A
#    strings to None-values.
def prepareVal(value):
	if(value == 'TRACE'):
		return 0.0000000001
	elif(value == '(N/A)'):
		return None
	else:
		return value