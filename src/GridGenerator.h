#ifndef __SAMIR_GRIDGENERATOR_H__
#define __SAMIR_GRIDGENERATOR_H__
#include<vector>
#include<string>
// Forward declarations
class Node;

class GridGenerator
{
public:
	GridGenerator(){}
	virtual ~GridGenerator(){}
	//-----------------------------
	// GETTERS
	//-----------------------------
	std::vector<std::vector<Node *> >& getGrid(){return m_grid;}

	//-----------------------------
	// FUNCTION DECLARATIONS
	//-----------------------------
	// Generate walls using data given either by python or read from file
	// //----From Python
	// @param _nwx : north wall x co-ordinates
	// @param _nwy : north wall y co-ordinates
	// @param _swx : south wall x co-ordinates
	// @param _swy : south wall y co-ordinates
	// @param _imax : maximum number of columns in grid
	// @param _jmax : maximum number of rows in grid
	void genWalls(double * _nwx, double * _nwy,
		double * _swx, double* _swy,
		unsigned int _imax,unsigned int _jmax);

	// //----From co-ordinate ascii text file
	// @param _filename : the file containing the north,south walls co-ordinates
	void genWalls(std::string _filename);

	// Generate structured grid for the walls given directly from python
	std::vector<std::vector<Node *> >& genGrid();

	// Print grid to file so that we can use it externally
	// @param string: name of the ascii file to which the data is printed
	void printGridToFile(std::string);

private:
	//-----------------------------
	// DATA MEMBERS
	//-----------------------------
	std::vector<Node *> m_swall;
	std::vector<Node *> m_nwall;
	std::vector<Node *> m_wwall;
	std::vector<Node *> m_ewall;
	std::vector<std::vector<Node *> > m_grid;

	//-----------------------------
	// FUNCTION DECLARATIONS
	//-----------------------------
	// Initialize grid by allocating memory and assigning the walls in the grid
	void initGrid();

	// Subdivide and create a segment using internal subidivision formula
	// @param Node* : the segment begining and end nodes
	// @param unsigned int : the number of subdivision levels that is wanted
	// @return : the subdivided vector from according to the specs of the user
	std::vector<Node *> subdivide(Node*,Node*,unsigned int);

	// Run a null pointer check to ensure our grid is full
	void nullCheck(std::vector<std::vector<Node *> >& );

	// Generate a uniform clustered grid
	// @param vec<vec<Node*> >: the computational grid sent by reference
	void genUniformCluster(std::vector<std::vector<Node *> >& );

};

#endif
