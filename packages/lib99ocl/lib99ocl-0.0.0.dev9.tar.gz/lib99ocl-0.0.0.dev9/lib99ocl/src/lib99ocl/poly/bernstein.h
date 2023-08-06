#ifndef _BERNSTEIN_H_
#define _BERNSTEIN_H_


#include "../core.h"
#include "../special/factorial.h"


WITHIN_KERNEL
ftype polyBernstein(const ftype x, const ftype *c, const int n);


#endif // _BERNSTEIN_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
