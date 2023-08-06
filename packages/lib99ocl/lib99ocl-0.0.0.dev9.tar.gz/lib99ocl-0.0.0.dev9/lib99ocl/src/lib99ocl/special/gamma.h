#ifndef _GAMMA_H_
#define _GAMMA_H_


#include "../core.h"


WITHIN_KERNEL
ftype rgamma(ftype x);

WITHIN_KERNEL
ftype gammasgn(ftype x);

WITHIN_KERNEL
ftype rgammaln(const ftype x);

WITHIN_KERNEL
ftype __core_igamc(ftype a, ftype x);


WITHIN_KERNEL
ftype __core_igam(ftype a, ftype x);


WITHIN_KERNEL
ftype rgammainc(const ftype a, const ftype x);


WITHIN_KERNEL
ftype rgammaincc(const ftype a, const ftype x);


#endif // _GAMMA_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
