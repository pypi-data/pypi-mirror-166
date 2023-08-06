#ifndef _LEGENDRE_H_
#define _LEGENDRE_H_


#include "../core.h"
#include "factorial.h"


WITHIN_KERNEL
ftype lpmv(const int m, const int l, const ftype cosT);


#endif // _LEGENDRE_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr et
