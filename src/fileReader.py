#------------------------------------------------------------------------------
def readFile(fileName,uncomment = True,echo = False):
	f = open(fileName,'r') # Open file in read mode
	data = f.read() # Read the data and save as a string
	
	m = data.__len__()
	
	i = 0
	temp = []
	splitData = []
	joinedData = []

	while(i<m):
		I = i
		i = i+1
		c = data[I]
		if(c == ';'): # if ; is encountered then 
			temp.append(c)
			splitData.append(temp)
			temp = []
		elif(c == '/' and data[I+1] == '/' and uncomment == True): # single line comment encountered
			splitData.append(temp)
			temp = []
		elif(c == '\n'): # skip new line characters
			#temp.append(c)
			pass 
		else: # just continue adding stuff
			temp.append(c)
	
	# Join data
	joinedData = "".join("".join(e) for e in splitData)
	#end while loop over i
	if(echo == True):
		print(splitData)
		print(joinedData)
	return splitData,joinedData
#------------------------------------------------------------------------------
















