#ifndef _CSPHERICAL_HARMONICS_C_
#define _CSPHERICAL_HARMONICS_C_

#include "spherical_harmonics.h"

WITHIN_KERNEL
ctype csph_harm(const int m, const int l, const ftype cosT, const ftype phi) {
  ftype ans = lpmv(m, l, cosT);
  ans *= sqrt(((2 * l + 1) * factorial(l - m)) / (4 * M_PI * factorial(l + m)));
  return C(ans * cos(m * phi), ans * sin(m * phi));
}

#endif // _CSPHERICAL_HARMONICS_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
