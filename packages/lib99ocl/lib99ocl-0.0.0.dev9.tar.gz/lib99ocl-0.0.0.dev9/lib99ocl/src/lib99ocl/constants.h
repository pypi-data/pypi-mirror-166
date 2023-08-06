#ifndef _CONSTANTS_H_
#define _CONSTANTS_H_

// Machine {{{
//
// intgration
#define EPS 1.0e-5
#define JMAX 20

// randon number generation
#define RNG_CYCLES 100


#define Inf (1./0.)
#define NaN (0./0.)

// }}}

// Define machine constants
#define SQRT_2PI_INV 0.3989422804
#define EUL 5.772156649015328606065e-1
#define MAXFAC 31
#define MAXNUM 1.79769313486231570815E308     // 2**1024*(1-MACHEP)
#define MAXLOG 8.8029691931113054295988E1     // log(2**127)
#define MACHEP 1.38777878078144567553E-17     // 2**-56
#define DBLEPS 2.2204460492503131e-16

#define SMALLEPS 1e-13
// MACHEP = 1.11022302462515654042E-16; // IEEE 2**-53
// MAXLOG = 7.09782712893383996843E2; // IEEE log(2**1024) denormalized
#define BIG 4.503599627370496e15
#define BIGINV 2.22044604925031308085e-16

// More math constants
#define M_SQRTPI_2 1.2533141373155001 // sqrt(pi/2)
#define M_SQRTPIHALF 0.8862269254527580136490837416705725913990 // sqrt(pi)/2
#define M_SQRT2PI 2.5066282746310005024157652848110 // sqrt(2*pi)

//#define M_SQRT2 1.4142135623730951
//
//
//
#ifndef M_E
#define M_E        2.71828182845904523536028747135      /* e */
#endif

#ifndef M_LOG2E
#define M_LOG2E    1.44269504088896340735992468100      /* log_2 (e) */
#endif

#ifndef M_LOG10E
#define M_LOG10E   0.43429448190325182765112891892      /* log_10 (e) */
#endif

#ifndef M_SQRT2
#define M_SQRT2    1.41421356237309504880168872421      /* sqrt(2) */
#endif

#ifndef M_SQRT1_2
#define M_SQRT1_2  0.70710678118654752440084436210      /* sqrt(1/2) */
#endif


#ifndef M_SQRT3
#define M_SQRT3    1.73205080756887729352744634151      /* sqrt(3) */
#endif

#ifndef M_PI
#define M_PI       3.14159265358979323846264338328      /* pi */
#endif

#ifndef M_PI_2
#define M_PI_2     1.57079632679489661923132169164      /* pi/2 */
#endif

#ifndef M_PI_4
#define M_PI_4     0.78539816339744830961566084582     /* pi/4 */
#endif

#ifndef M_SQRTPI
#define M_SQRTPI   1.77245385090551602729816748334      /* sqrt(pi) */
#endif

#ifndef M_2_SQRTPI
#define M_2_SQRTPI 1.12837916709551257389615890312      /* 2/sqrt(pi) */
#endif

#ifndef M_1_PI
#define M_1_PI     0.31830988618379067153776752675      /* 1/pi */
#endif

#ifndef M_2_PI
#define M_2_PI     0.63661977236758134307553505349      /* 2/pi */
#endif

#ifndef M_LN10
#define M_LN10     2.30258509299404568401799145468      /* ln(10) */
#endif

#ifndef M_LN2
#define M_LN2      0.69314718055994530941723212146      /* ln(2) */
#endif

#ifndef M_LNPI
#define M_LNPI     1.14472988584940017414342735135      /* ln(pi) */
#endif

#ifndef M_EULER
#define M_EULER    0.57721566490153286060651209008      /* Euler constant */
#endif

// these ones are for faddeva
#define ERRF_CONST 1.12837916709551
#define XLIM 5.33
#define YLIM 4.29


#endif // _CONSTANTS_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
