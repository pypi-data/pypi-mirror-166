#ifndef _EVAL_H_
#define _EVAL_H_

#include "../core.h"

WITHIN_KERNEL
ftype polyeval(const ftype x, const ftype *coef, const int N);

WITHIN_KERNEL
ftype pol1eval(const ftype x, const ftype *coef, const int N);

WITHIN_KERNEL
ftype polyratioeval(const ftype x, const ftype num[], const int M,
										const ftype denom[], const int N);

#endif // _EVAL_H_

// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
