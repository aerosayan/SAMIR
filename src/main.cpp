#include "main.h"
#include <iostream>
#include "Node.h"
#include "GridGenerator.h"
void runGridGenerator( double* _nwallx,
    double* _nwally,
    double* _swallx,
    double* _swally,
	unsigned int _imax,
    unsigned int _jmax,
	char* _outputFile)
{
	/*
	// Basic test
	for (int i=0; i<_nwallxnum; i++) {
		std::cout<<"_nwallx["<<i<<"] : "<<_nwallx[i]<<std::endl;
	}
	std::cout<<"_jmax : "<<_jmax<<std::endl;
	*/

	GridGenerator g;
	g.genGrid(_nwallx,_nwally,_swallx,_swally,_imax,_jmax);
	g.printGridToFile(_outputFile);
}
int main()
{
	//GridGenerator g;
	//g.genGrid();
	//g.printGridToFile("grid.dat");
	return 0;
}
