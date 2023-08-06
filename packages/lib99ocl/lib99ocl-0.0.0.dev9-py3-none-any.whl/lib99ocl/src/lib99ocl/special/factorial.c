#ifndef _FACTORIAL_C_
#define _FACTORIAL_C_


#include "../core.h"


WITHIN_KERNEL
int nfactorial(const int n)
{
   if (n <= 0) { return 1.; }

   int x = 1;
   int b = 0;
   do {
      b++;
      x *= b;
   } while(b!=n);

   return x;
}



WITHIN_KERNEL
ftype factorial(const int n)
{
   if (n <= 0) { return 1.; }

   ftype x = 1;
   int b = 0;
   do {
      b++;
      x *= b;
   } while(b!=n);

   return x;
}


WITHIN_KERNEL
ftype binom(const int n, const int k)
{
  return factorial(n)/(factorial(k)*factorial(n-k));
}


#endif // _FACTORIAL_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
