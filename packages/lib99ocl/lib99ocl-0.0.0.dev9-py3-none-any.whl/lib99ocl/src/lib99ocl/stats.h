#ifndef _STATS_H_
#define _STATS_H_

#include "core.h"

WITHIN_KERNEL
ftype kolmogorov_prob(const ftype z);

WITHIN_KERNEL
ftype erf_inverse(const ftype x);

#endif //_STATS_H_

// vim: fdm=marker ts=2 sw=2 sts=2 sr et
