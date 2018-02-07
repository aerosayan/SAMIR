import collections
from recordtype import recordtype

#------------------------------------------------------------------------------
# Create namedtuple for storing the lexemes
lex = collections.namedtuple('lex','name uid')
vlex = collections.namedtuple('vlex','type name data')
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Create different lexemes from the base namedtuple
# Create an array for storing all the lexeme objects 
arlex = []

BEGIN = lex(name='BEGIN',uid=0); arlex.append(BEGIN);
END = lex(name='END',uid=1); arlex.append(END);

POINT = lex(name='POINT',uid=100); arlex.append(POINT);
LINE = lex(name='LINE',uid=101); arlex.append(LINE);
SPLINE = lex(name='SPLINE',uid=102);arlex.append(SPLINE);

NEW = lex(name='NEW',uid=200); arlex.append(NEW);
FROM = lex(name='FROM',uid=201); arlex.append(FROM);
TO = lex(name='TO',uid = 202);arlex.append(TO);
BY = lex(name='BY',uid=203);arlex.append(BY);

LPAREN = lex(name='LPAREN',uid=300);arlex.append(LPAREN);
RPAREN = lex(name='RPAREN',uid=301);arlex.append(RPAREN);
LDANG = lex(name='LDANG',uid=302);arlex.append(LDANG);
RDANG = lex(name='RDANG',uid=303);arlex.append(RDANG);
LCURL = lex(name='LCURL',uid=304);arlex.append(LCURL);
RCURL = lex(name='RCURL',uid=305);arlex.append(RCURL);
LSQR = lex(name='LSQR',uid=306);arlex.append(LSQR);
RSQR = lex(name='RSQR',uid=307);arlex.append(RSQR);


SCOLON = lex(name='SEMICOLON',uid=400);arlex.append(SCOLON);
COMMA = lex(name ='COMMA',uid=401);arlex.append(COMMA);
DOT = lex(name='DOT',uid=402);arlex.append(DOT);
ASSIGN = lex(name='ASSIGN',uid=403);arlex.append(ASSIGN);
SUBDIV = lex(name='SUBDIV',uid=404);arlex.append(SUBDIV);
JOIN = lex(name='JOIN',uid=405);arlex.append(JOIN);


NORTH_WALL = lex(name='NORTH_WALL',uid=500);arlex.append(NORTH_WALL);
SOUTH_WALL = lex(name='SOUTH_WALL',uid=501);arlex.append(SOUTH_WALL);
EAST_WALL = lex(name='EAST_WALL',uid=502);arlex.append(EAST_WALL);
WEST_WALL = lex(name='WEST_WALL',uid=503);arlex.append(WEST_WALL);
SPLICE = lex(name='SPLICE',uid=504);arlex.append(SPLICE);

COLLECT = lex(name='COLLECT',uid=600);arlex.append(COLLECT);
CAN_COLLECT = lex(name='CAN_COLLECT',uid=601);arlex.append(CAN_COLLECT);
COLLECT_INDICES = lex(name='COLLECT_INDICES',uid=602);arlex.append(COLLECT_INDICES);

LINTERP = lex(name='LINTERP',uid=700);arlex.append(LINTERP)
CUBINTERP = lex(name='CUBINTERP',uid=701);arlex.append(CUBINTERP)

#------------------------------------------------------------------------------
# Integer and double variables and constant 
INT_CONST_UID = 5000
INT_VAR_UID = 5001
DBL_CONST_UID = 5002
DBL_VAR_UID = 5003


# Depends on recordtype library
# 3 fields are used for example
# constId = intConst
# constData = 0
# uid = INT_CONST_UID

INT_CONST = recordtype('INT_CONST',[('constId','intConst'),('constData',0)  ,('uid',INT_CONST_UID)])
INT_VAR   = recordtype('INT_VAR'  ,[('varId','')          ,('varData',0)    ,('uid',INT_VAR_UID)  ])
DBL_CONST = recordtype('DBL_CONST',[('constId','dblConst'),('constData',0.0),('uid',DBL_CONST_UID)])
DBL_VAR   = recordtype('DBL_VAR'  ,[('varId','')          ,('varData',0.0)  ,('uid',DBL_VAR_UID)  ])

# Two baisc instatntiation of the recordtype for easy use
basic_INT_CONST = INT_CONST(constId='basicIntConst')
basic_DBL_CONST = DBL_CONST(constId='basicDblConst')

#------------------------------------------------------------------------------
# Integration routines
INTERP_LINEAR_UID = 6000 # Linear interpolation UID
INTERP_CUBIC_UID = 6001 # Cubic interpolation UID

# TODO : Interpolation recordtypes
# INTERP_LINEAR : for linear interpolation between two different node positions 
# 		in the physical domain
# INTERP_CUBIC  : for cubic spline interpolation between two different node
#		positions in the physical domain

# FIELDS : 
# nodePos : the node positons in terms of percentage of total distance between 
# 		the two different nodes. Total sum = 100
# nodeDensity : the node density or no. of nodes in terms of percentage of total
# 		numaber of nodes. Total sum = 100

INTERP_LINEAR = recordtype('INTERP_LINEAR',[('nodePos',[]),('nodeDensity',[]),('lexdPos',-1)  ,('uid',INTERP_LINEAR_UID)])
INTERP_CUBIC  = recordtype('INTERP_CUBIC' ,[('nodePos',[]),('nodeDensity',[]),('lexdPos',-1)  ,('uid',INTERP_CUBIC_UID) ])

#------------------------------------------------------------------------------
# Mesh block creation technique
MESH_LINEAR_UID = 6100
MESH_ELLIPTIC_UID = 6101
MESH_PARABOLIC_UID = 6102
MESH_HYPERBOLIC_UID = 6103
MESH_TRIANGLE_UID = 6104

# TODO : Mesh block creation technique recordtypes
