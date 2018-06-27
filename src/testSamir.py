# NOTE : Developed and tested with only Python2.7.
import os
import time
import samir as mir           # cythonized library calling C++ code
import samirStandardV1  as sv # samir version 1 standard declaration
import samirFileReader as fr  # read in samir files and do pre-processing
import data_wall as daw       #  storage for boundary data created
import samirLexer as lex      # samir standard lexer
import samirParser as par     # samir standard parser
import samirPlotGrid as plt   # samir created grid plotting

# Read in MIR file, run lexer and parser to create the domain boundaries
splitData,joinedData = fr.readFile('mesh.mir')
lexd = lex.lexerStdV1(joinedData)                # tokenize
err  = par.parserStdV1(lexd,echo=True)           # parse

# Get created boundaries by the semantic analysis in parser
swx = daw.SOUTH_WALL_X
swy = daw.SOUTH_WALL_Y
nwx = daw.NORTH_WALL_X
nwy = daw.NORTH_WALL_Y

# Calling high performance C++ code
outputFile = "grid.dat" # file to store the grid co-ordinates
mir.cy_runGridGenerator(nwx,nwy,swx,swy,120,outputFile)

# Plot grid created by C++ code
plt.plot(outputFile)
