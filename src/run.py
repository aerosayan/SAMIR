#!/usr/bin/python2.7
#---
#---#---
#---#---#---
import os
import time 
import fileReader as fr
import samirStandardV1  as sv
import lexer as lex
import parser as par
import data_wall as daw

from pylab import *


data = fr.readFile('mesh.mir')
print('data saved')
#print(data)


lexd = lex.lexerStdV1(data)
"""
for elem in lexd:
	print(elem)
"""
err = par.parserStdV1(lexd,echo=True)

swx = daw.SOUTH_WALL_X
swy = daw.SOUTH_WALL_Y

nwx = daw.NORTH_WALL_X
nwy = daw.NORTH_WALL_Y


# Plot the sw and nw
plot(swx,swy)
plot(nwx,nwy)
show()

