#include "Node.h"
#include "GridGenerator.h"

int main()
{
	GridGenerator g;
	g.genGrid();
	g.printGridToFile("grid.dat");
	return 0;
}
