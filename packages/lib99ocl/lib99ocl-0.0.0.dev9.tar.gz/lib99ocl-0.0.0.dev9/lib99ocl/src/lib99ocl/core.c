#include "core.h"

/* #if USE_DOUBLE */
/*   #ifndef CUDA */
/*   #pragma OPENCL EXTENSION cl_khr_int64_base_atomics: enable */
/*     WITHIN_KERNEL */
/*     void */
/*     atomicAdd(volatile __global double *addr, double val) */
/*     { */
/*       union { */
/*         long u; */
/*         double f; */
/*       } next, expected, current; */
/*       current.f = *addr; */
/*       do { */
/*         expected.f = current.f; */
/*         next.f = expected.f + val; */
/*         current.u = atomic_cmpxchg( (volatile __global long *) addr, expected.u, next.u); */
/*       } while( current.u != expected.u ); */
/*     } */
/*   #endif */
/* #endif */



#ifdef CUDA
  WITHIN_KERNEL
  ftype fract(const ftype x)
  {
    return x - floorf(x);
  }
#else
  WITHIN_KERNEL
  ftype fract(const ftype x)
  {
    return x - floor(x);
  }
#endif



WITHIN_KERNEL
ftype rpow(const ftype x, const ftype n)
{
  return pow(x, n);
}



WITHIN_KERNEL
ftype sqr(const ftype x)
{
  return x*x;
}


WITHIN_KERNEL
int nearest_int(ftype x)
{
   int i;
   if (x >= 0) {
      i = (int)(x + 0.5);
      if ( i & 1 && x + 0.5 == (ftype)i ) i--;
   } else {
      i = (int)(x - 0.5);
      if ( i & 1 && x - 0.5 == (ftype)i ) i++;
   }
   return i;
}

// WITHIN_KERNEL
// ftype round(const ftype x)
// {
//     ftype y, r;
//
//     /* Largest integer <= x */
//     y = floor(x);
//
//     /* Fractional part */
//     r = x - y;
//
//     /* Round up to nearest. */
//     if (r > 0.5)
// 	goto rndup;
//
//     /* Round to even */
//     if (r == 0.5) {
// 	r = y - 2.0 * floor(0.5 * y);
// 	if (r == 1.0) {
// 	  rndup:
// 	    y += 1.0;
// 	}
//     }
//
//     /* Else round down. */
//     return (y);
// }


//static float sqrarg;
//#define SQR(a) ((sqrarg=(a)) == 0.0 ? 0.0 : sqrarg*sqrarg)
//#define SQUARE(a) ((a)*(a))

/* ftype hypotenuse(const ftype a, const ftype b) */
/* { */
/*   const ftype absa = fabs(a); */
/*   const ftype absb = fabs(b); */
/*   if (absa > absb) */
/*   { */
/*     return absa * sqrt(1.0 + SQUARE(absb/absa)); */
/*   } */
/*   else */
/*   { */
/*     return absb == 0.0 ? 0.0 : absb * sqrt(1.0 + SQUARE(absa/absb)); */
/*   } */
/* } */






