#------------------------------------------------------------------------------
# Read in the MIR file specified and do preliminary data processing
# \param fileName : the path of the file that is to be read in
# \param uncomment [debug] : whether the read in data is to be uncommented
# \param echo[debug] : whether the data is to be printed on screen
# \return splitData : the data stream with all the dat split in a char basis
# \return joinedData : the splitData is joined to make legible words
def readFile(filePath,uncomment = True,echo = False):
	f = open(filePath,'r') # Open file in read mode
	data = f.read() # Read the data and save as a string

	m = data.__len__()

	i = 0
	temp = []
	isCommentActive = True
	singleLineCommentStartPos = 0
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
			continue
		elif(c == '/' and data[I+1] == '/' and uncomment == True): # single line comment encountered
			temp.append(c)
			singleLineCommentStartPos = I # the position at which // is found
			i = data.find('\n',singleLineCommentStartPos) # jump to next '\n'
			continue
		elif(c=='\n'):# skip new line characters
			temp = []
			pass
		else: # just continue adding stuff
			temp.append(c)
		#end if
	#end while loop
	# Join data to form legible words
	joinedData = "".join("".join(e) for e in splitData)
	#end while loop over i

	if(echo == True):
		print(splitData)
		print(joinedData)
	return splitData,joinedData
#------------------------------------------------------------------------------
