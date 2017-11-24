
import samirStandardV1 as sv

#------------------------------------------------------------------------------
def findNextLex(xi,toFind,lexd):
	n = lexd.__len__()
	i = xi
	found = False
	while i<n:
		I = i
		i = i+1
		if (lexd[I].uid == toFind.uid):
			# The lex is found
			found = True
			return I	
			
	if (found == False):
		print('LEX NOT FOUND')
		return -1	

#------------------------------------------------------------------------------
def collectSplineObjects(xi,forLex,lexd):
	#cfg := [collectLex,sv.LSQR,sv.COLLECT_INDICES,sv.RSQR]
	start = findNextLex(xi,sv.LSQR,lexd)
	end = findNextLex(xi,sv.RSQR,lexd)
	#print('start : ',start,'| end : ',end)
	splineObjects = []
	i = start
	while i < end:
		I = i
		i = i+1
		if(lexd[I].uid == sv.basic_INT_CONST.uid):
			if (I == start):	
				splineObjects[0] = lexd[I]
			else:
				splineObjects.append(lexd[I])
			#endif
		#endif
	#end while loop
	print('splineObjects : ',splineObjects)
	print('splineObjects have been prepared')
	return splineObjects

#------------------------------------------------------------------------------
def makeLexCollectionOrder(xi,collect,lexd):
	#  Produce the order in which the lex are to be collected
	# eg { Line[1,2] + Spline[3,4] + Line[3,4] => return [LINE,SPLINE,LINE]
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
	return collectOrder,collectOrderPos

#------------------------------------------------------------------------------
def collectPointsFromSplice(xi,collect,lexd):
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
			collectionMatrix[cmCount] = collectSplineObjects(collectOrderPos[J],
			                                                 sv.LINE,lexd)
			collectionMatrix.append([]) # create space for next collection
			cmCount += 1 # Increase collection matrix counter
		elif(c.uid == sv.SPLINE.uid):
			print('INF :: Collecting SPLINE')
			collectionMatrix[cmCount] = collectSplineObjects(collectOrderPos[J],
			                                                 sv.SPLINE,lexd)
			collectionMatrix.append([]) # create space for next collection
			cmCount += 1 # Increase collection matrix counter
		else:
			print('ERR :: Could not collect the requseted lexeme')
			print(collect)
			exit()
	#}
	print('INF :: Finished collecting splice objects from splice')
	return collectionMatrix,collectOrder,collectOrderPos

#------------------------------------------------------------------------------
def verifyCFG(xi,cfg,collect,lexd):
	n = lexd.__len__()
	i = xi # lexd iterator index
	j=0 # cgf iterator index
	while i<n: #{ 
		I = i
		i=i+1 # update lexd counter	

		J = j
		c = cfg[J]
		j = j+1 # update cfg counter
		if(c.uid == sv.COLLECT.uid):
			# Within the iteration 
			# Do collection
			"""
			@params
			cmat : Collection matrix
			corder : Collection oreder
			corderpos : Collection order position
			"""
			cmat,corder,corderdpos = collectPointsFromSplice(I,collect,lexd)

			# skip collected entitites
			print('exit mark2')
			exit()
		elif(c.uid == lexd[I].uid):
			# cfg grammar verified
			print(c,' : is ok')
			
		else:
			print('ERROR: CFG grammar not verified')
			print('c : ',c)
			print('lexd[I] : ',lexd[I])
			exit()

#---
	return 1
		#} end while i<n loop

		

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
	return 0,0
