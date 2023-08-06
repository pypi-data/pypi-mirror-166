#ifndef _ERF_C_
#define _ERF_C_

#include "erf.h"
#include "../details/cerf.c"

WITHIN_KERNEL
ftype erfcx(const ftype x) {
  // Steven G. Johnson, October 2012.

  // This function combines a few different ideas.

  // First, for x > 50, it uses a continued-fraction expansion (same as
  // for the Faddeeva function, but with algebraic simplifications for z=i*x).

  // Second, for 0 <= x <= 50, it uses Chebyshev polynomial approximations,
  // but with two twists:
  //
  // a) It maps x to y = 4 / (4+x) in [0,1].  This simple transformation,
  // inspired by a similar transformation in the octave-forge/specfun
  // erfcx by Soren Hauberg, results in much faster Chebyshev convergence
  // than other simple transformations I have examined.
  //
  // b) Instead of using a single Chebyshev polynomial for the entire
  // [0,1] y interval, we break the interval up into 100 equal
  // subintervals, with a switch/lookup table, and use much lower
  // degree Chebyshev polynomials in each subinterval. This greatly
  // improves performance in my tests.
  //
  // For x < 0, we use the relationship erfcx(-x) = 2 exp(x^2) - erfc(x),
  // with the usual checks for overflow etcetera.

  // Performance-wise, it seems to be substantially faster than either
  // the SLATEC DERFC function [or an erfcx function derived therefrom]
  // or Cody's CALERF function (from netlib.org/specfun), while
  // retaining near machine precision in accuracy.

  if (x >= 0) {
    if (x > 50) { // continued-fraction expansion is faster
      const ftype ispi = 0.56418958354775628694807945156; // 1 / sqrt(pi)
      if (x > 5e7) // 1-term expansion, important to avoid overflow
        return ispi / x;
      /* 5-term expansion (rely on compiler for CSE), simplified from:
         ispi / (x+0.5/(x+1/(x+1.5/(x+2/x))))  */
      return ispi * ((x * x) * (x * x + 4.5) + 2) /
             (x * ((x * x) * (x * x + 5) + 3.75));
    }
    return erfcx_y100(400 / (4 + x));
  } else
    return x < -26.7 ? HUGE_VAL
                     : (x < -6.1 ? 2 * exp(x * x)
                                 : 2 * exp(x * x) - erfcx_y100(400 / (4 - x)));
}

#endif // _ERF_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr et
