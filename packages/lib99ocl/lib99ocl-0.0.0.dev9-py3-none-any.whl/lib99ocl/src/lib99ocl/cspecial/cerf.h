#ifndef _CERF_H_
#define _CERF_H_

#include "../complex.h"

WITHIN_KERNEL
ctype cwofz(const ctype z);

// WITHIN_KERNEL
// ctype ipanema_erfc2(const ctype z);

// WITHIN_KERNEL
// ctype ipanema_erfc(const ctype z);

WITHIN_KERNEL
ctype cerfc(const ctype x);

WITHIN_KERNEL
ctype cerf(const ctype z);

WITHIN_KERNEL
ctype cerfi(const ctype z);

WITHIN_KERNEL
ftype rwofzr(const ftype x, const ftype y);

WITHIN_KERNEL
ftype rwofzi(const ftype x, const ftype y);

WITHIN_KERNEL
ctype cerfcx(const ctype z);

WITHIN_KERNEL
ftype erfi(const ftype x);

WITHIN_KERNEL
ftype dawson(const ftype x);

#endif // _CERF_H_

// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
