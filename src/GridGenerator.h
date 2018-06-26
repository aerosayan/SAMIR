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
	// Generate structured grid for the given NEWS walls
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
	// Subdivide and create a segment using internal subidivision formula
	// @param Node* : the segment begining and end nodes
	// @param unsigned int : the number of subdivision levels that is wanted
	// @return : the subdivided vector from according to the specs of the user
	std::vector<Node *> subdivide(Node*,Node*,unsigned int);

	// Generate a uniform clustered grid
	// @param vec<vec<Node*> >: the computational grid sent by reference
	void genUniformCluster(std::vector<std::vector<Node *> >& );

	// Run a null pointer check to ensure our grid is full
	void nullptrCheck(std::vector<std::vector<Node *> >& );
};

#endif
