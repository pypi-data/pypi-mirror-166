#ifndef _SPECIAL_H_
#define _SPECIAL_H_

#include "core.h"

// #include "details/bessel.c"
// #include "details/gamma.c"

#define ERRF_CONST 1.12837916709551
#define XLIM 5.33
#define YLIM 4.29

#include "special/erf.h"
#include "special/factorial.h"
#include "special/gamma.h"
#include "special/legendre.h"
#include "special/spherical_harmonics.h"
#include "special/psi.h"
#include "special/hyp2f1.h"
#include "special/bessel.h"

/*
MORE FUNCTIONS TO BE INPLEMENTED
jv(v, z)
Bessel function of the first kind of real order and complex argument.
jve(v, z)
Exponentially scaled Bessel function of order v.
yn(n, x)
Bessel function of the second kind of integer order and real argument.
yv(v, z)
Bessel function of the second kind of real order and complex argument.
yve(v, z)
Exponentially scaled Bessel function of the second kind of real order.
kn(n, x)
Modified Bessel function of the second kind of integer order n
kv(v, z)
Modified Bessel function of the second kind of real order v
kve(v, z)
Exponentially scaled modified Bessel function of the second kind.
iv(v, z)
Modified Bessel function of the first kind of real order.
ive(v, z)
Exponentially scaled modified Bessel function of the first kind
hankel1(v, z)
Hankel function of the first kind
hankel1e(v, z)
Exponentially scaled Hankel function of the first kind
hankel2(v, z)
Hankel function of the second kind
hankel2e(v, z)
Exponentially scaled Hankel function of the second kind
*/

#endif // _SPECIAL_H_

// vim: fdm=marker ts=2 sw=2 sts=2 sr et
