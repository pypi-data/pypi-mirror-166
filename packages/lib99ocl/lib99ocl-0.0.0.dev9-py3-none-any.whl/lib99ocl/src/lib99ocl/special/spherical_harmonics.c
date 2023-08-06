#ifndef _SPHERICAL_HARMONICS_C_
#define _SPHERICAL_HARMONICS_C_


#include "spherical_harmonics.h"


WITHIN_KERNEL
ftype sph_harm(const int m, const int l, const ftype cosT, const ftype phi)
{
    if(m < 0)
    {
      return pow(-1.,m) * sqrt(2.) * cim( csph_harm(-m, l, cosT, phi) );
    }
    else if(m > 0)
    {
      return pow(-1.,m) * sqrt(2.) * cre( csph_harm(m,  l, cosT, phi) );
    }
    else
    {
      return sqrt( (2.*l+1.) / (4.*M_PI) ) * lpmv(m, l, cosT);
    }
}


#endif // _SPHERICAL_HARMONICS_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr noet
