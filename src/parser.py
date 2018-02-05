import samirStandardV1 as sv

#------------------------------------------------------------------------------
# Find the next lex in the lex data stream
# \param xi: Search start position
# \param toFind: The lexem to be found
# \param lexd: Lex data stream
def findNextLex(xi,toFind,lexd):
	n = lexd.__len__()
	i = xi
	found = False
	# Search over the given interval until a lex is found 
	while i<n:
		I = i
		i = i+1
		if (lexd[I].uid == toFind.uid):
			# The lex is found
			found = True
			return I
		#endif
	#end while loop 

	# If lex is not found then return error
	if (found == False):
		print('LEX NOT FOUND')
		return -1       


#------------------------------------------------------------------------------
# Find splice object position in lexd 

def findSpliceObjectPos(cmat,corder,lexd):
	m = corder.__len__()
	o = lexd.__len__()
	i = 0
	j = 0
	spObjPos = [] # Position of the spObj in lexd for further use
	
	while i<m: # For each splice object in corder
		I = i
		i = i+1
		n = cmat[I].__len__()
		while j<n: # For each splice object index in cmat
			J = j
			j = j+1
			indexObj = cmat[I][J]
			k = 0
			while k<o: # For each element in lexd see if the indices match and
			# if they do match then store it in a list
				K = k
				k = k+1
				if(K !=0):
					if(lexd[K-1].uid != sv.SCOLON.uid):
						continue
					#endif
				#endif 
				if(lexd[K].uid == corder[I].uid):
					if(lexd[K+2].constData == indexObj.constData):
						spObjPos.append(K)
					#endif
				#endif
			#end while loop over k
		#end while loop over j
	#end while loop over i
	return spObjPos

#------------------------------------------------------------------------------
# Find splice bounds
# If the splice is to start from Point(1) and to end at Point(5) for example
# return the start as 1 and the end as 5
# TODO : Code it if it is needed.
# But for now, we can use the lines and splice to form unique vector
def findSpliceBounds():
	pass 

#------------------------------------------------------------------------------
# Find subdivision vector

def findSubdivVec(spObjPos,lexd):
	m = spObjPos.__len__()
	i = 0
	subdivVec = []
	#subdivPosVec = []
	while i<m:
		I = i
		i = i+1
		xi = spObjPos[I]
		spObj = lexd[xi]
		subdivPos = findNextLex(xi,sv.SUBDIV,lexd)

		if(subdivPos > findNextLex(xi,sv.SCOLON,lexd)):
			#error 
			print('ERR : No suitable subdivision is found for spObjPos')
			print(xi)
			exit()
		else:
			subdivVec.append(lexd[subdivPos+2])
			#subdivPosVec.append(xi)
		#endif
	#end while
	return subdivVec

#------------------------------------------------------------------------------
# Find control node indices that will be then sorted and arranged 
def findControlNodeIndices(spObjPos,isPeriodic_BC,lexd):
	
	m = spObjPos.__len__()
	i = 0
	unsortedNodeVec = []
	sortedNodeVec = []
	while i<m:
		I = i
		i = i+1
		spObj = lexd[spObjPos[I]]
		if(spObj.uid == sv.LINE.uid):
			pointPos = findNextLex(spObjPos[I],sv.POINT,lexd)
			if(pointPos > findNextLex(spObjPos[I],sv.SCOLON,lexd)):
				print('ERR : Did not find sv.POINT before sv.SCOLON')
				exit()
			else:
				unsortedNodeVec.append(lexd[pointPos]) # sv.POINT
				unsortedNodeVec.append(lexd[pointPos+2]) # P1
				unsortedNodeVec.append(lexd[pointPos]) # sv.POINT
				unsortedNodeVec.append(lexd[pointPos+4]) # P2
		elif(spObj.uid == sv.SPLINE.uid):
			pass
		else:
			print('ERR : Unkwown splice object is passed to find control node')
			print(spObj)
			exit()
		#endif
	#end while

	#Sorting algorithm
	n = unsortedNodeVec.__len__()
	j = 1
	P1 = 0
	P2 = 0

	while j<n:
		J = j
		if(unsortedNodeVec[J-1].uid == sv.POINT.uid):
			P1 = unsortedNodeVec[J]
			P2 = unsortedNodeVec[J+2]
			P3 = unsortedNodeVec[j+4]
			P4 = unsortedNodeVec[j+6]
			if(P1.constData == P3.constData):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P2)
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P1)
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P4)
				# go to next elements
				j = j+8
				print('WORK TODO HERE')
				exit()
			elif(P2.constData == P3.cosntData):
				pass
			#endif
	if(isPeriodic_BC):
		pass
	#endif



#------------------------------------------------------------------------------
# Collect point indices from splice collection matrix and sort them in an 
# unique vector
def formWall(cmat,corder,corderpos,lexd):
	# Splice object positions
	spObjPos = findSpliceObjectPos(cmat,corder,lexd)
	isPeriodic_BC = False # Is a periodic BC present ?

	#print(lexd[spObjPos[0]]) # LINE or SPLINE etc
	#print(lexd[spObjPos[0]+2]) # indices 1,2,3 etc

	if(lexd[spObjPos[0]].uid == lexd[spObjPos[-1]].uid):
		if(lexd[spObjPos[0]+2].constData == lexd[spObjPos[-1]+2].constData):
			print('PERIODIC BC')
			isPeriodic_BC = True
		else:
			print('NON-PERIODIC BC')
			isPeriodic_BC = False
		#endif
	#endif

	# Find subdivision vector
	subdivVec = findSubdivVec(spObjPos,lexd)

	# TODO : Find and sort control node indices
	sortedNodeIndices= findControlNodeIndices(spObjPos,isPeriodic_BC,lexd)
	# TODO : Generate wall as  2 numpy arrays and populate  them with x and y
	# co-ordiantes respectively of the wall boundary

	print(spObjPos)
	print(subdivVec)
	print('mark test')
	exit()
#------------------------------------------------------------------------------
# Prepare the splice objects 
# TODO : Documentation
def collectSpliceObjects(xi,forLex,lexd):
	#cfg := [collectLex,sv.LSQR,sv.COLLECT_INDICES,sv.RSQR]
	start = findNextLex(xi,sv.LSQR,lexd)
	end = findNextLex(xi,sv.RSQR,lexd)
	#print('start : ',start,'| end : ',end)
	spliceObjects = []
	i = start
	while i < end:
		I = i
		i = i+1
		if(lexd[I].uid == sv.basic_INT_CONST.uid):
			if (I == start):        
				spliceObjects[0] = lexd[I]
			else:
				spliceObjects.append(lexd[I])
			#endif
		#endif
	#end while loop
	print('spliceObjects : ',spliceObjects)
	print('spliceObjects have been prepared')
	return spliceObjects

#------------------------------------------------------------------------------
# Prepare the order in which the lex are to be collected
# eg { Line[1,2] + Spline[3,4] + Line[3,4] => return [LINE,SPLINE,LINE]
# \param xi: Start position
# \param collect: The lex which are allowed to be collected
# \param lexd: The lex data stream
def makeLexCollectionOrder(xi,collect,lexd):
	n = lexd.__len__()
	m = collect.__len__()
	i = xi
	j = 0
	collectOrder = []
	collectOrderPos = []
	endLine = findNextLex(xi,sv.SCOLON,lexd)
	print('Current position : ',xi)
	print('Next SCOLON position : ',endLine)
	endCollect = findNextLex(xi,sv.RCURL,lexd)
	print('Current position : ',xi)
	print('Next RCURL position : ',endCollect)

	while i<endCollect:
		I = i
		i = i+1
		for k in collect:
			if(k.uid == lexd[I].uid):
				collectOrder.append(k)
				collectOrderPos.append(I)
				continue
			#endif
		# end for loop
	#end while loop
	print('collect : ', collect)
	print('collectOrder : ',collectOrder)
	print('collectOrderPos : ',collectOrderPos)
	print('collection order prepared')
	if (collectOrder.__len__() != collectOrderPos.__len__()):
		print('ERR : collectOrder and collectOrderPos length mismatch')
		exit()
	#endif
	return collectOrder,collectOrderPos

#------------------------------------------------------------------------------
# Collect the indices of all the objects that make up the splice
# i.e collect indices of LINE,SPLINE,etc from the splice collection region.
def collectSpliceObjectIndices(xi,collect,lexd):
	n = lexd.__len__()
	i = xi # lexd iterator index
	j = 0 # collect iterator index
	points = []
	# form ordered list of the tokens to collect from
	collectOrder,collectOrderPos = makeLexCollectionOrder(xi,collect,lexd)
	m = collectOrder.__len__()
	# matrix or 2d list used to store all the indices of collectOrder
	collectionMatrix = [[]]
	# collection matrix count : collect lex indices and store it in rows
	cmCount = 0;
	# Find number of occurences  and positions of the lex in collect
	# and arrange them in an ascending order eg [LINE,SPLINE,LINE] =>
	# check if all the lex in lexd in the collect region are collectable or not
	# run the index collector for each of the elements and form two arrays
	# to contain x and y co-ordinates of the points ??????
	while j<m: #{ Iterate through collectOrder list
		J = j
		j = j+1 # update collect iterator
		c = collectOrder[J]
		if(c.uid == sv.POINT.uid):
			print('INF :: Collecting POINT')
			print('exit mark4')
			exit()
		elif(c.uid == sv.LINE.uid):
			print('INF :: Collecting LINE')
			collectionMatrix[cmCount] = collectSpliceObjects(collectOrderPos[J],
									 sv.LINE,lexd)
			collectionMatrix.append([]) # create space for next object 
			cmCount += 1 # increase collection matrix counter
		elif(c.uid == sv.SPLINE.uid):
			print('INF :: Collecting SPLINE')
			collectionMatrix[cmCount] = collectSpliceObjects(collectOrderPos[J],
									 sv.SPLINE,lexd)
			collectionMatrix.append([]) # create space for next collection
			cmCount += 1 # Increase collection matrix counter
		else:
			print('ERR :: Could not collect the requseted lexeme')
			print(collect)
			exit()
		#endif
	#end while loop }
	print('INF :: Finished collecting splice objects from splice')
	collectionMatrix.pop() # remove the last empty row []
	return collectionMatrix,collectOrder,collectOrderPos

#------------------------------------------------------------------------------
# Verify the pseudo Context Free Grammar ???? is it CFG???
# and collect the data 
def verifyCFG(xi,cfg,collect,lexd):
	n = lexd.__len__()
	i = xi # lexd iterator index
	j=0 # cgf iterator index
	while i<n: #{ 
		I = i
		i = i+1 # update lexd counter     
		J = j
		c = cfg[J]
		j = j+1 # update cfg counter
		if(c.uid == sv.COLLECT.uid):
			# Within the iteration 
			# Do collection
			"""
			@params
			cmat : Collection matrix
			corder : Collection order
			corderpos : Collection order position
			"""
			cmat,corder,corderpos = collectSpliceObjectIndices(I,collect,lexd)
			print('INF :: Collected indices of splice object')
			print('------------------- COLLECTION MATRIX -------------------')
			print(cmat)
			print('------------------- COLLECTION ORDER  -------------------')
			print(corder)
			print('-------------------COLLECTION POSITION  -----------------')
			print(corderpos)

			# Since the collection is completed so skip those lexemes
			#print(I) # test to see where we are
			i = corderpos[corderpos.__len__() - 1]
			#print(i) # test to see if i is correct
			#print(lexd[i]) # test to verifiy that we are skipping the lexemes

			# TODO : Save or return the collected data
			formWall(cmat,corder,corderpos,lexd)
			print('exit mark2')
			exit()

		elif(c.uid == lexd[I].uid):
			# cfg grammar verified print(c,' : is ok')
			pass

		else:
			print('ERROR: CFG grammar not verified')
			print('c : ',c)
			print('lexd[I] : ',lexd[I])
			exit()
		#endif
	#} end while i<n loop
	return 1

                

#------------------------------------------------------------------------------
def parserStdV1(lexdata):
	lexd = lexdata
	n = lexd.__len__()
	SOUTH_WALL_PROCESSED = False
	NORTH_WALL_PROCESSED = False
	i=0     
	while i<n:
		I = i
		c = lexd[I]
		i = i+1
		if(c.uid == sv.SOUTH_WALL.uid and SOUTH_WALL_PROCESSED == False):
			print('SOUTH_WALL found')
			cfg = [sv.SOUTH_WALL,sv.ASSIGN,sv.NEW,sv.SPLICE,sv.LPAREN,sv.FROM,
			sv.POINT,sv.LSQR,sv.basic_INT_CONST,sv.RSQR,sv.TO,sv.POINT,sv.LSQR,
			sv.basic_INT_CONST,sv.RSQR,sv.COMMA,sv.BY,sv.LCURL,sv.COLLECT,sv.RCURL,
			sv.RPAREN,sv.SCOLON]

			collect = [sv.LINE,sv.SPLINE]
			#print(cfg)

			verifyCFG(I,cfg,collect,lexd)
			print('EXIT mark1')     
			exit()
		elif(c.uid == sv.NORTH_WALL.uid and SOUTH_WALL_PROCESSED == True and NORTH_WALL_PROCESSED == False):
			print('NORTH_WALL found')

			cfg = [sv.NORTH_WALL,sv.ASSIGN,sv.NEW,sv.SPLICE,sv.LPAREN,sv.FROM,
			sv.POINT,sv.LSQR, sv.basic_INT_CONST,sv.RSQR,sv.TO,sv.POINT,sv.LSQR,
			sv.basic_INT_CONST,sv.RSQR,sv.COMMA,sv.BY,sv.LCURL,sv.COLLECT,sv.RCURL,
			sv.RPAREN,sv.SCOLON]
			
			collect = [sv.LINE,sv.SPLINE]
		#endif
	return 0,0
