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




data = fr.readFile('mesh.mir')
print('data saved')
#print(data)

lexd = lex.lexerStdV1(data)
"""
for elem in lexd:
	print(elem)
"""

nw,sw,= par.parserStdV1(lexd)
print(nw,sw)
