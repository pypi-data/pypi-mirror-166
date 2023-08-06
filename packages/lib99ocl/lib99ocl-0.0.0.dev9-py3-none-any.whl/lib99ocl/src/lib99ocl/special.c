#ifndef _SPECIAL_C_
#define _SPECIAL_C_

#include "special.h"

#include "special/erf.c"
#include "special/factorial.c"
#include "special/gamma.c"
#include "special/legendre.c"
#include "special/spherical_harmonics.c"
#include "special/psi.c"
// #include "gsl/specfunc/psi.c"
#ifdef CUDA
#include "special/hyp2f1.c"
#endif /* CUDA */
#include "special/bessel.c"

#endif //_SPECIAL_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr et
