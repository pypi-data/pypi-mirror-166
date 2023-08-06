#ifndef _SPHERICAL_HARMONICS_H_
#define _SPHERICAL_HARMONICS_H_


#include "../core.h"
#include "../complex.h"
#include "../cspecial/spherical_harmonics.h"


/**
 * Bessel Jn
 *
 * Bessel 1st of integer order
 *
 * @param n Order.
 * @param x Point
 * @return Bessel J function of order n at x.
 */
WITHIN_KERNEL
ftype sph_harm(const int l, const int m, const ftype cos_theta, const ftype phi);


#endif // _SPHERICAL_HARMONICS_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr et
