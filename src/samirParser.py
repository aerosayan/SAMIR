import samirStandardV1 as sv
import numpy as np
import data_wall as datWall

#------------------------------------------------------------------------------
# Parse the SAMIR language version 1 standard
# \param lexData : the lexemes created in the lexer is used for easy parsing
# \param echo [debug] : whether to print or not
# \return errorcode of 1 or -1 for successfull and unsucessfull respectively
def parserStdV1(lexData,echo=False):
# MARKER :: __parserstdv1
	lexd = lexData
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
	# Run loops to check the remaining of the lexemes
	while i<n:
		I = i
		c = lexd[I]
		i = i+1
		if(c.uid == sv.SOUTH_WALL.uid and SOUTH_WALL_PROCESSED == False):
		# First process the SOUTH_WALL
			print('INF : processing south wall...')
			cfg = [sv.SOUTH_WALL,sv.ASSIGN,sv.NEW,sv.SPLICE,sv.LPAREN,sv.FROM,
			sv.POINT,sv.LSQR,sv.basic_INT_CONST,sv.RSQR,sv.TO,sv.POINT,sv.LSQR,
			sv.basic_INT_CONST,sv.RSQR,sv.COMMA,sv.BY,sv.LCURL,sv.COLLECT,
			sv.RCURL, sv.RPAREN,sv.SCOLON]

			collect = [sv.LINE,sv.SPLINE]
			#print(cfg)

			datWall.SOUTH_WALL_X,datWall.SOUTH_WALL_Y = verifyGrammar(I,cfg,collect,lexd)
			print('INF : south wall created...')
			SOUTH_WALL_PROCESSED = True
		elif(c.uid == sv.NORTH_WALL.uid and SOUTH_WALL_PROCESSED == True and NORTH_WALL_PROCESSED == False):
		# Second process the NORTH_WALL
			print('INF : processing north wall...')

			cfg = [sv.NORTH_WALL,sv.ASSIGN,sv.NEW,sv.SPLICE,sv.LPAREN,sv.FROM,
			sv.POINT,sv.LSQR, sv.basic_INT_CONST,sv.RSQR,sv.TO,sv.POINT,sv.LSQR,
			sv.basic_INT_CONST,sv.RSQR,sv.COMMA,sv.BY,sv.LCURL,sv.COLLECT,
			sv.RCURL, sv.RPAREN,sv.SCOLON]

			collect = [sv.LINE,sv.SPLINE]

			datWall.NORTH_WALL_X,datWall.NORTH_WALL_Y = verifyGrammar(I,cfg,collect,lexd)
			print('INF : north wall created...')
			NORTH_WALL_PROCESSED = True
		#endif

	if(echo == True):
		print('SOUTH_WALL_X : ',datWall.SOUTH_WALL_X)
		print('SOUTH_WALL_Y : ',datWall.SOUTH_WALL_Y)
		print('NORTH_WALL_X : ',datWall.NORTH_WALL_X)
		print('NORTH_WALL_Y : ',datWall.NORTH_WALL_Y)
	#endif
	return 1

#------------------------------------------------------------------------------
# Find the next lex in the lex data stream
# \param xi: Search start position
# \param toFind: The lexem to be searched
# \param lexd: Lex data stream
# \return i : (>0) the position of the next lexeme that is searched
# \return -1 : in case of lexeme not found
def findNextLex(xi,toFind,lexd):
# MARKER :: __findnextlex
	n = lexd.__len__()
	i = xi # accessor
	I = xi # iterator
	found = False
	# Search over the given interval until a lex is found
	while I<n:
		# update the accessor and iterator
		i = I # we access using i
		I = i+1 # we iterate using I
		if (lexd[i].uid == toFind.uid):
			# The lex is found
			found = True
			return i
		#endif
	#end while loop

	# If lex is not found then return error
	if (found == False):
		print('INF : lex not found...')
		return -1

#------------------------------------------------------------------------------
# Subdivide the boundary nodes to form a wall using internal line subdivision
# \param : xCoord :
# \param : yCoord :
# \param : subdivVec :
# \param : interpVec :
# \return : XWALL,YWALL : subdivided x & y co-ordinates of the wall
def subdivide(xCoord,yCoord,subdivVec,interpVec):
# MARKER :: __subdivide
# TODO : handle all kinds of subdivision like linear and cubic spline interpolation

	# check if x and y wall co-ordinates vector are of same length
	if(xCoord.__len__() != yCoord.__len__()):
		print('ERR : xCoord and yCoord lengths do not match')
		exit()

	XWALL = [] # final x co-ordinates
	YWALL = [] # final y co-ordinates

	i = 0 # accessor
	I = 0 # iterator
	while I<subdivVec.__len__():
		i = I # we access using this
		I = i+1 # we iterate using this

		x1 = float(xCoord[i])
		x2 = float(xCoord[i+1])
		y1 = float(yCoord[i])
		y2 = float(yCoord[i+1])

		k = subdivVec[i].constData # number of subdivisoin requested

		# the ratios of the line division
		m = 0.0
		n = 0.0

		# add the 1st control node x1 and y1
		if(i == 0): # Prevents double insertion of x2 and y2 at every iteration
			XWALL.append(x1)
			YWALL.append(y1)
		#endif

		j = 0 # accessor
		J = 0 # iterator
		while J<k-1: # loop k-1 times to create k-1 new nodes # TODO :check it
			j = J # we access using this
			J = j+1 # we iteratre using this

			m = m + float(1.0/float(k))
			n = 1.0 - m
			#print(m,n)
			x = (m*x2 + n*x1)/(m+n)
			y = (m*y2 + n*y1)/(m+n)

			XWALL.append(x)
			YWALL.append(y)
		#end while loop over k

		# add the control point x2 and y2
		XWALL.append(x2)
		YWALL.append(y2)

	#end while loop over i
	return np.array(XWALL),np.array(YWALL)

#------------------------------------------------------------------------------
# Find splice object position in lexd
# \param cmat : collection matrix
# \param corder : collection order used to collect cmat
# \param lexd : lexeme data stream
# \return spObjPos : splice objects positions
def findSpliceObjectPos(cmat,corder,lexd):
# MARKER :: __findspliceobjectpos

	#print('cmat :',cmat)
	#print('corder :',corder)

	m = corder.__len__()
	o = lexd.__len__()
	spObjPos = [] # Position of the spObj in lexd for further use

	i = 0 # accessor
	I = 0 # iterator
	while I<m: # For each splice object in corder
		i = I # we access using this
		I = i+1 # we iterate using this
		n = cmat[i].__len__()
		j = 0 # accessor
		J = 0 # iterator
		while J<n: # For each splice object index in cmat
			j = J # we access using this
			J = j+1 # we iterate using this
			indexObj = cmat[i][j]
			k = 0 # accessor
			K = 0 # iterator
			while K<o: # For each element in lexd see if the indices match and
			# if they do match then store it in a list
				k = K # we access using this
				K = k+1 # we iterate using this
				if(k !=0):
					if(lexd[k-1].uid != sv.SCOLON.uid):
						continue
					#endif
				#endif
				if(lexd[k].uid == corder[i].uid):
					if(lexd[k+2].constData == indexObj.constData):
						spObjPos.append(k)
					#endif
				#endif
			#end while loop over K
		#end while loop over J
	#end while loop over I

	for elem in spObjPos:
		print('INF : lexd[spObjPos] :',lexd[elem])
	# end for loop

	return spObjPos

#------------------------------------------------------------------------------
# Find splice bounds
# If the splice is to start from Point(1) and to end at Point(5) for example
# return the start as 1 and the end as 5
# TODO : Code it if it is needed.
# But for now, we can use the lines and splice to form unique vector
def findSpliceBounds():
# MARKER :: __findsplicebounds
	pass

#------------------------------------------------------------------------------
# Find subdivision vector from the lexeme data stream
# \param spObjPos : special object position
# \param lexd : lexeme data stream
# \return subdivVec : how the subdivision should happen
# \return interpVec : how the interpolation should happen
# \return meshBlockVec : how the mesh block creation should happen
def findSubdivVec(spObjPos,lexd):
# MARKER :: __findsubdivvec
	m = spObjPos.__len__()
	# How much to subdivide each interval
	subdivVec = []
	# How to subdivide each interval
	interpVec = []
	# What kind of mesh block is to be creatd for that interval
	meshBlockVec = []

	i = 0  # accessor
	I = 0  # iterator
	# Run loop over the number of splice objects to be collected
	while I<m:
		i = I # we access using this
		I = i+1 # we iterate using this
		xi = spObjPos[i] # Positon of the splice object eg LINE,SPLINE
		spObj = lexd[xi] # The splice object
		subdivPos = findNextLex(xi,sv.SUBDIV,lexd) # Positon of next subdivision
		scolonPos = findNextLex(xi,sv.SCOLON,lexd) # Position of next scolon
		if(subdivPos > scolonPos):
			#error
			print('ERR : subdivPos > scolonPos')
			print('ERR : No suitable subdivision is found for spObjPos')
			print(xi)
			exit()
		else: # when valid subdiv position is found
			subdivVec.append(lexd[subdivPos+2])
			# Find Interpolation Types after subdiv position
			lerpPos = findNextLex(subdivPos,sv.LERP,lexd)
			cerpPos = findNextLex(subdivPos,sv.CERP,lexd)
			print ('INF : lerpPos :',lerpPos)
			print ('INF : cerpPos :',cerpPos)
			print ('INF : scolonPos :',scolonPos)

			if(lerpPos > 0 and cerpPos > 0): # The lerp and cerp both are found
				if( lerpPos < scolonPos and cerpPos < scolonPos):
					print('ERR : lerpPos and cerpPos < scolonPos')
					print('ERR : both lerp and cerp can not be used at once')
					exit()
				#endif
			else : # if not found then pass
				pass
			#endif

			# Handle only one kind of interpoaltion that is closest
			if(lerpPos >0 and lerpPos < scolonPos): # valid lerp command
				interpVec.append(sv.INTERP_LINEAR(lexdPos=lerpPos))
			elif(cerpPos >0 and cerpPos < scolonPos): # valid cerp command
				interpVec.append(sv.INTERP_CUBIC(lexdPos=cerpPos))
			#endif

			#interpVec.append(sv.INTERP_LINEAR(lexdPos=subdivPos)) # TODO: better way
			meshBlockVec.append(sv.MESH_LINEAR_UID) # For now TODO : better way
		#endif
	#end while
	print('interpVec :',interpVec)
	return subdivVec,interpVec,meshBlockVec

#------------------------------------------------------------------------------
# Sort by common vector
# Sort the given vector by finding the common parts and coallascing them
# eg :
# 1,2 | 2,5 | 6,5 | 7,6 | should produce 1,2,5,6,7 for non periodic vec
# for periodic case it should handle that too
# eg :
# 1,2 | 2,5 | 6,5 | 7,6 | 1,2 should produce 1,2,5,6,7,2,1 in non periodic vec
#
# \param unsortedNodeVec : all the nodes collected in unsorted form
# \param isPeriodic_BC : (bool) is the boundary condition periodic ?
# \return sortedNodeVec : sorted node vector
def sortNodeVector(unsortedNodeVec,isPeriodic_BC):
# MARKER :: __sortnodevector
	m = unsortedNodeVec.__len__()
	sortedNodeVec = [] # placeholder

	# [P,1,P,2,P,2,P,5,][P,6,P,5,P,7,P,6,][P,1,P,2] Periodic
	# [P,1,P,2,P,2,P,5,][P,6,P,5,P,7,P,6,] Non-Periodic
	# therefore for Periodic m mod 8 = 2*2=4
	# m mod 8 = 2*2=4 since the type of node is also added thus doubling the no.
	# and for Non periodic m mod 8 = 0

	# Periodicity test
	# TODO : Unit test the F**K out of this condition and see if it holds true !
	if(m%8 ==4 and isPeriodic_BC):
		pass # Periodic
	elif(m%8 ==0 and ~isPeriodic_BC):
		print('INF :m :',m)
		pass # Non-periodic
	else:
		#TODO : Possible source of error while using periodic bc . Fix it later
		#TODO : Unit test this and make sure it works
		print('ERR : m%8 = 0 and isPeriodic_BC = True : are contradictory')
		print('INF :m :',m)
		exit()

	# Sorting loop
	i = 0 #accessor
	I = 0 #iterator
	while I<(m - m%8): # Only loop upto m-2-1 if periodic or m-1 if non periodic
		i = I
		I = i+8
		# Capture the points
		P1 = unsortedNodeVec[i+1]
		P2 = unsortedNodeVec[i+3]
		P3 = unsortedNodeVec[i+5]
		P4 = unsortedNodeVec[i+7]

		# Flags for fixing different points
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
		if(i == 0): # gather 3 numbers
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
		elif(i > 0): # gather 2 numbers
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
		else: #i < 0 ?
			print('WLeF! Have you done? XD')
			print('ERR : Iterator < 0')
			exit()
		#endif i > or = 0
	#end while loop over I

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
# \param spObjPos :
# \param isPeriodic_BC : (bool) is the boundary condition periodic?
# \param lexd : lexeme data stream
# \return sortedNodeVec : sorted node vector after calling the sorting algorithm
def findControlNodeIndices(spObjPos,isPeriodic_BC,lexd):
# MARKER :: __findcontrolnodeindices
	m = spObjPos.__len__()
	unsortedNodeVec = []
	sortedNodeVec = []

	i = 0 # accessor
	I = 0 # iterator
	while I<m:
		i = I
		I = i+1
		spObj = lexd[spObjPos[i]]
		if(spObj.uid == sv.LINE.uid):
			pointPos = findNextLex(spObjPos[i],sv.POINT,lexd)
			if(pointPos > findNextLex(spObjPos[i],sv.SCOLON,lexd)):
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
	sortedNodeVec = sortNodeVector(unsortedNodeVec,isPeriodic_BC)

	return sortedNodeVec

#------------------------------------------------------------------------------
# Find Control node co-ordinates
# Find the co-oridnates of the nodes that make up the wall
# \param sortedNodeIndices : sorted form of the node indices
# \param lexd : lexeme data stream
# \return x,y : control node co-ordinates
def findControlNodeCoordinates(sortedNodeIndices,lexd):
# MARKER :: __findcontrolnodecoordinates
	m = sortedNodeIndices.__len__()
	n = lexd.__len__()

	x = []
	y = []

	i = 1 # accessor
	I = 1 # iterator
	while I<m:
		i = I # we access using this
		I = i+2 # we iterate using this
		j = 0 # accessor
		J = 0 # iterator
		while J<n:
			j = J # we access using this
			J = j+1 # we iterate using this
			lex = lexd[j]
			if(lex.uid == sortedNodeIndices[i-1].uid): # find the operator type
				if(lexd[j-1].uid == sv.SCOLON.uid): # find only primary operators
					if(lexd[j+2].constData == sortedNodeIndices[i].constData): # data check
						scolonPos = findNextLex(j,sv.SCOLON,lexd)
						nodePos = findNextLex(j+1,sortedNodeIndices[i-1],lexd)
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
		#end while loop over J
	#end while loop over I

	#print('x :',x)
	#print('y :',y)

	return x,y

#------------------------------------------------------------------------------
# Collect point indices from splice collection matrix and sort them uniquely
# \param cmat : collection matrix
# \param corder :
# \param corderpos :
# \param lexd : lexeme date stream
# \return xwall,ywall : x & y co-ordinates of the wall
def formWall(cmat,corder,corderpos,lexd):
# MARKER :: __formwall
	# Splice object positions
	spObjPos = findSpliceObjectPos(cmat,corder,lexd)

	#print('spObjPos :',spObjPos)
	#for elem in spObjPos:
	#	print('lexd[spObjPos] :',lexd[elem])
	##end for loop

	isPeriodic_BC = False # Is a periodic BC present ?

	#print(lexd[spObjPos[0]]) # LINE or SPLINE etc
	#print(lexd[spObjPos[0]+2]) # indices 1,2,3 etc

	if(lexd[spObjPos[0]].uid == lexd[spObjPos[-1]].uid):
		if(lexd[spObjPos[0]+2].constData == lexd[spObjPos[-1]+2].constData):
			print('INF : periodic boundary condition encountered...')
			isPeriodic_BC = True
		else:
			print('INF : non-periodic boundary conditon encountered...')
			isPeriodic_BC = False
		#endif
	#endif

	# Find subdivision vector,interpolation type and mesh block type
	subdivVec,interpVec,meshBlockVec = findSubdivVec(spObjPos,lexd)

	#mark_work
	# Find and sort control node indices
	# TODO : refactor for spline
	sortedNodeIndices= findControlNodeIndices(spObjPos,isPeriodic_BC,lexd)


	#print('------------------------SORTED NODE VEC -------------------------')
	#print(sortedNodeIndices)
	#print('------------------------SUBDIVISION VEC -------------------------')
	#print(subdivVec)
	#print('----------------------INTERPOLATION VEC -------------------------')
	#print(interpVec)

	# TODO : Generate wall as  2 numpy arrays and populate  them with x and y
	# co-ordiantes respectively of the wall boundary
	xcoord,ycoord = findControlNodeCoordinates(sortedNodeIndices,lexd)

	#print('-------------------CONTROL NODE CO-ORDINATES --------------------')
	#print('x :',xcoord)
	#print('y :',ycoord)

	# TODO : subdivide subroutine possibly using numpy or C++
	xwall,ywall = subdivide(xcoord,ycoord,subdivVec,interpVec)

	return xwall,ywall

#------------------------------------------------------------------------------
# Prepare the splice objects
# TODO : Documentation
# \param xi : starting position of search
# \param forLex :
# \param lexd : lexeme data stream
# \return spliceObjects : the splice objects that have been prepared
def collectSpliceObjects(xi,forLex,lexd):
# MARKER :: __collectspliceobjects
	#cfg := [collectLex,sv.LSQR,sv.COLLECT_INDICES,sv.RSQR]
	start = findNextLex(xi,sv.LSQR,lexd)
	end = findNextLex(xi,sv.RSQR,lexd)
	#print('start : ',start,'| end : ',end)
	spliceObjects = []
	i = start # accessor
	I = start # iterator
	while I < end: # iterate using I
		i = I # we access using this
		I = i+1 # we iterate using this
		if(lexd[i].uid == sv.basic_INT_CONST.uid):
			if (i == start):
				spliceObjects[0] = lexd[i]
			else:
				spliceObjects.append(lexd[i])
			#endif
		#endif
	#end while loop
	print('INF : spliceObjects : ',spliceObjects)
	print('INF : spliceObjects have been prepared...')
	return spliceObjects

#------------------------------------------------------------------------------
# Prepare the order in which the lex are to be collected
# eg { Line[1,2] + Spline[3,4] + Line[3,4] => return [LINE,SPLINE,LINE]
# \param xi: Start position
# \param collect: The lex which are allowed to be collected
# \param lexd: The lex data stream
# \return collectOrder : which lexemes to collect?
# \retrun collectOrderPos : where is the positon of the lexemes to collect?
def makeLexCollectionOrder(xi,collect,lexd):
# MARKER :: __makecollectionorder
	n = lexd.__len__()
	m = collect.__len__()
	collectOrder = []
	collectOrderPos = []
	endLine = findNextLex(xi,sv.SCOLON,lexd)
	print('INF : current position : ',xi)
	print('INF : next SCOLON position : ',endLine)
	endCollect = findNextLex(xi,sv.RCURL,lexd)
	print('INF : current position : ',xi)
	print('INF : next RCURL position : ',endCollect)

	i = xi # accessor
	I = xi # iterator
	while I<endCollect:
		i = I # access using this
		I = i+1 # iterate using this
		for k in collect:
			if(k.uid == lexd[i].uid):
				collectOrder.append(k)
				collectOrderPos.append(i)
				continue
			#endif
		# end for loop
	#end while loop
	print('DBG : collect : ', collect)
	print('DBG : collectOrder : ',collectOrder)
	print('DBG : collectOrderPos : ',collectOrderPos)
	print('INF : collection order prepared...')
	if (collectOrder.__len__() != collectOrderPos.__len__()):
		print('ERR : collectOrder and collectOrderPos length mismatch')
		exit()
	#endif
	return collectOrder,collectOrderPos

#------------------------------------------------------------------------------
# Collect the indices of all the objects that make up the splice
# i.e collect indices of LINE,SPLINE,etc from the splice collection region.
# \param xi :
# \param collect :
# \param lexd :
# \return collectionMatrix : the collection matrix
# \return collectOrder : the order of collection for the collection matrix
# \return collectOrderPos : the position of the lexemes ordered in collectOrder
def collectSpliceObjectIndices(xi,collect,lexd):
# MARKER :: __collectspliceobjectindices
	n = lexd.__len__()
	i = xi # lexd iterator index
	j = 0 # collect iterator index
	points = []
	# form ordered list of the tokens to collect from
	collectOrder,collectOrderPos = makeLexCollectionOrder(xi,collect,lexd)

	#print('collectOrder :',collectOrder)
	#print('collectOrderPos :',collectOrderPos)

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
			print('INF : collecting POINT')
			print('ERR : POINT cannot be directly collected...exiting...')
			exit()
		elif(c.uid == sv.LINE.uid):
			print('INF : collecting LINE')
			collectionMatrix[cmCount] = collectSpliceObjects(collectOrderPos[J],
									 sv.LINE,lexd)
			collectionMatrix.append([]) # create space for next object
			cmCount += 1 # increase collection matrix counter
		elif(c.uid == sv.SPLINE.uid):
			print('INF : collecting SPLINE')
			collectionMatrix[cmCount] = collectSpliceObjects(collectOrderPos[J],
									 sv.SPLINE,lexd)
			collectionMatrix.append([]) # create space for next collection
			cmCount += 1 # Increase collection matrix counter
		else:
			print('ERR : could not collect the requseted lexeme')
			print(collect)
			exit()
		#endif
	#end while loop }
	print('INF : finished collecting splice objects from splice')
	collectionMatrix.pop() # remove the last empty row []
	#print('collectionMatrix :',collectionMatrix)
	#print('collectOrder :',collectOrder)
	return collectionMatrix,collectOrder,collectOrderPos

#------------------------------------------------------------------------------
# Verify the language grammar and collect the data
# \param xi : the postion from which it is called
# \param cfg : the grammar to be checked
# \param collect : what to collect
# \param lexd : lexeme data stream
# \return xwall,ywall : after verifying everything, create and return the walls
def verifyGrammar(xi,cfg,collect,lexd):
# MARKER :: __verifygrammar
	n = lexd.__len__()
	i = xi # lexd iterator index # The position of SOUTH_WALL
	j=0 # cfg iterator index
	xwall = []
	ywall = []
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
			#print('INF : collected indices of splice object')
			#print('------------------- COLLECTION MATRIX -------------------')
			#print(cmat)
			#print('------------------- COLLECTION ORDER  -------------------')
			#print(corder)
			#print('-------------------COLLECTION POSITION  -----------------')
			#print(corderpos)

			# Since the collection is completed so skip those lexemes
			#print(I) # test to see where we are
			i = corderpos[corderpos.__len__() - 1]
			#print(i) # test to see if i is correct
			#print(lexd[i]) # test to verifiy that we are skipping the lexemes

			# TODO : Save or return the collected data
			xwall,ywall = formWall(cmat,corder,corderpos,lexd)

			# Skip over the collected positions in lexd
			collectEndPos = findNextLex(I,sv.RCURL,lexd)
			i = xi+collectEndPos
		elif(c.uid == lexd[I].uid):
			# cfg grammar verified print(c,' : is ok')
			pass

		else:
			print('ERROR: grammar not verified...exiting...')
			print('c : ',c)
			print('lexd[I] : ',lexd[I])
			exit()
		#endif
	#} end while i<n loop
	print('INF : returning wall...')
	return xwall,ywall
#------------------------------------------------------------------------------
