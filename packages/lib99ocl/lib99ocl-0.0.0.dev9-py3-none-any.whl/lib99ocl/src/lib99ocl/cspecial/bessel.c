#ifndef _CBESSEL_C_
#define _CBESSEL_C_

#include "bessel.h"

WITHIN_KERNEL
ctype cjv(const ftype n, const ctype x) {
#ifdef CUDA
  /* printf("not yet implemented\n"); */
  return C(0., 0.);
#else
  return C(0., 0.);
#endif
}

#endif // _CBESSEL_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
