c        common for my GRACE software.   P. Tregoning  14 March 2007


c  This common block is to pass C, S coefficients, Legendre polynomials and Love
c  numbers freely through whatever GRACE software I might end up generating.
c
c  PT070329: nmax from the calsea definition, this is the spherical harmonic
c            expansion definition of the outputted field.
c      nmax    - spherical harmonic degree of calculation, must be a power of 2


         integer ioerr,maxdeg,maxord,maxnm,nmax,nlatd2
         parameter (nmax=128)
         integer lucoeff,lulove,luout
         parameter (maxdeg=nmax,maxord=nmax)
         parameter (maxnm=(maxdeg+1)*(maxdeg+2)/2)
         double precision pi,epoch
         common /ints/ ioerr,lucoeff,lulove,luout

c  spherical harmonic coefficients
         real*8 coefC(maxdeg,maxord),coefS(maxdeg,maxord)
         real*8 coef_errC(maxdeg,maxord),coef_errS(maxdeg,maxord)
         real*8 stokescoefC(maxdeg,maxord),stokescoefS(maxdeg,maxord) 
         real*8 stokes_errC(maxdeg,maxord),stokes_errS(maxdeg,maxord) 
         common /coeffs/coefC,coefS,coef_errC,coef_errS

c  Jekeli weighting function
         real*8 W(maxdeg+1)

c  Legendre polynomials
         double precision Plm(maxnm), dplm(maxnm)
         common /norm_legendre/ Plm, dplm

c  Load Love numbers
         real*8 lovenums(maxdeg,3)
         common /love/lovenums

c  some necessary constants
         real*8 earthrad, GM, G, mean_g

         common /values/ pi,epoch,earthrad, GM, G, mean_g
         
