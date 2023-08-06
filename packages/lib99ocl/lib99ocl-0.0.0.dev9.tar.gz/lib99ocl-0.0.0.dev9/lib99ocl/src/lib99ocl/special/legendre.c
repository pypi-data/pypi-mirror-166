#ifndef _LEGENDRE_C_
#define _LEGENDRE_C_


#include "legendre.h"


WITHIN_KERNEL
ftype lpmv(const int m, const int l, const ftype cosT)
{
    const int L = (l<0) ? abs(l)-1 : l;
    const int M = abs(m);
    ftype factor = 1.0;

    if (m<0){
        factor = pow(-1.0, 1.*m) * factorial(L-M) / factorial(L+M);
    }

    // shit
    if (M>l){
        /* printf("WARNING: Associated Legendre polynomial (%+d,%+d) is out of the scope of this function.", l, m); */
        return 0;
    }

    // L = 0
    if (L==0)
    {
        return 1.0;
    }
    // L = 1
    else if (L==1)
    {
        if      (M==0) { return cosT; }
        else           { return -factor*sqrt(1.0-cosT*cosT); } // OK
    }
    // L = 2
    else if (L==2)
    {
        if      (M==0) { return  0.5*(3.*cosT*cosT - 1.); } // OK
        else if (M==1) { return -3.0*factor*cosT*sqrt(1.-cosT*cosT); } // OK
        else           { return  3.0*factor*(1.-cosT*cosT); } // OK
    }
    // L = 3
    else if (L==3)
    {
        ftype sinT = sqrt(1.0-cosT*cosT);
        if      (M==0) { return   0.5*(5.*cosT*cosT*cosT - 3.*cosT); }
        else if (M==1) { return  -1.5*factor*(5.*cosT*cosT - 1.)*sinT; }
        else if (M==2) { return  15.0*factor*sinT*sinT*cosT; }
        else           { return -15.0*factor*sinT*sinT*sinT; }
    }
    // L = 4
    else if (L==4)
    {
        ftype sinT = sqrt(1.0-cosT*cosT);
        if      (M==0) { return 0.125*(35.*cosT*cosT*cosT*cosT - 30.*cosT*cosT + 3.); }
        else if (M==1) { return  -2.5*factor*(7.*cosT*cosT*cosT - 3.*cosT)*sinT; }
        else if (M==2) { return   7.5*factor*(7.*cosT*cosT - 1.)*sinT*sinT; }
        else if (M==3) { return -105.*factor*sinT*sinT*sinT*cosT; }
        else           { return  105.*factor*sinT*sinT*sinT*sinT; }
    }
    else {
        /* if (get_global_id(0) < 10000000000) { */
        /*   printf("WARNING: Associated Legendre polynomial (%+d,%+d) is out of the scope of this function.", l, m); */
        /* } */
        //asm(“trap;”);
        return 0;
    }

}


/*  NEEED TO FIX THIS
WITHIN_KERNEL
ftype lpmv(const int M, const int l, const ftype x)
{
  //const int l = (L<0) ? abs(L)-1 : L;
  const int m = abs(M);

  ftype factor = 1.0;

  ftype fact, pll, pmm, pmmp1, somx2; 
  int i, ll;

  if (m < 0 || m > l || fabs(x) > 1.0) 
    printf("Wrong arguments in routine lpmv\n");
 
  pmm = 1;
  if (m > 0)
  {
    somx2 = sqrt((1.0-x)*(1.0+x));
    fact = 1.0;
    for (i=1; i<=m; i++)
    {
      pmm *= -fact*somx2;
      fact += 2.0;
    }
  }
  
  if (l == m)
  {
    return pmm;
  }
  else
  {
    pmmp1 = x* (2*m+1) * pmm;
    if (l == (m+1))
    {
      return pmmp1;
    }
    else
    {
      for (ll=m+2; ll<=l; ll++)
      {
        pll = (x*(2*ll-1)*pmmp1-(ll+m-1)*pmm) / (ll-m);
        pmm = pmmp1;
        pmmp1 = pll;
      }
      return pll;
    }
  }
}
*/


#endif // _LEGENDRE_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr et
