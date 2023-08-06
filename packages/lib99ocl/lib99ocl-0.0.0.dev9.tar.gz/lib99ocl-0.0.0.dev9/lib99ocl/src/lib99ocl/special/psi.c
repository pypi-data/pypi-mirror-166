#ifndef _PSI_C_
#define _PSI_C_

#include "psi.h"
#include "lib99ocl/machine.h"
#include "../poly/eval.c"

// WITHIN_KERNEL
// ftype psi(ftype x) {
//
//   const ftype GAMMA = 0.577215664901532860606512090082;
//   const ftype GAMMA_MINX = 1.e-12;
//   const ftype DIGAMMA_MINNEGX = -1250;
//   const ftype C_LIMIT = 49;
//   const ftype S_LIMIT = 1e-5;
//
//   if (x == floor(x)) {
//     // mtherr_with_arg("psi", CEPHES_SING, x);
// 		if ( x < 0)
// 			return NaN;
// 		else if (floor(x) == 0)
// 			return -MAXNUM;
// 		// else
//
//   }
//   ftype value = 0;
//
//   while (1) {
//
//     if (x >= 0 && x < GAMMA_MINX) {
//       x = GAMMA_MINX;
//     }
//     if (x < DIGAMMA_MINNEGX) {
//       x = DIGAMMA_MINNEGX + GAMMA_MINX;
//       continue;
//     }
//     if (x > 0 && x <= S_LIMIT) {
//       return value + -GAMMA - 1 / x;
//     }
//
//     if (x >= C_LIMIT) {
//       ftype inv = 1 / (x * x);
//       return value + log(x) - 0.5 / x - inv * ((1.0 / 12) + inv * (1.0 / 120
//       - inv / 252));
//     }
//
//     value -= 1 / x;
//     x = x + 1;
//   }
// }


WITHIN_KERNEL
ftype __detail_digamma_imp_1_2(ftype x) {
  /*
   * Rational approximation on [1, 2] taken from Boost.
   *
   * Now for the approximation, we use the form:
   *
   * digamma(x) = (x - root) * (Y + R(x-1))
   *
   * Where root is the location of the positive root of digamma,
   * Y is a constant, and R is optimised for low absolute error
   * compared to Y.
   *
   * Maximum Deviation Found:               1.466e-18
   * At ftype precision, max error found:  2.452e-17
   */
  ftype r, g;

  const float Y = 0.99558162689208984f;

  const ftype root1 = 1569415565.0 / 1073741824.0;
  const ftype root2 = (381566830.0 / 1073741824.0) / 1073741824.0;
  const ftype root3 = 0.9016312093258695918615325266959189453125e-19;

  const ftype P[] = {-0.0020713321167745952, -0.045251321448739056,
               -0.28919126444774784,   -0.65031853770896507,
               -0.32555031186804491,   0.25479851061131551};
  const ftype Q[] = {-0.55789841321675513e-6,
               0.0021284987017821144,
               0.054151797245674225,
               0.43593529692665969,
               1.4606242909763515,
               2.0767117023730469,
               1.0};
  g = x - root1;
  g -= root2;
  g -= root3;
  r = polyeval(x - 1.0, P, 5) / polyeval(x - 1.0, Q, 6);

  return g * Y + g * r;
}

WITHIN_KERNEL
ftype __detail_psi_asy(ftype x) {
  ftype y, z;
  const ftype A[] = {8.33333333333333333333E-2, -2.10927960927960927961E-2,
             7.57575757575757575758E-3, -4.16666666666666666667E-3,
             3.96825396825396825397E-3, -8.33333333333333333333E-3,
             8.33333333333333333333E-2};

  if (x < 1.0e17) {
    z = 1.0 / (x * x);
    y = z * polyeval(z, A, 6);
  } else {
    y = 0.0;
  }

  return log(x) - (0.5 / x) - y;
}

WITHIN_KERNEL
ftype digamma(ftype x) {
  ftype y = 0.0;
  ftype q, r;
  int i, n;

  if (isnan(x)) {
    return x;
  } else if (x == Inf) {
    return x;
  } else if (x == -Inf) {
    return NaN;
  } else if (x == 0) {
    // sf_error("psi", SF_ERROR_SINGULAR, NULL);
    return (x<0) ? -Inf : Inf;
  } else if (x < 0.0) {
    /* argument reduction before evaluating tan(pi * x) */
    r = modf(x, &q);
    if (r == 0.0) {
      // sf_error("psi", SF_ERROR_SINGULAR, NULL);
      return NaN;
    }
    y = -M_PI / tan(M_PI * r);
    x = 1.0 - x;
  }

  /* check for positive integer up to 10 */
  if ((x <= 10.0) && (x == floor(x))) {
    n = (int)x;
    for (i = 1; i < n; i++) {
      y += 1.0 / i;
    }
    y -= M_EULER;
    return y;
  }

  /* use the recurrence relation to move x into [1, 2] */
  if (x < 1.0) {
    y -= 1.0 / x;
    x += 1.0;
  } else if (x < 10.0) {
    while (x > 2.0) {
      x -= 1.0;
      y += 1.0 / x;
    }
  }
  if ((1.0 <= x) && (x <= 2.0)) {
    y += __detail_digamma_imp_1_2(x);
    return y;
  }

  /* x is large, use the asymptotic series */
  y += __detail_psi_asy(x);
  return y;
}

#endif // _PSI_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
