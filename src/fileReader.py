#------------------------------------------------------------------------------
def readFile(fileName,echo = False):
	f = open(fileName,'r') # Open file in read mode
	data = f.read() # Read the data and save as a string

	if(echo == True):
		print(data)

	return data 
#------------------------------------------------------------------------------
















