#ifndef _CSPHERICAL_HARMONICS_H_
#define _CSPHERICAL_HARMONICS_H_

#include "../complex.h"
#include "../core.h"
#include "../special/factorial.h"
#include "../special/legendre.h"

WITHIN_KERNEL
ctype csph_harm(const int l, const int m, const ftype cosT, const ftype phi);

#endif // _CSPHERICAL_HARMONICS_H_

// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
