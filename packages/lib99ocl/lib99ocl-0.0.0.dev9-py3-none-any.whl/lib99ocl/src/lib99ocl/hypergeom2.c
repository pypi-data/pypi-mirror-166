#ifndef _HYPERGEOM2_C_
#define _HYPERGEOM2_C_

#include <lib99ocl/machine.h>

#define HYPERGEOM_EPS 1e-10

#define GSL_SUCCESS 0
#define GSL_FAILURE  -1,
#define GSL_CONTINUE -2,  /* iteration has not converged */
#define GSL_EDOM     1,   /* input domain error, e.g sqrt(-1) */
#define GSL_ERANGE   2,   /* output range error, e.g. exp(1e100) */
#define GSL_EFAULT   3,   /* invalid pointer */
#define GSL_EINVAL   4,   /* invalid argument supplied by user */
#define GSL_EFAILED  5,   /* generic failure */
#define GSL_EFACTOR  6,   /* factorization failed */
#define GSL_ESANITY  7,   /* sanity check failed - shouldn't happen */
#define GSL_ENOMEM   8,   /* malloc failed */
#define GSL_EBADFUNC 9,   /* problem with user-supplied function */
#define GSL_ERUNAWAY 10,  /* iterative process is out of control */
#define GSL_EMAXITER 11,  /* exceeded max number of iterations */
#define GSL_EZERODIV 12,  /* tried to divide by zero */
#define GSL_EBADTOL  13,  /* user specified an invalid tolerance */
#define GSL_ETOL     14,  /* failed to reach the specified tolerance */
#define GSL_EUNDRFLW 15,  /* underflow */
#define GSL_EOVRFLW  16,  /* overflow  */
#define GSL_ELOSS    17,  /* loss of accuracy */
#define GSL_EROUND   18,  /* failed because of roundoff error */
#define GSL_EBADLEN  19,  /* matrix, vector lengths are not conformant */
#define GSL_ENOTSQR  20,  /* matrix not square */
#define GSL_ESING    21,  /* apparent singularity detected */
#define GSL_EDIVERGE 22,  /* integral or series is divergent */
#define GSL_EUNSUP   23,  /* requested feature is not supported by the hardware */
#define GSL_EUNIMPL  24,  /* requested feature not (yet) implemented */
#define GSL_ECACHE   25,  /* cache limit exceeded */
#define GSL_ETABLE   26,  /* table limit exceeded */
#define GSL_ENOPROG  27,  /* iteration is not making progress towards solution */
#define GSL_ENOPROGJ 28,  /* jacobian evaluations are not improving the solution */
#define GSL_ETOLF    29,  /* cannot reach the specified tolerance in F */
#define GSL_ETOLX    30,  /* cannot reach the specified tolerance in X */
#define GSL_ETOLG    31,  /* cannot reach the specified tolerance in gradient */
#define GSL_EOF      32   /* end of file */


#ifdef INFINITY
# define GSL_POSINF INFINITY
# define GSL_NEGINF (-INFINITY)
#elif defined(HUGE_VAL)
# define GSL_POSINF HUGE_VAL
# define GSL_NEGINF (-HUGE_VAL)
#else
# define GSL_POSINF (gsl_posinf())
# define GSL_NEGINF (gsl_neginf())
#endif

#ifdef NAN
# define GSL_NAN NAN
#elif defined(INFINITY)
# define GSL_NAN (INFINITY/INFINITY)
#else
# define GSL_NAN (gsl_nan())
#endif

#define GSL_POSZERO (+0.0)
#define GSL_NEGZERO (-0.0)

#define GSL_IS_ODD(n)  ((n) & 1)
#define GSL_IS_EVEN(n) (!(GSL_IS_ODD(n)))
#define GSL_SIGN(x)    ((x) >= 0.0 ? 1 : -1)



#define GSL_MAX(a,b) ((a) > (b) ? (a) : (b))
#define GSL_MIN(a,b) ((a) < (b) ? (a) : (b))
#define GSL_MAX_INT(a,b)   GSL_MAX(a,b)
#define GSL_MIN_INT(a,b)   GSL_MIN(a,b)
#define GSL_MAX_DBL(a,b)   GSL_MAX(a,b)
#define GSL_MIN_DBL(a,b)   GSL_MIN(a,b)
#define GSL_MAX_LDBL(a,b)  GSL_MAX(a,b)
#define GSL_MIN_LDBL(a,b)  GSL_MIN(a,b)


















// Error {{{

/* GSL_ERROR_NULL suitable for out-of-memory conditions */

#define GSL_ERROR_NULL(reason, gsl_errno) GSL_ERROR_VAL(reason, gsl_errno, 0)

/* Sometimes you have several status results returned from
 * function calls and you want to combine them in some sensible
 * way. You cannot produce a "total" status condition, but you can
 * pick one from a set of conditions based on an implied hierarchy.
 *
 * In other words:
 *    you have: status_a, status_b, ...
 *    you want: status = (status_a if it is bad, or status_b if it is bad,...)
 *
 * In this example you consider status_a to be more important and
 * it is checked first, followed by the others in the order specified.
 *
 * Here are some dumb macros to do this.
 */
#define GSL_ERROR_SELECT_2(a,b)       ((a) != GSL_SUCCESS ? (a) : ((b) != GSL_SUCCESS ? (b) : GSL_SUCCESS))
#define GSL_ERROR_SELECT_3(a,b,c)     ((a) != GSL_SUCCESS ? (a) : GSL_ERROR_SELECT_2(b,c))
#define GSL_ERROR_SELECT_4(a,b,c,d)   ((a) != GSL_SUCCESS ? (a) : GSL_ERROR_SELECT_3(b,c,d))
#define GSL_ERROR_SELECT_5(a,b,c,d,e) ((a) != GSL_SUCCESS ? (a) : GSL_ERROR_SELECT_4(b,c,d,e))

#define GSL_STATUS_UPDATE(sp, s) do { if ((s) != GSL_SUCCESS) *(sp) = (s);} while(0)





//#define GSL_ERROR(reason, gsl_errno) do { printf ("LIB99OCL: %s:%d: %s: %s\n", __FILE__, __LINE__, "ERROR", reason); return gsl_errno; } while (0)
#define GSL_ERROR(reason, gsl_errno) do { 0; } while (0)

#define OVERFLOW_ERROR(result) do { (result)->val = GSL_POSINF; (result)->err = GSL_POSINF; GSL_ERROR ("overflow", GSL_EOVRFLW); } while(0)
#define UNDERFLOW_ERROR(result) do { (result)->val = 0.0; (result)->err = GSL_DBL_MIN; GSL_ERROR ("underflow", GSL_EUNDRFLW); } while(0)
#define INTERNAL_OVERFLOW_ERROR(result) do { (result)->val = GSL_POSINF; (result)->err = GSL_POSINF; return GSL_EOVRFLW; } while(0)
#define INTERNAL_UNDERFLOW_ERROR(result) do { (result)->val = 0.0; (result)->err = GSL_DBL_MIN; return GSL_EUNDRFLW; } while(0)
#define DOMAIN_ERROR(result) do { (result)->val = GSL_NAN; (result)->err = GSL_NAN; GSL_ERROR ("domain error", GSL_EDOM); } while(0)
#define DOMAIN_ERROR_MSG(msg, result) do { (result)->val = GSL_NAN; (result)->err = GSL_NAN; GSL_ERROR ((msg), GSL_EDOM); } while(0)
#define DOMAIN_ERROR_E10(result) do { (result)->val = GSL_NAN; (result)->err = GSL_NAN; (result)->e10 = 0 ; GSL_ERROR ("domain error", GSL_EDOM); } while(0)
#define OVERFLOW_ERROR_E10(result) do { (result)->val = GSL_POSINF; (result)->err = GSL_POSINF; (result)->e10 = 0; GSL_ERROR ("overflow", GSL_EOVRFLW); } while(0)
#define UNDERFLOW_ERROR_E10(result) do { (result)->val = 0.0; (result)->err = GSL_DBL_MIN; (result)->e10 = 0; GSL_ERROR ("underflow", GSL_EUNDRFLW); } while(0)
#define OVERFLOW_ERROR_2(r1,r2) do { (r1)->val = GSL_POSINF; (r1)->err = GSL_POSINF; (r2)->val = GSL_POSINF ; (r2)->err=GSL_POSINF; GSL_ERROR ("overflow", GSL_EOVRFLW); } while(0)
#define UNDERFLOW_ERROR_2(r1,r2) do { (r1)->val = 0.0; (r1)->err = GSL_DBL_MIN; (r2)->val = 0.0 ; (r2)->err = GSL_DBL_MIN; GSL_ERROR ("underflow", GSL_EUNDRFLW); } while(0)
#define DOMAIN_ERROR_2(r1,r2) do { (r1)->val = GSL_NAN; (r1)->err = GSL_NAN;  (r2)->val = GSL_NAN; (r2)->err = GSL_NAN;  GSL_ERROR ("domain error", GSL_EDOM); } while(0)
#define MAXITER_ERROR(result) do { (result)->val = GSL_NAN; (result)->err = GSL_NAN; GSL_ERROR ("too many iterations error", GSL_EMAXITER); } while(0)

// }}}



struct gsl_sf_result_struct {
  double val;
  double err;
};
typedef struct gsl_sf_result_struct gsl_sf_result;



int gsl_sf_lngamma_e(ftype x, gsl_sf_result *result)
{
  result->val = lgamma(x);
  return 0;
}

int gsl_sf_lngamma_sgn_e(ftype x, gsl_sf_result *result, double *sgn)
{
	const ftype sign = (fabs(rgamma(x)) >0) ? 1:0;
	*sgn = sign;
  result->val = lgamma(x);
  return 0;
}

int
gsl_sf_exp_err_e(const double x, const double dx, gsl_sf_result * result)
{
  const double adx = fabs(dx);

  /* CHECK_POINTER(result) */

  if(x + adx > GSL_LOG_DBL_MAX) {
    OVERFLOW_ERROR(result);
  }
  else if(x - adx < GSL_LOG_DBL_MIN) {
    UNDERFLOW_ERROR(result);
  }
  else {
    const double ex  = exp(x);
    const double edx = exp(adx);
    result->val  = ex;
    result->err  = ex * GSL_MAX_DBL(GSL_DBL_EPSILON, edx - 1.0/edx);
    result->err += 2.0 * GSL_DBL_EPSILON * fabs(result->val);
    return GSL_SUCCESS;
  }
}

int gsl_sf_exp_mult_err_e(const double x, const double dx,
                             const double y, const double dy,
                             gsl_sf_result * result)
{
  const double ay  = fabs(y);

  if(y == 0.0) {
    result->val = 0.0;
    result->err = fabs(dy * exp(x));
    return GSL_SUCCESS;
  }
  else if(   ( x < 0.5*GSL_LOG_DBL_MAX   &&   x > 0.5*GSL_LOG_DBL_MIN)
          && (ay < 0.8*GSL_SQRT_DBL_MAX  &&  ay > 1.2*GSL_SQRT_DBL_MIN)
    ) {
    double ex = exp(x);
    result->val  = y * ex;
    result->err  = ex * (fabs(dy) + fabs(y*dx));
    result->err += 2.0 * GSL_DBL_EPSILON * fabs(result->val);
    return GSL_SUCCESS;
  }
  else {
    const double ly  = log(ay);
    const double lnr = x + ly;

    if(lnr > GSL_LOG_DBL_MAX - 0.01) {
      OVERFLOW_ERROR(result);
    }
    else if(lnr < GSL_LOG_DBL_MIN + 0.01) {
      UNDERFLOW_ERROR(result);
    }
    else {
      const double sy  = GSL_SIGN(y);
      const double M   = floor(x);
      const double N   = floor(ly);
      const double a   = x  - M;
      const double b   = ly - N;
      const double eMN = exp(M+N);
      const double eab = exp(a+b);
      result->val  = sy * eMN * eab;
      result->err  = eMN * eab * 2.0*GSL_DBL_EPSILON;
      result->err += eMN * eab * fabs(dy/y);
      result->err += eMN * eab * fabs(dx);
      return GSL_SUCCESS;
    }
  }
}






/* Assumes c != negative integer.
 */
WITHIN_KERNEL int
hyperg_2F1_series(const ftype a, const ftype b, const ftype c,
                  const ftype x, 
                  gsl_sf_result * result
                  )
{
  ftype sum_pos = 1.0;
  ftype sum_neg = 0.0;
  ftype del_pos = 1.0;
  ftype del_neg = 0.0;
  ftype del = 1.0;
  ftype k = 0.0;
  int i = 0;

  if(fabs(c) < DBLEPS) {
    result->val = 0.0; /* FIXME: ?? */
    result->err = 1.0;
    // GSL_ERROR ("error", GSL_EDOM);
  }

  do {
    if(++i > 30000) {
      result->val  = sum_pos - sum_neg;
      result->err  = del_pos + del_neg;
      result->err += 2.0 * DBLEPS * (sum_pos + sum_neg);
      result->err += 2.0 * DBLEPS * (2.0*sqrt(k)+1.0) * fabs(result->val);
      // GSL_ERROR ("error", GSL_EMAXITER);
    }
    del *= (a+k)*(b+k) * x / ((c+k) * (k+1.0));  /* Gauss series */

    if(del > 0.0) {
      del_pos  =  del;
      sum_pos +=  del;
    }
    else if(del == 0.0) {
      /* Exact termination (a or b was a negative integer).
       */
      del_pos = 0.0;
      del_neg = 0.0;
      break;
    }
    else {
      del_neg  = -del;
      sum_neg -=  del;
    }

    k += 1.0;
  } while(fabs((del_pos + del_neg)/(sum_pos-sum_neg)) > DBLEPS);

  result->val  = sum_pos - sum_neg;
  result->err  = del_pos + del_neg;
  result->err += 2.0 * DBLEPS * (sum_pos + sum_neg);
  result->err += 2.0 * DBLEPS * (2.0*sqrt(k) + 1.0) * fabs(result->val);

  return GSL_SUCCESS;
}


/* a = aR + i aI, b = aR - i aI */
WITHIN_KERNEL
int
hyperg_2F1_conj_series(const ftype aR, const ftype aI, const ftype c,
                       ftype x,
                       gsl_sf_result * result)
{
  if(c == 0.0) {
    result->val = 0.0; /* FIXME: should be Inf */
    result->err = 0.0;
    // GSL_ERROR ("error", GSL_EDOM);
  }
  else {
    ftype sum_pos = 1.0;
    ftype sum_neg = 0.0;
    ftype del_pos = 1.0;
    ftype del_neg = 0.0;
    ftype del = 1.0;
    ftype k = 0.0;
    do {
      del *= ((aR+k)*(aR+k) + aI*aI)/((k+1.0)*(c+k)) * x;

      if(del >= 0.0) {
        del_pos  =  del;
        sum_pos +=  del;
      }
      else {
        del_neg  = -del;
        sum_neg -=  del;
      }

      if(k > 30000) {
        result->val  = sum_pos - sum_neg;
        result->err  = del_pos + del_neg;
        result->err += 2.0 * DBLEPS * (sum_pos + sum_neg);
        result->err += 2.0 * DBLEPS * (2.0*sqrt(k)+1.0) * fabs(result->val);
        // GSL_ERROR ("error", GSL_EMAXITER);
      }

      k += 1.0;
    } while(fabs((del_pos + del_neg)/(sum_pos - sum_neg)) > DBLEPS);

    result->val  = sum_pos - sum_neg;
    result->err  = del_pos + del_neg;
    result->err += 2.0 * DBLEPS * (sum_pos + sum_neg);
    result->err += 2.0 * DBLEPS * (2.0*sqrt(k) + 1.0) * fabs(result->val);

    return GSL_SUCCESS;
  }
}


/* Luke's rational approximation. The most accesible
 * discussion is in [Kolbig, CPC 23, 51 (1981)].
 * The convergence is supposedly guaranteed for x < 0.
 * You have to read Luke's books to see this and other
 * results. Unfortunately, the stability is not so
 * clear to me, although it seems very efficient when
 * it works.
 */
WITHIN_KERNEL
int
hyperg_2F1_luke(const ftype a, const ftype b, const ftype c,
                const ftype xin, 
                gsl_sf_result * result)
{
  int stat_iter;
  const ftype RECUR_BIG = 1.0e+50;
  const int nmax = 20000;
  int n = 3;
  const ftype x  = -xin;
  const ftype x3 = x*x*x;
  const ftype t0 = a*b/c;
  const ftype t1 = (a+1.0)*(b+1.0)/(2.0*c);
  const ftype t2 = (a+2.0)*(b+2.0)/(2.0*(c+1.0));
  ftype F = 1.0;
  ftype prec;

  ftype Bnm3 = 1.0;                                  /* B0 */
  ftype Bnm2 = 1.0 + t1 * x;                         /* B1 */
  ftype Bnm1 = 1.0 + t2 * x * (1.0 + t1/3.0 * x);    /* B2 */
 
  ftype Anm3 = 1.0;                                                      /* A0 */
  ftype Anm2 = Bnm2 - t0 * x;                                            /* A1 */
  ftype Anm1 = Bnm1 - t0*(1.0 + t2*x)*x + t0 * t1 * (c/(c+1.0)) * x*x;   /* A2 */

  while(1) {
    ftype npam1 = n + a - 1;
    ftype npbm1 = n + b - 1;
    ftype npcm1 = n + c - 1;
    ftype npam2 = n + a - 2;
    ftype npbm2 = n + b - 2;
    ftype npcm2 = n + c - 2;
    ftype tnm1  = 2*n - 1;
    ftype tnm3  = 2*n - 3;
    ftype tnm5  = 2*n - 5;
    ftype n2 = n*n;
    ftype F1 =  (3.0*n2 + (a+b-6)*n + 2 - a*b - 2*(a+b)) / (2*tnm3*npcm1);
    ftype F2 = -(3.0*n2 - (a+b+6)*n + 2 - a*b)*npam1*npbm1/(4*tnm1*tnm3*npcm2*npcm1);
    ftype F3 = (npam2*npam1*npbm2*npbm1*(n-a-2)*(n-b-2)) / (8*tnm3*tnm3*tnm5*(n+c-3)*npcm2*npcm1);
    ftype E  = -npam1*npbm1*(n-c-1) / (2*tnm3*npcm2*npcm1);

    ftype An = (1.0+F1*x)*Anm1 + (E + F2*x)*x*Anm2 + F3*x3*Anm3;
    ftype Bn = (1.0+F1*x)*Bnm1 + (E + F2*x)*x*Bnm2 + F3*x3*Bnm3;
    ftype r = An/Bn;

    prec = fabs((F - r)/F);
    F = r;

    if(prec < DBLEPS || n > nmax) break;

    if(fabs(An) > RECUR_BIG || fabs(Bn) > RECUR_BIG) {
      An   /= RECUR_BIG;
      Bn   /= RECUR_BIG;      Anm1 /= RECUR_BIG;
      Bnm1 /= RECUR_BIG;
      Anm2 /= RECUR_BIG;
      Bnm2 /= RECUR_BIG;
      Anm3 /= RECUR_BIG;
      Bnm3 /= RECUR_BIG;
    }
    else if(fabs(An) < 1.0/RECUR_BIG || fabs(Bn) < 1.0/RECUR_BIG) {
      An   *= RECUR_BIG;
      Bn   *= RECUR_BIG;
      Anm1 *= RECUR_BIG;
      Bnm1 *= RECUR_BIG;
      Anm2 *= RECUR_BIG;
      Bnm2 *= RECUR_BIG;
      Anm3 *= RECUR_BIG;
      Bnm3 *= RECUR_BIG;
    }

    n++;
    Bnm3 = Bnm2;
    Bnm2 = Bnm1;
    Bnm1 = Bn;
    Anm3 = Anm2;
    Anm2 = Anm1;
    Anm1 = An;
  }

  result->val  = F;
  result->err  = 2.0 * fabs(prec * F);
  result->err += 2.0 * DBLEPS * (n+1.0) * fabs(F);

  /* FIXME: just a hack: there's a lot of shit going on here */
  result->err *= 8.0 * (fabs(a) + fabs(b) + 1.0);

  stat_iter = (n >= nmax ? GSL_EMAXITER : GSL_SUCCESS );

  return stat_iter;
}


/* Luke's rational approximation for the
 * case a = aR + i aI, b = aR - i aI.
 */
WITHIN_KERNEL
int
hyperg_2F1_conj_luke(const ftype aR, const ftype aI, const ftype c,
                     const ftype xin, 
                     gsl_sf_result * result)
{
  const ftype RECUR_BIG = 1.0e+50;
  const int nmax = 10000;
  int n = 3;
  const ftype x = -xin;
  const ftype x3 = x*x*x;
  const ftype atimesb = aR*aR + aI*aI;
  const ftype apb     = 2.0*aR;
  const ftype t0 = atimesb/c;
  const ftype t1 = (atimesb +     apb + 1.0)/(2.0*c);
  const ftype t2 = (atimesb + 2.0*apb + 4.0)/(2.0*(c+1.0));
  ftype F = 1.0;
  ftype prec;

  ftype Bnm3 = 1.0;                                  /* B0 */
  ftype Bnm2 = 1.0 + t1 * x;                         /* B1 */
  ftype Bnm1 = 1.0 + t2 * x * (1.0 + t1/3.0 * x);    /* B2 */
 
  ftype Anm3 = 1.0;                                                      /* A0 */
  ftype Anm2 = Bnm2 - t0 * x;                                            /* A1 */
  ftype Anm1 = Bnm1 - t0*(1.0 + t2*x)*x + t0 * t1 * (c/(c+1.0)) * x*x;   /* A2 */

  while(1) {
    ftype nm1 = n - 1;
    ftype nm2 = n - 2;
    ftype npam1_npbm1 = atimesb + nm1*apb + nm1*nm1;
    ftype npam2_npbm2 = atimesb + nm2*apb + nm2*nm2;
    ftype npcm1 = nm1 + c;
    ftype npcm2 = nm2 + c;
    ftype tnm1  = 2*n - 1;
    ftype tnm3  = 2*n - 3;
    ftype tnm5  = 2*n - 5;
    ftype n2 = n*n;
    ftype F1 =  (3.0*n2 + (apb-6)*n + 2 - atimesb - 2*apb) / (2*tnm3*npcm1);
    ftype F2 = -(3.0*n2 - (apb+6)*n + 2 - atimesb)*npam1_npbm1/(4*tnm1*tnm3*npcm2*npcm1);
    ftype F3 = (npam2_npbm2*npam1_npbm1*(nm2*nm2 - nm2*apb + atimesb)) / (8*tnm3*tnm3*tnm5*(n+c-3)*npcm2*npcm1);
    ftype E  = -npam1_npbm1*(n-c-1) / (2*tnm3*npcm2*npcm1);

    ftype An = (1.0+F1*x)*Anm1 + (E + F2*x)*x*Anm2 + F3*x3*Anm3;
    ftype Bn = (1.0+F1*x)*Bnm1 + (E + F2*x)*x*Bnm2 + F3*x3*Bnm3;
    ftype r = An/Bn;

    prec = fabs(F - r)/fabs(F);
    F = r;

    if(prec < DBLEPS || n > nmax) break;

    if(fabs(An) > RECUR_BIG || fabs(Bn) > RECUR_BIG) {
      An   /= RECUR_BIG;
      Bn   /= RECUR_BIG;
      Anm1 /= RECUR_BIG;
      Bnm1 /= RECUR_BIG;
      Anm2 /= RECUR_BIG;
      Bnm2 /= RECUR_BIG;
      Anm3 /= RECUR_BIG;
      Bnm3 /= RECUR_BIG;
    }
    else if(fabs(An) < 1.0/RECUR_BIG || fabs(Bn) < 1.0/RECUR_BIG) {
      An   *= RECUR_BIG;
      Bn   *= RECUR_BIG;
      Anm1 *= RECUR_BIG;
      Bnm1 *= RECUR_BIG;
      Anm2 *= RECUR_BIG;
      Bnm2 *= RECUR_BIG;
      Anm3 *= RECUR_BIG;
      Bnm3 *= RECUR_BIG;
    }

    n++;
    Bnm3 = Bnm2;
    Bnm2 = Bnm1;
    Bnm1 = Bn;
    Anm3 = Anm2;
    Anm2 = Anm1;
    Anm1 = An;
  }
  
  result->val  = F;
  result->err  = 2.0 * fabs(prec * F);
  result->err += 2.0 * DBLEPS * (n+1.0) * fabs(F);

  /* FIXME: see above */
  result->err *= 8.0 * (fabs(aR) + fabs(aI) + 1.0);

  int stat_iter = (n >= nmax) ? GSL_EMAXITER : GSL_SUCCESS ;

  return stat_iter;
}


/* Do the reflection described in [Moshier, p. 334].
 * Assumes a,b,c != neg integer.
 */
WITHIN_KERNEL
int
hyperg_2F1_reflect(const ftype a, const ftype b, const ftype c,
                   const ftype x, gsl_sf_result * result)
{
  const ftype d = c - a - b;
  const int intd  = floor(d+0.5);
  const int d_integer = ( fabs(d - intd) < HYPERGEOM_EPS );

  if(d_integer) {
    const ftype ln_omx = log(1.0 - x);
    const ftype ad = fabs(d);
    int stat_F2 = GSL_SUCCESS;
    ftype sgn_2;
    gsl_sf_result F1;
    gsl_sf_result F2;
    ftype d1, d2;
    gsl_sf_result lng_c;
    gsl_sf_result lng_ad2;
    gsl_sf_result lng_bd2;
    int stat_c;
    int stat_ad2;
    int stat_bd2;

    if(d >= 0.0) {
      d1 = d;
      d2 = 0.0;
    }
    else {
      d1 = 0.0;
      d2 = d;
    }

    stat_ad2 = gsl_sf_lngamma_e(a+d2, &lng_ad2);
    stat_bd2 = gsl_sf_lngamma_e(b+d2, &lng_bd2);
    stat_c   = gsl_sf_lngamma_e(c,    &lng_c);

    /* Evaluate F1.
     */
    if(ad < DBLEPS) {
      /* d = 0 */
      F1.val = 0.0;
      F1.err = 0.0;
    }
    else {
      gsl_sf_result lng_ad;
      gsl_sf_result lng_ad1;
      gsl_sf_result lng_bd1;
      int stat_ad  = gsl_sf_lngamma_e(ad,   &lng_ad);
      int stat_ad1 = gsl_sf_lngamma_e(a+d1, &lng_ad1);
      int stat_bd1 = gsl_sf_lngamma_e(b+d1, &lng_bd1);

      if(stat_ad1 == GSL_SUCCESS && stat_bd1 == GSL_SUCCESS && stat_ad == GSL_SUCCESS) {
        /* Gamma functions in the denominator are ok.
         * Proceed with evaluation.
         */
        int i;
        ftype sum1 = 1.0;
        ftype term = 1.0;
        ftype ln_pre1_val = lng_ad.val + lng_c.val + d2*ln_omx - lng_ad1.val - lng_bd1.val;
        ftype ln_pre1_err = lng_ad.err + lng_c.err + lng_ad1.err + lng_bd1.err + DBLEPS * fabs(ln_pre1_val);
        int stat_e;

        /* Do F1 sum.
         */
        for(i=1; i<ad; i++) {
          int j = i-1;
          term *= (a + d2 + j) * (b + d2 + j) / (1.0 + d2 + j) / i * (1.0-x);
          sum1 += term;
        }
        
        stat_e = gsl_sf_exp_mult_err_e(ln_pre1_val, ln_pre1_err,
                                       sum1, DBLEPS*fabs(sum1),
                                       &F1);
        if(stat_e == GSL_EOVRFLW) {
          OVERFLOW_ERROR(result);
        }
      }
      else {
        /* Gamma functions in the denominator were not ok.
         * So the F1 term is zero.
         */
        F1.val = 0.0;
        F1.err = 0.0;
      }
    } /* end F1 evaluation */


    /* Evaluate F2.
     */
    if(stat_ad2 == GSL_SUCCESS && stat_bd2 == GSL_SUCCESS) {
      /* Gamma functions in the denominator are ok.
       * Proceed with evaluation.
       */
      const int maxiter = 2000;
      ftype psi_1 = -M_EULER;
      gsl_sf_result psi_1pd; 
      gsl_sf_result psi_apd1;
      gsl_sf_result psi_bpd1;
      int stat_1pd  = 0;
      int stat_apd1 = 0;
      int stat_bpd1 = 0;
      // int stat_1pd  = gsl_sf_psi_e(1.0 + ad, &psi_1pd);
      // int stat_apd1 = gsl_sf_psi_e(a + d1,   &psi_apd1);
      // int stat_bpd1 = gsl_sf_psi_e(b + d1,   &psi_bpd1);
      int stat_dall = GSL_ERROR_SELECT_3(stat_1pd, stat_apd1, stat_bpd1);

      ftype psi_val = psi_1 + psi_1pd.val - psi_apd1.val - psi_bpd1.val - ln_omx;
      ftype psi_err = psi_1pd.err + psi_apd1.err + psi_bpd1.err + DBLEPS*fabs(psi_val);
      ftype fact = 1.0;
      ftype sum2_val = psi_val;
      ftype sum2_err = psi_err;
      ftype ln_pre2_val = lng_c.val + d1*ln_omx - lng_ad2.val - lng_bd2.val;
      ftype ln_pre2_err = lng_c.err + lng_ad2.err + lng_bd2.err + DBLEPS * fabs(ln_pre2_val);
      int stat_e;

      int j;

      /* Do F2 sum.
       */
      for(j=1; j<maxiter; j++) {
        /* values for psi functions use recurrence; Abramowitz+Stegun 6.3.5 */
        ftype term1 = 1.0/(ftype)j  + 1.0/(ad+j);
        ftype term2 = 1.0/(a+d1+j-1.0) + 1.0/(b+d1+j-1.0);
        ftype delta = 0.0;
        psi_val += term1 - term2;
        psi_err += DBLEPS * (fabs(term1) + fabs(term2));
        fact *= (a+d1+j-1.0)*(b+d1+j-1.0)/((ad+j)*j) * (1.0-x);
        delta = fact * psi_val;
        sum2_val += delta;
        sum2_err += fabs(fact * psi_err) + DBLEPS*fabs(delta);
        if(fabs(delta) < DBLEPS * fabs(sum2_val)) break;
      }

      if(j == maxiter) stat_F2 = GSL_EMAXITER;

      if(sum2_val == 0.0) {
        F2.val = 0.0;
        F2.err = 0.0;
      }
      else {
        stat_e = gsl_sf_exp_mult_err_e(ln_pre2_val, ln_pre2_err,
                                       sum2_val, sum2_err,
                                       &F2);
        if(stat_e == GSL_EOVRFLW) {
          result->val = 0.0;
          result->err = 0.0;
          // GSL_ERROR ("error", GSL_EOVRFLW);
        }
      }
      stat_F2 = GSL_ERROR_SELECT_2(stat_F2, stat_dall);
    }
    else {
      /* Gamma functions in the denominator not ok.
       * So the F2 term is zero.
       */
      F2.val = 0.0;
      F2.err = 0.0;
    } /* end F2 evaluation */

    sgn_2 = ( GSL_IS_ODD(intd) ? -1.0 : 1.0 );
    result->val  = F1.val + sgn_2 * F2.val;
    result->err  = F1.err + F2. err;
    result->err += 2.0 * DBLEPS * (fabs(F1.val) + fabs(F2.val));
    result->err += 2.0 * DBLEPS * fabs(result->val);
    return stat_F2;
  }
  else {
    /* d not an integer */

    gsl_sf_result pre1, pre2;
    ftype sgn1, sgn2;
    gsl_sf_result F1, F2;
    int status_F1, status_F2;

    /* These gamma functions appear in the denominator, so we
     * catch their harmless domain errors and set the terms to zero.
     */
    gsl_sf_result ln_g1ca,  ln_g1cb,  ln_g2a,  ln_g2b;
    ftype sgn_g1ca, sgn_g1cb, sgn_g2a, sgn_g2b;
    int stat_1ca = gsl_sf_lngamma_sgn_e(c-a, &ln_g1ca, &sgn_g1ca);
    int stat_1cb = gsl_sf_lngamma_sgn_e(c-b, &ln_g1cb, &sgn_g1cb);
    int stat_2a  = gsl_sf_lngamma_sgn_e(a, &ln_g2a, &sgn_g2a);
    int stat_2b  = gsl_sf_lngamma_sgn_e(b, &ln_g2b, &sgn_g2b);
    int ok1 = (stat_1ca == GSL_SUCCESS && stat_1cb == GSL_SUCCESS);
    int ok2 = (stat_2a  == GSL_SUCCESS && stat_2b  == GSL_SUCCESS);
    
    gsl_sf_result ln_gc,  ln_gd,  ln_gmd;
    ftype sgn_gc, sgn_gd, sgn_gmd;
    gsl_sf_lngamma_sgn_e( c, &ln_gc,  &sgn_gc);
    gsl_sf_lngamma_sgn_e( d, &ln_gd,  &sgn_gd);
    gsl_sf_lngamma_sgn_e(-d, &ln_gmd, &sgn_gmd);
    
    sgn1 = sgn_gc * sgn_gd  * sgn_g1ca * sgn_g1cb;
    sgn2 = sgn_gc * sgn_gmd * sgn_g2a  * sgn_g2b;

    if(ok1 && ok2) {
      ftype ln_pre1_val = ln_gc.val + ln_gd.val  - ln_g1ca.val - ln_g1cb.val;
      ftype ln_pre2_val = ln_gc.val + ln_gmd.val - ln_g2a.val  - ln_g2b.val + d*log(1.0-x);
      ftype ln_pre1_err = ln_gc.err + ln_gd.err + ln_g1ca.err + ln_g1cb.err;
      ftype ln_pre2_err = ln_gc.err + ln_gmd.err + ln_g2a.err  + ln_g2b.err;
      if(ln_pre1_val < GSL_LOG_DBL_MAX && ln_pre2_val < GSL_LOG_DBL_MAX) {
        gsl_sf_exp_err_e(ln_pre1_val, ln_pre1_err, &pre1);
        gsl_sf_exp_err_e(ln_pre2_val, ln_pre2_err, &pre2);
        pre1.val *= sgn1;
        pre2.val *= sgn2;
      }
      else {
        OVERFLOW_ERROR(result);
      }
    }
    else if(ok1 && !ok2) {
      ftype ln_pre1_val = ln_gc.val + ln_gd.val - ln_g1ca.val - ln_g1cb.val;
      ftype ln_pre1_err = ln_gc.err + ln_gd.err + ln_g1ca.err + ln_g1cb.err;
      if(ln_pre1_val < GSL_LOG_DBL_MAX) {
        gsl_sf_exp_err_e(ln_pre1_val, ln_pre1_err, &pre1);
        pre1.val *= sgn1;
        pre2.val = 0.0;
        pre2.err = 0.0;
      }
      else {
        OVERFLOW_ERROR(result);
      }
    }
    else if(!ok1 && ok2) {
      ftype ln_pre2_val = ln_gc.val + ln_gmd.val - ln_g2a.val - ln_g2b.val + d*log(1.0-x);
      ftype ln_pre2_err = ln_gc.err + ln_gmd.err + ln_g2a.err + ln_g2b.err;
      if(ln_pre2_val < GSL_LOG_DBL_MAX) {
        pre1.val = 0.0;
        pre1.err = 0.0;
        gsl_sf_exp_err_e(ln_pre2_val, ln_pre2_err, &pre2);
        pre2.val *= sgn2;
      }
      else {
        OVERFLOW_ERROR(result);
      }
    }
    else {
      pre1.val = 0.0;
      pre2.val = 0.0;
      UNDERFLOW_ERROR(result);
    }

    status_F1 = hyperg_2F1_series(  a,   b, 1.0-d, 1.0-x, &F1);
    status_F2 = hyperg_2F1_series(c-a, c-b, 1.0+d, 1.0-x, &F2);

    result->val  = pre1.val*F1.val + pre2.val*F2.val;
    result->err  = fabs(pre1.val*F1.err) + fabs(pre2.val*F2.err);
    result->err += fabs(pre1.err*F1.val) + fabs(pre2.err*F2.val);
    result->err += 2.0 * DBLEPS * (fabs(pre1.val*F1.val) + fabs(pre2.val*F2.val));
    result->err += 2.0 * DBLEPS * fabs(result->val);

    return GSL_SUCCESS;
  }
}


WITHIN_KERNEL int
pow_omx(const double x, const double p, gsl_sf_result * result)
{
  double ln_omx;
  double ln_result;
  if(fabs(x) < GSL_ROOT5_DBL_EPSILON) {
    ln_omx = -x*(1.0 + x*(1.0/2.0 + x*(1.0/3.0 + x/4.0 + x*x/5.0)));
  }
  else {
    ln_omx = log(1.0-x);
  }
  ln_result = p * ln_omx;
  return gsl_sf_exp_err_e(ln_result, GSL_DBL_EPSILON * fabs(ln_result), result);
}


#include <lib99ocl/gsl/specfunc/hyperg_1F1.c>


WITHIN_KERNEL
int
gsl_sf_hyperg_2F1_e(double a, double b, const double c,
                       const double x,
                       gsl_sf_result * result)
{
  const double d = c - a - b;
  const double rinta = floor(a + 0.5);
  const double rintb = floor(b + 0.5);
  const double rintc = floor(c + 0.5);
  const int a_neg_integer = ( a < 0.0  &&  fabs(a - rinta) < HYPERGEOM_EPS );
  const int b_neg_integer = ( b < 0.0  &&  fabs(b - rintb) < HYPERGEOM_EPS );
  const int c_neg_integer = ( c < 0.0  &&  fabs(c - rintc) < HYPERGEOM_EPS );

  result->val = 0.0;
  result->err = 0.0;

   /* Handle x == 1.0 RJM */

  if (fabs (x - 1.0) < HYPERGEOM_EPS && (c - a - b) > 0 && c != 0 && !c_neg_integer) {
    gsl_sf_result lngamc, lngamcab, lngamca, lngamcb;
    double lngamc_sgn, lngamca_sgn, lngamcb_sgn;
    int status;
    int stat1 = gsl_sf_lngamma_sgn_e (c, &lngamc, &lngamc_sgn);
    int stat2 = gsl_sf_lngamma_e (c - a - b, &lngamcab);
    int stat3 = gsl_sf_lngamma_sgn_e (c - a, &lngamca, &lngamca_sgn);
    int stat4 = gsl_sf_lngamma_sgn_e (c - b, &lngamcb, &lngamcb_sgn);
    
    if (stat1 != GSL_SUCCESS || stat2 != GSL_SUCCESS
        || stat3 != GSL_SUCCESS || stat4 != GSL_SUCCESS)
      {
        DOMAIN_ERROR (result);
      }
    
    status =
      gsl_sf_exp_err_e (lngamc.val + lngamcab.val - lngamca.val - lngamcb.val,
                        lngamc.err + lngamcab.err + lngamca.err + lngamcb.err,
                        result);
    
    result->val *= lngamc_sgn / (lngamca_sgn * lngamcb_sgn);
      return status;
  }
  
  if(x < -1.0 || 1.0 <= x) {
    DOMAIN_ERROR(result);
  }

  if(c_neg_integer) {
    /* If c is a negative integer, then either a or b must be a
       negative integer of smaller magnitude than c to ensure
       cancellation of the series. */
    if(! (a_neg_integer && a > c + 0.1) && ! (b_neg_integer && b > c + 0.1)) {
      DOMAIN_ERROR(result);
    }
  }

  if(fabs(c-b) < HYPERGEOM_EPS || fabs(c-a) < HYPERGEOM_EPS) {
    return pow_omx(x, d, result);  /* (1-x)^(c-a-b) */
  }

  if(a >= 0.0 && b >= 0.0 && c >=0.0 && x >= 0.0 && x < 0.995) {
    /* Series has all positive definite
     * terms and x is not close to 1.
     */
    return hyperg_2F1_series(a, b, c, x, result);
  }

  if(fabs(a) < 10.0 && fabs(b) < 10.0) {
    /* a and b are not too large, so we attempt
     * variations on the series summation.
     */
    if(a_neg_integer) {
      return hyperg_2F1_series(rinta, b, c, x, result);
    }
    if(b_neg_integer) {
      return hyperg_2F1_series(a, rintb, c, x, result);
    }

    if(x < -0.25) {
      return hyperg_2F1_luke(a, b, c, x, result);
    }
    else if(x < 0.5) {
      return hyperg_2F1_series(a, b, c, x, result);
    }
    else {
      if(fabs(c) > 10.0) {
        return hyperg_2F1_series(a, b, c, x, result);
      }
      else {
        return hyperg_2F1_reflect(a, b, c, x, result);
      }
    }
  }
  else {
    /* Either a or b or both large.
     * Introduce some new variables ap,bp so that bp is
     * the larger in magnitude.
     */
    double ap, bp; 
    if(fabs(a) > fabs(b)) {
      bp = a;
      ap = b;
    }
    else {
      bp = b;
      ap = a;
    }

    if(x < 0.0) {
      /* What the hell, maybe Luke will converge.
       */
      return hyperg_2F1_luke(a, b, c, x, result);
    }

    if(GSL_MAX_DBL(fabs(ap),1.0)*fabs(bp)*fabs(x) < 2.0*fabs(c)) {
      /* If c is large enough or x is small enough,
       * we can attempt the series anyway.
       */
      return hyperg_2F1_series(a, b, c, x, result);
    }

    if(fabs(bp*bp*x*x) < 0.001*fabs(bp) && fabs(ap) < 10.0) {
      /* The famous but nearly worthless "large b" asymptotic.
       */
      int stat = gsl_sf_hyperg_1F1_e(ap, c, bp*x, result);
      result->err = 0.001 * fabs(result->val);
      return stat;
    }

    /* We give up. */
    result->val = 0.0;
    result->err = 0.0;
    GSL_ERROR ("error", GSL_EUNIMPL);
  }
}


WITHIN_KERNEL
ftype gsl_sf_hyperg_2F1(ftype a, ftype b, ftype c, ftype x)
{
  gsl_sf_result result;
  int errcode = gsl_sf_hyperg_2F1_e(a, b, c, x, &result);
	return result.val;
}


#endif // _HYPERGEOM2_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
