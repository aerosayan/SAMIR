#include "main.h"
#include <iostream>
#include "Node.h"
#include "GridGenerator.h"
void runGridGenerator( double* _nwallx, double* _nwally,
    double* _swallx, double* _swally,
	unsigned int _imax, unsigned int _jmax,
	char* _outputFile)
{
	GridGenerator g;
	g.genWalls(_nwallx,_nwally,_swallx,_swally,_imax,_jmax);
    g.genGrid();
	g.printGridToFile(_outputFile);
}
int main()
{
	GridGenerator g;
    g.genWalls("walls.dat");
	g.genGrid();
	g.printGridToFile("grid.dat");
	return 0;
}
