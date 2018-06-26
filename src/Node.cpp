#include "Node.h"

Node::Node():m_x(0.0),m_y(0.0) {}

Node::Node(double _x,double _y):m_x(_x),m_y(_y){}

void Node::setX(double _x)
{
	m_x = _x;
}
void Node::setY(double _y)
{
	m_y = _y;
}
