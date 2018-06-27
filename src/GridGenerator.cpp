#include "GridGenerator.h"
#include "Node.h"
#include <iostream>
#include <fstream>
#include <iomanip>

std::vector<std::vector<Node *> >& GridGenerator::genGrid(double * _nwx,
	double * _nwy, double * _swx, double* _swy,
	unsigned int _imax,unsigned int _jmax)
// MARKER :: __gengrid
{
	/*
	// Read in file and create the boundaries
	// TODO : Direct connection with python
	std::ifstream file;
	file.open("walls.dat");
	double xswall,yswall,xnwall,ynwall;

	while(file) {
		file >> xswall >>  yswall >> xnwall >> ynwall;
		m_swall.push_back(new Node(xswall,yswall));
		m_nwall.push_back(new Node(xnwall,ynwall));
	}
	file.close();
	*/
	// Create iterators
	unsigned int i=0;
	unsigned int j=0;
	for(i=0; i<_imax; i++){
		m_swall.push_back(new Node(_swx[i],_swy[i]));
		m_nwall.push_back(new Node(_nwx[i],_nwy[i]));
	}
	// Reset iterators
	i=0;j=0;

	//TODO : The end points are missing so make a new subdivide func
	// to take in the wall vector and push back the newly created nodes
	//m_wwall.push_back(new Node(m_swall.at(0)))
	m_wwall = subdivide(m_swall.at(0),m_nwall.at(0),_jmax);
	//m_wwall.push_back(new Node(m_nwall.at(0)))

	m_ewall = subdivide(m_swall.at(m_swall.size()-1),
	                    m_nwall.at(m_nwall.size()-1),_jmax);

	if(m_swall.size() != m_nwall.size() || m_swall.size() == 0
	                                    || m_nwall.size() == 0) {
		std::cout<<"ERR : FATAL : north and south wall size error..."
				 <<std::endl;
		// TODO : runtime execution stop
	}

	if(m_ewall.size() != m_wwall.size() || m_ewall.size() == 0
	                                    || m_wwall.size() == 0) {
		std::cout<<"ERR : FATAL : east and west wall sizes error ..."
		         <<std::endl;
		// TODO : runtime execution stop
	}

	unsigned int n = m_swall.size();
	unsigned int m = m_ewall.size();

	std::cout<<"INF:: n : "<<n<<std::endl;
	std::cout<<"INF:: m : "<<m<<std::endl;

	// Initialize the grid to required size and all the elements to NULL
	std::vector<std::vector<Node *> > m_grid(m,std::vector<Node *>(n,NULL));
	// Set the boundaries
	// First row shall be south wall
	for(i=0;i<n;i++) {
		m_grid.at(0).at(i) = m_swall.at(i);
	}
	// Last row shall be north wall
	for(i=0;i<n;i++) {
		m_grid.at(m-1).at(i) = m_nwall.at(i);
	}
	// First column shall be west wall
	for(j=0;j<m;j++) {
		m_grid.at(j).at(0) = m_wwall.at(j);
	}
	// Last column shall be east wall
	for(j=0;j<m;j++) {
		m_grid.at(j).at(n-1) = m_ewall.at(j);
	}

	std::cout<<m_grid.size()<<std::endl;
	// Create a uniform cluster for now
	genUniformCluster(m_grid);
	// Run a null pointer check to ensure the mesh is full
	nullCheck(m_grid);
	return m_grid;
}

void GridGenerator::printGridToFile(std::string _file)
{
	std::ofstream meshFile;
	meshFile.open(_file.c_str());

	Node * n;
	std::cout<<"INF: creating mesh file ... "<<std::endl;
	std::cout<<m_grid.size()<<std::endl;
	for(int j =0;j<m_grid.size();j++) {
		for (int i=0; i<m_grid.at(j).size();i++) {
			n = m_grid.at(j).at(i);
			meshFile <<std::fixed<<std::setprecision(6)<<std::endl;
			meshFile << n->getX() <<"\t"<<n->getY()<<"\n";
		}
	}
	meshFile.close();
}

std::vector<Node*> GridGenerator::subdivide(Node* _n1, Node* _n2,
	unsigned int _subdivLevel)
// MARKER :: __subdivide
{
	// Create temporary co-ordinate variables
	double x1 = _n1->getX();
	double y1 = _n1->getY();
	double x2 = _n2->getX();
	double y2 = _n2->getY();
	double _tempx;
	double _tempy;

	std::vector<Node*> segment;
	unsigned int nmax = _subdivLevel -1;

	// Subivision segment ratios
	double m = (double) 1.0;
	double n = (double) nmax;

	// Subdivide
	for(int i=0; i<nmax ;i++) {
		// Find out position of the next point
		_tempx = ((n*x1)+(m*x2))/(m+n);
		_tempy = ((n*y1)+(m*y2))/(m+n);

		// Push back newly created node
		segment.push_back(new Node(_tempx,_tempy));

		// Update values of the subidivision ratios
		m = (double) m + 1.0;
		n = (double) n - 1.0;
	}
	return segment;
}

void GridGenerator::nullCheck(std::vector<std::vector<Node *> >& _grid)
// MARKER :: __nullcheck
{
	unsigned int i = 0;
	unsigned int j = 0;
	unsigned int nullCount = 0;
	for(i=0; i<_grid.size();i++) {
		for(j=0;j<_grid.at(i).size();j++) {
			if(_grid.at(i).at(j) == NULL) {
				nullCount++;
			}
		}
	}
	std::cout<<"INF:: null count : "<<nullCount<<std::endl;
}

void GridGenerator::genUniformCluster(std::vector<std::vector<Node *> >& _grid)
// MARKER :: __genuniformcluster
{
	std::cout<<_grid.size()<<std::endl;
	// Get the number of rows and columns
	unsigned int n = m_swall.size();
	unsigned int m = m_ewall.size();

	unsigned int i = 0;
	unsigned int j = 0;
	std::vector<Node*> segment;
	// Loop over the south wall direction for every column
	// // subdivide and create column segments and fill them in the grid
	for(i=1;i<n-1;i++) {
		//segment.clear();
		segment = subdivide(_grid.at(0).at(i), _grid.at(m-1).at(i),m);
		//std::cout<<"DBG:: segment.size : "<<segment.size()<<std::endl;
		// Loop over the east wall direction
		for(j=1;j<m-1;j++) {
			// TODO : we need to do error checking here
			_grid.at(j).at(i) = segment.at(j);
		}
	}
	std::cout<<_grid.size()<<std::endl;
	// Make sure that we are setting the reference correctly
	m_grid = _grid;

}
