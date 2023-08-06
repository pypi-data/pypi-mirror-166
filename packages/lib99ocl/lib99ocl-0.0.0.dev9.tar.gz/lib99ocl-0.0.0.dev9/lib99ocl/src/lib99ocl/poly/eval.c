#ifndef _EVAL_C_
#define _EVAL_C_

#include "eval.h"
// #include "lib99ocl/opencl.h"

/*
 * Evaluates polynomial of degree N:
 *
 *                     2          N
 * y  =  C  + C x + C x  +...+ C x
 *        0    1     2          N
 *
 * Coefficients are stored in reverse order:
 *
 * coef[0] = C  , ..., coef[N] = C  .
 *            N                   0
 *
 */
WITHIN_KERNEL
ftype polyeval(const ftype x, const ftype coef[], const int N)
{
    ftype ans;
    int i;
    const ftype *p;

    p = coef;
    ans = *p++;
    i = N;

    do
	ans = ans * x + *p++;
    while (--i);

    return (ans);
}

/*
 * Evaluate polynomial when coefficient of x  is 1.0.
 * Otherwise same as polevl.
 */
WITHIN_KERNEL
ftype pol1eval(const ftype x, const ftype coef[], const int N)
{
    ftype ans;
    const ftype *p;
    int i;

    p = coef;
    ans = x + *p++;
    i = N - 1;

    do
	ans = ans * x + *p++;
    while (--i);

    return (ans);
}

/* Evaluate a rational function. See [1]. */

WITHIN_KERNEL
ftype polyratioeval(const ftype x, const ftype num[], const int M, const ftype denom[], const int N)
{
    int i, dir;
    ftype y, num_ans, denom_ans;
    ftype absx = fabs(x);
    const ftype *p;

    if (absx > 1) {
	/* Evaluate as a polynomial in 1/x. */
	dir = -1;
	p = num + M;
	y = 1 / x;
    } else {
	dir = 1;
	p = num;
	y = x;
    }

    /* Evaluate the numerator */
    num_ans = *p;
    p += dir;
    for (i = 1; i <= M; i++) {
	num_ans = num_ans * y + *p;
	p += dir;
    }

    /* Evaluate the denominator */
    if (absx > 1) {
	p = denom + N;
    } else {
	p = denom;
    }

    denom_ans = *p;
    p += dir;
    for (i = 1; i <= N; i++) {
	denom_ans = denom_ans * y + *p;
	p += dir;
    }

    if (absx > 1) {
	i = N - M;
	return pow(x, i) * num_ans / denom_ans;
    } else {
	return num_ans / denom_ans;
    }
}


#endif // _EVAL_C_

// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
