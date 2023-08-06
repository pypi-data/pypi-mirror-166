#ifndef _HYP2F1_H_
#define _HYP2F1_H_

#include "../core.h"
#include "gamma.h"
#include "psi.h"


/* hyp2f1.c
 *
 *      Gauss hypergeometric function   F
 *                                     2 1
 *
 *
 * SYNOPSIS:
 *
 * double a, b, c, x, y, hyp2f1();
 *
 * y = hyp2f1( a, b, c, x );
 *
 *
 * DESCRIPTION:
 *
 *
 *  hyp2f1( a, b, c, x )  =   F ( a, b; c; x )
 *                           2 1
 *
 *           inf.
 *            -   a(a+1)...(a+k) b(b+1)...(b+k)   k+1
 *   =  1 +   >   -----------------------------  x   .
 *            -         c(c+1)...(c+k) (k+1)!
 *          k = 0
 *
 *  Cases addressed are
 *      Tests and escapes for negative integer a, b, or c
 *      Linear transformation if c - a or c - b negative integer
 *      Special case c = a or c = b
 *      Linear transformation for  x near +1
 *      Transformation for x < -0.5
 *      Psi function expansion if x > 0.5 and c - a - b integer
 *      Conditionally, a recurrence on c to make c-a-b > 0
 *
 *      x < -1  AMS 15.3.7 transformation applied (Travis Oliphant)
 *         valid for b,a,c,(b-a) != integer and (c-a),(c-b) != negative integer
 *
 * x >= 1 is rejected (unless special cases are present)
 *
 * The parameters a, b, c are considered to be integer
 * valued if they are within 1.0e-14 of the nearest integer
 * (1.0e-13 for IEEE arithmetic).
 *
 * ACCURACY:
 *
 *
 *               Relative error (-1 < x < 1):
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      -1,7        230000      1.2e-11     5.2e-14
 *
 * Several special cases also tested with a, b, c in
 * the range -7 to 7.
 *
 * ERROR MESSAGES:
 *
 * A "partial loss of precision" message is printed if
 * the internally estimated relative error exceeds 1^-12.
 * A "singularity" message is printed on overflow or
 * in cases not addressed (such as x < -1).
 */

/*
 * Cephes Math Library Release 2.8:  June, 2000
 * Copyright 1984, 1987, 1992, 2000 by Stephen L. Moshier
 */

/* This variant of cephes hyp2f1.c is a lightly revised version of
   that found at
   https://pulvinar.cin.ucsf.edu/ipnotebooks/build/scipy/scipy/special/cephes/
   dated 2013-06-12 and downloaded 2020-06-08. We would give credit
   to the author if its authorship were apparent. It extends the
   original cephes version to handle certain awkward cases involving
   negative integer values that are not properly handled in the
   original: for example, hyp2f1(3, -2, 4, 0.99).
*/


/**
 * hyt2f1() - Gauss hypergeometric function 2F1
 *
 * @a Coeff 1
 * @returns value of 2f1
 */
WITHIN_KERNEL ftype
hyt2f1 (ftype a, ftype b, ftype c, ftype x, ftype *loss);


WITHIN_KERNEL ftype
hys2f1 (ftype a, ftype b, ftype c, ftype x, ftype *loss);


WITHIN_KERNEL ftype
hyp2f1ra (ftype a, ftype b, ftype c, ftype x, ftype *loss);


#endif // _HYP2F1_H_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
