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
	subdivTypeVec = []
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
			subdivTypeVec.append(sv.INTERP_LIN_UID) # For now TODO : better way
			#subdivPosVec.append(xi)
		#endif
	#end while
	return subdivVec,subdivTypeVec

#------------------------------------------------------------------------------
# Sort by common vector
# Sort the given vector by finding the common parts and coallascing them
# eg 1,2 | 2,5 | 6,5 | 7,6 | should produce 1,2,5,6,7 for non periodic vec
# for periodic case it should handle that too
# eg 1,2 | 2,5 | 6,5 | 7,6 | 1,2 should produce 1,2,5,6,7,2,1 for non periodic vec
def sortNodeVector(unsortedNodeVec,isPeriodic_BC):
	m = unsortedNodeVec.__len__()
	sortedNodeVec = [] # placeholder

	# [P,1,P,2,P,2,P,5,][P,6,P,5,P,7,P,6,][P,1,P,2] Periodic
	# [P,1,P,2,P,2,P,5,][P,6,P,5,P,7,P,6,] Non-Periodic 
	# therefore for Periodic m mod 8 = 2*2=4
	# m mod 8 = 2*2=4 since the type of node is also added thus doubling the no.
	# and for Non periodic m mod 8 = 0
	
	# Periodicity test
	if(m%8 ==4 and isPeriodic_BC):
		pass # Periodic
	elif(m%8 ==0 and ~isPeriodic_BC):
		print('m :',m)
		pass # Non-periodic
	else:
		#TODO : Possible source of error while using periodic bc . Fix it later
		print('ERR : m%8 = 0 and isPeriodic_BC = True : are contradictory')
		print('m :',m)
		exit()
	
	# Sorting loop
	i = 0
	while i<(m - m%8): # Only loop upto m-2-1 if periodic or m-1 if non periodic
		I = i
		i = i+8
		# Generate the points
		P1 = unsortedNodeVec[I+1]
		P2 = unsortedNodeVec[I+3]
		P3 = unsortedNodeVec[I+5]
		P4 = unsortedNodeVec[I+7]
		
		# Flags
		P1P3 = False
		P1P4 = False
		P2P3 = False
		P2P4 = False

		if(P1.constData == P3.constData):
			P1P3 = True
		elif(P1.constData == P4.constData):
			P1P4 = True
		elif(P2.constData == P3.constData):
			P2P3 = True
		elif(P2.constData == P4.constData):
			P2P4 = True
		else: # Discontinuity
			print('ERR : Discontinuity in line splice')
			exit()


		# First loop : gather 3 numbers
		# Rest of the loops : gather 2 numbers
		if(I == 0): # gather 3 numbers
			if(P1P3):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P2)
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P1) # or  P3
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P4)
			elif(P1P4):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P2)
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P1) # or  P4
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P3)
			elif(P2P3):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P1)
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P2) # or  P3
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P4)
			elif(P2P4):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P1)
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P2) # or  P4
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P3)
			#endif
		elif(I > 0): # gather 2 numbers
			if(P1P3):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P1) # or  P3
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P4)
			elif(P1P4):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P1) # or  P4
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P3)
			elif(P2P3):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P2) # or  P3
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P4)
			elif(P2P4):
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P2) # or  P4
				sortedNodeVec.append(sv.POINT)
				sortedNodeVec.append(P3)
			#endif
		else: #I < 0 ?
			print('WLeF! Have you done? XD')
			print('ERR : Iterator < 0')
			exit()
		#endif I > or = 0 
	#end while loop over i

	# If periodic_BC does exist then handle it 
	if(isPeriodic_BC):
		# Make sure that discontinuities do not occur.
		if(sortedNodeVec[-1] != sortedNodeVec[3]):
			print('ERR : Discontinuity error for periodic boundary conditon')
			print('sortedNodeVec[-1] : ',sortedNodeVec[-1])
			print('sortedNodeVec[3] : ',sortedNodeVec[3])
			print('ERR : Common node numbers are not found')
			exit()
		else: # since one node is already common thus we just add the last node
			sortedNodeVec.append(sv.POINT)
			sortedNodeVec.append(sortedNodeVec[1])
	#endif
	return sortedNodeVec 


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
	sortedNodeVec = sortNodeVector(unsortedNodeVec,isPeriodic_BC)

	return sortedNodeVec


#------------------------------------------------------------------------------
# Find Control node co-ordinates
# Find the co-oridnates of the nodes that make up the wall
def findControlNodeCoordinates(sortedNodeIndices,lexd):
	m = sortedNodeIndices.__len__()
	n = lexd.__len__()

	x = []
	y = []

	i = 1
	while i<m:
		I = i
		i = i+2
		j = 0
		while j<n:
			J = j
			j = j+1
			lex = lexd[J]
			if(lex.uid == sortedNodeIndices[I-1].uid): # find the operator type
				if(lexd[J-1].uid == sv.SCOLON.uid): # find only primary operators
					if(lexd[J+2].constData == sortedNodeIndices[I].constData): # data check
						scolonPos = findNextLex(J,sv.SCOLON,lexd)
						nodePos = findNextLex(J+1,sortedNodeIndices[I-1],lexd)
						if(nodePos < scolonPos): # valid position check
								x.append(float(lexd[nodePos+2].constData))
								y.append(float(lexd[nodePos+4].constData))
						else:
							print('ERR : nodePos > scolonPos')
							exit()
						#endif nodePos and semi colon pos check
					#endif const data check
				#endif primary operator check
			#endif operator type check
		#end while loop over j
	#end while loop over i

	#print('x :',x)
	#print('y :',y)
	
	return x,y
	
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
	subdivVec,subidvTypeVec = findSubdivVec(spObjPos,lexd)

	# Find and sort control node indices
	sortedNodeIndices= findControlNodeIndices(spObjPos,isPeriodic_BC,lexd)

	print('------------------------SORTED NODE VEC -------------------------')
	print(sortedNodeIndices)
	print('------------------------SUBDIVISION VEC -------------------------')
	print(subdivVec)

	# TODO : Generate wall as  2 numpy arrays and populate  them with x and y
	# co-ordiantes respectively of the wall boundary
	xcoord,ycoord = findControlNodeCoordinates(sortedNodeIndices,lexd)
	
	print('-------------------CONTROL NODE CO-ORDINATES --------------------')
	print('x :',xcoord)
	print('y :',ycoord)

	# TODO : subdivide subroutine possibly using numpy or C++
	# work_here
	#xwall,ywall = subdivide(sortedNodeVec,subdivVec,subdivType)


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

	# Initial syntax check
	if(lexd[0].uid != sv.BEGIN.uid):
		print('ERR : MIR file should start with code BEGIN;')
		exit()
	elif(lexd[-2].uid != sv.END.uid):
		print('ERR : MIR file should end with code END;')
		exit()

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
