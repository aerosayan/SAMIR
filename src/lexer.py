import samirStandardV1 as sv


#------------------------------------------------------------------------------ 
# Delimiter string to be used for text processing
DELSTR = ' ;,.()<>[]' # Every delimiter

#------------------------------------------------------------------------------ 
# Collect double value from the text data stream
# \param xi: the postion from which the collection is to begin
# \param lhs,rhs : left and right hand side bounds respectively,
#        within which the collection is to be done 
# \param data : The data from which the double is to be collected
def collectDouble(xi,lhs,rhs,data):
	dval = 0.0;
	dval = float(data[xi-lhs+1:xi+rhs])
	return dval

#------------------------------------------------------------------------------ 
# Collect integer value from the text data stream
# \param xi: the postion from which the collection is to begin
# \param lhs,rhs : left and right hand side bounds respectively,
#        within which the collection is to be done 
# \param data : The data from which the integer is to be collected
def collectInteger(xi,lhs,rhs,data):
	ival = 0;
	ival = int(data[xi-lhs+1:xi+rhs])
	return ival

#------------------------------------------------------------------------------ 
# Find the position of the next delimeter from the current position
# \param xi: The position from which the search is to begin
# \param data: The data within which the search is to be done
# \param delstr: The string containing all the delimeters for which the search
#        is to be performed
def findNext(xi,data,delstr):
	d = data[xi:] # Gather all data from the position xi to RHS
	k = 0
	deltry = [] # placeholder for find operation of delstr over d
	delxi  = []  
	for k in delstr: #{ 
		deltry.append(d.find(k))
	#} end for loop over k in delstr
	for k in deltry: #{
		if( k != -1) and (k != 0): #{ k!=0 since we are wanting to find next one
			delxi.append(k)
		#} endif
    #} end for loop over k in deltry
	if(delxi != []):
		nextPos = min(delxi)
		return nextPos # found
	else:
		return -1 # not found  



#------------------------------------------------------------------------------ 
# Find the position of the previous delimeter from the current position
# \param xi: The position from which the search is to begin
# \param data: The data within which the search is to be done
# \param delstr: The string containing all the delimeters for which the search
#        is to be performed
def findPrev(xi,data,delstr):
	d = data[:xi+1] # Gather all data from the position xi to LHS [:xi+1] is
	# used because python removes one letter forcibly during back splicing
	d = d[::-1] # Reverse the string
	prevPos = findNext(0,d,delstr)
	return prevPos

#------------------------------------------------------------------------------ 
# Find the previous and the next delimeter position from the current position
# \param xi: The position from which the search is to begin
def findTokenBounds(xi,data):
	rhs = findNext(xi,data,DELSTR)
	lhs = findPrev(xi,data,DELSTR)
	return lhs,rhs

#------------------------------------------------------------------------------ 
# Tokenize the data stream for further processing
# \param data: The data of the  MIR file
def tokenizerStdV1(data_upper,data_original):
	data = data_upper
	n = data.__len__()
	c = ''; t = '';
	i = 0 # Iteration starts at zero
	ni = 0 # next i
	lexd = [] # Placeholder fot the lexeme form of the data
	
	isCollectingString = False

	while i < n: #{
		I = i
		i = i+1 # Update iteration counter
		c = data[I] # current letter 
		t = t + c # current token
		if(c == ' '):
			t=''
			continue
		if(c == '\n'):
			t=''
			continue
		if(c == '\t'):
			t=''
			continue
		elif(c == ';'):
			lexd.append(sv.SCOLON)
			t= ''
			continue
		elif(c == ','):
			lexd.append(sv.COMMA)
			t= ''
			continue
		elif(c == '\"'):
			# Very important :: Denotes that it is a string
			# and dot(.) may be present inside it so we have to make sure that
			# this dot is not processe as a double or otherwise it will cause
			# an error when it tries to collec the string as a double
			if(isCollectingString == False): # are we currently collecting string?
				isCollectingString = True
				strEndPos = findNext(I+1,data,'\"')
				lexd.append( sv.STRING(stringData=str(data_original[I+1:I+strEndPos+1])) ) # It just works
				i = I+strEndPos+1+1 # It just works
				isCollectingString = False
				#print(lexd[-1].stringData+'HAKUNA_MATATA')
				#print(i)
				#print(data[i]
			#endif
			continue
		elif(c == '.'):
			# find if the dot belongs to any double const`
			lhs,rhs = findTokenBounds(I,data)
			dval = 0
			dval = collectDouble(I,lhs,rhs,data)
			lexd.append(sv.DBL_CONST(constData=dval))
			t= ''
			i = I+rhs;
			continue
		# Finding numerical digits such as integers and doubles
		elif(c.isdigit()== True):
			#print('FOUND DIGIT :',c)
			nextdot = findNext(I,data,'.')
			prevdot = findPrev(I,data,'.') # MARK sometimes no dot are present before
			prevdel = findPrev(I,data,DELSTR)
			nextdel = findNext(I,data,DELSTR)
			#print('nextdot : '+str(nextdot))
			#print('nextdel : '+str(nextdel))
			#print('prevdot : '+str(prevdot))
			#print('prevdel : '+str(prevdel))

	# Finding integer
			if(nextdel != nextdot and prevdel != prevdot ): # It is an interger const
				#print('Found integer')
				lhs,rhs = findTokenBounds(I,data)
				ival = 0
				ival = collectInteger(I,lhs,rhs,data)
				lexd.append(sv.INT_CONST(constData=ival))
				#print(ival)
				i = I+rhs
	# Finding double
			elif(nextdel == nextdot): # It is double const
				#print('Double encountered, dot at next del')
				i = I+nextdot # set i so that the dot lexer will take care of it
			elif(prevdel == prevdot): 
				#print('Double encountered,dot at prev del') # So we skip to the next delimiter
				i = I+nextdel
			else:
				print('collectInteger FAULT')
				exit()
			#print('HITTING CONTINUE AT END')
			t= ''
			continue
#-----------
		elif(c == '='):
			lexd.append(sv.ASSIGN)
			t= ''
			continue
		elif(c == '('):
			lexd.append(sv.LPAREN)
			t= ''
			continue
		elif(c == ')'):
			lexd.append(sv.RPAREN)
			t= ''
			continue
		elif(c =='['):
			lexd.append(sv.LSQR)
			t= ''
			continue
		elif(c==']'):
			lexd.append(sv.RSQR)
			t= ''
			continue
		elif(c=='{'):
			lexd.append(sv.LCURL)
			t=''
			continue
		elif(c=='}'):
			lexd.append(sv.RCURL)
			t=''
			continue
		elif(t == '<<'):
			lexd.append(sv.LDANG)
			t= ''
			continue
		elif(t == '>>'):
			lexd.append(sv.RDANG)
			t=''
			continue
		elif(t == 'BEGIN'):
			lexd.append(sv.BEGIN)
			t = ''
			continue
		elif(t == 'END'):
			lexd.append(sv.END)
			t = ''
			continue
		elif(t == 'POINT'):
			lexd.append(sv.POINT)
			t = ''
			continue
		elif(t == 'LINE'):
			lexd.append(sv.LINE)
			t = ''
			continue
		elif(t == 'SPLINE'):
			lexd.append(sv.SPLINE)
			t = ''
			continue
		elif(t == 'NEW'):
			lexd.append(sv.NEW)
			t = ''
			continue
		elif(t == 'FROM'):
			lexd.append(sv.FROM)
			t=''
			continue
		elif(t == 'TO'):
			lexd.append(sv.TO)
			t = ''
			continue
		elif(t == 'BY'):
			lexd.append(sv.BY)
			t=''
			continue
		elif(t == 'SUBDIV'):
			lexd.append(sv.SUBDIV)
			t=''
			continue
		elif(t == 'JOIN'):
			lexd.append(sv.JOIN)
			t=''
			continue
		elif(t == 'NORTH_WALL'):
			lexd.append(sv.NORTH_WALL)
			t=''
			continue
		elif(t == 'SOUTH_WALL'):
			lexd.append(sv.SOUTH_WALL)
			t=''
			continue
		elif(t == 'EAST_WALL'):
			lexd.append(sv.EAST_WALL)
			t=''
			continue
		elif(t == 'WEST_WALL'):
			lexd.append(sv.WEST_WALL)
			t=''
			continue
		elif(t == 'SPLICE'):
			lexd.append(sv.SPLICE)
			t=''
			continue
		elif(t == 'LERP'):
			lexd.append(sv.LERP)
			t=''
			continue
		elif(t == 'CERP'):
			lexd.append(sv.CERP)
			t=''
			continue
		elif(t == 'MESH_LINEAR'):
			lexd.append(sv.MESH_LINEAR_LEX)
			t=''
			continue
		elif(t == 'MESH_ELLIPTIC'):
			lexd.append(sv.MESH_ELLIPTIC_LEX)
			t=''
			continue
		elif(t == 'MESH_HYPERBOLIC'):
			lexd.append(sv.MESH_HYPERBOLIC_LEX)
			t=''
			continue
		elif(t == 'MESH_PARABOLIC'):
			lexd.append(sv.MESH_PARABOLIC_LEX)
			t=''
			continue




	#} end for loop over i  
	return lexd
#------------------------------------------------------------------------------ 

#------------------------------------------------------------------------------
def lexerStdV1(data):
	print('STARTING LEXER')
	data_upper  = data.upper() # convert all text to upper case
	lexd = tokenizerStdV1(data_upper,data) # send all text for tokenizing
	#print(lexd)
	return lexd
#------------------------------------------------------------------------------
