#ifndef _BERNSTEIN_C_
#define _BERNSTEIN_C_


#include "bernstein.h"


WITHIN_KERNEL
ftype polyBernstein(const ftype x, const ftype *c, const int n)
{
  ftype ans = 0.0;
  for (int k=0; k<n; k++)
  {
    ans += binom(n, k) * rpow(x, k) * rpow(1-x, n-k);
  }
  return ans;
}


#endif // _BERNSTEIN_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
