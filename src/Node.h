#ifndef __SAMIR_NODE_H__
#define __SAMIR_NODE_H__

class Node
{
public:
	Node();
	Node(double,double);
	virtual ~Node(){}
	double getX(){return m_x;}
	double getY(){return m_y;}

	void setX(double);
	void setY(double);
private:
	double m_x;
	double m_y;
};
#endif
