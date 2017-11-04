import samirStandardV1 as sv

def verifyCFG(xi,cfg,collect,lexd):
	n = lexd.__len__()
	i=0
	j = xi
	while j<n: #{ 
		I = i
		c = cfg[I]
		i=i+1 # update cfg counter	
		J = j
		j = j+1 # update lexd counter
		if(c.uid == sv.COLLECT.uid):
			# Within the iteration 
			# Do collection
			# skip collected entitites
			print('exit mark2')
			exit()
		elif(c.uid == lexd[J].uid):
			# cfg grammar verified
			print(c,' : is ok')
			
		else:
			print('ERROR: CFG grammar not verified')
			print('c : ',c)
			print('lexd[J] : ',lexd[J])
			exit()

#---
	return 1
		#} end while k<n loop

		

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
		if(c == sv.SOUTH_WALL and SOUTH_WALL_PROCESSED == False):
			print('SOUTH_WALL found')

			cfg = [sv.SOUTH_WALL,sv.ASSIGN,sv.NEW,sv.SPLICE,sv.LPAREN,sv.FROM,
			sv.POINT,sv.LSQR,sv.INT_CONST(constId='cfgTestIntConst'),sv.RSQR,sv.TO,sv.POINT,sv.LSQR,
			sv.INT_CONST(constId='cfgTestIntConst'),sv.RSQR,sv.COMMA,sv.BY,sv.LCURL,sv.COLLECT,sv.RCURL,
			sv.RPAREN,sv.SCOLON]

			collect = [sv.LINE]
			#print(cfg)
			verifyCFG(I,cfg,collect,lexd)
			print('EXIT mark1')	
			exit()
		elif(c == sv.NORTH_WALL and SOUTH_WALL_PROCESSED == True and NORTH_WALL_PROCESSED == False):
			print('NORTH_WALL found')

			cfg = [sv.NORTH_WALL,sv.ASSIGN,sv.NEW,sv.SPLICE,sv.LPAREN,sv.FROM,
			sv.POINT,sv.LSQR, sv.INT_CONST(constId='cfgTestIntConst'),sv.RSQR,sv.TO,sv.POINT,sv.LSQR,
			sv.INT_CONST(constId='cfgTestIntConst'),sv.RSQR,sv.COMMA,sv.BY,sv.LCURL,sv.COLLECT,sv.RCURL,
			sv.RPAREN,sv.SCOLON]
			
			collect = [sv.LINE]
	return 0,0
