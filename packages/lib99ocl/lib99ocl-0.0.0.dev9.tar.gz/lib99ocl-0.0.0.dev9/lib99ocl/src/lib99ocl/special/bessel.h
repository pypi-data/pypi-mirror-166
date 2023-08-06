#ifndef _BESSEL_H_
#define _BESSEL_H_


#include "../core.h"


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
ftype rjn(const int n, const ftype x);



/**
 * Bessel Jv
 *
 * Bessel 1st of real order
 *
 * @param n Order.
 * @param x Point
 * @return Bessel J function of order n at x.
 */
WITHIN_KERNEL
ftype rjv(const ftype n, const ftype x);



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
ftype ryn(const int n, const ftype x);



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
ftype ryv(const ftype n, const ftype x);



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
ftype rin(const int n, const ftype x);



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
ftype riv(const ftype n, const ftype x);



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
ftype rin(const int n, const ftype x);



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
ftype riv(const ftype n, const ftype x);



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
ftype rkn(const int n, const ftype x);



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
ftype rkv(const ftype n, const ftype x);


#endif // _BESSEL_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
