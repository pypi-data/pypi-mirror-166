#ifndef _GAMMA_C_
#define _GAMMA_C_


#include "gamma.h"


// rgamma {{{

WITHIN_KERNEL
ftype rgamma(ftype x)
{
  #ifdef CUDA
    return tgammaf(x);
  #else
    return tgamma(x);
  #endif
}

WITHIN_KERNEL
ftype gammasgn(ftype x)
{
    ftype fx;

    if (isnan(x)) {
      return x;
    }
    if (x > 0) {
        return 1.0;
    }
    else {
        fx = floor(x);
        if (x - fx == 0.0) {
            return 0.0;
        }
        else if ((int)fx % 2) {
            return -1.0;
        }
        else {
            return 1.0;
        }
    }
}

/*
WITHIN_KERNEL
ftype tarasca(ftype n)
{
  // Integrate[x^n*Sqrt[1 - x^2], {x, -1, 1}]
  ftype ans = (1 + pow(-1.,n)) * sqrt(M_PI) * rgamma((1 + n)/2);
  return ans / (4.*rgamma(2 + n/2));
}



WITHIN_KERNEL
ftype curruncho(const ftype n, const ftype m, const ftype xi, const ftype xf) {
  // Integrate[x^n*Cos[x]^m, {x, -1, 1}]
  ftype ans = 0;
  if (xi == xf) return ans;
  if (n == 0.0) return pow(xf, m+1.)/(m+1.) - pow(xi, m+1.)/(m+1.);

  ftype kf = 0;
  ftype mupp = floor((m+1)/2);
  ftype mlow = floor((m-1)/2);
  for (int k=0; k<mlow; k++){
    kf = k;
    ans += pow(-1., kf) * (rgamma(m+1)/rgamma(m-2*k)) * pow(n*M_PI, m-2*kf-1);
  }
  ans *= pow(-1., n) / pow(n, m+1);
  ans += pow(-1.,mupp) * (rgamma(m+1)*floor(2*mupp - m))/pow(n, m+1);
  return ans*(xf - pow(-1.,m)*xi)/M_PI;
}



WITHIN_KERNEL
ftype pozo(const ftype n, const ftype m, const ftype xi, const ftype xf)  {
  // Integrate[x^n*Sin[x]^m, {x, -1, 1}]
  ftype ans = 0;
  if (xi == xf) return ans;
  if (n == 0.0) return ans;

  ftype kf = 0;
  ftype mhalf = floor(m/2);
  for (int k=0; k<mhalf; k++){
     kf = k;
     ans += pow(-1., kf) * (rgamma(m+1)/rgamma(m-2*k+1)) * pow(n*M_PI, m-2*k);
  }
  ans *= pow(-1., n+1) / pow(n, m+1);
  ans -= pow(-1., mhalf) * (rgamma(m+1)*floor(m-2*mhalf-1)) / pow(n, m+1);
  return ans*(xf - pow(-1.,m)*xi)/M_PI;
}
*/

// }}}


// rgammaln {{{

WITHIN_KERNEL
ftype rgammaln(const ftype x)
{
  if (isnan(x)) return(x);
  if (!isfinite(x)) return(INFINITY);
  return lgamma(x);
}

// }}}


// details_igamma {{{

WITHIN_KERNEL
ftype __core_igamc(ftype a, ftype x)
{

    ftype ans, ax, c, yc, r, t, y, z;
    ftype pk, pkm1, pkm2, qk, qkm1, qkm2;

    /* Compute  x**a * exp(-x) / gamma(a)  */
    ax = a * log(x) - x - lgamma(a);
    if (ax < -MAXLOG) return 0.0;  // underflow
    ax = exp(ax);

    /* continued fraction */
    y = 1.0 - a;
    z = x + y + 1.0;
    c = 0.0;
    pkm2 = 1.0;
    qkm2 = x;
    pkm1 = x + 1.0;
    qkm1 = z * x;
    ans = pkm1/qkm1;

    do {
        c += 1.0;
        y += 1.0;
        z += 2.0;
        yc = y * c;
        pk = pkm1 * z  -  pkm2 * yc;
        qk = qkm1 * z  -  qkm2 * yc;
        if (qk != 0) {
            r = pk/qk;
            t = fabs( (ans - r)/r );
            ans = r;
        } else {
            t = 1.0;
        }
        pkm2 = pkm1;
        pkm1 = pk;
        qkm2 = qkm1;
        qkm1 = qk;
        if (fabs(pk) > BIG) {
            pkm2 *= BIGINV;
            pkm1 *= BIGINV;
            qkm2 *= BIGINV;
            qkm1 *= BIGINV;
        }
    } while( t > MACHEP );

    return( ans * ax );
}


WITHIN_KERNEL
ftype __core_igam(ftype a, ftype x)
{
    //const ftype MACHEP = 1.11022302462515654042E-16; // IEEE 2**-53
    //const ftype MAXLOG = 7.09782712893383996843E2; // IEEE log(2**1024) denormalized
    ftype ans, ax, c, r;

    /* Compute  x**a * exp(-x) / gamma(a)  */
    ax = a * log(x) - x - lgamma(a);
    if (ax < -MAXLOG) return 0.0; // underflow
    ax = exp(ax);

    /* power series */
    r = a;
    c = 1.0;
    ans = 1.0;

    do {
        r += 1.0;
        c *= x/r;
        ans += c;
    } while (c/ans > MACHEP);

    return ans * ax/a;
}

// }}}


// incomplete gamma functions {{{

WITHIN_KERNEL
ftype rgammainc(const ftype a, const ftype x)
{
    if ((x <= 0) || ( a <= 0)) return 0.0;
    if ((x > 1.0) && (x > a)) return 1.0 - __core_igamc(a, x);
    return __core_igam(a, x);
}



WITHIN_KERNEL
ftype rgammaincc(const ftype a, const ftype x)
{
    if ((x <= 0.0) || (a <= 0)) return 1.0;
    if ((x <  1.0) || (x <  a)) return 1.0 - __core_igam(a, x);
    return __core_igamc(a, x);
}

// }}}


// Probably not interesting functions anymore {{{

/*
WITHIN_KERNEL
ftype corzo(ftype n, ftype xi, ftype xf)
{
  // Integrate[x^n*Cos[x]*Cos[x], {x, xi, xf}]
  ctype cte = C(0., +pow(2.,-n) );

  ftype fi = (4*xi)/(1+n);
  fi -= rgamma(1+n)*cre(
                        cmul(
                            cmul(cte, cpow(C(0.,-xi), C(-n,0.))),
                            cgammaincc(1+n, C(0.,-2*xi))
                            )
                        );
  fi += rgamma(1+n)*cre(
                        cmul(
                            cmul(cte, cpow(C(0.,+xi), C(-n,0.))),
                            cgammaincc(1+n, C(0.,+2*xi))
                            )
                        );

  ftype ff = (4*xf)/(1+n);
  ff -= rgamma(1+n)*cre(
                        cmul(
                            cmul(cte, cpow(C(0.,-xf), C(-n,0.))),
                            cgammaincc(1+n, C(0.,-2*xf))  )  );
  ff += rgamma(1+n)*cre(
                        cmul(
                            cmul(cte, cpow(C(0.,+xf), C(-n,0.))),
                            cgammaincc(1+n, C(0.,+2*xf))
                            )
                        );

  return 0.125*( pow(xf,n)*ff - pow(xi,n)*fi );
}



WITHIN_KERNEL
ftype maycar(ftype n, ftype xi, ftype xf)
{
  // Integrate[x^n*Sin[x]*Sin[x], {x, xi, xf}]
  ctype cte = C(0., +pow(2.,-n) );

  ftype fi = pow(2.,2.+n)*xi*pow(xi*xi,n);
  fi += rgamma(1+n)*cre(
                        cmul(
                            cmul(C(0.,1+n), cpow(C(0.,+xi), C(n,0.))),
                            cgammaincc(1+n, C(0.,-2*xi))
                            )
                        );
  fi -= rgamma(1+n)*cre(
                        cmul(
                            cmul(C(0.,1+n), cpow(C(0.,-xi), C(n,0.))),
                            cgammaincc(1+n, C(0.,+2*xi))
                            )
                        );

  ftype ff = pow(2.,2.+n)*xf*pow(xf*xf,n);
  ff += rgamma(1+n)*cre(
                        cmul(
                            cmul(C(0.,1+n), cpow(C(0.,+xf), C(n,0.))),
                            cgammaincc(1+n, C(0.,-2*xf))  )  );
  ff -= rgamma(1+n)*cre(
                        cmul(
                            cmul(C(0.,1+n), cpow(C(0.,-xf), C(n,0.))),
                            cgammaincc(1+n, C(0.,+2*xf))
                            )
                        );

  return (pow(2.,-3-n)/(1+n))*( pow(xf,-n)*ff - pow(xi,-n)*fi );
}
*/

// }}}


#endif // _GAMMA_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
