#include "core.h"
#include "complex.h"

#ifndef _HYPERGEOM_C_
#define _HYPERGEOM_C_




/*
 * Returns the hypergeometric series 2F1 and its derivative.
 * The series converges on the complex unit circle, |z|<1.
 */
void __hyp2f1_unit_circle(ctype a, ctype b, ctype c, ctype z,
		                      ftype _series[2], ftype _deriv[2])
{
  ctype __deriv = C(0,0);
  ctype __series = C(0,0);
	ctype __fac = C(1.0,0.0);
	ctype __temp = C(1.0, 0.0);

	ctype __a = a;
	ctype __b = b;
	ctype __c = cadd(c, C(MACHEP,MACHEP));

	for (int n=1; n<=1000; n++) {
		__fac = cmul(__fac, cdiv(cmul(__a, __b), __c));
    __deriv = cadd(__deriv, __fac);
		__fac = cmul(__fac, cmul(C(1.0/n,0), z));
		__series = cadd(__temp, __fac);

	  if ( ( fabs(cre(__series)-cre(__temp)) < MACHEP ) && ( fabs(cim(__series)-cim(__temp)) < MACHEP ))
		{
			_series[0] = cre(__series);
			_series[1] = cim(__series);
			_deriv[0] = cre(__deriv);
			_deriv[1] = cim(__deriv);
			return;
		}
	  __temp = C(cre(__series), cim(__series));
	  __a = cadd(__a, C(1,0));
	  __b = cadd(__b, C(1,0));
	  __c = cadd(__c, C(1,0));
	}
  #ifdef DEBUG
	   printf("hypergeo Didnt converge bro\n");
  #endif
}


/*
 * Computes derivatives blah
 */
void __hyp2f1_diff(ftype s, ftype yy[4], ftype dyyds[4], ftype z0, ftype dz, ftype a, ftype b, ftype c)
{
	ctype y1 = C(yy[0], yy[1]);
	ctype y2 = C(yy[2], yy[3]);

  ctype z = cadd(C(z0,0), cmul(C(s,0), C(dz,0)));

  ctype dy1ds = cmul(y2, C(dz,0));
	ctype dy2ds = cmul(
			        csub(
								  cmul(cmul(C(a,0), C(b,0)), y1),
								  cmul(csub(C(c,0), cmul(cadd(cadd(C(a,0), C(b,0)), C(1,0)), z)), y2)
							),
			        cdiv(C(dz,0), cmul(z, csub(C(1,0), z)))
					);

	dyyds[0] = cre(dy1ds);
	dyyds[1] = cim(dy1ds);
	dyyds[2] = cre(dy2ds);
	dyyds[3] = cim(dy2ds);
}


ctype chyp2f1(const ctype a, const ctype b, const ctype c, const ctype z)
// Complex hypergeometric function 2F1 for complex a,b,c, and z, by
// direct integration of the hypergeometric equation in the complex plane.
// The branch cut is taken to lie along the real axis, Re z > 1.
{

    int nBAD, nOK;
		ctype ans = C(0, 0);

		ftype _series[2] = {0,0};
		ftype _derivs[2] = {0,0};

    if (cnorm(z) <= 1)
		{
			// use series expansion at z=0
			__hyp2f1_unit_circle(a, b, c, z, _series, _derivs);
			ans = C(_series[0], _series[1]);
			return ans;
		}
    // else if (cre(z) < 0.0) 
		// {
		// 	ctype z0 = C(-0.5,0.0);
		// }
		// else if (cre(z) <= 1.0)
		// {
		// 	ctype z0 = C(0.5,0.0);
		// }
		else
		{
			ctype z0 = C(0.0, cim(z) >= 0.0 ? 0.5 : -0.5);
      #ifdef DEBUG
		    printf("hyp2f1 is not defined outside the unit circle\n");
      #endif

      ctype dz = csub(z, z0);
      __hyp2f1_unit_circle(a, b, c, z0, _series, _derivs);

      ftype __y[4] = {0, 0, 0, 0};
      __y[0] = _series[0];
      __y[1] = _series[1];
      __y[2] = _derivs[0];
      __y[3] = _derivs[1];

		  // TODO: create rk4a algorithm to integrate the ODE and get values
      // odeint(__y, 4, 0.0, 1.0, EPS, 0.1, 0.0001, &nOK, &nBAD, __hyp2f1_diff, bsstep);

      // The arguments to odeint are the vector of independent variables,
		  // its length, the starting and ending values of the dependent variable, 
		  // the accuracy parameter, an initial guess for stepsize, a minimum 
		  // stepsize, the (returned) number of good and bad steps taken, and the 
		  // names of the derivative routine and the (here Bulirsch-Stoer) stepping 
		  // routine. 
		  ans = C(__y[1], __y[2]);
      return ans;
		}
}

#endif // _HYPERGEOM_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
