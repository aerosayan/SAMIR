# Cython code to link the C++ backend to python
from cpython cimport array


cdef extern from "main.h":
	void runGridGenerator( double* _nwallx, double* _nwally,
		double* _swallx, double* _swally,
		unsigned int _imax, unsigned int _jmax,
		char* _outputFile)


def cy_runGridGenerator(_nwallx,_nwally,_swallx,_swally,_jmax,_outputFile):
	# Create array objects to allow passing to extern C code
	cdef array.array _arr_nwallx = array.array('d',_nwallx)
	cdef array.array _arr_nwally = array.array('d',_nwally)
	cdef array.array _arr_swallx = array.array('d',_swallx)
	cdef array.array _arr_swally = array.array('d',_swally)

	# Call extern C code
	runGridGenerator( _arr_nwallx.data.as_doubles, _arr_nwally.data.as_doubles,
	 	_arr_swallx.data.as_doubles, _arr_swally.data.as_doubles,
	 	_nwallx.__len__(), _jmax,
		_outputFile)
