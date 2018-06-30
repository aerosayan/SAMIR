#ifndef __MAIN_H__
#define __MAIN_H__

#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif


EXTERNC void runGridGenerator(double* _nwallx, double* _nwally,
	double* _swallx, double* _swally,
	unsigned int _imax, unsigned int _jmax,
	char* _outputFile);


#undef EXTERNC
#endif
