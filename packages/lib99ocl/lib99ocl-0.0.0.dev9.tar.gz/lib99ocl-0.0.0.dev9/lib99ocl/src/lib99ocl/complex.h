#ifndef _COMPLEX_H_
#define _COMPLEX_H_

#include "core.h"

WITHIN_KERNEL
ctype C(const ftype re, const ftype im);

WITHIN_KERNEL
ctype cpolar(const ftype re, const ftype im);

WITHIN_KERNEL
ctype cmul(const ctype z1, const ctype z2);

WITHIN_KERNEL
ctype cdiv(const ctype z1, const ctype z2);

WITHIN_KERNEL
ctype cadd(const ctype z1, const ctype z2);

WITHIN_KERNEL
ctype csub(const ctype z1, const ctype z2);

WITHIN_KERNEL
ctype cexp(const ctype z);

WITHIN_KERNEL
ctype csquare(const ctype z);

WITHIN_KERNEL
ctype cconj(const ctype z);

WITHIN_KERNEL
ftype cnorm(const ctype z);

WITHIN_KERNEL
ftype cabs(const ctype z);

WITHIN_KERNEL
ftype cre(const ctype z);

WITHIN_KERNEL
ftype cim(const ctype z);

WITHIN_KERNEL
ftype carg(const ctype z);

WITHIN_KERNEL
ctype clog(const ctype z);

WITHIN_KERNEL
ctype cpow(const ctype w, const ctype z);

WITHIN_KERNEL
ctype csqrt(const ctype w, const ctype z);

#endif // _COMPLEX_H_

// vim: fdm=marker ts=2 sw=2 sts=2 sr et
