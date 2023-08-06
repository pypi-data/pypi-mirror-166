#ifndef _FACTORIAL_H_
#define _FACTORIAL_H_


#include "../core.h"


/**
 * Factorial Jn
 *
 * Bessel 1st of integer order
 *
 * @param n Order.
 * @param x Point
 * @return Bessel J function of order n at x.
 */
WITHIN_KERNEL
int nfactorial(const int n);



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
ftype factorial(const int n);



/**
 * Returns ( n / k ) binomial coefficient.
 *
 * @param n Order.
 * @param k Point
 * @return Bessel J function of order n at x.
 */
WITHIN_KERNEL
ftype binom(const int n, const int k);


#endif // _FACTORIAL_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr et
