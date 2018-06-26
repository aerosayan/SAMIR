import os
import time
import samirFileReader as fr
import samirStandardV1  as sv
import data_wall as daw
import samirLexer as lex
import samirParser as par

from pylab import *


splitData,joinedData = fr.readFile('mesh.mir')
print('data saved')
print(joinedData)


lexd = lex.lexerStdV1(joinedData)

err = par.parserStdV1(lexd,echo=True)

swx = daw.SOUTH_WALL_X
swy = daw.SOUTH_WALL_Y

nwx = daw.NORTH_WALL_X
nwy = daw.NORTH_WALL_Y

print(nwy)
"""
# Plot the sw and nw
plot(nwy,'go')
plot(swy,'ro')
show()
"""
figure()
plot(swx,swy,'r.')
plot(nwx,nwy,'b.')
show()

zip(nwx,nwy,swx,swy)

import csv

with open("walls.dat","w") as f:
	writer = csv.writer(f,delimiter='\t')
	writer.writerows(zip(nwx,nwy,swx,swy))
