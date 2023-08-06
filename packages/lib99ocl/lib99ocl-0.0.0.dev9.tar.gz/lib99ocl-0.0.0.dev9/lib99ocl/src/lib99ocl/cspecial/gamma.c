#ifndef _CGAMMA_C_
#define _CGAMMA_C_

#include "gamma.h"
#include "../details/cigamma.c"

WITHIN_KERNEL
ctype cgammaincc(ftype a, ctype z) {
  ctype ans = C(0, 0);
  if ((cabs(z) <= 0.0) || (a <= 0))
    return C(1., 0.);
  if ((cabs(z) < 1.0) || (cabs(z) < a))
    return csub(C(1., 0.), __core_cigam(a, z));
  return __core_cigamc(a, z);
}

#endif // _CGAMMA_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr et
