#ifndef _COMPLEX_C_
#define _COMPLEX_C_

#include "complex.h"

#define I C(0., 1.)

// Constructors {{{

WITHIN_KERNEL
ctype C(const ftype re, const ftype im) {
#if USE_DOUBLE
  // complex_double ans;
  // ans.x = re;
  // ans.y = im;
  // return ans;
  return COMPLEX_CTR(double2) (re,im);
#else
  // complex_float ans;
  // ans.x = re;
  // ans.y = im;
  // return ans;
  return COMPLEX_CTR(float2) (re,im);
#endif
}

WITHIN_KERNEL
ctype cpolar(const ftype mod, const ftype arg) {
  return C(mod * cos(arg), mod * sin(arg));
}

// }}}

// Arithmetic operands {{{

WITHIN_KERNEL
ctype cadd(const ctype z1, const ctype z2) {
  ftype a = z1.x;
  ftype b = z1.y;
  ftype c = z2.x;
  ftype d = z2.y;
  return C(a + c, b + d);
}

WITHIN_KERNEL
ctype csub(const ctype z1, const ctype z2) {
  ftype a = z1.x;
  ftype b = z1.y;
  ftype c = z2.x;
  ftype d = z2.y;
  return C(a - c, b - d);
}

WITHIN_KERNEL
ctype cmul(const ctype z1, const ctype z2) {
  ftype a = z1.x;
  ftype b = z1.y;
  ftype c = z2.x;
  ftype d = z2.y;
  return C(a * c - b * d, a * d + b * c);
}

WITHIN_KERNEL
ctype cdiv(const ctype z1, const ctype z2) {
  ftype a = z1.x;
  ftype b = z1.y;
  ftype c = z2.x;
  ftype d = z2.y;
  ftype den = c * c + d * d;
  return C((a * c + b * d) / den, (b * c - a * d) / den);
}

// }}}

// Exponential and logarithm {{{

WITHIN_KERNEL
ctype cexp(const ctype z) {
  ftype re = exp(z.x);
  ftype im = z.y;
  return C(re * cos(im), re * sin(im));
}

WITHIN_KERNEL
ctype clog(const ctype z) { return C(log(cabs(z)), atan2(cim(z), cre(z))); }

// }}}

// Complex basic functions {{{

WITHIN_KERNEL
ctype cconj(const ctype z) { return C(z.x, -z.y); }

WITHIN_KERNEL
ftype cnorm(const ctype z) { return z.x * z.x + z.y * z.y; }

WITHIN_KERNEL
ftype cabs(const ctype z) { return sqrt(cnorm(z)); }

WITHIN_KERNEL
ftype cre(const ctype z) { return z.x; }

WITHIN_KERNEL
ftype cim(const ctype z) { return z.y; }

WITHIN_KERNEL
ftype carg(const ctype z) { return atan(z.y / z.x); }

// }}}

// Powers {{{

WITHIN_KERNEL
ctype csquare(const ctype z) {
  ftype re = -z.x * z.x + z.y * z.y;
  ftype im = -2. * z.x * z.y;
  return C(re, im);
}

WITHIN_KERNEL
ctype cpow(const ctype w, const ctype z) { return cexp(cmul(z, clog(w))); }

WITHIN_KERNEL
ctype csqrt(const ctype w, const ctype z) { return cexp(cmul(z, clog(w))); }

// }}}

#endif // _COMPLEX_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr et
