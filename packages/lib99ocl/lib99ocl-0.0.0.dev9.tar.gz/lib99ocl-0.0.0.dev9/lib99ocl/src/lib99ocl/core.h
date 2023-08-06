#ifndef _CORE_H_
#define _CORE_H_

#include "constants.h"
#include "machine.h"

#ifndef float2
struct double2_struct {
  double x;
  double y;
};
typedef struct double2_struct complex_double;
struct float2_struct {
  float x;
  float y;
};
typedef struct float2_struct complex_float;
#endif

#if USE_DOUBLE
// #define ftype double
// #define ctype complex_double
#define ftype double
#define ctype double2
#else
#define ftype float
#define ctype float2
// #define ctype complex_float
#endif

#ifndef CUDA
#include "opencl.h"
#else
#define _CUDA_H_
#include "cuda.h"
#endif

WITHIN_KERNEL
ftype fract(const ftype a);

WITHIN_KERNEL
ftype rmax(const ftype a, const ftype b) { return (a > b) ? a : b; }

WITHIN_KERNEL
ftype rmin(const ftype a, const ftype b) { return (a < b) ? a : b; }

WITHIN_KERNEL
ftype rpow(const ftype x, const ftype n);

WITHIN_KERNEL
ftype sqr(const ftype x);

WITHIN_KERNEL
int nearest_int(const ftype x);

#endif //_CORE_H_

// vim: fdm=marker
