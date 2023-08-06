#ifndef _ODESOLVERS_C_
#define _ODESOLVERS_C_





// Runge-Kutta routines {{{

void rkcoeff(float y[], float dydx[], int n, float x, float h, 
		         float yout[], float yerr[],
						 void (*derivs)(float, float [], float []))
// Given values for n variables y[1..n] and their derivatives dydx[1..n] known at x, use the fifth-order Cash-Karp Runge-Kutta method to advance the solution over an interval h and return the incremented variables as yout[1..n]. Also return an estimate of the local truncation error in yout using the embedded fourth-order method. The user supplies the routine derivs(x,y,dydx), which returns derivatives dydx at x.
{
    int i;
    const float a2=0.2,
    const float a3=0.3,
    const float a4=0.6,
    const float a5=1.0,
    const float a6=0.875,
    const float b21=0.2,
    const float b31=3.0/40.0,
    const float b32=9.0/40.0,
    const float b41=0.3,
    const float b42 = -0.9,
    const float b43=1.2,
    const float b51 = -11.0/54.0,
    const float b52=2.5,
    const float b53 = -70.0/27.0,
    const float b54=35.0/27.0,
    const float b61=1631.0/55296.0,
    const float b62=175.0/512.0,
    const float b63=575.0/13824.0,
    const float b64=44275.0/110592.0,
    const float b65=253.0/4096.0,
    const float c1=37.0/378.0,
    const float c3=250.0/621.0,
    const float c4=125.0/594.0,
    const float c6=512.0/1771.0,
    const float dc5 = -277.00/14336.0;
    const float dc1=c1-2825.0/27648.0,
    const float dc3=c3-18575.0/48384.0,
    const float dc4=c4-13525.0/55296.0,
    const float dc6=c6-0.25;
    
    float *ak2,*ak3,*ak4,*ak5,*ak6,*ytemp;
    ak2=vector(1,n);
    ak3=vector(1,n);
    ak4=vector(1,n);
    ak5=vector(1,n);
    ak6=vector(1,n);
    ytemp=vector(1,n);
    
    // 1st step
    for (i=1;i<=n;i++) ytemp[i] = y[i] + b21*h*dydx[i];
    (*derivs)(x+a2*h,ytemp,ak2);
    
    // 2nd step
    for (i=1;i<=n;i++) ytemp[i] = y[i] + h*(b31*dydx[i] + b32*ak2[i]);
    (*derivs)(x+a3*h,ytemp,ak3); 
    
    // 3rd step
    for (i=1;i<=n;i++) ytemp[i] = y[i] + h*(b41*dydx[i] + b42*ak2[i] + b43*ak3[i]); 
    (*derivs)(x+a4*h,ytemp,ak4);
    
    // 4th step
    for (i=1;i<=n;i++) ytemp[i]=y[i]+h*(b51*dydx[i]+b52*ak2[i]+b53*ak3[i]+b54*ak4[i]);
    (*derivs)(x+a5*h,ytemp,ak5);
    
    // 5th step.
    for (i=1;i<=n;i++) ytemp[i]=y[i]+h*(b61*dydx[i]+b62*ak2[i]+b63*ak3[i]+b64*ak4[i]+b65*ak5[i]);
    (*derivs)(x+a6*h,ytemp,ak6);
    
    // 6th step (Accumulate increments with proper weights.)
    for (i=1;i<=n;i++) yout[i] = y[i] + h*(c1*dydx[i]+c3*ak3[i]+c4*ak4[i]+c6*ak6[i]);
    // Estimate error as difference between fourth and fifth order methods.
    for (i=1;i<=n;i++) yerr[i] =        h*(dc1*dydx[i]+dc3*ak3[i]+dc4*ak4[i]+dc5*ak5[i]+dc6*ak6[i]);
    
    free_vector(ytemp,1,n);
    free_vector(ak6,1,n);
    free_vector(ak5,1,n);
    free_vector(ak4,1,n);
    free_vector(ak3,1,n);
    free_vector(ak2,1,n);
}



// }}}






/*
 * Runge Kutta-based adapative ODE solver
 * Intrgrades starting from ystart from x1 fro x2 with accuracy eps,
 * storing intermediate results in global varaibles.
 */
void odeint(float ystart[], int nvar,
		float x1, float x2, float eps, float h1, float hmin, int *nok, int *nbad,
void (*derivs)(float, float [], float []),
void (*rkqs)(float [], float [], int, float *, float, float, float [], float *, float *, void (*)(float, float [], float [])))
Runge-Kutta driver with adaptive stepsize control. 
Integrate starting values ystart[1..nvar] from x1 to x2 with accuracy eps, storing intermediate results in global variables. h1 should be set as a guessed first stepsize, 
					hmin as the minimum allowed stepsize (can be zero). 
					On output nok and nbad are the number of good and bad (but retried and fixed) steps taken, and 
					ystart is replaced by values at the end of the integration interval. derivs is the user-supplied routine for calculating the right-hand side derivative, while rkqs is the name of the stepper routine to be used.
 
{
    int nstp,i;
    float xsav,x,hnext,hdid,h; float *yscal,*y,*dydx;
    yscal=vector(1,nvar); y=vector(1,nvar); dydx=vector(1,nvar);
    x=x1;
    h=SIGN(h1,x2-x1);
    *nok = (*nbad) = kount = 0;
    for (i=1;i<=nvar;i++)
		{
			y[i] = ystart[i];
		}
		if (kmax > 0) {
			// ensure we store first step
			xsav = x - dxsav*2.0;
		}
    for (nstp=1; nstp<=MAXSTP; nstp++)
		{
		  	(*derivs)(x, y, dydx);
        for (i=1; i<=nvar; i++)
				{
            // Scaling used to monitor accuracy.
						// This general-purpose choice can be modified if need be.
            yscal[i]=fabs(y[i])+fabs(dydx[i]*h)+TINY;
				}

    // Assures storage of first step. Take at most MAXSTP steps.
    if (kmax > 0 && kount < kmax-1 && fabs(x-xsav) > fabs(dxsav)) 
		{
			xp[++kount]=x; // Store intermediate results.
			for (i=1;i<=nvar;i++)
			{
				yp[i][kount]=y[i];
			}
			xsav=x;
    }

    if ((x+h-x2)*(x+h-x1) > 0.0)
		{
			// If stepsize can overshoot, decrease.
			h=x2-x;
		}

    (*rkqs)(y,dydx,nvar,&x,h,eps,yscal,&hdid,&hnext,derivs);

		if (hdid == h) 
		{
			++(*nok);
		}
		else
		{
			++(*nbad);
		}

    if ((x-x2)*(x2-x1) >= 0.0)
		{
		  	// Are we done?
        for (i=1;i<=nvar;i++)
		  	{
		  		ystart[i]=y[i];
		  	}
		  	if (kmax)
		  	{
		  		xp[++kount] = x; // Save final step.
		  		for (i=1;i<=nvar;i++)
		  		{
		  			yp[i][kount]=y[i]; 
		  		}
		  	}

       free_vector(dydx,1,nvar);
		   free_vector(y,1,nvar);
		   free_vector(yscal,1,nvar); 
		   return; // Normal exit.
    }

    if (fabs(hnext) <= hmin)
		{
			printf("Step size too small in odeint\n");
		}

		h=hnext;

    }

    printf("Too many steps in odeintegrate\n"); 
}




#endif // _ODESOLVERS_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
